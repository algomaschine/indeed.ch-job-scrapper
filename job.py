import re
import sys
import urllib2
from BeautifulSoup import BeautifulSoup
from langdetect import detect
import time

'''

	Here's the sequence:
	1) Use Email Grabber software on www.indeed.ch with certain keywords to create a list of URLs and extracted Emails from these pages.
	   A sample is located in the file indee-jobs.txt - that's the format
	    "personal@paracelsus-spital.ch","https://www.indeed.ch/rc/clk?jk=0b1301ff7c78bbdd&from=recjobs&vjtk=1ct5l0dca93oo800"
		"mail@huk-ag.ch","https://www.indeed.ch/rc/clk?jk=d13c666a35586dc9&from=vj&pos=bottom"

	2) python job.py ./indee-jobs.txt > report.txt
		This will do the following:
		- identify the language of the job ad (we need only English) using langdetect
		- identify the title of the pages
		- identify what keywords included
		- identify the presense of keywords that should not be there, and discard those URLs
		- print the report
		
		This report can then be used to send an automated email newsletter with variables of {job keywords}, {page title} etc
		
	

'''

keywords_include_lower = ["director","technical","owner","founder"]
keywords_include_case = ["CTO","of IT","IT","CIO"]

keywords_exclude_lower = ["credit suisse","recruit","stamford"]
keywords_exclude_case = ["HR"]


with open(sys.argv[1]) as f:
  lines = f.readlines()
  

for l in lines:
  email = (l.split(',')[0])
  url = (l.split(',')[1])
  url = re.sub('"', '', url)
  email = re.sub('"', '', email)
  if (email=="Email"): continue
  title =""
  lang = ""
  
  #print(url)
  try:  
    soup = BeautifulSoup(urllib2.urlopen(url))
    title = soup.title.string
    tlang = detect(title)
    print(tlang,title, url, email)
    time.sleep(10)
  except:	
    print(url, sys.exc_info()[0])
    time.sleep(60)

new_csv = "new.csv"
old_csv = "old.csv"

# 


newf = open(new_csv, 'r')

with open(old_csv) as f:
    oldfile = ''.join(f.readlines()) #  now we have all file being read here
	
line = newf.readline()
while line:
	
	line = line.replace("\"","")
	lineID = line.split(",")
	full_name = lineID[1] + " " + lineID[3]
	email = lineID[5]
	full_work = lineID[29] + " " + lineID[31]

	#print full_name + " / " + email + " / " + full_work
	
	# 1. check for email not to be present in the old file
	
	if oldfile.find(email) != -1:
		print email + ": found in old file"
		line = newf.readline() # make sure to read new line
		continue
	else:
		print email + ": NOT THERE"
	

	# 2. check for full_work to (1) exclude keywords (2) include keywords /  all not case sensitive

	for k in keywords_exclude_lower:
		if full_work.find(k) != -1:
			line = newf.readline()
			continue

	for k in keywords_exclude_case:
		if full_work.find(k) != -1:
			line = newf.readline()
			continue

	kw = False

	for k in keywords_include_lower:
		if full_work.find(k) != -1:
			kw = True
			break

	for k in keywords_include_case:
		if full_work.find(k) != -1:
			kw = True
			break

	if not kw:
		line = newf.readline()
		continue

	# TYPE name to process manually
	if full_name.find(",") != -1:
		print "MANUAL: " + full_name
		line = newf.readline() # make sure to read new line
		continue

	# show it
	print full_name + ": " + full_work
	# continue
	line = newf.readline()



