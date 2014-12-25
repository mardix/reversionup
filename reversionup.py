"""
ReversionUp

ReversionUp, is a simple command line tool that helps you increment the version number
of your project.

ReversionUp follows strictly the 2.0.0 version of the [SemVer](http://semver.org/) scheme.

Version must be in the following scheme:

- major.minor.patch

- major.minor.patch-prerelease+build

ReversionUp can be used along with Git to increment the version on each commit.

> [ReversionUp](https://github.com/mardix/reversionup)

Usage:

    reversionup -i
"""

__version__ = "0.1"
__author__ = "Mardix"
__license__ = "MIT"
__NAME__ = "ReversionUp"


import os
import re
import argparse

CWD = os.getcwd()
reversionup_file = CWD + "/reversionup.txt"


_REGEX = re.compile('^(?P<major>(?:0|[1-9][0-9]*))'
                    '\.(?P<minor>(?:0|[1-9][0-9]*))'
                    '\.(?P<patch>(?:0|[1-9][0-9]*))'
                    '(\-(?P<prerelease>[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?'
                    '(\+(?P<build>[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?$')

def parse(version):
    """
    Parse version to major, minor, patch, pre-release, build parts.
    :params version: string
    """
    match = _REGEX.match(version)
    if not match:
        raise ValueError("'%s' is not a valid SemVer string" % version)
    verinfo = match.groupdict()
    verinfo['major'] = int(verinfo['major'])
    verinfo['minor'] = int(verinfo['minor'])
    verinfo['patch'] = int(verinfo['patch'])
    return verinfo

def build_version(parseinfo):
    """
    Build the parseinfo back to string
    :param parseinfo: dict of {major, minor, patch, prerelease, build}
    :return: string of major.minor.patch[-release+build]
    """
    version = "%s.%s.%s" % (parseinfo["major"], parseinfo["minor"], parseinfo["patch"])
    if "prerelease" in parseinfo and parseinfo["prerelease"]:
        version += "-%s" % parseinfo["prerelease"]
    if "build" in parseinfo and parseinfo["build"]:
        if "prerelease" in parseinfo and parseinfo["prerelease"]:
            version += "+"
        version += parseinfo["build"]
    return version


class Version(object):
    """
    To increase versioning
    """
    _version = None

    def __init__(self, version):
        self._version = parse(version)

    def inc_major(self):
        """
        increase major and reset minor and patch
        :return: Object
        """
        self._version["major"] += 1
        self._version.update({"minor": 0, "patch": 0})
        return self

    def inc_minor(self):
        """
        increase minor and reset patch
        :return: Object
        """
        self._version["minor"] += 1
        self._version.update({"patch": 0})
        return self

    def inc_patch(self):
        """
        increase patch
        :return: Object
        """
        self._version["patch"] += 1
        return self

    def __str__(self):
        """
        return the string of the version
        :return: Object
        """
        return build_version(self._version)

    @property
    def version(self):
        """
        Return the string of the version
        :return: String
        """
        return self.__str__()

class File(Version):
    """
    To edit a reversionup file
    The file must contain 1 line, which is the version to edit
    If the file doesn't exist it will create it
    """
    filename = None

    def __init__(self, filename="./reversionup.txt"):
        self.filename = filename
        version = "0.0.0"
        if os.path.isfile(filename):
            with open(filename) as f:
                version = f.readline().strip() or "0.0.0"
        super(self.__class__, self).__init__(version)

    def write(self, version=None):
        """
        Write the version to file
        :param version: string. A valid semver to use
        :return:
        """
        if version:
            super(self.__class__, self).__init__(version)

        with open(self.filename, "wb") as f:
            f.write(self.__str__())

def main():
    """
    Main application
    :return:
    """
    try:
        parser = argparse.ArgumentParser(description="%s %s" % (__NAME__, __version__))
        parser.add_argument("-i", "--inc",
                            help="Automatically increment the version number",
                            action="store_true")
        parser.add_argument("-m", "--major",
                           help="Increment MAJOR version and reset minor and patch [ie -i -m]",
                           action="store_true")
        parser.add_argument("-n", "--minor",
                           help="Increment MINOR version and reset patch [ie -i -n]",
                           action="store_true")
        parser.add_argument("-p", "--patch",
                           help="Increment PATCH version [ie -i -p]",
                           action="store_true")
        parser.add_argument("-v", "--version",
                           help="Manually enter the version number to bump to [ie: -i -v 1.2.4]",
                           action="store")

        arg = parser.parse_args()

        version = File(reversionup_file)
        if arg.inc:
            if arg.version:
                _version = arg.version
                version.write(_version)
            else:
                if arg.major:
                    version.inc_major()
                elif arg.minor:
                    version.inc_minor()
                else:
                    version.inc_patch()
                version.write()
        print(version.version)
    except Exception as ex:
        print("Exception: %s" % ex.message)
