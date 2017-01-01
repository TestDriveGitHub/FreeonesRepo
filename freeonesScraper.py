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
	return str(int(weightInLbs))
	
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
	if careerEnd != str(date.today().year):
		return careerEnd
	else:
		return ''
	
#pornstarList = ['April ONeil', 'Ariana Marie', 'Archana Sharma', 'Kay Parker', 'Janet Mason']
pornstarList = ['Kay Parker', 'Janet Mason']
#pornstarList = ['Archana Sharma']
unprocessedPornstars = []


with open('./Scraped.csv', 'wb') as csvfile:
	csvWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	csvWriter.writerow(['Id'] + ['Name'] + ['DateAdded'] + ['DateFavorited'] + ['DateRunnerUpped'] + ['LastWatched'] + ['PlayCount'] + ['BirthDate'] + ['Favorite'] + ['RunnerUp'] + ['Rating'] + ['BreastSize'] + ['HairColor'] + ['Description'] + ['Gender'] + ['EyeColor'] + ['Ethnicity'] + ['Organized'] + ['ButtSize'] + ['Nationality'] + ['StartYear'] + ['EndYear'] + ['Height'] + ['Weight'])

	for pornstar in pornstarList:
		url = 'http://www.freeones.com/html/' + pornstar[:1] + '_links/bio_' + pornstar.replace(' ','_') + '.php'

		# print 'Processing ' + pornstar + '[' + url + ']'
		
		response = requests.get(url)
		html = response.content

		soup = BeautifulSoup(html)
		table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="biographyTable") 

		name = ''
		dateofBirth = ''
		weight = ''
		height = ''
		bustSize = 'Undetermined'
		buttSize = 'Undetermined'
		nationality = ''
		hairColor = ''
		eyeColor = ''
		ethnicity = ''
		tattoos = ''
		piercings = ''
		aliases = ''
		careerStartYear = ''
		careerEndYear = ''
		
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
					
					#DATE OF BIRTH
					if cellName == 'Date of Birth':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							cellValue = cell.text.replace('&nbsp;', '').replace(':','')
							dateofBirth = cellValue[:cellValue.find('(')].replace(',',';')
					
					#WEIGHT
					if cellName == 'Weight':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							cellValue = cell.text.replace('&nbsp;', '').replace(':','')
							weight = determineWeightInLb(cellValue)

					#HEIGHT
					if cellName == 'Height':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							cellValue = cell.text.replace('&nbsp;', '').replace(':','')
							height = determineHeight(cellValue)
					
					# BUST & BUTT SIZE
					if cellName == 'Measurements':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							cellValue = cell.text.replace('&nbsp;', '').replace(':','')
							bustSize = determineBustSize(cellValue)
							buttSize = determineButtSize(cellValue)
							
					#NATIONALITY
					if cellName == 'Country of Origin':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							nationality = cell.text.replace('&nbsp;', '').replace(':','')						

					#HAIR COLOR
					if cellName == 'Hair Color':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							hairColor = cell.text.replace('&nbsp;', '').replace(':','')						
							
					#EYE COLOR
					if cellName == 'Eye Color':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							eyeColor = cell.text.replace('&nbsp;', '').replace(':','')						
							
					#ETHNICITY
					if cellName == 'Ethnicity':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							ethnicity = cell.text.replace('&nbsp;', '').replace(':','')						
					
					#TATTOOS
					if cellName == 'Tattoos':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							cellValue = cell.text.replace('&nbsp;', '').replace(':','')
							if cellValue != 'None': tattoos = cellValue
					
					#PIERCINGS
					if cellName == 'Piercings':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							cellValue = cell.text.replace('&nbsp;', '').replace(':','')						
							if cellValue != 'None': piercings = cellValue
							
					#ALIASES
					if cellName == 'Aliases':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							aliases = cell.text.replace('&nbsp;', '').replace(':','')						

					#CAREER START-END
					if cellName == 'Career Start And End':
						for cell in row.findAll('td', {'class':'paramvalue'}):
							cellValue = cell.text.replace('&nbsp;', '').replace(':','').strip(' \t\n\r')						
							if cellValue != 'unknown - unknown':
								cellValue = cellValue[:cellValue.find('(') - 1]
								careerStartYear = determineCareerStart(cellValue)
								careerEndYear = determineCareerEnd(cellValue)

		except:
			unprocessedPornstars.append(pornstar +  ' [' + url + ']')

		finally:
			# if name != '': print 'Successfully scraped the following information for ' + name + '[' + url + ']'
			# if dateofBirth != '': print '\t' + 'DoB::: ' + dateofBirth
			# if weight != '': print '\t' + 'Weight::: ' + weight
			# if height != '': print '\t' + 'Height::: ' + height
			# if bustSize != '': print '\t' + 'Bust size::: ' + bustSize
			# if buttSize != '': print '\t' + 'Butt size::: ' + buttSize
			# if nationality != '': print '\t' + 'Nationality::: ' + nationality
			# if ethnicity != '': print '\t' + 'Ethnicity::: ' + ethnicity
			# if hairColor != '': print '\t' + 'Hair Color::: ' + hairColor
			# if eyeColor != '': print '\t' + 'Eye color::: ' + eyeColor
			# if tattoos != '': print '\t' + 'Tattoos::: ' + tattoos
			# if piercings != '': print '\t' + 'Piercings::: ' + piercings
			# if aliases != '': print '\t' + 'Aliases::: ' + aliases
			# if careerStartYear != '': print '\t' + 'Career Star Year::: ' + careerStartYear
			# if careerEndYear != '': print '\t' + 'Career End Year::: ' + careerEndYear
			
			print 'Writing... ' + name
			csvWriter.writerow(['0'] + [name] + [str(date.today())] + [str(date.today())] + [str(date.today())] + [str(date.today())] + ['0'] + [dateofBirth] + ['0'] + ['0'] + ['0'] + [bustSize] + [hairColor] + ['-'] + ['Female'] + [eyeColor] + [ethnicity] + ['1'] + [buttSize] + [nationality] + [careerStartYear] + [careerEndYear] + [height] + [weight])		

if len(unprocessedPornstars) > 0:
	print ''
	print 'Unable to process ' + str(len(unprocessedPornstars)) + ' pornstar(s):'
	for failedPornstars in unprocessedPornstars:
		print failedPornstars

#outfile = open("./Scraped.csv", "wb")
#writer = csv.writer(outfile)
#writer.writerows(list_of_rows)