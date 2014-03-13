from DataStructures import LinkedList
from UsefulData import russianStopList as stopList
from UsefulData import russianAlphabet as alphabet
import math

# A bunch of helper methods.

def mean(valueList):
    """
    Computes the mean from a list of numbers.
    """
    return sum(valueList) / len(valueList)

def sd(valueList):
    """
    Computes the standard deviation from a list of numbers.
    """
    mu = mean(valueList)
    return math.sqrt(
        mean(
            [(mu - value)**2 for value in valueList]
            )
        )

def clear(word):
    """
    Reduces the word to its most basic form for the ease of comparison.
    """
    word = word.lower()
    redundantChars = '!?"№%:–,—.;()_+=»«“”…„“‘’\'[]`\u03010123456789<>'
    for char in redundantChars:
        word = word.replace(char, '')
    word = word.replace('ё', 'е')
    word = word.replace('г̇', 'г')
    return word

def clearText(txt, alphabet):
    """
    Removes all the non-word segments (dashes, numbers, etc.) from the text.
    """
    txt = txt.replace('\ufeff', '')
    txt = txt.replace('\u0301', '')
    txt = txt.replace('\xab', '')
    txt = txt.replace('\xbb', '')
    txtClear = ''
    lines = txt.splitlines()
    for line in lines:
        wordList = line.split()
        wordListFiltered = []
        for word in wordList:
            for letter in word:
                if letter in alphabet:
                    wordListFiltered.append(word)
                    break
        for word in wordListFiltered:
            txtClear += word.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('<', '').replace('>', '') + ' '
        txtClear = txtClear.strip()
        txtClear = txtClear + '\n'
    return txtClear

# Data-structures used for analysis.

class Word:
    """
    The word furnished with its line number and its position in the line.
    """
    def __init__(self, word, lineN, wordN):
        self.word  = word
        self.line  = lineN
        self.index = wordN
    def __str__(self):
        return self.word
    __repr__ = __str__
    def __len__(self):
        return len(self.word)
    def __eq__(self, other):
        return self.word == other.word

class NGram:
    """
    An N-gram consisting of a Word-tuple of length N and a key.
    """
    def __init__(self, wordList):
        self.words = tuple(wordList)
        key = ''
        for word in self.words:
            key += clear(word.word)[0:4]
        self.key = key
    def __str__(self):
        out = ''
        for word in self.words[:-1]:
            out += word.word + ' '
        out += self.words[-1].word
        return out
    __repr__ = __str__
    def __len__(self):
        return len(self.words)
    def __eq__(self, other):
        return self.key == other.key

class Poem:
    """
    The main class. Computes all the necessary statistics on itialisation.
    """
    def __init__(self, txt, userAlphabet = None, userStopList = None, verbose = False):
        # Checking if user provided an alphabet and a stop-list. Both could be any iterables.
        if userAlphabet == None:
            self.alphabet = alphabet
        else:
            self.alphabet = userAlphabet
        if userStopList == None:
            self.stopList = stopList
        else:
            self.stopList = userStopList
        self.verbose = verbose
        txt = clearText(txt, self.alphabet)
        # The main data structure: two associated 2-D arrays, one for the words themselves
        # and the other to keep track of whether they form part of some formula.
        poem      = []
        useMatrix = []
        # Populating the arrays.
        lines = txt.splitlines()
        for i in range(len(lines)):
            line    = lines[i].split()
            lineArr = []
            useArr  = []
            for j in range(len(line)):
                poeticWord = Word(line[j], i, j)
                lineArr.append(poeticWord)
                useArr.append(False)
            poem.append(lineArr)
            useMatrix.append(useArr)
        self.poem      = poem
        self.useMatrix = useMatrix
        self.formulas  = self.makeFormulas()
        # Start- and end-word indices of formula words for bracketing in the highlightFormulas method.
        self.startWords = []
        self.endWords   = []
        for item in self.formulas:
            for formula in self.formulas[item]:
                self.startWords.append((formula.words[0].line, formula.words[0].index))
                self.endWords.append((formula.words[-1].line, formula.words[-1].index))
        # Computing the formulaicDensity.
        wordsTotal      = 0
        wordsInFormulas = 0
        for line in poem:
            for word in line:
                wordsTotal += 1
                if self.useMatrix[word.line][word.index]:
                    wordsInFormulas += 1
        self.formulaicDensity = round((wordsInFormulas/wordsTotal)*100, 1)

    def getFormulaicDensity(self):
        """
        The getter method for formulaicDensity.
        """
        return self.formulaicDensity

    def makeFormulas(self):
        """
        The main workhorse method, which extracts formulas from the text.
        """
        formulaDict = {}
        for i in reversed(range(2, 15)):
            if self.verbose:
                print('Поиск n-грамм длины ' + str(i))
            Ngrams = []
            for line in self.poem:
                Ngrams += self.makeNGrams(line, i)
            if self.verbose and len(Ngrams) > 0:
                for item in Ngrams[:-1]:
                    print(item, end=' | ')
                print(Ngrams[-1])
            while True:
                Ngrams = self.filter(Ngrams)
                if len(Ngrams) > 1:
                    basis  = Ngrams[0]
                    formulas2Be = LinkedList()
                    formulas2Be.add(basis)
                    for Ngram in Ngrams[1:]:
                        if Ngram == basis:
                            formulas2Be.add(Ngram)
                    for item in formulas2Be:
                        Ngrams.remove(item)
                    if len(formulas2Be) >= 2:
                        for item in formulas2Be:
                            for word in item.words:
                                self.useMatrix[word.line][word.index] = True
                        formulaDict[basis.key] = formulas2Be
                else:
                    break
        return formulaDict

    def filter(self, arrOfNgrams):
        """
        The method for removing N-grams with used words from the list.
        """
        outNGrams = []
        for item in arrOfNgrams:
            addIt = True
            for word in item.words:
                if self.useMatrix[word.line][word.index]:
                    addIt = False
                    break
            if addIt:
                outNGrams.append(item)
        return outNGrams

    def makeNGrams(self, line, N):
        """
        Extracts an array of N-grams of length N from a line, which is itself an array of Words.
        """
        Ngrams = []
        if N == 2:
            for i in range(0, len(line)-1):
                if clear(line[i].word) not in self.stopList and clear(line[i+1].word) not in self.stopList:
                    Ngrams.append(NGram([line[i], line[i+1]]))
        else:
            for i in range(0, len(line)-N+1):
                NgramWords = []
                for j in range(i, i+N):
                    NgramWords.append(line[j])
                wordsFromStopList = 0
                for word in NgramWords:
                    if clear(word.word) in self.stopList:
                        wordsFromStopList += 1
                if len(NgramWords) - wordsFromStopList >= wordsFromStopList:
                    Ngram = NGram(NgramWords)
                    Ngrams.append(Ngram)
        return Ngrams

    def highlightFormulas(self, filename):
        """
        Prints the poem to an html-file with formulas bracketed.
        """
        outStr = """<html><meta charset="UTF-8"><body><p>"""
        for line in self.poem:
            for word in line:
                if (word.line, word.index) in self.startWords:
                    outStr = outStr + '[' + word.word + ' '
                elif (word.line, word.index) in self.endWords:
                    outStr = outStr + word.word + ']' + ' '
                else:
                    outStr = outStr + word.word + ' '
            outStr = outStr.strip() + '<br />'
        outStr = outStr + """</p></body></html>"""
        with open(filename + '.html', 'w', encoding='utf-8') as out:
            out.write(outStr)
        lastChar = ']'
        for char in outStr:
            if char != '[' and char != ']':
                continue
            elif char == '[' and lastChar == ']':
                lastChar = '['
            elif char == ']' and lastChar == '[':
                lastChar = ']'
            else:
                print('Bracketing error!')
                break
        if lastChar == '[':
            print('Bracketing error!')

    def printFormulas(self):
        """
        Prints all the formulas to the stdout in no particular order.
        """
        for item in self.formulas:
            print(self.formulas[item])
            print()

    def printFormulasToFile(self, filename):
        """
        Prints all the formulas to the file in no particular order.
        """
        with open(filename, 'w', encoding='utf-8') as out:
            for item in self.formulas:
                out.write(str(self.formulas[item]))
                out.write('\n')

    def computeFormulaicSpatialDensity(self):
        """
        Returns a list of lengths of consecutive formulaic and non-formulaic fragments.
        """
        if self.useMatrix[0][0]:
            spatialDensities = [1]
        else:
            spatialDensities = [-1]
        for item in self.useMatrix[0][1:]:
            if item and spatialDensities[-1] > 0:
                spatialDensities[-1] += 1
            elif item and spatialDensities[-1] < 0:
                spatialDensities.append(1)
            elif not item and spatialDensities[-1] > 0:
                spatialDensities.append(-1)
            else:
                spatialDensities[-1] -= 1
        for row in self.useMatrix[1:]:
            for item in row:
                if item and spatialDensities[-1] > 0:
                    spatialDensities[-1] += 1
                elif item and spatialDensities[-1] < 0:
                    spatialDensities.append(1)
                elif not item and spatialDensities[-1] > 0:
                    spatialDensities.append(-1)
                else:
                    spatialDensities[-1] -= 1
        return spatialDensities

    def computeSDOfNonFormulaicFrags(self):
        """
        Computes the standard deviation of lengths of non-formulaic fragments.
        """
        nonFormulaicFrags = [abs(value) for value in self.computeFormulaicSpatialDensity() if value < 0]
        return sd(nonFormulaicFrags)
