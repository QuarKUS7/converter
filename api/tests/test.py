import unittest

from .app import app


class TestPost(unittest.TestCase):
    def test_post(self):

        self.test_app = api.test_client()

        response = self.test_api.get("/latest", content_type="html/text")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
