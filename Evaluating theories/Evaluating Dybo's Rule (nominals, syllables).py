from itertools import product

#This script takes a corpus of Abkhaz nominal forms as input,
#and asks, for each nominal, whether there is any underlying
#representation such that, when Dybo's Rule is applied,
#the correct stress pattern is predicted.
#Dybo's Rule is defined as assigning primary stress to
#the leftmost accent that is not immediately followed
#by another accent. If no accent exists, stress is
#root-final.
#I assume one accent per underlying vowel.
#The definite prefix is
#accented, and the indefinite suffix is unaccented.

accentStatus = {}

#Specify the accent of each functional morpheme
#A = accented, U = unaccented
accentStatus["DEF"] = "A"
accentStatus["INDF"] = "U"

#This function takes a phonological string (e.g. A-CaaCa-Ca)
#and a corresponding gloss string (e.g. DEF-R-INF), and a
#morpheme that appears in the gloss (e.g. R), and returns
#a phonological string and gloss string where the morpheme
#m has been divided into syllables: [A-Caa-Ca-Ca, DEF-R0-R1-INF]
def parseSyllables(phonString, glossString, m):

    #Get the phonological shape of m (e.g. CaaCa)
    phonList = phonString.split("-")
    glossList = glossString.split("-")
    phonMorpheme = phonList[glossList.index(m)]

    #Add hyphens corresponding to syllable boundaries

    #Note that syllabification entirely ignores the
    #non-underlying vowel schwa

    #Pre-/a/ boundary
    phonMorpheme = phonMorpheme.replace("A", "-A")    
    phonMorpheme = phonMorpheme.replace("a", "-a")

    #Treat aa as a single unit (following Spruit 1986)
    #*Stressed* long vowels don't occur in the corpus,
    #so we can limit ourselves to lowercase a here
    phonMorpheme = phonMorpheme.replace("a-a", "aa")

    #We want CCaCa to be syllabified CCaC-a, and not
    #CC-aC-a, and this fixes that. Note that this
    #syllabification is coda-maximizing with no
    #consequences. It could easily be rewritten to
    #be onset-maximizing, but it has no impact

    if "-" in phonMorpheme and "a" in phonMorpheme.lower():

        #If there's a syllable boundary before the first vowel
        if phonMorpheme.index("-") < phonMorpheme.lower().index("a"):

            #Remove that syllable boundary
            phonMorpheme = phonMorpheme.replace("-", "", 1)

    #Update phonList with the newly parsed form
    phonList[glossList.index(m)] = phonMorpheme

    #Add corresponding hyphens to the gloss
    newMorphemeGloss = ""

    #The number of root syllables is the number of hyphens
    #in phonMorpheme plus one    
    for i in range(phonMorpheme.count("-") + 1):

        newMorphemeGloss += m + str(i) + "-"

    if newMorphemeGloss.endswith("-"):

        newMorphemeGloss = newMorphemeGloss[:-1]

    #Replace the old gloss with the new gloss
    glossList[glossList.index(m)] = newMorphemeGloss

    #Return new forms
    return ["-".join(phonList), "-".join(glossList)]

#This function takes in a gloss string(e.g. "DEF-R0-R1-R2-INF")
#and returns the number of morphemes that start with m. For example,
#for m = "R", this function returns 2. It counts the number of
#elements that are in the morpheme m in glossString
def countSyllables(glossString, m):

    glossList = glossString.split("-")
    counter = 0

    for g in glossList:

        if g.startswith(m):

            counter += 1

    return counter

#This function takes in a list of accents (e.g. ["A", "U", "A"])
#and a corresponding list of glosses (e.g. ["DEF", "R0", "INF"]),
#and applies Dybo's Rule to the form. It returns an integer: the
#index of the syllable that Dybo's Rule predicts should carry
#primary stress
def applyDybo(accentList, glossList):

    #If there is no accent, stress is root-final
    if "A" not in accentList:

        #Loop through the glossList backwards to quickly
        #find the final syllable glossed as part of the root
        for i in range(len(glossList) - 1, -1, -1):

            #If this is part of the root
            if glossList[i].startswith("R"):

                #It's the final syllable of the root since we're
                #looping backwards, so just return this index:
                #stress is on the final syllable of the root
                return i

    #If there is at least one underlying accent, we apply Dybo's Rule
    #proper, stressing the leftmost accent not immediately followed
    #by an accent
    else:

        #Go through each accent from left to right
        for i in range(len(accentList)):

            #If this is the final accent, and we haven't
            #assigned stress yet, this is the morpheme
            #that should be stressed
            if i == len(accentList) - 1:

                return i

            #For any non-final syllable
            else:

                #Assign stress here if it's an A followed by a U
                if accentList[i] == "A" and accentList[i + 1] == "U":

                    return i

#This function evaluates Dybo's Rule against a nominal's 2 forms.
#It takes in a nominal (phonology, gloss), and a list of accents
#for each syllable in the root, and returns a number between 0 and 2
#(both inclusive) for how many of the verb's forms had their stress
#correctly predicted.
def evaluateDybo(n, rAccent):

    evaluation = []

    #Look at both nominal forms (indices 0 and 2 in n)
    for i in [0, 2]:

        #Extract phonology and gloss information
        #We make a copy oldGlossList, since we'll
        #modify glossList in the code below, but we
        #still want access to the original (in particular,
        #to know where the root is so we can assign root-
        #final stress if needed)
        phonList = n[i].split("-")
        glossList = n[i + 1].split("-")
        oldGlossList = glossList[::]

        #Replace the glosses with the accent of the relevant
        #morpheme
        for j in range(len(glossList)):

            #If this element is part of the root
            if glossList[j].startswith("R"):

                #Replace with the relevant accent specification
                #from the rAccent list
                glossList[j] = rAccent[int(glossList[j][1:])]

            #If this is a functional morpheme
            else:

                #Use the dictionary accentStatus to look up the
                #accent status of this morpheme
                glossList[j] = accentStatus[glossList[j]]

        #Now we can pass the list of accents (e.g. [A, U, U, A]) to a
        #function which will tell us which syllable Dybo's Rule
        #predicts will be stressed, and compare that against the
        #actual corpus data

        #Dybo's Rule    
        stressIndex = applyDybo(glossList, oldGlossList)

        #Consistent initial stress
        #stressIndex = 0

        #Consistent final stress
        #stressIndex = len(glossList) - 1

        #Consistent root-initial stress
        #stressIndex = oldGlossList.index("R0")

        #Consistent root-final stress
        #for i in range(len(oldGlossList) - 1, -1, -1):

            #if oldGlossList[i].startswith("R"):

                #stressIndex = i

                #break

        #Now we have a prediction, and we want to check if it matches
        #the data. Does the predicted syllable have a stressed vowel?
        #We check for stressed A, but if the morpheme is vowelless then
        #we allow a final epenthetic schwa to count as a correct
        #prediction too.
        if ("A" in phonList[stressIndex] or
        ("a" not in phonList[stressIndex].lower() and
         phonList[stressIndex][-1] == "Y")):

            #If yes, add 1 for a correct prediction
            evaluation.append(1)

        else:
            
            #If no, add 0 for an incorrect prediction
            evaluation.append(0)

    return evaluation

#Load the corpus data
allNominals = []

with open("10. C(V)C(V)C(V), UUU.txt", encoding = "utf-8") as f:

    allNominals = f.read().split("\n")

#Add morpheme boundaries and glosses
nominals = []

for nominal in allNominals:

    tempNominal = nominal.split(" ")

    #We add in a hyphen after the first segment of the definite
    #(the prefix), and before the last segment of the indefinite
    #(the suffix)
    nominals.append([f"{tempNominal[1][0]}-{tempNominal[1][1:]}", "DEF-R", f"{tempNominal[3][:-1]}-{tempNominal[3][-1:]}", "R-INDF", tempNominal[0], tempNominal[2]])

nominal = []
tempScore = []
tempHighscore = []
tempHighAccents = ""
nominalsCorrect = 0
nominalsTotal = 0
totalCorrect = 0
totalTotal = 0

#Look through all words in the corpus after it's been filtered
for n in nominals:

    nominal = n

    tempScore = []
    tempHighscore = [0, 0]

    numRootSyllables = []

    #This code checks for root allomorphy, and exits if we find it, warning the user
    rootURDef = nominal[0].split("-")[1].lower().replace("y", "")
    rootURIndf = nominal[2].split("-")[0].lower().replace("y", "")

    if len(set([rootURDef, rootURIndf])) > 1:

        print(f"{nominal[-2]}, {nominal[-1]}: ROOT ALLOMORPHY. NOMINAL NOT EVALUATED.")

        continue

    #This code breaks up the root into syllables
    for i in [0, 2]:

        tempPhonString, tempGlossString = parseSyllables(nominal[i], nominal[i + 1], "R")
        
        nominal[i] = tempPhonString
        nominal[i + 1] = tempGlossString

        numRootSyllables.append(countSyllables(tempGlossString, "R"))

    #Go through every possibility for accents of the root
    for rootAccent in product(["U", "A"], repeat = numRootSyllables[0]):

        #If a root has no underlying syllables (no /a/),
        #we only allow the root to be unaccented
        if "a" not in nominal[0][1:].lower() and "A" in rootAccent:

            continue

        #See how many forms this rootAccent accounts for
        tempScore = evaluateDybo(nominal, rootAccent)

        #If we do better than our previous highscore
        if tempScore.count(1) > tempHighscore.count(1):

            #Update highscore to current score
            #Store the rootAccent that led to this score
            tempHighscore = tempScore
            tempHighAccents = rootAccent

        #We're never going to beat accounting for both forms
        if tempHighscore.count(1) == 2:

            break

    totalCorrect += tempHighscore.count(1)
    totalTotal += 2

    if tempHighscore.count(1) == 2:

        nominalsCorrect += 1

    else:

        print(f"{nominal[-2]}, {nominal[-1]}: {tempHighscore} with {str(tempHighAccents)}")

    nominalsTotal += 1

print(f"Total correct predictions: {totalCorrect}")
print(f"Total forms predicted: {totalTotal}")
print(f"Nominals with 2/2 correct predictions: {nominalsCorrect}")
print(f"Nominals evaluated: {nominalsTotal}")
