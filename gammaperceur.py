#!/usr/bin/python
# -*- coding: utf-8 -*-

# === Documentation ===

# Gamma Perceur is a driller: it asks words from a dictionary.
#
# Dictionary format: emacs org-mode
#
# - Lines beginning with one or more "*" are ignored (headings)
# - Word definition format is " - foreign word :: native word"
# - The bullet can be "-", "+" or "*"
# - Subsequent versions will support the following:
# - Items with bullet "-" are less important (rare) words
# - Items with bullet "+" are more important (common) words
# - Items with bullet "*" are ordinary (default) words

# TODO
# - check sytax of dictionary file before proceeding
#   ^^^ that would eliminate 'random' 'index out of range' messages

# === Libraries ===

import sys
import string
import random
import fileinput

# === Variables ===

# TODO: have a more sensible default value and check sys.argv[1] as well!
motsf = "paraules.org"
mots = []
fauts = 0
questions = 0
bold = "\033[1m"
reset = "\033[0;0m"

# === Parse command line arguments ===
try:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print "Usage: python gammaperceur [categorie] [questions] [any/...]"
        sys.exit(0)
except:
    pass

try:
    qcat = sys.argv[1]
except:
    qcat = "none"

try:
    qmax = int(sys.argv[2])
except:
    qmax = 0

if qmax < 0:
    print "qmax has to be a positive integer!"
    exit

try:
    qfreq = sys.argv[3]
except:
    qfreq = "any"

# === Functions ===

def demande(mot):
    global fauts
    print string.strip(mot[1])
    if mot[0] == raw_input('? '):
        print "{---- :) -------- " + str(questions) + "/" + str(len(mots)) + " ----}"
    else:
        print "Mais non, c'est \033[0;31m" + mot[0] + "\033[0m"
        print "{---- :( -------- " + str(questions) + "/" + str(len(mots)) + " ----}"
        # For the colours see this blog post:
        # http://travelingfrontiers.wordpress.com/2010/08/22/how-to-add-colors-to-linux-command-line-output/
        fauts += 1

# === Logic ===

# -- Greet user --
print "Bonjour!"
print "Je suis γ Perceur, un instructeur éléctronique."

# -- Load words --
category = "none"
for line in fileinput.input(motsf):
    # DEBUG
    #print line
    if not line:
        continue
    line = line.rstrip()
    try:
        if line[0] != "#":
            if line[0] == "*":
                category = line.lstrip("*")
                category = category.lstrip(" ")
            else:
                line = line.lstrip()
                mots += [ string.split(line[2:]," :: ") ]
                if line[0] == "*":
                    mots[-1].append("ordinary")
                elif line[0] == "+":
                    mots[-1].append("common")
                elif line[0] == "-":
                    mots[-1].append("rare")
                else:
                    print "Syntax error:" + line
                mots[-1].append(category)
    except:
        print "Error parsing dictionary line:"
        if line == '':
            print "(Empty line.)"
        else:
            print line
        print '~' * 20

# -- Filter words --
if qfreq != "any":
    mots = filter(lambda x: x[2] == qfreq, mots)
if qcat != "none":
    mots = filter(lambda x: x[3] == qcat, mots)
if len(mots) < 1:
    print "Aucune mots comme ca. :("
    sys.exit(2)

# -- Ask words --
q = 0
# mix the order of words:
random.shuffle(mots)

for mot in mots:
    questions += 1
    if qmax > 1:
        if questions > qmax:
            break
#    print "DEBUG: x => ", x
    demande(mot)


print "Combien des fauts?"
print str(fauts) + "/" + str(questions) + " => " + str(float(fauts)/float(questions)*100).split('.')[0] + "%"


