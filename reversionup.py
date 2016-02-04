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

    reversionup : show version number

    reversionup -p : increment path

    reversionup -n : increment minor

    reversionup -m : increment major

    reversionup --git-tag : To tag

    reversionup --git-push-tags: to push the tags

"""

__version__ = "0.2.3"
__author__ = "Mardix"
__license__ = "MIT"
__NAME__ = "ReversionUp"


import os
import re
import argparse
import subprocess

CWD = os.getcwd()

reversionup_file = CWD + "/reversionup.cfg"

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

def run(cmd):
    process = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return process.communicate()[0]

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

    def __init__(self, filename="./reversionup.cfg"):
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
        parser.add_argument("-p", "--patch",
                           help="Increment PATCH version [ie reversionup -p]",
                           action="store_true")
        parser.add_argument("-n", "--minor",
                           help="Increment MINOR version and reset patch [ie reversionup -n]",
                           action="store_true")
        parser.add_argument("-m", "--major",
                           help="Increment MAJOR version and reset minor and patch [ie reversionup -m]",
                           action="store_true")
        parser.add_argument("-v", "--version",
                           help="Manually enter the version number to bump to [ie: reversionup  -v 1.2.4]",
                           action="store")
        parser.add_argument("--git-tag",
                           help="To GIT TAG the release",
                           action="store_true")
        parser.add_argument("--git-push-tags",
                           help="To Push tags",
                           action="store_true")
        arg = parser.parse_args()
        version = File(reversionup_file)

        if arg.version:
            _version = arg.version
            version.write(_version)
        elif arg.patch:
            version.inc_patch()
            version.write()
        elif arg.minor:
            version.inc_minor()
            version.write()
        elif arg.major:
            version.inc_major()
            version.write()

        print("-" * 80)
        print("%s: %s" % (__NAME__, version.version))

        # Tagging
        if arg.git_tag:
            v = "v%s" % version.version
            print("Git Tag: %s" % v)
            test = "if [[ -n $(cd %s; git status --porcelain) ]]; then echo 1; fi" % CWD
            if run(test).strip() == "1":
                raise Exception("Unable to TAG. There are uncommitted files")
            s = "git tag -a %s -m '%s'" % (v, v)
            run("cd %s; %s" % (CWD, s))

        if arg.git_push_tags:
            print("Git Push Tags....")
            s = "git push --tags"
            run("cd %s; %s" % (CWD, s))

        print("-" * 80)

    except Exception as ex:
        print("Error: %s" % ex.message)
        exit(1)
