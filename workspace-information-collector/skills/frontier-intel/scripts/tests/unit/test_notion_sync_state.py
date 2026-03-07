import tempfile
import unittest
from pathlib import Path

from scripts.lib.notion.sync import NotionSyncState


class NotionSyncStateTest(unittest.TestCase):
    def test_sync_state_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            state = NotionSyncState(project_dir)
            payload = {"items": {"a": "page-1"}, "digests": {"daily-1": "page-2"}}

            state.write(payload)
            loaded = state.read()

            self.assertEqual(loaded, payload)


if __name__ == "__main__":
    unittest.main()
