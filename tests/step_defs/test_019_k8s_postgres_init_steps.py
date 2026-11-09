"""Topic D: the Postgres init script is delivered by ConfigMap and works (feature 019)."""

import os
import shutil
import socket
import subprocess
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from pytest_bdd import given, scenarios, then, when

from tests.k8s_helpers import REPO_ROOT, require_text, run, yaml_docs

scenarios("../features/019_k8s_postgres_init.feature")

POSTGRES_MANIFEST = "k8s/04-postgres.yaml"
COMPOSE_FILE = "docker_compose/docker-compose-db-graf-rmq.yml"
INIT_SCRIPT = "scripts/db_init/01-init.sh"
APP_VARS = {"APP_DB_USER", "APP_DB_PASS", "APP_DB_NAME"}
AWKWARD_PASSWORD = "p'a\"s$s;--\\x #{}"  # quotes, $, ;, SQL comment, backslash: all must survive


Doc = dict[str, Any]  # one parsed YAML document


def _by_kind(docs: list[Doc], kind: str) -> list[Doc]:
    """Return the documents of the given Kubernetes kind."""
    return [doc for doc in docs if doc.get("kind") == kind]


def _pod_spec(deployment: Doc) -> Doc:
    """Return the pod spec of a Deployment."""
    return deployment["spec"]["template"]["spec"]


def _database_volumes(pg_docs: list[Doc]) -> list[Doc]:
    """Return the volumes of the database Deployment's pod."""
    return _pod_spec(_by_kind(pg_docs, "Deployment")[0]).get("volumes", [])


# ---------------------------------------------------------------- manifest scenarios


@given("the Postgres manifest", target_fixture="pg_docs")
def postgres_manifest() -> list[Doc]:
    """Load the Postgres manifest and require a Deployment in it."""
    docs = yaml_docs(POSTGRES_MANIFEST)
    assert docs, f"{POSTGRES_MANIFEST} is missing or is not valid YAML"
    assert _by_kind(docs, "Deployment"), "no Deployment in the Postgres manifest"
    return docs


@when(
    "I look at how the database Deployment mounts its init scripts",
    target_fixture="init_volume",
)
def init_volume(pg_docs: list[Doc]) -> Doc:
    """Find the volume the init scripts are mounted from."""
    found = [vol for vol in _database_volumes(pg_docs) if vol.get("name") == "init-scripts"]
    assert found, "the Deployment has no 'init-scripts' volume"
    return found[0]


@then("they come from a ConfigMap that exists in the same namespace")
def init_from_configmap(init_volume: Doc, pg_docs: list[Doc]) -> None:
    """Require the init volume to be a ConfigMap defined in the Deployment's namespace."""
    assert (
        "configMap" in init_volume
    ), f"init-scripts is not a ConfigMap volume: {sorted(init_volume)}"
    name = init_volume["configMap"]["name"]
    deployment_ns = _by_kind(pg_docs, "Deployment")[0]["metadata"].get("namespace")
    maps = [doc for doc in _by_kind(pg_docs, "ConfigMap") if doc["metadata"]["name"] == name]
    assert maps, f"the volume refers to ConfigMap '{name}' but the manifest does not define it"
    assert maps[0]["metadata"].get("namespace") == deployment_ns
    assert "01-init.sh" in maps[0]["data"]


@then("the Postgres pod mounts no host path")
def no_host_path(pg_docs: list[Doc]) -> None:
    """Fail if any volume still points at a path on one machine's disk."""
    host_paths = [vol["name"] for vol in _database_volumes(pg_docs) if "hostPath" in vol]
    assert not host_paths, f"volumes still use a path on one machine's disk: {host_paths}"


@then("the ConfigMap script is identical to scripts/db_init/01-init.sh")
def configmap_matches_source(pg_docs: list[Doc]) -> None:
    """Require the ConfigMap copy to equal the script Docker Compose mounts."""
    maps = [
        doc for doc in _by_kind(pg_docs, "ConfigMap") if "01-init.sh" in (doc.get("data") or {})
    ]
    assert maps, "no ConfigMap in the manifest carries 01-init.sh"
    source = require_text(INIT_SCRIPT)
    assert (
        maps[0]["data"]["01-init.sh"].strip() == source.strip()
    ), f"ConfigMap copy differs from {INIT_SCRIPT}: update both together"


@then("the init volume is mounted with an executable mode")
def init_volume_executable(pg_docs: list[Doc]) -> None:
    """Require an executable defaultMode, without which the image skips the script."""
    volume = next((v for v in _database_volumes(pg_docs) if v.get("name") == "init-scripts"), None)
    assert volume and "configMap" in volume, "init-scripts is not a ConfigMap volume"
    mode = volume["configMap"].get("defaultMode")
    assert (
        mode is not None and mode & 0o111
    ), f"defaultMode {mode!r} leaves the script non-executable"


@then("the database container receives the Postgres password and the application role settings")
def pod_gets_variables(pg_docs: list[Doc]) -> None:
    """Require the database container to receive every variable the script reads."""
    container = _pod_spec(_by_kind(pg_docs, "Deployment")[0])["containers"][0]
    names = {entry["name"] for entry in container.get("env", [])}
    missing = ({"POSTGRES_PASSWORD"} | APP_VARS) - names
    assert not missing, f"the container is not given: {sorted(missing)}"


@given("the Docker Compose database service", target_fixture="compose_service")
def compose_service() -> Doc:
    """Find the Compose service that mounts scripts/db_init."""
    docs = yaml_docs(COMPOSE_FILE)
    assert docs, f"{COMPOSE_FILE} is missing or is not valid YAML"
    services = docs[0].get("services", {}).values()
    mounting = [
        service
        for service in services
        if any("db_init" in str(volume) for volume in service.get("volumes", []))
    ]
    assert mounting, "no Compose service mounts scripts/db_init"
    return mounting[0]


@then("it mounts scripts/db_init and passes the application role settings")
def compose_passes_variables(compose_service: Doc) -> None:
    """Compose must pass the same application role variables as Kubernetes."""
    env = compose_service.get("environment", [])
    names = set(env) if isinstance(env, dict) else {str(item).split("=", 1)[0] for item in env}
    assert names >= APP_VARS, f"Compose does not pass: {sorted(APP_VARS - names)}"


# ---------------------------------------------------------------- script behaviour


@given("the init script")
def init_script_exists() -> None:
    """Require the init script to exist."""
    assert (REPO_ROOT / INIT_SCRIPT).is_file(), f"{INIT_SCRIPT} is missing"


@when("I run it with the application database password missing", target_fixture="result")
def run_without_password() -> subprocess.CompletedProcess[str]:
    """Run the script with APP_DB_PASS unset."""
    env = {
        "PATH": os.environ["PATH"],
        "POSTGRES_USER": "postgres",
        "POSTGRES_DB": "postgres",
        "APP_DB_USER": "cgp",
        "APP_DB_NAME": "cgpbackbone",
    }
    return run(["bash", str(REPO_ROOT / INIT_SCRIPT)], env=env)


@then("it stops with a message naming APP_DB_PASS")
def stops_naming_variable(result: subprocess.CompletedProcess[str]) -> None:
    """Require the script to fail and say which variable is missing."""
    assert result.returncode != 0, "the script carried on without a password"
    assert "APP_DB_PASS" in result.stderr, result.stderr


# ---------------------------------------------------------------- real Postgres


def _pg_bin_dir() -> Path | None:
    """Locate the directory holding initdb, pg_ctl and psql (newest installed version)."""
    found = shutil.which("initdb")
    if found:
        return Path(found).parent
    candidates = sorted(
        Path("/usr/lib/postgresql").glob("*/bin/initdb"),
        key=lambda path: int(path.parent.parent.name) if path.parent.parent.name.isdigit() else 0,
    )
    return candidates[-1].parent if candidates else None


class ThrowawayPostgres:
    """A real Postgres in a temp dir. Runs as the 'postgres' OS user when the tests run as root."""

    def __init__(self, bindir: Path) -> None:
        """Prepare (but do not start) a server whose files live under a new temp dir."""
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
    def _free_port() -> int:
        """Ask the OS for a currently unused TCP port on localhost."""
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]

    def env(self, **extra: str) -> dict[str, str]:
        """Return a minimal environment pointing client tools at this server."""
        base = {
            "PATH": f"{self.bindir}:/usr/bin:/bin",
            "PGHOST": str(self.sock),
            "PGPORT": str(self.port),
        }
        return {**base, **extra}

    def run(self, cmd: list[str], **extra_env: str) -> subprocess.CompletedProcess[str]:
        """Run a command against this server, as the postgres OS user when started as root."""
        env = self.env(**extra_env)
        if self.as_root:
            assignments = [f"{name}={value}" for name, value in env.items()]
            cmd = ["runuser", "-u", "postgres", "--", "env", "-i", *assignments, *cmd]
            return run(cmd)
        return run(cmd, env=env)

    def start(self) -> None:
        """Create the data directory and start the server."""
        res = self.run(
            [
                str(self.bindir / "initdb"),
                "-D",
                str(self.data),
                "-U",
                "postgres",
                "--auth-local=trust",
                "--auth-host=scram-sha-256",
                "-E",
                "UTF8",
                "--no-sync",
            ]
        )
        assert res.returncode == 0, res.stderr
        options = f"-p {self.port} -k {self.sock} -c listen_addresses=127.0.0.1 -c fsync=off"
        res = self.run(
            [
                str(self.bindir / "pg_ctl"),
                "-D",
                str(self.data),
                "-w",
                "-l",
                str(self.root / "pg.log"),
                "-o",
                options,
                "start",
            ]
        )
        assert res.returncode == 0, res.stderr + (self.root / "pg.log").read_text()

    def stop(self) -> None:
        """Stop the server and delete its files."""
        self.run([str(self.bindir / "pg_ctl"), "-D", str(self.data), "-m", "immediate", "stop"])
        shutil.rmtree(self.root, ignore_errors=True)

    def sql(self, query: str, user: str = "postgres", dbname: str = "postgres") -> str:
        """Run one SQL statement and return its trimmed output."""
        res = self.run([str(self.bindir / "psql"), "-XtA", "-U", user, "-d", dbname, "-c", query])
        assert res.returncode == 0, res.stderr
        return res.stdout.strip()


@pytest.fixture
def throwaway_pg() -> Iterator[ThrowawayPostgres]:
    """Start a real Postgres for one test and always stop it afterwards."""
    bindir = _pg_bin_dir()
    if bindir is None or not (bindir / "pg_ctl").exists() or not (bindir / "psql").exists():
        pytest.skip(
            "needs a local PostgreSQL server (initdb, pg_ctl, psql); "
            "e.g. `sudo apt install postgresql`"
        )
    server = ThrowawayPostgres(bindir)
    try:
        server.start()
        yield server
    finally:
        server.stop()


@given("a throwaway Postgres server", target_fixture="pg")
def throwaway_postgres(throwaway_pg: ThrowawayPostgres) -> ThrowawayPostgres:
    """Hand the running server to the scenario."""
    return throwaway_pg


def _run_init_script(pg: ThrowawayPostgres, postgres_db: str) -> subprocess.CompletedProcess[str]:
    """Run the repo's init script against the throwaway server, the way the image would."""
    script = pg.root / "01-init.sh"
    script.write_text(require_text(INIT_SCRIPT))
    script.chmod(0o755)
    return pg.run(
        ["bash", str(script)],
        POSTGRES_USER="postgres",
        POSTGRES_DB=postgres_db,
        APP_DB_USER="cgp",
        APP_DB_PASS=AWKWARD_PASSWORD,
        APP_DB_NAME="cgpbackbone",
    )


@given("the application database already exists, owned by the superuser")
def app_db_precreated(pg: ThrowawayPostgres) -> None:
    """Create the database first, as the official image does for POSTGRES_DB.

    In this repo POSTGRES_DB and APP_DB_NAME are the same name, so the script
    meets an existing database.
    """
    pg.sql("create database cgpbackbone")


@when("I run the init script with POSTGRES_DB set to that same database")
def run_init_script_existing_db(pg: ThrowawayPostgres) -> None:
    """Run the script when the application database already exists."""
    res = _run_init_script(pg, postgres_db="cgpbackbone")
    assert (
        res.returncode == 0
    ), f"init script failed when the database already existed:\n{res.stderr}"


@when("I run the init script with an awkward password")
def run_init_script(pg: ThrowawayPostgres) -> None:
    """Run the script with a password full of quotes and shell/SQL metacharacters."""
    res = _run_init_script(pg, postgres_db="postgres")
    assert res.returncode == 0, f"init script failed:\n{res.stderr}"


def _login(pg: ThrowawayPostgres, password: str) -> subprocess.CompletedProcess[str]:
    """Try to log in as the application role over TCP with the given password."""
    return pg.run(
        [
            str(pg.bindir / "psql"),
            "-XtA",
            "-h",
            "127.0.0.1",
            "-U",
            "cgp",
            "-d",
            "cgpbackbone",
            "-c",
            "select current_user",
        ],
        PGPASSWORD=password,
    )


@then("the application role can log in with that password")
def role_can_log_in(pg: ThrowawayPostgres) -> None:
    """Require the role to exist, be able to log in, and accept the awkward password."""
    assert pg.sql("select rolcanlogin from pg_roles where rolname = 'cgp'") == "t"
    res = _login(pg, AWKWARD_PASSWORD)
    assert res.returncode == 0 and res.stdout.strip() == "cgp", res.stderr


@then("the application database exists and is owned by that role")
def database_owned_by_role(pg: ThrowawayPostgres) -> None:
    """Require the database to exist and belong to the application role."""
    owner = pg.sql("select pg_get_userbyid(datdba) from pg_database where datname = 'cgpbackbone'")
    assert owner == "cgp", f"database 'cgpbackbone' is missing or owned by {owner!r}"


@then("a wrong password is rejected")
def wrong_password_rejected(pg: ThrowawayPostgres) -> None:
    """Require a wrong password to be refused, proving real password authentication."""
    assert _login(pg, "not-the-password").returncode != 0
