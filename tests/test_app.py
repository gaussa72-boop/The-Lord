import os
import tempfile
import unittest

os.environ["THE_LORD_DB_PATH"] = os.path.join(tempfile.gettempdir(), "the_lord_test.sqlite3")

import app as lord_app

class AgentNetworkTests(unittest.TestCase):
    def setUp(self):
        self.client = lord_app.app.test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["ok"])

    def test_agent_catalog_is_visible(self):
        response = self.client.get("/api/v1/agents")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json["agents"]), 1)

    def test_update_proposals_require_admin_key(self):
        response = self.client.post("/api/v1/updates/proposals", json={"repo":"owner/repo","summary":"test"})
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
