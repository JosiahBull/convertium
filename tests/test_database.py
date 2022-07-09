import unittest
import psycopg2
from src.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        # remove entry from the database
        with psycopg2.connect(
            user="convertium",
            password="convertium",
            host="localhost",
            port=5432,
            dbname="convertium_test",
        ) as conn:
            with conn.cursor() as curr:
                curr.execute("DROP TABLE IF EXISTS paths;")

    def test_add(self) -> None:
        """
        Test adding an item to the database
        """
        db = Database(host="localhost", dbname="convertium_test")
        db.add("test_video_1.mp4")
        with psycopg2.connect(
            user="convertium",
            password="convertium",
            host="localhost",
            port=5432,
            dbname="convertium_test",
        ) as conn:
            with conn.cursor() as curr:
                curr.execute(
                    "SELECT * FROM paths WHERE path = %s;", ("test_video_1.mp4",)
                )
                self.assertEqual(curr.rowcount, 1)

    def test_contains(self) -> None:
        """
        Test if an item is in the database
        """
        db = Database(host="localhost", dbname="convertium_test")
        self.assertFalse(db.contains("test_video_2.mp4"))
        db.add("test_video_2.mp4")
        self.assertTrue(db.contains("test_video_2.mp4"))
        self.assertFalse(db.contains("test_video_3.mp4"))

    def tearDown(self) -> None:
        # remove entry from the database
        with psycopg2.connect(
            user="convertium",
            password="convertium",
            host="localhost",
            port=5432,
            dbname="convertium_test",
        ) as conn:
            with conn.cursor() as curr:
                curr.execute("DROP TABLE IF EXISTS paths;")


if __name__ == "__main__":
    unittest.main()
