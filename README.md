# ReversionUp 

version: 0.3.x

---

ReversionUp, is a straight simple python module that helps you increment the version number
of your project. It can be used in the command line or accessed from your code.

ReversionUp follows strictly the 2.0.0 version of the [SemVer](http://semver.org/) scheme.

Version must be in the following scheme:

- major.minor.patch
   
- major.minor.patch-prerelease+build


---

## | Install

     pip install reversionup
    

## | Command Line Tool: *reversionup*

Use the command `reversionup` in the command line to increment the version number.

	reversionup 
	
In the current working directory, ReversionUp will create `reversionup.cfg`, which is a one line text file that will contain the version.

Accessed for the first time, the version will be `0.0.0`. But the commands below will help you increment the major, minor and patch number of the file.

---

**reversionup or reversionup (-v|--version)**

Show the current version number

	reversionup

 	> 0.0.1

---

**reversionup (-p|--patch)**

Increment the patch number

	reversionup -p

 	> 0.0.2

---

**reversionup (-n|--minor)**

Increment the minor number and reset the patch

	reversionup -n

 	> 0.1.0

---

**reversionup (-m|--major)**

Increment the major number and reset the minor and the patch number

	reversionup -m

 	> 1.0.0


---


**reversionup (-e|--edit) [version]**

Edit your own version (semver compatible) version

	reversionup -e 1.4.10

	> 1.4.10

---


---


##| Use as Module

As a module you can use the class `reversionup.Reversionup(version="0.0.0", file=None)` to access and increment the version.

## Examples
 
It is recommended to have a file `setup.cfg` with the option. This file will be used 
to save the versioning data.

    
	# setup.cfg
	
    [reversionup]
    version = 0.0.0


### Using the setup.cfg file and save the new version

	from reversionup import Reversionup
	
	filename = "setup.cfg"
	
	rvnup = Reversionup(file=filename)
	
	# read the version
	version = rvnup.version

	# increment major and reset minor and patch
	rvnup.inc_major()
	
	# increment minor and reset patch
	# rvnup.inc_minor()
	
	# increment patch
	# rvnup.inc_patch()
	
	# set the version manually 
	rvnup.version = "1.2.3"
	
	# Save the file
	rvnup.write()
	
	
### Manually load a version number and save to different file

	from reversionup import Reversionup

	rvnup = Reversionup("0.3.5")
	
	# read the version
	version = rvnup.version

	# increment major and reset minor and patch
	rvnup.inc_major()
	
	# increment minor and reset patch
	# rvnup.inc_minor()
	
	# increment patch
	# rvnup.inc_patch()
	
	# set the version manually 
	rvnup.version = "1.2.3"
	
	# Save the file to a different file
	rvnup.write("myfile.cfg")
	

---

## GIT Pre-Commit Hook

You can hook reversionup with git to update on each commit.

The script below will increase the patch number on commit. But you can find any other variant for it.

First (create if not exists) edit `.git/hooks/pre-commit` and add the code below.

	#!/bin/sh
	cd ./
	reversionup -p
	git add setup.cfg

Save it and type on the command line `chmod +x .git/hooks/pre-commit`

Now on each commit it will increase the patch number.

---

License: MIT - Copyright 2014-2016 Mardix
