# GEDCOM_SSW553 

"""
Turki Alelyani

Project 2. SSW 555

"""
import sys

import time

class Solution():

	VALID_TAGS = set(['INDI','NAME','SEX','BIRT','DEAT','FAMC','FAMS','FAM','MARR','HUSB','WIFE','CHIL','DIV','DATE','HEAD','TRLR','NOTE'])

	def __init__(self, GEDCOMFileName):

		self.GEDCOMFileName = GEDCOMFileName

	def parseLine(self, line):

		level = line[0]

		try:

			secondWhitespaceIndex = line.index(' ', 2)

			tag = line[2:secondWhitespaceIndex]

			arg = line[secondWhitespaceIndex+1:]

			if level == '0':

				arg, tag = tag, arg

		except ValueError:

			tag = line[2:]

			arg = None

		print line

		print level

		print tag if tag in self.VALID_TAGS else "Invalid tag"

	def printFile(self):

		try:

			with open(self.GEDCOMFileName) as inFile:

				for line in inFile:

					self.parseLine(line.rstrip())


		except IOError:

			print 'GEDCOM file does not exist.'

if __name__ == '__main__':

	if len(sys.argv) != 2:

		print 'usage: assignment1a <GEDCOM file>'

	fileName = sys.argv[1]

	solution = Solution(fileName)

	solution.printFile()



	
