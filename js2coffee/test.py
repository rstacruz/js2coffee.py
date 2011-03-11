import unittest
import subprocess as sub
import os
import sys

from builder import build

class CoffeeTestCase(unittest.TestCase):
  def setUp(self):
    pass

  def compare(self, js, cs, name=''):
    out = build(js)
    if out.strip() == cs.strip():
      self.assertEqual(out.strip(), cs.strip())
    else:
      print ""
      print "----------------------------------------------------------------------"
      print "%s" % name
      print ""
      print "Output:"
      print "> " + out.strip().replace(' ', '_').replace("\n", "\n> ")
      print ""
      print "Expected:"
      print "> " + cs.strip().replace(' ', '_').replace("\n", "\n> ")
      self.assertTrue(False)

  def compare_file(self, name):
    js = file("%s.js" % name).read()
    cs = file("%s.coffee" % name).read()

    # Inspect the output
    out = "fixtures/%s.txt" % name
    if os.path.exists(out):
      p = sub.Popen(['coffee', "fixtures/%s.coffee"%name], stdout=sub.PIPE, stderr=sub.PIPE)
      output, errors = p.communicate()
      self.assertEqual(output, file(out).read())

    self.compare(js=js, cs=cs, name=name)

