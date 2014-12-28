# ReversionUp
---

ReversionUp, is a straight simple command line tool that helps you increment the version number
of your project.

ReversionUp follows strictly the 2.0.0 version of the [SemVer](http://semver.org/) scheme.

Version must be in the following scheme:

- major.minor.patch
   
- major.minor.patch-prerelease+build

ReversionUp can be used along with Git to increment the version on each commit. 


---

## | Install

     pip install reversionup
    

## | Command Line Tool: *reversionup*

Use the command `reversionup` in the command line to increment the version number.

	reversionup 
	
In the current working directory, ReversionUp will create `reversionup.cnf`, which is a one line text file that will contain the version.

Accessed for the first time, the version will be `0.0.0`. But the commands below will help you increment the major, minor and patch number of the file.

---

**reversionup -i**

Increment the patch number

	reversionup -i

 	> 0.0.1

---

**reversionup -i (-p|--patch)**

Increment the patch number

	reversionup -i -p

 	> 0.0.2

---

**reversionup -i (-n|--minor)**

Increment the minor number and reset the patch

	reversionup -i -n

 	> 0.1.0

---

**reversionup -i (-m|--major)**

Increment the major number and reset the minor and the patch number

	reversionup -i -m

 	> 1.0.0


---


**reversionup -i (-v|--version) [version]**

Insert your own version (semver compatible) version

	reversionup -i -v 1.4.10

	> 1.4.10

---


##| Use as Module

As a module you can use the class `reversionup.File(filename)` to access and increment the version.

If a filename is not provided, by default it will access (and create) `reversionup.cnf` in
the current directory.


### Increment Version 

	import reversionup
	
	v = reversionup.File()
	
	# increment major and reset minor and patch
	v.inc_major()
	
	# increment minor and reset patch
	# v.inc_minor()
	
	# increment patch
	# v.inc_patch()
	
	# save the file
	v.write()
	
### Read Version

	import reversionup

	v = reversionup.File()
	
	my_app_version = v.version 
	
	# or
	# v.__str__()



### reversionup.Version

This class access and manipulate the version. It doesn't save the version.

To save the version, use and save the property `version` in the object which is a string.


	import reversionup

	my_v = "1.2.3"

	v = reversionup.Version(my_v)

	# increment major and reset minor and patch
	v.inc_major()

	# increment minor and reset patch
	# v.inc_minor()

	# increment patch
	# v.inc_patch()

	# Get the new version
	my_new_version = v.version

	# or
	# v.__str__()

---

## GIT Pre-Commit Hook

You can hook reversionup with git to update on each commit.

The script below will increase the patch number on commit. But you can find any other variant for it.

First (create if not exists) edit `.git/hooks/pre-commit` and add the code below.

	#!/bin/sh
	cd ./
	reversionup -i
	git add -p

Save it and type on the command line `chmod +x .git/hooks/pre-commit`

Now on each commit it will increase the patch number.

---

License: MIT - Copyright 2014 Mardix
