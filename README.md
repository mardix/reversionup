# SemVersion
---

SemVersion is a simple command line tool that helps you increment the version number 
of your project.

SemVersion follows strictly the 2.0.0 version of the [SemVer](http://semver.org/) scheme.

Version must be in the following scheme:

- major.minor.patch
   
- major.minor.patch-prerelease+build

SemVersion can be used along with Git to increment the version on each commit. 


---

## | Install

     pip install semversion
    

## | Command Line Tool: *semversion*

Use the command `semversion` in the command line to increment the version number.

	semversion 
	
In the current working directory, SemVersion will create `semversion.txt`, which is a one line text file that will contain the version. 

Accessed for the first time, the version will be `0.0.0`. But the commands below will help you increment the major, minor and patch number of the file.

---

** semversion -i **

Increment the patch number

	semversion -i

 	> 0.0.1

---

** semversion -i (-p|--patch) **

Increment the patch number

	semversion -i -p

 	> 0.0.2

---

** semversion -i (-n|--minor) **

Increment the minor number and reset the patch

	semversion -i -n

 	> 0.1.0

---

** semversion -i (-m|--major) **

Increment the major number and reset the minor and the patch number
	
	semversion -i -m
	
 	> 1.0.0


---


** semversion -i (-v|--version) [version]**

Insert your own version (semver compatible) version


	semversion -i -v 1.4.10
	
	> 1.4.10

---

	
##| Use as Module


### Increment Version 

	import semversion
	
	semversion_file = "./semversion.txt"
	
	v = semversion.File(semversion_file)
	
	# increment major
	v.inc_major()
	
	# increment minor
	# v.inc_minor()
	
	# increment patch
	# v.inc_patch()
	
	# save the file
	v.write()
	
### Read Version

	import semversion
	
	semversion_file = "./semversion.txt"
	
	v = semversion.File(semversion_file)
	
	my_app_version = v.version 
	
	# or
	# v.__str__()
	


---

License: MIT - Copyright 2014 Mardix
