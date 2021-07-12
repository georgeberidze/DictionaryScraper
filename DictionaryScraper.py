"""
Name: George Beridze
Last Modified: March 19, 2021
Description: Final Programming Assignment Part 2 (extension) 
"""

from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time

def GetDictionary(term):
  'crawls dictionary.com and returns the description for a specific term. If the definition has an unusual HTML pattern, it will be ignored'
  head = 'https://www.dictionary.com/browse/'
  search_term = term
  tail = search_term
  tail += "?s=t" 
  blacklist = ["<span", "(", "<a"]    
  error = "N/A"

  try:
    website = urlopen(urljoin(head,tail))
    soup = BeautifulSoup(website, "html.parser")
    aspan = soup.find('span', attrs = {'class': 'one-click-content'})
    aspan_text = aspan.decode_contents().split(';')
    definition = aspan_text[0]
    for x in blacklist:
      if x in definition:
        'HTML is not typical, so the definition is invalid'
        definition = error
    return definition
  except:
    definition = error
    return definition

head = 'https://www.classicshorts.com/stories/'
try: 
  tail = input("What's the short story called? ")
  tail += '.html'
  approval = input("Would you like to automatically populate term descriptions from dictionary.com? Please note, some descriptions may show 'N/A' as they could not be fetched from the website. This may take up to 30-40 seconds for longer stories. Do not quit while waiting. (Y/N) ")
  if approval == "Y" or approval == "y":
    print("Counting your terms. Get yourself a cup of tea.", sep ='', end= '')
  start = time.time()                           # start the timer
  website = urlopen(urljoin(head,tail))

except: 
  #stop = time.time()
  print("Short story not found.")
  quit() #this way the errors below won't run

# set up Beautiful Soup and look for tags
soup = BeautifulSoup(website, "html.parser")
atag = soup.findAll('a')
longest_term = 0                              
dictionary = {}                               # stores terms and descriptions
counter = 1

# loops through each tag and only parses the ones that are hyperlinked to dictionary.com
for tag in atag:
    if "dictionary.reference.com" in tag.get('href'):
      'this term is needed as it hyperlinks to dictionary.com'
      term = tag.decode_contents()
      if term not in dictionary.keys():
        'term is added to the dictionary'
        if approval == "Y" or approval == "y":
          'fetch descriptions from dictionary.com'
          dictionary[term.capitalize()] = GetDictionary(term)
          print(".", end='')                       # this is supposed to be a loading bar, but it does not always works
        else:
          'apply default blank descriptions'
          dictionary[term.capitalize()] = ''
        if len(term) > longest_term:
          'term is the longest'
          longest_term = len(term)

# returns the time (in seconds) it took to run the user's request through Beautiful Soup, including all the steps it took to open the URL, scrape HTML and return the count of terms
stop = time.time()          
runtime = stop - start
print("")
if not dictionary.keys():
  'there are no terms'
  print("Short story found. There are no vocabulary words.")
  print("Your inquiry took {:.2f} seconds.". format(runtime)) 
  quit()
else:
  'there are terms'
  print("Short story found. There are", len(dictionary.keys()), "unique vocabulary words.")
  print("Your inquiry took {:.2f} seconds.". format(runtime)) 
update = True

# runs the loop until the user decides not to make any more updates
while (update):
  update_response = input("Would you like to update a definition (Y/N)? ")
  if update_response == 'N':
    'user no longer wants to update'
    update = False
  else: 
    term_choice = input("Term: ")
    if term_choice not in dictionary.keys():
      'term does not exist'
      print("ERROR! Term not found.")
      continue
    else:
      'term exists'
      if not dictionary.get(term_choice):
        'The term has no definition'
        definition_choice = input("Definition: ")
        dictionary[term_choice] = definition_choice
      else:
        'term has an existing definition'
        print("WARNING! ", term_choice," is currently defined as \'", dictionary.get(term_choice),"\'", sep='') 
        definition_choice = input("Definition: ")
        dictionary[term_choice] = definition_choice

# prompts user for the text file to save the output to 
outputName = input("What would you like to save the file as?: ")
inOutput = open(outputName, 'w')

# writes the dictionaty in the output file
for term in dictionary:
  data = '{:<{var1}} {} {:<}\n'.format(term,'-', dictionary.get(term), var1 = longest_term)
  inOutput.write(data)

inOutput.write("")
inOutput.write("Longest term length is: ")
inOutput.write(str(longest_term))
inOutput.close()
print("File saved!")
