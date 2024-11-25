# abkhaz-nominals
Python code for an Abkhaz nominal corpus

## Description

This repository contains a series of Python 3 scripts to be run in order, which create a corpus database of 545 definite and indefinite pairs of Abkhaz nominals (nouns and adjectives). I also provide the final corpus, as well as a series of scripts for evaluating different linguistic theories of stress placement against the data. For a more complete description, see the details in Andersson (2024).

## Input and output format

The input is a plaintext version of Yanagisawa's (2010) dictionary of Abkhaz. The output of the corpus creation scripts is a plaintext file with one word per line. Each line contains four forms separated by space: 1) the definite form in Abkhaz orthography (e.g. абӷьЫц), 2) the definite form in an abstract phonological transcription scheme, where vowels are retained but consonants are replaced by C (e.g. aCCYC), 3) the indefinite form in Abkhaz orthography (e.g. бҕьЫцк), and 4) the indefinite form in the same phonological transcription (e.g. CCYCC). Capitalisation marks the stressed vowel.

## Acknowledgements

This work was only possible thanks to Tamio Yanagisawa, who kindly provided me with a PDF version of his dictionary. I am grateful to him for sharing his work with me, and for giving me permission to share the final corpus I have created.

## How to cite

Please cite the following when using data or code from this repository: the ultimate source of the data, my work describing the corpus, and this GitHub repo. Suggested citations:

Andersson, S. (2024). abkhaz-nominals. GitHub repository: <https://github.com/SJAndersson/abkhaz-nominals> [Accessed YYYY-MM-DD]

Andersson, S. (2024). The Phonetics and Phonology of Abkhaz Word Stress. PhD Dissertation: Yale University.

Yanagisawa, T. (with Tsvinaria-Abramishivili, A.). (2010). Analytic Dictionary of Abkhaz. Hitsuji Shobo.
