import unittest
from reversionup import Reversionup

class TestSemver(unittest.TestCase):
    def test_should_parse_version(self):
        self.assertEqual(
            Reversionup.parse("1.2.3-alpha.1.2+build.11.e0f985a"),
            {'major': 1,
             'minor': 2,
             'patch': 3,
             'prerelease': 'alpha.1.2',
             'build': 'build.11.e0f985a'})

        self.assertEqual(
            Reversionup.parse("1.2.3-alpha-1+build.11.e0f985a"),
            {'major': 1,
             'minor': 2,
             'patch': 3,
             'prerelease': 'alpha-1',
             'build': 'build.11.e0f985a'})

    def test_should_raise_value_error_for_zero_prefixed_versions(self):
        self.assertRaises(ValueError, Reversionup.parse, "01.2.3")
        self.assertRaises(ValueError, Reversionup.parse, "1.02.3")
        self.assertRaises(ValueError, Reversionup.parse, "1.2.03")

    def test_build_version(self):
        v = "1.2.3-alpha.1.2+build.11.e0f985a"
        parse = Reversionup.parse(v)
        self.assertEqual(Reversionup.build_version(parse), v)

    def test_increase_major(self):
        v = "1.2.3"
        rvnup = Reversionup(v)
        rvnup.inc_major()
        self.assertEqual(rvnup.version, "2.0.0")

    def test_increase_minor(self):
        v = "1.2.3"
        rvnup = Reversionup(v)
        rvnup.inc_minor()
        self.assertEqual(rvnup.version, "1.3.0")

    def test_increase_patch(self):
        v = "1.2.3"
        rvnup = Reversionup(v)
        rvnup.inc_patch()
        self.assertEqual(rvnup.version, "1.2.4")

    def test_manual_set(self):
        v = "1.2.3"
        rvnup = Reversionup(v)
        rvnup.version = "1.2.10"
        self.assertEqual(rvnup.version, "1.2.10")

if __name__ == '__main__':
    unittest.main()

