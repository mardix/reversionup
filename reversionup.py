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


__version__ = "0.3.0"
__author__ = "Mardix"
__license__ = "MIT"
__NAME__ = "ReversionUp"


import os
import re
import argparse
import subprocess
import ConfigParser
import sh

CWD = os.getcwd()

reversionup_file = CWD + "/setup.cfg"

def run(cmd):
    process = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return process.communicate()[0]


class Reversionup(object):
    """
    Class to save the reversion number.
    """
    section_name = "reversionup"

    DEFAULT_VERSION = "0.0.0"
    REGEX = re.compile('^(?P<major>(?:0|[1-9][0-9]*))'
                       '\.(?P<minor>(?:0|[1-9][0-9]*))'
                       '\.(?P<patch>(?:0|[1-9][0-9]*))'
                       '(\-(?P<prerelease>[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?'
                       '(\+(?P<build>[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?$')

    @classmethod
    def parse(cls, version):
        """
        Parse version to major, minor, patch, pre-release, build parts.
        :params version: string
        """
        match = cls.REGEX.match(version)
        if not match:
            raise ValueError("'%s' is not a valid SemVer string" % version)
        verinfo = match.groupdict()
        verinfo['major'] = int(verinfo['major'])
        verinfo['minor'] = int(verinfo['minor'])
        verinfo['patch'] = int(verinfo['patch'])
        return verinfo

    @classmethod
    def build_version(cls, parseinfo):
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

    def __init__(self, version=DEFAULT_VERSION, file=None):
        self._config = ConfigParser.ConfigParser()
        self._config.add_section(self.section_name)
        self._config.set(self.section_name, "version", version)
        self._file = file
        self.version = self.from_file(self._file) if file else version

    @property
    def version(self):
        """
        Return the string of the version
        :return: String
        """
        return self.build_version(self._version)

    @version.setter
    def version(self, version):
        self._version = self.parse(version)

    def from_file(self, file):
        """
        Load a version from a config file
        :param file:
        :return:
        """
        self._config.read(file)
        return self._config.get(self.section_name, "version")


    def write(self, file=None):
        """
        To write the config to file
        :param file:
        :return:
        """
        self._config.set(self.section_name, "version", self.version)
        with open(file or self._file, "w+") as f:
            self._config.write(f)

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
        return self.version

def main():
    """
    Main application
    :return:
    """
    try:
        parser = argparse.ArgumentParser(description="%s %s" % (__NAME__, __version__))
        parser.add_argument("-v", "--version",
                           help="Return the version [ie reversionup -v]",
                           action="store_true")
        parser.add_argument("-p", "--patch",
                           help="Increment PATCH version [ie reversionup -p]",
                           action="store_true")
        parser.add_argument("-n", "--minor",
                           help="Increment MINOR version and reset patch [ie reversionup -n]",
                           action="store_true")
        parser.add_argument("-m", "--major",
                           help="Increment MAJOR version and reset minor and patch [ie reversionup -m]",
                           action="store_true")
        parser.add_argument("-e", "--edit",
                           help="Manually edit the version number to bump to [ie: reversionup  -v 1.2.4]",
                           action="store")
        parser.add_argument("--tag",
                           help="To tag a release. Require git",
                           action="store_true")
        parser.add_argument("--push-tags",
                           help="To Push tags. Require git",
                           action="store_true")
        arg = parser.parse_args()

        rvnup = Reversionup(file=reversionup_file)

        if arg.edit:
            rvnup.version = arg.edit
        elif arg.patch:
            rvnup.inc_patch()
        elif arg.minor:
            rvnup.inc_minor()
        elif arg.major:
            rvnup.inc_major()
        #rvnup.write()

        print(rvnup.version)

        with sh.pushd(CWD):
            print type(sh.git("status", "--porcelain"))

        exit()

        print("-" * 80)
        print("%s: %s" % (__NAME__, version.version))

        # Tagging
        if arg.tag:
            v = "v%s" % version.version
            print("Git Tag: %s" % v)
            test = "if [[ -n $(cd %s; git status --porcelain) ]]; then echo 1; fi" % CWD
            if run(test).strip() == "1":
                raise Exception("Unable to TAG. There are uncommitted files")
            s = "git tag -a %s -m '%s'" % (v, v)
            run("cd %s; %s" % (CWD, s))

        if arg.push_tags:
            print("Git Push Tags....")
            s = "git push --tags"
            run("cd %s; %s" % (CWD, s))

        print("-" * 80)

    except Exception as ex:
        print("Error: %s" % ex.message)
        exit(1)
