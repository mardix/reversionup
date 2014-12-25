import unittest
import reversionup

class TestSemver(unittest.TestCase):
    def test_should_parse_version(self):
        self.assertEqual(
            reversionup.parse("1.2.3-alpha.1.2+build.11.e0f985a"),
            {'major': 1,
             'minor': 2,
             'patch': 3,
             'prerelease': 'alpha.1.2',
             'build': 'build.11.e0f985a'})

        self.assertEqual(
            reversionup.parse("1.2.3-alpha-1+build.11.e0f985a"),
            {'major': 1,
             'minor': 2,
             'patch': 3,
             'prerelease': 'alpha-1',
             'build': 'build.11.e0f985a'})

    def test_should_raise_value_error_for_zero_prefixed_versions(self):
        self.assertRaises(ValueError, reversionup.parse, "01.2.3")
        self.assertRaises(ValueError, reversionup.parse, "1.02.3")
        self.assertRaises(ValueError, reversionup.parse, "1.2.03")

    def test_build_version(self):
        v = "1.2.3-alpha.1.2+build.11.e0f985a"
        parse = reversionup.parse(v)
        self.assertEqual(reversionup.build_version(parse), v)

    def test_increase_major(self):
        v = "1.2.3"
        version = reversionup.Version(v)
        version.inc_major()
        self.assertEqual(version.version, "2.0.0")

    def test_increase_minor(self):
        v = "1.2.3"
        version = reversionup.Version(v)
        version.inc_minor()
        self.assertEqual(version.version, "1.3.0")

    def test_increase_patch(self):
        v = "1.2.3"
        version = reversionup.Version(v)
        version.inc_patch()
        self.assertEqual(version.version, "1.2.4")


if __name__ == '__main__':
    unittest.main()