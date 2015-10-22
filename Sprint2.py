"""
Turki Alelyani
Vinod Tiwari
Project SSW 555
Gedcom Parser

"""

import sys

import time


class Person:

	def __init__(self, uniqueID):

		self.uniqueID = uniqueID

		self.name = None

		self.sex = None

		self.birth = None

		self.death = None

		self.childInFamily = None

		self.spouseInFamily = None



	def setDate(self, attr, date):

			if attr == 'birth':

				self.birth = date

			else:

				self.death = date



class Family:

	def __init__(self, uniqueID):

		self.uniqueID = uniqueID

		self.husband = None

		self.wife = None

		self.child = None

		self.marriage = None

		self.divorce = None



	def setDate(self, attr, date):

			if attr == 'marriage':

				self.marriage = date

			else:

				self.divorce = date



class SolutionWithReport():

	VALID_TAGS = set(['INDI','NAME','SEX','BIRT','DEAT','FAMC','FAMS','FAM','MARR','HUSB','WIFE','CHIL','DIV','DATE','HEAD','TRLR','NOTE'])



	def __init__(self, GEDCOMFileName):

		self.GEDCOMFileName = GEDCOMFileName

		self.families = {}

		self.people = {}

		self.levelCache = {0:None, 1:None}

		self.errors = []



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



		return (level, tag, arg) if tag in self.VALID_TAGS else (None, None, None)



	def extract(self):

		try:

			with open(self.GEDCOMFileName) as inFile:

				count = 1

				for line in inFile:

					level, tag, arg = self.parseLine(line.rstrip())



					# if the tag is valid

					if tag is not None:

						self.applyTag(count, tag, arg)



					count += 1



		except IOError:

			print 'GEDCOM file does not exist.'



	def applyTag(self, lineNumber, tag, arg):

		# Person related tags

		if tag == 'INDI':

			person = Person(arg)

			self.people[person.uniqueID] = person

			self.levelCache[0] = person

			self.levelCache[1] = None

		elif tag == 'NAME' and self.levelCache[0] != None:

			self.levelCache[0].name = arg

		elif tag == 'SEX':

			self.levelCache[0].sex = arg

		elif tag == 'BIRT':

			self.levelCache[1] = 'birth'

		elif tag == 'DEAT':

			self.levelCache[1] = 'death'

		elif tag == 'FAMC':

			if arg not in self.families:

				pass

			else:

				self.levelCache[0].childInFamily = families[arg]

				families[arg].child = self.levelCache[0]

		elif tag == 'FAMS':

			if arg not in self.families:

				pass

			else:

				self.levelCache[0].spouseInFamily = families[arg]



		# Family related tags

		elif tag == 'FAM':

			family = Family(arg)

			self.families[family.uniqueID] = family

			self.levelCache[0] = family

			self.levelCache[1] = None

		elif tag == 'MARR':

			self.levelCache[1] = 'marriage'

		elif tag == 'HUSB':

			if arg not in self.people:

				pass

			else:

				self.levelCache[0].husband = self.people[arg]

				self.people[arg].spouseInFamily = self.levelCache[0]



			if self.levelCache[0].wife is not None and self.levelCache[0].wife.death is not None:

				self.errors.append("Error 3, line {}: {} ({}) has a marriage of a dead person {} ({}).".format(lineNumber, self.levelCache[0].husband.name, self.levelCache[0].husband.uniqueID, self.levelCache[0].wife.name, self.levelCache[0].wife.uniqueID))



			if self.people[arg].sex == 'F':

				self.errors.append("Error 4, line {}: Female husband {} ({}) in Family {}.".format(lineNumber, self.levelCache[0].husband.name, self.levelCache[0].husband.uniqueID, self.levelCache[0].uniqueID))



		elif tag == 'WIFE':

			if arg not in self.people:

				pass

			else:

				self.levelCache[0].wife = self.people[arg]



				if self.people[arg].spouseInFamily is not None:

					self.errors.append("Anomaly 2, line {}: {} ({}) is being a spouse in two marriages ({}, {}) at the same time.".format(lineNumber, self.people[arg].name, self.people[arg].uniqueID, self.levelCache[0].uniqueID, self.people[arg].spouseInFamily.uniqueID))



				self.people[arg].spouseInFamily = self.levelCache[0]



			if self.levelCache[0].husband is not None and self.levelCache[0].husband.death is not None:

				self.errors.append("Error 3, line {}: {} ({}) has a marriage of a dead person {} ({}).".format(lineNumber, self.levelCache[0].wife.name, self.levelCache[0].wife.uniqueID, self.levelCache[0].husband.name, self.levelCache[0].husband.uniqueID))



		elif tag == 'CHIL':

			if arg not in self.people:

				pass

			else:

				self.levelCache[0].child = self.people[arg]

				self.people[arg].childInFamily = self.levelCache[0]



			if self.levelCache[0].marriage is not None and self.people[arg].birth < self.levelCache[0].marriage:

				self.errors.append("Anomaly 1, line {}: Birth date of {} (%) occurs before the marriage date of his parents in Family {}.".format(lineNumber, self.levelCache[0].child.name, self.levelCache[0].child.uniqueID, self.levelCache[0].uniqueID))



		elif tag == 'DIV':

			self.levelCache[1] = 'divorce'



		elif tag == 'DATE':

			if self.levelCache[1] is None:

				self.errors.append("Error 1, line {}: Date is not associated to any attribute.".format(lineNumber))

			else:

				self.levelCache[0].setDate(self.levelCache[1], time.strptime(arg, "%d %b %Y"))



				if self.levelCache[1] == 'death'and self.levelCache[0].death < self.levelCache[0].birth:

					self.errors.append("Error 2, line %d: Birth date of {} ({}) occurs after {} death date.".format(lineNumber, self.levelCache[0].name, self.levelCache[0].uniqueID, 'his' if self.levelCache[0].sex == 'M' else 'her'))



				self.levelCache[1] = None



		elif tag == 'HEAD':

			pass

		elif tag == 'TRLR':

			pass

		elif tag == 'NOTE':

			pass

		else:

			pass



	def generateReport(self):

		# report individuals

		print

		print "Individual found:"

		print "uniqueID\tname\t\tsex\tbirth date\tDeath"

		for uid in sorted(list(self.people.keys())):

			print "{}\t\t{}\t{}\t{}\t{}".format(uid, self.people[uid].name, self.people[uid].sex, time.strftime("%d %b %Y", self.people[uid].birth) if self.people[uid].birth is not None else "None", time.strftime("%d %b %Y", self.people[uid].death) if self.people[uid].death is not None else "Alive")



		print 



		print "Family found:"

		print "uniqueID\thusband\t\twife\t\tchild\t\tMarriage\tDivorce"

		for uid in sorted(list(self.families.keys())):

			print "{}\t\t{}\t{}\t{}\t{}\t{}".format(uid, self.families[uid].husband.name if self.families[uid].husband is not None else "None", self.families[uid].wife.name if self.families[uid].wife is not None else 'None', self.families[uid].child.name if self.families[uid].child is not None else 'None', time.strftime("%d %b %Y", self.families[uid].marriage) if self.families[uid].marriage is not None else "None", time.strftime("%d %b %Y", self.families[uid].divorce) if self.families[uid].divorce is not None else "None")



		print 



		print "Error found:"

		for error in self.errors:

			print error



if __name__ == '__main__':

	if len(sys.argv) != 2:

		print 'usage: assignment1b <GEDCOM file>'


	fileName = sys.argv[1]

	solution = SolutionWithReport(fileName)

	solution.extract()

	solution.generateReport()
	
