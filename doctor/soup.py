import requests
from bs4 import BeautifulSoup
import csv
from string import strip
from string import ascii_uppercase
import os

def more_info(href) :
    target = base_url + href
    info = requests.get(target)
    subsoup = BeautifulSoup(info.content , "html.parser")
    gname = use = seffect = bname = ""
    for brand_name in subsoup.find_all("span" , id="ContentPlaceHolder1_lblBrandName") :
        bname = brand_name.text
    for gen_name in subsoup.find_all("span" , id="ContentPlaceHolder1_lblGenericName") :
        gname = gen_name.text
    for usage in subsoup.find_all("textarea" , id="ContentPlaceHolder1_tbUses") :
        use = usage.text
    for s in subsoup.find_all("textarea" , id="ContentPlaceHolder1_tbSideEffects") :
        seffect = s.text
    seffect = seffect.lstrip().replace('\n' , ',')
    bname = bname.strip(' ')
    gname = gname.strip(' ')
    use = use.strip(' ')
    file = open("list.csv" , "a")
    fieldnames = ['Brand Name' , 'Generic Name' , 'Usage' , 'Side Effects']
    csvfile = csv.DictWriter(file , fieldnames = fieldnames)
    csvfile.writerow({'Brand Name' : bname.strip(' ') , 'Generic Name' : gname.strip(' ') , 'Usage' : use.strip(' ') , 'Side Effects' : seffect.replace('\n' , ',')})
    file.close()
    print(bname.strip(' '))

file = open('list.csv' , 'w')
fieldnames = ['Brand Name' , 'Generic Name' , 'Usage' , 'Side Effects']
csvfile = csv.DictWriter(file , fieldnames = fieldnames)
csvfile.writeheader()
file.close()
base_url = "http://www.medsplan.com"
for alpha in ascii_uppercase :
    source = requests.get("http://www.medsplan.com/AlphabeticalSearchFor/" + alpha)
    soup = BeautifulSoup(source.content , "html.parser")
    for links in soup.find_all("div" , class_="overview") :
        for link in  links.find_all("a") :
            more_info(link.get("href"))

brand = []
file = open('list.csv' , 'r')
newfile = open('medicines.csv' , 'w')
fieldnames = ['Brand Name' , 'Generic Name' , 'Usage' , 'Side Effects']
csvfile = csv.DictReader(file)
icsvfile = csv.DictWriter(newfile , fieldnames = fieldnames)
prev = {'Brand Name' : '', 'Generic Name' : '', 'Usage' : '', 'Side Effects' : ''}
for row in csvfile :
    if prev['Generic Name'] == row['Generic Name'] :
        brand.append(row['Brand Name'])
        print("first")
    elif prev['Generic Name'] != '' :
        icsvfile.writerow({'Brand Name' : ' , '.join(str(b) for b in brand) , 'Generic Name' : prev['Generic Name'] , 'Usage' : prev['Usage'] , 'Side Effects' : prev['Side Effects']})
        brand = [row['Brand Name']]
    prev = row
icsvfile.writerow({'Brand Name' : ' , '.join(str(b) for b in brand) , 'Generic Name' : prev['Generic Name'] , 'Usage' : prev['Usage'] , 'Side Effects' : prev['Side Effects']})
os.remove('list.csv')
newfile.close()
