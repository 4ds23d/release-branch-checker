import unittest
from src.main import is_release_branch

class TestReleaseBranchChecker(unittest.TestCase):

    def test_is_release_branch(self):
        self.assertTrue(is_release_branch('release/1.0.0', 'release'))

    def test_is_not_release_branch(self):
        self.assertFalse(is_release_branch('release/1.0.0', 'master'))

if __name__ == '__main__':
    unittest.main()