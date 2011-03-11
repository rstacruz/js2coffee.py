#!/usr/bin/env python
from js2coffee.test import CoffeeTestCase

class FeaturesTest(CoffeeTestCase):
  def test_var(self):
    self.compare_file('features/var')

  def test_for(self):
    self.compare_file('features/for')

  def test_if(self):
    self.compare_file('features/if')

  def test_empty_function(self):
    self.compare_file('features/empty_function')

  def test_switch(self):
    self.compare_file('features/switch')

  def test_ternary(self):
    self.compare_file('features/ternary')

  def test_unary(self):
    self.compare_file('features/unary')

  def test_throw(self):
    self.compare_file('features/throw')

  def test_return_function(self):
    self.compare_file('features/return_function')

  def test_single_return(self):
    self.compare_file('features/single_return')

  def test_for_in(self):
    self.compare_file('features/for_in')

  def test_not(self):
    self.compare_file('features/not')

  def test_instanceof(self):
    self.compare_file('features/instanceof')

  def test_blank_lines(self):
    self.compare_file('features/blank_lines')

  def test_void(self):
    self.compare_file('features/void')

  def test_assignment(self):
    self.compare_file('features/assignment')

  def test_reserved_words(self):
    self.compare_file('features/reserved_words')

  def test_index(self):
    self.compare_file('features/index')

  def test_assignment_condition(self):
    self.compare_file('features/assignment_condition')

  def test_delete(self):
    self.compare_file('features/delete')

  def test_do(self):
    self.compare_file('features/do')

  def test_return_in_if(self):
    self.compare_file('features/return_in_if')

  def test_call_statement(self):
    self.compare_file('features/call_statement')

  def test_function_order(self):
    self.compare_file('features/function_order')

  def test_empty_semicolon(self):
    self.compare_file('features/empty_semicolon')

  def test_others(self):
    self.compare_file('features/7')
    self.compare_file('features/12')
    self.compare_file('features/14')
    self.compare_file('features/15')
    self.compare_file('features/16')
    self.compare_file('features/17')
    self.compare_file('features/21')
    self.compare_file('features/23')

if __name__ == '__main__':
  import unittest
  unittest.main()
