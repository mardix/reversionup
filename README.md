# ReversionUp
---

ReversionUp, is a simple command line tool that helps you increment the version number
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
	
In the current working directory, ReversionUp will create `reversionup.txt`, which is a one line text file that will contain the version. 

Accessed for the first time, the version will be `0.0.0`. But the commands below will help you increment the major, minor and patch number of the file.

---

** reversionup -i **

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


### Increment Version 

	import reversionup
	
	reversionup_file = "./reversionup.txt"
	
	v = reversionup.File(reversionup_file)
	
	# increment major
	v.inc_major()
	
	# increment minor
	# v.inc_minor()
	
	# increment patch
	# v.inc_patch()
	
	# save the file
	v.write()
	
### Read Version

	import reversionup
	
	reversionup_file = "./reversionup.txt"
	
	v = reversionup.File(reversionup_file)
	
	my_app_version = v.version 
	
	# or
	# v.__str__()
	


---

License: MIT - Copyright 2014 Mardix
