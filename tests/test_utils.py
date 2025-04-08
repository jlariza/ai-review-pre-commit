import unittest

from src.utils import todo_function


class TestUtils(unittest.TestCase):
    def test_todo_function_success(self):
        # Test case where the function should return True
        result = todo_function("This is a valid commit message.")
        self.assertTrue(result)

    def test_todo_function_failure(self):
        # Test case where the function should return False
        result = todo_function("TODO: This is a placeholder.")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
