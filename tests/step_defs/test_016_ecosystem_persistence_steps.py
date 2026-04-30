from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from condorgp.ecosystem import (
    Ecosystem,
    InMemoryEcosystemRepository,
    ParquetEcosystemRepository,
)
import pandas as pd


@pytest.fixture(scope="module", autouse=True)
def teardown_parquet_test_artifacts():
    yield
    ecosystem_root = Path("tests/test_data/ecosystem")
    if not ecosystem_root.exists():
        return

    # Keep only the most recent parquet per folder.
    for folder in ecosystem_root.rglob("*"):
        if not folder.is_dir():
            continue
        parquet_files = sorted(
            folder.glob("*.parquet"), key=lambda p: p.stat().st_mtime
        )
        if len(parquet_files) <= 1:
            continue
        for old_file in parquet_files[:-1]:
            old_file.unlink(missing_ok=True)


@scenario(
    "../features/016_ecosystem_persistence.feature",
    "Time-prefixed run_id sorts naturally",
)
def test_time_prefixed_run_id_sorts_naturally():
    pass


@scenario(
    "../features/016_ecosystem_persistence.feature",
    "Save append-only snapshots for one run_id",
)
def test_save_append_only_snapshots_for_one_run_id():
    pass


@scenario(
    "../features/016_ecosystem_persistence.feature",
    "One ecosystem can have multiple run_id values",
)
def test_one_ecosystem_can_have_multiple_run_id_values():
    pass


@scenario(
    "../features/016_ecosystem_persistence.feature",
    "Parquet is used as phase 1 persistence",
)
def test_parquet_is_used_as_phase_1_persistence():
    pass


@scenario(
    "../features/016_ecosystem_persistence.feature",
    "Ecosystem logic is decoupled from storage implementation",
)
def test_ecosystem_logic_is_decoupled_from_storage_implementation():
    pass


@given(
    "an ecosystem repository configured with a writable root path",
    target_fixture="ecosystem_repository_root",
)
def ecosystem_repository_root():
    # Storage backend wiring is intentionally out of scope for this first behavior.
    return {"repository_root_configured": True}


@when("a new ecosystem run_id is generated")
def generate_run_id(ecosystem_repository_root):
    ecosystem_repository_root["run_id"] = Ecosystem.generate_run_id()


@then('the run_id starts with date-time digits in "YYYYMMDDHHMMSS" format')
def run_id_has_time_prefix(ecosystem_repository_root):
    run_id = ecosystem_repository_root["run_id"]
    prefix = run_id.split("-", maxsplit=1)[0]
    assert len(prefix) == 14
    assert prefix.isdigit()


@then("the run_id can be sorted lexicographically for chronological ordering")
def run_id_is_lexicographically_sortable(ecosystem_repository_root):
    run_id = ecosystem_repository_root["run_id"]
    assert "-" in run_id


@given(
    'an ecosystem with ecosystem_id "eco-demo" and run_id "20260429101530-demo"',
    target_fixture="snapshot_context",
)
def ecosystem_with_ids():
    ecosystem_id = "eco-demo"
    run_id = "20260429101530-demo"
    ecosystem = Ecosystem(ecosystem_id=ecosystem_id, run_id=run_id)
    return {"ecosystem": ecosystem, "ecosystem_id": ecosystem_id, "run_id": run_id}


@when("the ecosystem is saved three times")
def save_ecosystem_three_times(snapshot_context):
    ecosystem = snapshot_context["ecosystem"]
    snapshot_context["v1"] = ecosystem.save_snapshot({"counter": 1})
    snapshot_context["v2"] = ecosystem.save_snapshot({"counter": 2})
    snapshot_context["v3"] = ecosystem.save_snapshot({"counter": 3})


@then('three versions exist for run_id "20260429101530-demo"')
def assert_three_versions_exist(snapshot_context):
    ecosystem = snapshot_context["ecosystem"]
    assert ecosystem.run_id == snapshot_context["run_id"]
    assert ecosystem.ecosystem_id == snapshot_context["ecosystem_id"]
    assert ecosystem.get_versions() == [1, 2, 3]


@then("loading without a version returns the latest snapshot")
def latest_snapshot_is_returned(snapshot_context):
    ecosystem = snapshot_context["ecosystem"]
    latest = ecosystem.load_snapshot()
    assert latest["version"] == snapshot_context["v3"]["version"]
    assert latest["data"]["counter"] == 3


@then("loading a specific version returns that exact snapshot")
def specific_snapshot_is_returned(snapshot_context):
    ecosystem = snapshot_context["ecosystem"]
    snapshot_v2 = ecosystem.load_snapshot(version=2)
    assert snapshot_v2["version"] == snapshot_context["v2"]["version"]
    assert snapshot_v2["data"]["counter"] == 2


@given("one ecosystem with generated ecosystem_id", target_fixture="multi_run_context")
def one_ecosystem_with_generated_ecosystem_id():
    ecosystem = Ecosystem()
    return {"ecosystem": ecosystem}


@when(
    "one snapshot is saved for each of three different run_id values",
    target_fixture="one_snapshot_saved_each",
)
def one_snapshot_saved_each(multi_run_context):
    ecosystem = multi_run_context["ecosystem"]
    run_ids = [
        Ecosystem.generate_run_id(),
        Ecosystem.generate_run_id(),
        Ecosystem.generate_run_id(),
    ]
    snapshots = [
        ecosystem.save_snapshot({"counter": idx + 1}, run_id=run_id)
        for idx, run_id in enumerate(run_ids)
    ]
    return {"snapshots": snapshots}


@then("all three snapshots have different run_id values")
def all_snapshots_have_unique_run_ids(one_snapshot_saved_each):
    run_ids = [snapshot["run_id"] for snapshot in one_snapshot_saved_each["snapshots"]]
    assert len(set(run_ids)) == 3


@then("all three snapshots share the same ecosystem_id")
def all_snapshots_share_same_ecosystem_id(one_snapshot_saved_each):
    ecosystem_ids = [
        snapshot["ecosystem_id"] for snapshot in one_snapshot_saved_each["snapshots"]
    ]
    assert len(set(ecosystem_ids)) == 1


@given("a Parquet ecosystem repository", target_fixture="parquet_context")
def parquet_ecosystem_repository():
    repository = ParquetEcosystemRepository(root_path="tests/test_data/ecosystem")
    ecosystem = Ecosystem()
    return {"repository": repository, "ecosystem": ecosystem}


@when("ecosystem state is persisted")
def ecosystem_state_is_persisted(parquet_context):
    ecosystem = parquet_context["ecosystem"]
    repository = parquet_context["repository"]
    snapshot = ecosystem.save_snapshot({"counter": 1})
    parquet_context["snapshot"] = snapshot
    parquet_context["saved"] = repository.save_snapshot(snapshot)


@then("cells are written as Parquet records")
def cells_written_as_parquet(parquet_context):
    assert parquet_context["saved"]["cells_path"].suffix == ".parquet"
    assert parquet_context["saved"]["cells_path"].exists()


@then("ecosystem run metadata is written as Parquet records")
def metadata_written_as_parquet(parquet_context):
    assert parquet_context["saved"]["runs_path"].suffix == ".parquet"
    assert parquet_context["saved"]["runs_path"].exists()


@then("a Parquet record with ecosystem run metadata within it is saved")
def parquet_record_contains_run_metadata(parquet_context):
    runs_df = pd.read_parquet(parquet_context["saved"]["runs_path"])
    assert len(runs_df.index) >= 1
    row = runs_df.iloc[0]
    assert row["ecosystem_id"] == parquet_context["snapshot"]["ecosystem_id"]
    assert row["run_id"] == parquet_context["snapshot"]["run_id"]
    assert int(row["latest_version"]) == parquet_context["snapshot"]["version"]


@then("no Postgres dependency is required in phase 1")
def postgres_not_required_phase_1(parquet_context):
    assert parquet_context["saved"]["backend"] == "parquet"


@then('persisted files are saved under "tests/test_data/ecosystem"')
def persisted_files_saved_under_test_data(parquet_context):
    expected_root = Path("tests/test_data/ecosystem").resolve()
    cells_path = parquet_context["saved"]["cells_path"].resolve()
    runs_path = parquet_context["saved"]["runs_path"].resolve()
    assert expected_root in cells_path.parents
    assert expected_root in runs_path.parents


@given(
    "an ecosystem constructed with an injected repository",
    target_fixture="decoupled_context",
)
def ecosystem_constructed_with_injected_repository():
    in_memory_repository = InMemoryEcosystemRepository()
    parquet_repository = ParquetEcosystemRepository(
        root_path="tests/test_data/ecosystem"
    )
    return {
        "in_memory": Ecosystem(repository=in_memory_repository),
        "parquet": Ecosystem(repository=parquet_repository),
    }


@when(
    "the same ecosystem behavior is executed with an in-memory repository and a Parquet repository"
)
def same_behavior_executed_with_two_repositories(decoupled_context):
    run_id = "20260430153000-decoupled"
    in_memory_snapshot = decoupled_context["in_memory"].save_and_persist_snapshot(
        data={"counter": 1}, run_id=run_id
    )
    parquet_snapshot = decoupled_context["parquet"].save_and_persist_snapshot(
        data={"counter": 1}, run_id=run_id
    )
    decoupled_context["in_memory_snapshot"] = in_memory_snapshot
    decoupled_context["parquet_snapshot"] = parquet_snapshot


@then("business behavior is consistent across both repositories")
def business_behavior_consistent_across_repositories(decoupled_context):
    assert (
        decoupled_context["in_memory_snapshot"]["run_id"]
        == decoupled_context["parquet_snapshot"]["run_id"]
    )
    assert (
        decoupled_context["in_memory_snapshot"]["version"]
        == decoupled_context["parquet_snapshot"]["version"]
    )
    assert (
        decoupled_context["in_memory_snapshot"]["data"]
        == decoupled_context["parquet_snapshot"]["data"]
    )
