#!/usr/bin/python
#
# tomsUlbFunctions.py: define functions useful for more than one program in /usr/local/bin
# ----------------------------------------------------------------------------------------
#
import getopt   # for processing command line options
import os       # for getting values for environment vars
import string
import sys      # for accessing command line arguments
import time     # for the date string in our backup file name

## from re import *
import re

## from subprocess import call, check_output
## from subprocess import Popen, PIPE
import subprocess

##
#  Wrapper function to run a command
#
def myCall( shellCommand ) :
	call( shellCommand, shell=True )

##
#  Wrapper function to run a command and return its output
#  Version 1 (untested...)
#
def runCommand ( shellCommand ) :
	process = Popen(["ls", "-la", "."], stdout=PIPE)
	(output, err) = process.communicate()
	exit_code = process.wait()
	return output

##
#  Wrapper to check_output function
#
def getCommandOutput( shellCommand, commandArgs ) :
	commandOutput = subprocess.check_output( [ shellCommand, commandArgs ] )
	return commandOutput

##
#  Determine whether we are using Yocto Linux (on the Edison)
#  If not, assume debian
#
def isYoctoLinux() :
	unameOutput = getCommandOutput( 'uname', '-a' )
	pattern = re.compile( 'poky' )
	matchObjectOrNone = pattern.search( unameOutput )
##	print( 'unameOutput: ' + unameOutput )
##	print( 'matchObjectOrNone: ' + str(matchObjectOrNone) )
	if( str(matchObjectOrNone) == 'None' ) :
		isYocto = False
	else :
		isYocto = True
	return isYocto

##
# Runs ps command and returns lines containing string to match
#
def getMatchingProcesses( toMatch ) :
	if ( isYoctoLinux() ) :
		psCommandArgs = ''
	else :
		psCommandArgs = '-aef'
	psCommandOutput = getCommandOutput( 'ps', psCommandArgs )
	psOutputLines = string.split( psCommandOutput, '\n' )
	matchingLines = []
	if( len(toMatch) > 0 ) :
		pattern = re.compile( toMatch )
		for psLine in psOutputLines :
			matchObjectOrNone = pattern.search( psLine )
			if( str(matchObjectOrNone) != 'None' ) :
				matchingLines.append( psLine )
	else :
		matchingLines = psOutputLines
	for matchingLine in matchingLines :
		print( 'matchingLine: ' + matchingLine )
	return matchingLines

#
#  Process the command line arguments.
#
def processArguments( backupOrRestore ) :
	siteArg = ''
	suffixArg = ''
	if ( len(sys.argv) == 2 ) :
		if ( sys.argv[1] == '--help' ) :
			syntax( backupOrRestore )
			exit( 0 )
		siteArg = sys.argv[1]
	elif ( len(sys.argv) == 3 ) :
		siteArg = sys.argv[1]
		suffixArg = sys.argv[2]
	elif ( backupOrRestore == 'command' ) :   # Really a trivial case (no file name involved)
		siteArg = 'all'                        # TODO: implement in a future iteration
	else :
		syntax( backupOrRestore )
		print( 'Wrong number of args.' )
		print( 'len(sys.argv) =', len(sys.argv) )
		print( 'str(sys.argv) =', str(sys.argv) )
		exit( 1 )
	arguments = [siteArg, suffixArg]
	return arguments

#
#  Display a brief syntax statement, describing the options and purpose of the script
#
def syntax( backupOrRestore ) :
	restoreOptions = ''
	if( backupOrRestore == 'restore' ) :
		restoreOptions = '[-d YYYY_MM_DD] [-h hostName]'
	basename = os.path.basename( sys.argv[0] )
	print( 'Syntax:' )
	print( '  ' + basename + ' [--help] ' + restoreOptions + ' site [suffix]' )
	if( backupOrRestore == 'restore' ) :
		print( '    -d: optionally override today\'s date in fileName (YYYY_MM_DD)' )
		print( '    -h: optionally override current hostName in fileName' )
	print( '    --help: display syntax statement then exit' )
	print( '    site: site name or recognized abbreviation' )
	print( '    suffix: optional string appended to standard backup file name' )
	if( backupOrRestore == 'backup' ) :
		print( 'Saves a copy of database in a file named as follows:' )
	else :
		print( 'Restores a copy of database from a file named as follows:' )
	print( '  siteName-YYYY_MM_DD-hostname[-suffix].sql.gz' )

