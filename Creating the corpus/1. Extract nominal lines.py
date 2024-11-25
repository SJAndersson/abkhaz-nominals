#This is the first script used to create a corpus of nominal stress
#alternations in Abkhaz. It starts from a plaintext version of
#Yanagisawa (2010) and extracts all lines containing noun and
#adjective headwords.

dictionary = []

with open("full dictionary.txt", encoding = "utf-8") as f:

    dictionary = f.read().split("\n")

dictionary = [line for line in dictionary if (line.startswith("a-") or line.startswith("a¡-")) and ("[n.]" in line or "[adj.]" in line)]

#Save all the lines containing nominals to 1. nominal lines.txt
with open("1. Nominal lines.txt", mode = "w", encoding = "utf-8") as f:

    f.write("\n".join(dictionary))
