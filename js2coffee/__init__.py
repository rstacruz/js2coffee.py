from builder  import Builder, Unsupported, build
from jsparser import SyntaxError_
import test
import sys

def Main():
  if len(sys.argv) == 1:
    print "Usage: %s file.js" % sys.argv[0]
    exit()

  try:
    data = file(sys.argv[1]).read()
    out  = build(data)
    print out

  except SyntaxError_ as e:
    print e
