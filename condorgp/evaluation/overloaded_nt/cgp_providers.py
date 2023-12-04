from nautilus_trader.test_kit.providers import TestDataProvider
from condorgp.params import Params
import fsspec
import pathlib


class CondorGPTestDataProvider(TestDataProvider):
    """
    Provides an API to load data from either the 'test/' directory or the projects
    GitHub repo.

    Parameters
    ----------
    branch : str
        The NautilusTrader GitHub branch for the path.

    """

    def __init__(self, branch: str = "develop") -> None:
        TestDataProvider.__init__(self)

    @staticmethod
    def _test_data_directory() -> str | None:
        # override so next-door repo can use Nautilus Trader repo test data
        p = Params()
        test_data_dir = pathlib.Path(
            p.test_dict['NAUTILUS_TEST_DATA_PATH'])
        if test_data_dir.exists():
            return str(test_data_dir)
        else:
            return None

    def _determine_filesystem(self) -> None:
        test_data_dir = CondorGPTestDataProvider._test_data_directory()
        if test_data_dir:
            self.root = test_data_dir
            self.fs = fsspec.filesystem("file")
        else:
            print("Couldn't find test data directory, test data will be pulled from GitHub")
            self.root = "tests/test_data"
            self.fs = fsspec.filesystem("github", org="nautechsystems", repo="nautilus_trader")
