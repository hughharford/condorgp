import os
import shutil
import socket
import subprocess
import tempfile
from pathlib import Path

import pytest
from pytest_bdd import scenarios, given, when, then

from tests.k8s_helpers import REPO_ROOT, read_text, run, yaml_docs

scenarios("../features/019_k8s_postgres_init.feature")

POSTGRES_MANIFEST = "k8s/04-postgres.yaml"
COMPOSE_FILE = "docker_compose/docker-compose-db-graf-rmq.yml"
INIT_SCRIPT = "scripts/db_init/01-init.sh"
APP_VARS = {"APP_DB_USER", "APP_DB_PASS", "APP_DB_NAME"}
AWKWARD_PASSWORD = "p'a\"s$s;--\\x #{}"  # quotes, $, ;, SQL comment, backslash: all must survive


def _by_kind(docs, kind):
    return [d for d in docs if d.get("kind") == kind]


def _pod_spec(deployment):
    return deployment["spec"]["template"]["spec"]


# ---------------------------------------------------------------- manifest scenarios


@given("the Postgres manifest", target_fixture="pg_docs")
def postgres_manifest():
    docs = yaml_docs(POSTGRES_MANIFEST)
    assert docs, f"{POSTGRES_MANIFEST} is missing or is not valid YAML"
    assert _by_kind(docs, "Deployment"), "no Deployment in the Postgres manifest"
    return docs


@when("I look at how the database Deployment mounts its init scripts", target_fixture="init_volume")
def init_volume(pg_docs):
    volumes = _pod_spec(_by_kind(pg_docs, "Deployment")[0]).get("volumes", [])
    found = [v for v in volumes if v.get("name") == "init-scripts"]
    assert found, "the Deployment has no 'init-scripts' volume"
    return found[0]


@then("they come from a ConfigMap that exists in the same namespace")
def init_from_configmap(init_volume, pg_docs):
    assert "configMap" in init_volume, f"init-scripts is not a ConfigMap volume: {sorted(init_volume)}"
    name = init_volume["configMap"]["name"]
    deployment_ns = _by_kind(pg_docs, "Deployment")[0]["metadata"].get("namespace")
    maps = [d for d in _by_kind(pg_docs, "ConfigMap") if d["metadata"]["name"] == name]
    assert maps, f"the volume refers to ConfigMap '{name}' but the manifest does not define it"
    assert maps[0]["metadata"].get("namespace") == deployment_ns
    assert "01-init.sh" in maps[0]["data"]


@then("the Postgres pod mounts no host path")
def no_host_path(pg_docs):
    host_paths = [v["name"] for v in _pod_spec(_by_kind(pg_docs, "Deployment")[0]).get("volumes", []) if "hostPath" in v]
    assert not host_paths, f"volumes still use a path on one machine's disk: {host_paths}"


@then("the ConfigMap script is identical to scripts/db_init/01-init.sh")
def configmap_matches_source(pg_docs):
    maps = [d for d in _by_kind(pg_docs, "ConfigMap") if "01-init.sh" in (d.get("data") or {})]
    assert maps, "no ConfigMap in the manifest carries 01-init.sh"
    source = read_text(INIT_SCRIPT)
    assert source, f"{INIT_SCRIPT} is missing"
    assert maps[0]["data"]["01-init.sh"].strip() == source.strip(), (
        f"ConfigMap copy differs from {INIT_SCRIPT}: update both together"
    )


@then("the init volume is mounted with an executable mode")
def init_volume_executable(pg_docs):
    volumes = _pod_spec(_by_kind(pg_docs, "Deployment")[0]).get("volumes", [])
    vol = next((v for v in volumes if v.get("name") == "init-scripts"), None)
    assert vol and "configMap" in vol, "init-scripts is not a ConfigMap volume"
    mode = vol["configMap"].get("defaultMode")
    assert mode is not None and mode & 0o111, f"defaultMode {mode!r} leaves the script non-executable"


@then("the database container receives the Postgres password and the application role settings")
def pod_gets_variables(pg_docs):
    container = _pod_spec(_by_kind(pg_docs, "Deployment")[0])["containers"][0]
    names = {e["name"] for e in container.get("env", [])}
    missing = ({"POSTGRES_PASSWORD"} | APP_VARS) - names
    assert not missing, f"the container is not given: {sorted(missing)}"


@given("the Docker Compose database service", target_fixture="compose_service")
def compose_service():
    docs = yaml_docs(COMPOSE_FILE)
    assert docs, f"{COMPOSE_FILE} is missing or is not valid YAML"
    for service in docs[0].get("services", {}).values():
        if any("db_init" in str(v) for v in service.get("volumes", [])):
            return service
    pytest.fail("no Compose service mounts scripts/db_init")


@then("it mounts scripts/db_init and passes the application role settings")
def compose_passes_variables(compose_service):
    env = compose_service.get("environment", [])
    names = set(env) if isinstance(env, dict) else {str(e).split("=", 1)[0] for e in env}
    assert APP_VARS <= names, f"Compose does not pass: {sorted(APP_VARS - names)}"


# ---------------------------------------------------------------- script behaviour


@given("the init script")
def init_script_exists():
    assert (REPO_ROOT / INIT_SCRIPT).is_file(), f"{INIT_SCRIPT} is missing"


@when("I run it with the application database password missing", target_fixture="result")
def run_without_password():
    env = {
        "PATH": os.environ["PATH"],
        "POSTGRES_USER": "postgres",
        "POSTGRES_DB": "postgres",
        "APP_DB_USER": "cgp",
        "APP_DB_NAME": "cgpbackbone",
    }
    return run(["bash", str(REPO_ROOT / INIT_SCRIPT)], env=env)


@then("it stops with a message naming APP_DB_PASS")
def stops_naming_variable(result):
    assert result.returncode != 0, "the script carried on without a password"
    assert "APP_DB_PASS" in result.stderr, result.stderr


# ---------------------------------------------------------------- real Postgres


def _pg_bin_dir():
    found = shutil.which("initdb")
    if found:
        return Path(found).parent
    candidates = sorted(
        Path("/usr/lib/postgresql").glob("*/bin/initdb"),
        key=lambda p: int(p.parent.parent.name) if p.parent.parent.name.isdigit() else 0,
    )
    return candidates[-1].parent if candidates else None


class ThrowawayPostgres:
    """A real Postgres in a temp dir. Runs as the 'postgres' OS user when the tests run as root."""

    def __init__(self, bindir):
        self.bindir = bindir
        self.root = Path(tempfile.mkdtemp(prefix="cgp-pgtest-"))
        self.sock = self.root / "sock"
        self.data = self.root / "data"
        self.port = self._free_port()
        self.as_root = os.geteuid() == 0
        self.root.chmod(0o755)
        self.sock.mkdir()
        if self.as_root:
            shutil.chown(self.root, "postgres")
            shutil.chown(self.sock, "postgres")

    @staticmethod
    def _free_port():
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

    def env(self, **extra):
        base = {"PATH": f"{self.bindir}:/usr/bin:/bin", "PGHOST": str(self.sock), "PGPORT": str(self.port)}
        return {**base, **extra}

    def run(self, cmd, **extra_env):
        env = self.env(**extra_env)
        if self.as_root:
            cmd = ["runuser", "-u", "postgres", "--", "env", "-i", *[f"{k}={v}" for k, v in env.items()], *cmd]
            return run(cmd)
        return run(cmd, env=env)

    def start(self):
        res = self.run([str(self.bindir / "initdb"), "-D", str(self.data), "-U", "postgres",
                        "--auth-local=trust", "--auth-host=scram-sha-256", "-E", "UTF8", "--no-sync"])
        assert res.returncode == 0, res.stderr
        res = self.run([str(self.bindir / "pg_ctl"), "-D", str(self.data), "-w", "-l", str(self.root / "pg.log"),
                        "-o", f"-p {self.port} -k {self.sock} -c listen_addresses=127.0.0.1 -c fsync=off", "start"])
        assert res.returncode == 0, res.stderr + (self.root / "pg.log").read_text()

    def stop(self):
        self.run([str(self.bindir / "pg_ctl"), "-D", str(self.data), "-m", "immediate", "stop"])
        shutil.rmtree(self.root, ignore_errors=True)

    def sql(self, query, user="postgres", dbname="postgres"):
        res = self.run([str(self.bindir / "psql"), "-XtA", "-U", user, "-d", dbname, "-c", query])
        assert res.returncode == 0, res.stderr
        return res.stdout.strip()


@pytest.fixture
def throwaway_pg():
    bindir = _pg_bin_dir()
    if not bindir or not (bindir / "pg_ctl").exists() or not (bindir / "psql").exists():
        pytest.skip("needs a local PostgreSQL server (initdb, pg_ctl, psql); e.g. `sudo apt install postgresql`")
    server = ThrowawayPostgres(bindir)
    try:
        server.start()
        yield server
    finally:
        server.stop()


@given("a throwaway Postgres server", target_fixture="pg")
def throwaway_postgres(throwaway_pg):
    return throwaway_pg


@given("the application database already exists, owned by the superuser")
def app_db_precreated(pg):
    # The official image creates POSTGRES_DB before it runs the init scripts. In this
    # repo POSTGRES_DB and APP_DB_NAME are the same name, so the script meets an existing DB.
    pg.sql('create database cgpbackbone')


@when("I run the init script with POSTGRES_DB set to that same database")
def run_init_script_existing_db(pg):
    source = read_text(INIT_SCRIPT)
    script = pg.root / "01-init.sh"
    script.write_text(source)
    script.chmod(0o755)
    res = pg.run(
        ["bash", str(script)],
        POSTGRES_USER="postgres", POSTGRES_DB="cgpbackbone",
        APP_DB_USER="cgp", APP_DB_PASS=AWKWARD_PASSWORD, APP_DB_NAME="cgpbackbone",
    )
    assert res.returncode == 0, f"init script failed when the database already existed:\n{res.stderr}"


@when("I run the init script with an awkward password")
def run_init_script(pg):
    source = read_text(INIT_SCRIPT)
    assert source, f"{INIT_SCRIPT} is missing"
    script = pg.root / "01-init.sh"
    script.write_text(source)
    script.chmod(0o755)
    res = pg.run(
        ["bash", str(script)],
        POSTGRES_USER="postgres", POSTGRES_DB="postgres",
        APP_DB_USER="cgp", APP_DB_PASS=AWKWARD_PASSWORD, APP_DB_NAME="cgpbackbone",
    )
    assert res.returncode == 0, f"init script failed:\n{res.stderr}"


def _login(pg, password):
    return pg.run(
        [str(pg.bindir / "psql"), "-XtA", "-h", "127.0.0.1", "-U", "cgp", "-d", "cgpbackbone", "-c", "select current_user"],
        PGPASSWORD=password,
    )


@then("the application role can log in with that password")
def role_can_log_in(pg):
    assert pg.sql("select rolcanlogin from pg_roles where rolname = 'cgp'") == "t"
    res = _login(pg, AWKWARD_PASSWORD)
    assert res.returncode == 0 and res.stdout.strip() == "cgp", res.stderr


@then("the application database exists and is owned by that role")
def database_owned_by_role(pg):
    owner = pg.sql("select pg_get_userbyid(datdba) from pg_database where datname = 'cgpbackbone'")
    assert owner == "cgp", f"database 'cgpbackbone' is missing or owned by {owner!r}"


@then("a wrong password is rejected")
def wrong_password_rejected(pg):
    assert _login(pg, "not-the-password").returncode != 0
