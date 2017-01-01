import csv
import math
import requests
from datetime import date
from BeautifulSoup import BeautifulSoup

def determineBustSize(measurements):
	bustSize = ''
	bustSize_Huge = 'Huge'
	bustSize_Large = 'Large'
	bustSize_Medium = 'Medium'
	bustSize_Small = 'Small'
	bustSizeTiny = 'Tiny'
	bustSizeUndetermined = 'Undetermined'

	tinyBust = 'A'
	smallBust = 'B'
	mediumBust = 'C'
	largeBust = ['D', 'DD']
	hugeBust = ['DDD', 'E', 'F', 'G', 'GG', 'H', 'MM', 'ZZ']

	cup = measurements[2:measurements.find('-')]

	if cup == mediumBust:
		bustSize = bustSize_Medium
	elif cup == smallBust:
		bustSize = bustSize_Small
	elif cup == tinyBust:
		bustSize = bustSizeTiny
	else:
		bustSize = ''

	for hugeCup in hugeBust:
		if cup == hugeCup:
			bustSize = bustSize_Huge
	for largeCup in largeBust:
		if cup == largeCup:
			bustSize = bustSize_Large

	if bustSize == '':
		return bustSizeUndetermined
	else:
		return bustSize

def determineButtSize(measurements):
	buttSize = ''

	buttSize_Huge = 'Huge'
	buttSize_Large = 'Large'
	buttSize_Medium = 'Medium'
	buttSize_Small = 'Small'
	buttSizeTiny = 'Tiny'
	buttSizeUndetermined = 'Undetermined'

	cupSize = int(measurements[:2])
	waistCircumference = int(measurements[measurements.find('-')+1:measurements.find('-')+3])
	hipCircumference = int(measurements[measurements.find('-')+4:])

	if ((waistCircumference / hipCircumference == 0.7) or (hipCircumference - cupSize < 5)):
		buttSize = buttSize_Medium
	elif (hipCircumference > cupSize and (hipCircumference - cupSize >= 5)) :
		buttSize = buttSize_Large
	else:
		buttSize = buttSize_Small

	if buttSize == '':
		return buttSizeUndetermined
	else:
		return buttSize

def determineWeightInLb(input):
	input = input.replace('<!--','').replace('// -->','').replace('document.write(message);','').strip(' \t\n\r')
	weightInKg = input[12:14]
	weightInLbs = math.ceil(float(weightInKg) / 0.4545)
	return int(weightInLbs)
	
def determineHeight(input):
	input = input.replace('<!--','').replace('// -->','').strip(' \t\n\r')
	heightInCm = input[ (input.find('\"') + 1) : (input.find(';') - 1) ]	
	feet = float(heightInCm) / 30.48
	inches = (feet - math.floor(feet)) * 30.48 / 2.54
	return str(int(math.floor(feet))) + '.' + str(int(math.ceil(inches)))

def determineCareerStart(careerStDt):
	careerStart = careerStDt[:4]
	return careerStart

def determineCareerEnd(careerEndDt):
	careerEnd = careerEndDt[7:11]
	return careerEnd
	
pornstarList = ['April ONeil', 'Ariana Marie', 'Archana Sharma', 'Kay Parker', 'Janet Mason']
#pornstarList = ['Ariana Marie']
#pornstarList = ['Archana Sharma']
unprocessedPornstars = []

list_of_rows = []

for pornstar in pornstarList:
	url = 'http://www.freeones.com/html/' + pornstar[:1] + '_links/bio_' + pornstar.replace(' ','_') + '.php'

	print 'Processing ' + pornstar + '[' + url + ']'
	
	response = requests.get(url)
	html = response.content

	soup = BeautifulSoup(html)
	table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="biographyTable") 

	name = ''
	dateofBirth = ''
	weight = ''
	height = ''
	bustSize = ''
	buttSize = ''
	nationality = ''
	hairColor = ''
	ethnicity = ''
	tattoos = ''
	piercings = ''
	aliases = ''
	careerStartYear = ''
	careerEndYear = ''
	measurements = ''
	careerDuration = ''
	
	try:
		for row in table.findAll('tr'):
			list_of_cells = []
			for cell in row.findAll('td', {'class':'paramname'}):
				cellName = cell.text.replace('&nbsp;', '').replace(':','').replace('\n', ' ').strip()
				
				#NAME
				if cellName == 'Babe Name':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')
						name = cellValue
						list_of_cells.append('Name')
						list_of_cells.append(cellValue)
					list_of_rows.append(list_of_cells)
				
				#DATE OF BIRTH
				if cellName == 'Date of Birth':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')
						cellValue = cellValue[:cellValue.find('(')]
						print '\t' + pornstar + '\'s Date of Birth is ' + cellValue
						list_of_cells.append('BirthDate')
						list_of_cells.append(cellValue)
					list_of_rows.append(list_of_cells)
				
				#WEIGHT
				if cellName == 'Weight':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')
						weightInLbs = determineWeightInLb(cellValue)
						print '\t' + pornstar + '\'s Weight is ' + str(weightInLbs)
						list_of_cells.append('Weight')
						list_of_cells.append(weightInLbs)
					list_of_rows.append(list_of_cells)
				
				#HEIGHT
				if cellName == 'Height':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')
						height = determineHeight(cellValue)
						print '\t' + pornstar + '\'s Height is ' + str(height)
						list_of_cells.append('Height')
						list_of_cells.append(height)
					list_of_rows.append(list_of_cells)
				
				# BUST & BUTT SIZE
				if cellName == 'Measurements':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')
						print '\t' + pornstar + '\'s Bust Size is ' + determineBustSize(cellValue)
						print '\t' + pornstar + '\'s Butt Size is ' + determineButtSize(cellValue)
						measurements = cellValue
						
				#NATIONALITY
				if cellName == 'Country of Origin':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')						
						print '\t' + pornstar + '\'s Country of Origin is ' + cellValue
						list_of_cells.append('Nationality')
						list_of_cells.append(cellValue)
					list_of_rows.append(list_of_cells)

				#HAIR COLOR
				if cellName == 'Hair Color':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')						
						print '\t' + pornstar + '\'s Hair Color is ' + cellValue
						list_of_cells.append('HairColor')
						list_of_cells.append(cellValue)
					list_of_rows.append(list_of_cells)
						
				#EYE COLOR
				if cellName == 'Eye Color':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')						
						print '\t' + pornstar + '\'s Eye Color is ' + cellValue
						list_of_cells.append('EyeColor')
						list_of_cells.append(cellValue)
					list_of_rows.append(list_of_cells)
						
				#ETHNICITY
				if cellName == 'Ethnicity':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')						
						print '\t' + pornstar + '\'s Ethnicity is ' + cellValue
						list_of_cells.append('Ethnicity')
						list_of_cells.append(cellValue)
					list_of_rows.append(list_of_cells)
				
				#TATTOOS
				if cellName == 'Tattoos':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')						
						print '\t' + pornstar + '\'s Tattoos::: ' + cellValue
						list_of_cells.append('Tattoos')
						list_of_cells.append(cellValue)
					list_of_rows.append(list_of_cells)
				
				#PIERCINGS
				if cellName == 'Piercings':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')						
						print '\t' + pornstar + '\'s Piercings::: ' + cellValue
						list_of_cells.append('Piercings')
						list_of_cells.append(cellValue)
					list_of_rows.append(list_of_cells)
						
				#ALIASES
				if cellName == 'Aliases':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','')						
						print '\t' + pornstar + '\'s Aliases::: ' + cellValue
						list_of_cells.append('Aliases')
						list_of_cells.append(cellValue)
					list_of_rows.append(list_of_cells)

				#CAREER START-END
				if cellName == 'Career Start And End':
					for cell in row.findAll('td', {'class':'paramvalue'}):
						cellValue = cell.text.replace('&nbsp;', '').replace(':','').strip(' \t\n\r')						
						if cellValue != 'unknown - unknown':
							cellValue = cellValue[:cellValue.find('(') - 1]
							if str(date.today().year) or '2016' in cellValue:
							#if str(date.today().year) in cellValue:
								print '\t' + pornstar + ' first started performing in the year ' + determineCareerStart(cellValue) + ' and is still going strong!'								
								careerDuration = cellValue
							else:
								print '\t' + pornstar + ' was an adult entertainment performer between the years ' + determineCareerStart(cellValue) + ' and ' + determineCareerEnd(cellValue)								
								careerDuration = cellValue
						else:
							print '\t' + pornstar + '\'s career duration is unknown'
		
		if careerDuration != '':
			list_of_cells.append('StartYear')
			list_of_cells.append(determineCareerStart(careerDuration))
			list_of_rows.append(list_of_cells)
			list_of_cells.append('EndYear')
			list_of_cells.append(determineCareerEnd(careerDuration))
			list_of_rows.append(list_of_cells)
			careerDuration = ''

		if measurements != '':
			list_of_cells.append('BreastSize')
			list_of_cells.append(determineBustSize(measurements))
			list_of_rows.append(list_of_cells)
			list_of_cells.append('ButtSize')
			list_of_cells.append(determineButtSize(measurements))
			list_of_rows.append(list_of_cells)
			measurements = ''
	
	except:
		#print 'Could not process ' + pornstar
		unprocessedPornstars.append(pornstar)

if len(unprocessedPornstars) > 0:
	print ''
	print 'Unable to process ' + str(len(unprocessedPornstars)) + ' pornstar(s):'
	for failedPornstars in unprocessedPornstars:
		print failedPornstars

outfile = open("./Scraped.csv", "wb")
writer = csv.writer(outfile)
writer.writerows(list_of_rows)