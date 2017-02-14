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
        unique_links[key] = link

print ("The downloadable files are: ")
print (" ")
for key, value in unique_links.items():
    print(key)
print(" ")

choice = input("Which one do you want to download .Separate by comma if more than one and type all to download the entire dataset ")
exit()

urllib.request.urlretrieve("https://www.dropbox.com/sh/rukexajbm9fsmd4/AAADo5IW2O9nA1Ejp9xSER0ka/training_dataset.csv?dl=1", "teste.csv")
