#just a really simple script to help developers download dataset

import urllib.request

response = urllib.request.urlopen("https://www.dropbox.com/sh/rukexajbm9fsmd4/AAAMZ3-kWS8wFhfphxAxTmfNa?dl=0")

source_code = response.read().decode('utf-8')

links = []

for line in source_code.split('"'):
    if ".csv?dl=0" in line:
        if "https://www.dropbox.com/sh/rukexajbm9fsmd4/" in line:
            links.append(line)

unique_links = {}

for link in sorted(links):
    begin = link.rfind('/')
    end = link.rfind('?')

    key = link[begin+1:end]

    if key not in unique_links:
        unique_links[key] = link.replace(".csv?dl=0",".csv?dl=1")

print ("The downloadable files are: ")
print (" ")
for key, _ in unique_links.items():
    print(key)
print(" ")

choice = input("Which one do you want to download .Separate by comma(no spaces) if more than one and type all to download the entire dataset ")

if choice != 'all':
    files = choice.split(',')
else:
    files = [key for key, _ in unique_links.items()]
    print(files)

for file_name in files:
    if file_name in unique_links:
        print ("Downloading " + file_name)
        urllib.request.urlretrieve(unique_links[file_name],file_name)
    else:
        print ("No file named "+ file_name)

print("Done. The requested files are downloaded! ")
