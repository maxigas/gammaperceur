import sys

print sys.argv[0]
try:
    print sys.argv[1]
except:
    print "No command line arguments."

