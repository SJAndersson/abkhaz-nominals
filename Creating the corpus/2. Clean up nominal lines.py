#This is the second script used to create a nominal stress corpus.
#It takes in 1. nominal lines.txt, containing lines with nominals.
#This script cleans up some of the punctuation and other symbols
#which we would not want to keep around.

nominals = []

with open("1. Nominal lines.txt", encoding = "utf-8") as f:

    nominals = f.read()

#Clean up some things that would cause problems if they stuck around
#Specifically, I add spaces around these characters, so that they
#aren't accidentally parsed as part of an Abkhaz word
for item in [".", ",", "(", ")", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "=", "[", "]", "/"]:

    nominals = nominals.replace(item, " " + item)
    nominals = nominals.replace(item, item + " ")

#Remove double spaces
while "  " in nominals:

    nominals = nominals.replace("  ", " ")

with open("2. Nominal lines cleaned.txt", mode = "w", encoding = "utf-8") as f:

    f.write(nominals)
