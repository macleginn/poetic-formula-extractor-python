poetic-formula-extractor-python
===============================

A script for extracting formulas from poetic texts.

The software backbone of this paper: https://www.academia.edu/6304149/_ (in Russian). Computes formulaic density of a poetic text, optionally prints the formulas from it to stdout or to a file or prints the original text with formulas bracketed to an html-file.

The scripts takes as its input a text of a poem, an alphabet, and a stop list (the latter two are iterables of any type and default to built-in Russian ones if not provided). UsefulData.py contains alphabets and stop lists for Russian, Homeric Greek, and Anglo-Saxon.

A console-usage example:

```python
>>> import os
>>> os.chdir([The name of the working directory here.])
>>> import PoeticAnalysisNew as pan
>>> with open('Bylina.txt', 'r', encoding='utf-8') as inp:
        bylina = pan.Poem(inp.read())
>>> bylina.getFormulaicDensity()
31.5
>>> bylina.highlightFormulas('Bylina') # See the results in Bylina.html.
>>> from UsefulData import angloSaxonAlphabet
>>> from UsefulData import angloSaxonStopList
>>> with open('Beowulf.txt', 'r', encoding='utf-8') as inp:
        beowulf = pan.Poem(inp.read(), angloSaxonAlphabet, angloSaxonStopList)
>>> beowulf.getFormulaicDensity()
13.6
>>> beowulf.printFormulas()
feorh ealgian;
feorh ealgian
feorh ealgian,

beorhtode bencsweg;
beorsele benc

monig oft
Monig oft

eft cuman.
eft cuman,

ecean dryhtne,
ecean dryhtne,
ecean dryhtne;

wigena strengel,
wigena strengest,

...
```

A batch-analysis example:

```python
from PoeticAnalysisNew import *
fileNames = []
os.chdir('texts')
directories = os.listdir()
for directory in directories:
    for root, dirs, files in os.walk(directory):
        for name in files:
            fileNames.append(os.path.join(root, name))
with open('../report.txt', 'w', encoding='utf-8') as out:
    for item in fileNames:
        if item.endswith('txt'):
            with open(item, 'r', encoding='utf-8') as inp:
                poem = Poem(inp.read())
            out.write(str(poem.getFormulaicDensity()) + '\n')
```

The algorithm is lousy and slow. All attempts at improving it only made the matters worse because new versions relied less heavily on C-based library routines. Eventually, I rewrote everything in Java. The new version is more than 4 times faster; I will create a repo for it presently.
