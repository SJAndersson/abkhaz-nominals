#This script removes all words with non-native graphemes
#i e o u (и е о у) from 3. Nominal corpus.txt. It outputs
#4. Nominal corpus (no loans).txt. Note that there are
#native words containing these graphemes, and non-native
#words which do not contain them, so this is far from a
#perfect substitute for going through the corpus with an
#etymological dictionary and removing loans manually.
nominals = []

with open("3. Nominal corpus.txt", encoding = "utf-8") as f:

    nominals = f.read().split("\n")

#Remove any lines containing i e o u
#It's better to look for the Cyrillic letters, since some
#of и у are treated as C rather than I U in the phonological
#transcription.    
nominals = [nominal for nominal in nominals if not True in [bool(v in nominal.lower()) for v in ["и", "е", "о", "у"]]]

with open("4. Nominal corpus (no loans).txt", encoding = "utf-8", mode = "w") as f:

    f.write("\n".join(nominals))
