#This script goes through 2. Nominal lines cleaned.txt, and extracts
#definite and indefinite forms for all nominals which have them.
#It excludes words with stress on aa, which Yanagisawa (2010: 14)
#says had stresses assigned based on etymological factors and other
#dictionaries, rather than speaker judgements.
#It attempts to catch any exceptions due to odd uses of parentheses.
#It removes words with multiple stresses.
#It standardizes monovocalic forms to all have stress marked.
#It turns all consonants into C, but keeps vowel qualities distinct.
#It also converts to standard modern Abkhaz orthography.
#The script saves a file with one line per stem, containing:
#definite (orthography), definite (phonology),
#indefinite (orthography), indefinite (phonology) in that order

#A helper function which takes in a form (string) and a list of
#vowels, and counts how many vowels there are in the form.
def countVowels(form, vowels):

    sumVowels = 0

    for v in vowels:

        sumVowels += form.count(v)

    return sumVowels

#This helper function takes in a definite or indefinite form
#and checks that it has exactly one stress marked. However,
#monovocalic forms are also valid, even if they don't have
#stress marked. All other forms are invalid. The function
#returns an empty string for invalid forms, and returns
#the form itself for valid forms, adding in stress on mono-
#vocalic forms if needed.
def getValid(form):

    #Forms with one stress marked
    if countVowels(form, ["A", "Y", "U", "I", "E", "O"]) == 1:

            return form

    #Forms with exactly one vowel and stress unmarked
    if countVowels(form, ["a", "y", "u", "i", "e", "o"]) == 1:

            #Add stress on the single vowel
            for v in ["a", "y", "u", "i", "e", "o"]:

                form = form.replace(v, v.upper())

            return form

    return ""

#Start of main code
nominals = []

with open("2. Nominal lines cleaned.txt", encoding = "utf-8") as f:
    #Double parentheses caused problems previously
    nominals = f.read().replace(") ) ", ") ").split("\n")

nominalsKeep = []
tempS = ""
tempL = []
tempDef = ""
tempIndf = ""

#This for-loop goes through all nominal lines, and tries to find
#both a definite and an indefinite form. It only saves lines where
#this succeeds, and several types of forms are removed.
for line in nominals:

    #Entries with morphologically related forms all have parentheses,
    #and we want to make sure there's a possible indefinite in there
    if ")" in line and "-k " in line:

        #Variables for storing the current definite/indefinite
        tempDef = ""
        tempIndf = ""

        #A temporary variable useful for text processing
        tempS = line

        #Some irregular/word-specific formatting for parentheses means we generally want to remove all but the last one
        tempS = tempS.replace(") ", "", tempS.count(") ") - 1)

        #Indefinites come before a right parenthesis somewhere,
        #so we only check words before the first right parenthesis
        tempL = tempS[:tempS.index(")")].split(" ")

        #Check all words on this line for definites and indefinites
        for i in range(len(tempL)):

            #The definite is the first word (the headword)
            #We exclude forms with stress on aa
            if i == 0 and "a¡a" not in tempL[i] and "aa¡" not in tempL[i]:
                
                tempDef = tempL[i]

            #Look for indefinites:
            #we look for forms with one morpheme boundary only,
            #which end in the indefinite suffix, and
            #we throw out forms with stress on aa
            if tempL[i].endswith("-k") and tempL[i].count("-") == 1 and len(tempL[i]) > 2 and "a¡a" not in tempL[i] and "aa¡" not in tempL[i]:

                tempIndf = tempL[i]

                break
                #Note that this only saves the first possible pronunciation,
                #if multiple are given (but that's only done rarely).
                #Excluding anything but the first is also generally
                #useful to stop the corpus from containing indefinites
                #of unrelated nouns which are used in example
                #sentences on the same line as the headword.

        #This bit of code saves only lines with both forms
        if tempDef and tempIndf:

            nominalsKeep.append(f"{tempDef} {tempIndf}")

#So far everything is in mangled text encodings.
#We want to convert to orthography, and to a
#simplified phonological transcription.
#Replacing symbols is easier to do on the whole
#file as a string, than on individual items in a list.
nominalsOrth = "\n".join(nominalsKeep)
nominalsPhon = "\n".join(nominalsKeep)

#These convert to standard Abkhaz orthography
dictIn = ["a¡", "y¡", "u¡", "i¡", "e¡", "o¡", ";", "´", "ә", "ь", "b", "v", "g", "ҕ", "d", "'", "z", "ӡ", "k", "º", "ҟ", "l", "m", "n", "p", "ҧ", "r", "s", "t", "ҭ", "f", "x", "≈", "c", "ҵ", "h", "˙", "ҽ", "w", "ҩ", "ҿ", "ç", "∞", "-", "a", "y", "e", "o", "i", "u"]
dictOt = ["А", "Ы", "У", "И", "Е", "О", "ь", "ә", "ә", "ь", "б", "в", "г", "ӷ", "д", "ж", "з", "ӡ", "к", "қ", "ҟ", "л", "м", "н", "п", "ԥ", "р", "с", "т", "ҭ", "ф", "х", "ҳ", "ц", "ҵ", "ч", "ҷ", "ҽ", "ш", "ҩ", "ҿ", "џ", "ҕ", "", "а", "ы", "е", "о", "и", "у"]

for i in range(len(dictIn)):

    nominalsOrth = nominalsOrth.replace(dictIn[i], dictOt[i])

#These convert to simplified phonological transcriptions.
#The ends of these lists attempt to deal with the same
#character being used for i & j, and for u & w. This is
#nice to have, but in future scripts, I will discard
#the relevant words as possible loanwords anyway.
dictIn = ["a¡", "y¡", "u¡", "i¡", "e¡", "o¡", ";", "´", "ә", "ь", "b", "v", "g", "ҕ", "d", "'", "z", "ӡ", "k", "º", "ҟ", "l", "m", "n", "p", "ҧ", "r", "s", "t", "ҭ", "f", "x", "≈", "c", "ҵ", "h", "˙", "ҽ", "w", "ҩ", "ҿ", "ç", "∞", "-", "a", "y", "e", "o", "CiC", "\niC", " iC", "Ci ", "Ci\n", "i", "и", "CuC", " uC", "Cu ", "u", "Cw\n", "\nwC", "w", "у"]
dictOt = ["A", "Y", "U", "I", "E", "O", "", "", "", "", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "", "a", "y", "e", "o","CиC", "\nиC", " иC", "Cи ", "Cи\n", "C", "i", "CуC", " уC", "Cу ", "w", "Cу\n", "\nуC", "C", "u"]

for i in range(len(dictIn)):

    nominalsPhon = nominalsPhon.replace(dictIn[i], dictOt[i])

#The code below removes words with multiple stresses (only a handful)
#and words with no stresses
#I re-use some variables here
nominalsKeep = []
nominalsOrthL = nominalsOrth.split("\n")
nominalsPhonL = nominalsPhon.split("\n")
tempDef = ""
tempIndf = ""

#Go through all nominals
for i in range(len(nominalsPhonL)):

    if nominalsPhonL[i]:

        #Store the definite and indefinite forms
        tempDef, tempIndf = nominalsPhonL[i].split(" ")

        #Check that both forms satisfy validity requirements,
        #which are to have at most one stress marked, or
        #to be monovocalic, such that there is only one place
        #where the stress could go.
        validDef = getValid(tempDef)
        validIndf = getValid(tempIndf)

        #If both forms are valid, save them. Note that I only
        #add in stresses in the phonological representations,
        #I don't care to add them in in the orthography as well.
        if validDef and validIndf:

            nominalsKeep.append(" ".join([nominalsOrthL[i].split(" ")[0], validDef, nominalsOrthL[i].split(" ")[1], validIndf]))

#Two items are parsed incorrectly: one is Азна 'full (of)', which
#has no indefinite form in the dictionary, but which does have an
#example phrase which happens to start with the indefinite of another
#noun, and this incorrectly gets included. The other is written
#аҳә(ы)сҭА ҳә(ы)сҭАк in the dictionary, and the parentheses mess with
#everything. I'm excluding 'full (of)', but keeping the other word,
#adding its information manually.
nominalsKeep = [n for n in nominalsKeep if not n == "Азна ACCa ҵәык CYC"]

nominalsKeep[nominalsKeep.index("аҳә AC сҭАк CCAC")] = "аҳәысҭА aCyCCA ҳәысҭАк CyCCAC"

#Save the corpus
with open("3. Nominal corpus.txt", mode = "w", encoding = "utf-8") as f:

    f.write("\n".join(nominalsKeep))
