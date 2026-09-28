import json
import tempfile
import unittest
from pathlib import Path

from web_app import create_app


class WebAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tasks_file = Path(self.temp_dir.name) / "tasks.json"
        self.client = create_app(self.tasks_file).test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_task_persists_and_displays_it(self):
        response = self.client.post("/tasks", data={"title": "  Ship the app  "})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            json.loads(self.tasks_file.read_text(encoding="utf-8")),
            [{"title": "Ship the app", "done": False}],
        )
        self.assertIn("Ship the app", self.client.get("/").get_data(as_text=True))

    def test_blank_title_is_not_saved(self):
        self.client.post("/tasks", data={"title": "   "})

        self.assertFalse(self.tasks_file.exists())
        self.assertIn("Write a task", self.client.get("/").get_data(as_text=True))

    def test_toggle_and_delete_task(self):
        self.client.post("/tasks", data={"title": "Review"})
        self.client.post("/tasks/0/toggle")

        self.assertTrue(json.loads(self.tasks_file.read_text(encoding="utf-8"))[0]["done"])
        self.client.post("/tasks/0/delete")
        self.assertEqual(json.loads(self.tasks_file.read_text(encoding="utf-8")), [])

    def test_unknown_task_index_returns_not_found(self):
        self.assertEqual(self.client.post("/tasks/0/toggle").status_code, 404)


if __name__ == "__main__":
    unittest.main()