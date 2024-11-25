from itertools import product

#This script takes a corpus of Abkhaz nominal forms as input,
#and asks, for each nominal, whether there is any underlying
#representation such that, when Dybo's Rule is applied,
#the correct stress pattern is predicted.
#Dybo's Rule is defined as assigning primary stress to
#the leftmost accent that is not immediately followed
#by another accent. If no accent exists, stress is
#root-final.
#I assume one accent per morpheme.
#The definite prefix is
#accented, and the indefinite suffix is unaccented.

accentStatus = {}

#Specify the accent of each functional morpheme
#A = accented, U = unaccented
accentStatus["DEF"] = "A"
accentStatus["INDF"] = "U"

#This function takes in a list of accents (e.g. ["A", "U", "A"])
#and a corresponding list of glosses (e.g. ["DEF", "R0", "INF"]),
#and applies Dybo's Rule to the form. It returns an integer: the
#index of the morpheme that Dybo's Rule predicts should carry
#primary stress
def applyDybo(accentList, glossList):

    #If there is no accent, stress is root-final
    if "A" not in accentList:

        #Loop through the glossList backwards to quickly
        #find the root
        for i in range(len(glossList) - 1, -1, -1):

            #If this is part of the root
            if glossList[i].startswith("R"):

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
#for each morpheme, and returns a number between 0 and 2
#(both inclusive) for how many of the nominal's forms had their stress
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
                glossList[j] = rAccent[0]

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

        #Now we have a prediction, and we want to check if it matches
        #the data. Dybo has the unaccented сас 'guest' surfacing with
        #final stress as сасЫ, so I'm going to allow the same thing
        #here, and say: morpheme-final stress results in absolute
        #final stress. He assumes that 'fixed' stress within these
        #paradigms is a secondary historical development, so he
        #shouldn't be able to analyze cases like акьАҿ кьАҿк.
        #I.e., what we want to check for is whether the morpheme
        #ends in a stressed vowel

        if phonList[stressIndex][-1] in ["A", "Y"]:

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

    #This code checks for root allomorphy, and exits if we find it, warning the user
    rootURDef = nominal[0].split("-")[1].lower().replace("y", "")
    rootURIndf = nominal[2].split("-")[0].lower().replace("y", "")

    if len(set([rootURDef, rootURIndf])) > 1:

        print(f"{nominal[-2]}, {nominal[-1]}: ROOT ALLOMORPHY. NOMINAL NOT EVALUATED.")

        continue

    #Go through every possibility for accents of the root
    for rootAccent in product(["U", "A"], repeat = 1):

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
