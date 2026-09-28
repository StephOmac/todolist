import json
import tempfile
import unittest
from pathlib import Path

from todo_app import TaskStore


class TaskStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "tasks.json"
        self.store = TaskStore(self.path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_trims_title_and_persists_task(self):
        self.assertTrue(self.store.add("  Buy milk  "))
        self.assertEqual(self.store.tasks, [{"title": "Buy milk", "done": False}])
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8")), self.store.tasks)

    def test_blank_task_is_not_added(self):
        self.assertFalse(self.store.add("   "))
        self.assertEqual(self.store.tasks, [])

    def test_toggle_and_delete_persist(self):
        self.store.add("Read")
        self.store.toggle(0)
        self.assertTrue(TaskStore(self.path).tasks[0]["done"])
        self.store.delete(0)
        self.assertEqual(TaskStore(self.path).tasks, [])


if __name__ == "__main__":
    unittest.main()