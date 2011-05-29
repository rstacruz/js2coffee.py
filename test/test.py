#!/usr/bin/env python
from js2coffee.test import CoffeeTestCase

class est(CoffeeTestCase):
  def test_var(self):
    self.compare_file('var')

  def test_for(self):
    self.compare_file('for')

  def test_if(self):
    self.compare_file('if')

  def test_empty_function(self):
    self.compare_file('empty_function')

  def test_equal_regex(self):
    self.compare_file('equal_regex')

  def test_switch(self):
    self.compare_file('switch')

  def test_ternary(self):
    self.compare_file('ternary')

  def test_unary(self):
    self.compare_file('unary')

  def test_throw(self):
    self.compare_file('throw')

  def test_return_function(self):
    self.compare_file('return_function')

  def test_single_return(self):
    self.compare_file('single_return')

  def test_for_in(self):
    self.compare_file('for_in')

  def test_not(self):
    self.compare_file('not')

  def test_instanceof(self):
    self.compare_file('instanceof')

  def test_blank_lines(self):
    self.compare_file('blank_lines')

  def test_void(self):
    self.compare_file('void')

  def test_assignment(self):
    self.compare_file('assignment')

  def test_reserved_words(self):
    self.compare_file('reserved_words')

  def test_index(self):
    self.compare_file('index')

  def test_assignment_condition(self):
    self.compare_file('assignment_condition')

  def test_delete(self):
    self.compare_file('delete')

  def test_do(self):
    self.compare_file('do')

  def test_return_in_if(self):
    self.compare_file('return_in_if')

  def test_call_statement(self):
    self.compare_file('call_statement')

  def test_function_order(self):
    self.compare_file('function_order')

  def test_empty_semicolon(self):
    self.compare_file('empty_semicolon')

  def test_others(self):
    self.compare_file('7')
    self.compare_file('12')
    self.compare_file('14')
    self.compare_file('15')
    self.compare_file('16')
    self.compare_file('17')
    self.compare_file('21')
    self.compare_file('23')

if __name__ == '__main__':
  import unittest
  unittest.main()
