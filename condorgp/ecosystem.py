from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pandas as pd


class Ecosystem():
    '''
    Ecosystem runs and manages the GP or trading runs

    Input:
        > Ecosystem data structure from previous, if specified

    Process:
        > instantiates GP or Trader as needed
        > pushes all cells through simple specified loop per cell

    Returns:
        > Ecosystem data structure
    '''

    _version_counter_by_ecosystem_and_run_id = {}

    def __init__(self, ecosystem_id=None, run_id=None, repository=None):
        self.ecosystem_id = ecosystem_id or self.generate_ecosystem_id()
        self.run_id = run_id or self.generate_run_id()
        self._snapshots_by_run_id = {self.run_id: []}
        self.repository = repository

    @staticmethod
    def generate_ecosystem_id():
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        suffix = uuid4().hex[:12]
        return f"eco-{timestamp}-{suffix}"

    @staticmethod
    def generate_run_id():
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        suffix = uuid4().hex[:12]
        return f"{timestamp}-{suffix}"

    def save_snapshot(self, data, run_id=None):
        target_run_id = run_id or self.run_id
        if target_run_id not in self._snapshots_by_run_id:
            self._snapshots_by_run_id[target_run_id] = []

        counter_key = (self.ecosystem_id, target_run_id)
        current_count = Ecosystem._version_counter_by_ecosystem_and_run_id.get(counter_key, 0)
        version = current_count + 1
        Ecosystem._version_counter_by_ecosystem_and_run_id[counter_key] = version
        snapshot = {
            "ecosystem_id": self.ecosystem_id,
            "run_id": target_run_id,
            "version": version,
            "data": data,
        }
        self._snapshots_by_run_id[target_run_id].append(snapshot)
        return snapshot

    def get_versions(self, run_id=None):
        target_run_id = run_id or self.run_id
        snapshots = self._snapshots_by_run_id.get(target_run_id, [])
        return [snapshot["version"] for snapshot in snapshots]

    def load_snapshot(self, version=None, run_id=None):
        target_run_id = run_id or self.run_id
        snapshots = self._snapshots_by_run_id.get(target_run_id, [])
        if not snapshots:
            raise ValueError("No snapshots found for this ecosystem")
        if version is None:
            return snapshots[-1]
        for snapshot in snapshots:
            if snapshot["version"] == version:
                return snapshot
        raise ValueError(f"Snapshot version {version} not found for run_id {target_run_id}")

    def save_and_persist_snapshot(self, data, run_id=None):
        snapshot = self.save_snapshot(data=data, run_id=run_id)
        if self.repository is not None:
            self.repository.save_snapshot(snapshot)
        return snapshot

    def run_gp_iterations(self):
        pass

    def run_trade_iterations(self):
        pass


class ParquetEcosystemRepository:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.cells_dir = self.root_path / "cells"
        self.runs_dir = self.root_path / "runs"
        self.cells_dir.mkdir(parents=True, exist_ok=True)
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    def save_snapshot(self, snapshot):
        ecosystem_id = snapshot["ecosystem_id"]
        run_id = snapshot["run_id"]
        version = snapshot["version"]

        cells_path = self.cells_dir / f"ecosystem_id={ecosystem_id}__run_id={run_id}__v={version}.parquet"
        runs_path = self.runs_dir / f"ecosystem_id={ecosystem_id}__run_id={run_id}.parquet"

        cells_df = pd.DataFrame(
            [
                {
                    "ecosystem_id": ecosystem_id,
                    "run_id": run_id,
                    "version": version,
                    "data": snapshot["data"],
                }
            ]
        )
        cells_df.to_parquet(cells_path, index=False)

        runs_df = pd.DataFrame(
            [
                {
                    "ecosystem_id": ecosystem_id,
                    "run_id": run_id,
                    "latest_version": version,
                    "updated_at_utc": datetime.now(timezone.utc).isoformat(),
                }
            ]
        )
        runs_df.to_parquet(runs_path, index=False)

        return {"backend": "parquet", "cells_path": cells_path, "runs_path": runs_path}


class InMemoryEcosystemRepository:
    def __init__(self):
        self._snapshots = []

    def save_snapshot(self, snapshot):
        self._snapshots.append(snapshot)
        return {"backend": "in_memory", "count": len(self._snapshots)}
