import jsparser
import re as regex

class Unsupported(Exception):
  pass

class Code(str):
  """A utility class that extends str with some neato stuff."""

  def __iadd__(self, other):
    """Adds an expression."""
    self = Code(self + other)

    return self

  def __imul__(self, other):
    """Adds a scope."""
    self = Code(self.rstrip() + ("\n  " + regex.sub(r"(\n+)", "\\1  ", other).strip()) + "\n")
    return self

  def __repr__(self):
    import json
    return json.dumps(self, indent=4)

def build(string):
  b = Builder()
  return b.build(string)

class Builder:
  """
  Code builder.

  Common usage:

    b = self.builder()
    b.self.build("var a = 2;")    # string
  """

  def build(self, item):
    # Needs to be a JSParser tree.
    if type(item) == str:
      item = jsparser.parse(item)

    # Get the handler (eg: blocks._bitwise_and)
    kind = "_%s" % item.type.lower()
    fn   = getattr(self, kind) if hasattr(self, kind) else self._other

    return fn(item)

  # The main thing! Always returns a string.
  def _script(self, tree, no_break=False, returnable=False):
    re = Code()

    if len(tree) > 0:
      # Optimize: omit return if not needed.
      if returnable:
        tree[-1].last = True

      # No breaks for switches
      if no_break and tree[-1].type == "BREAK":
        tree = tree[0:-1]

    for i in tree:
      if i.type == "FUNCTION":
        re += self.build(i)

    for i in tree:
      if i.type != "FUNCTION":
        re += self.build(i)

    return re

  _block = _script

  # All of these functions return either a string (expr)
  # or array (statement).

  def _var(self, item):
    re = ""

    for i in item:
      if i.type == "IDENTIFIER":
        if hasattr(i, 'initializer'):
          # var a = ...;
          re += "%s = " % self._id(i.name)
          re += self.build(i.initializer)
          re += "\n"

    return re

  def _function(self, item):
    re = Code()

    # "function name() { ... }" => "name = -> ..."
    if hasattr(item, 'name'):
      re += "%s = " % self._id(item.name)

    if item.params:
      re += "(%s) -> " % ', '.join([ self._id(str) for str in item.params ])
    else:
      re += "->"

    re *= self._script(item.body, returnable=True)
    return re

  def _number(self, item):
    return str(item.value)

  def _string(self, item):
    return repr(str(item.value))

  def _semicolon(self, item):
    # Optimize: "alert(2)" should be "alert 2" and omit extra
    # parentheses. Only do this if it's the main statement in
    # the line.
    if item.expression == None:
      return ""

    if not hasattr(item.expression, 'type'):
      print item
      exit()
    if item.expression.type == "CALL":
      return self._call_statement(item.expression) + "\n"

    else:
      return self.build(item.expression) + "\n"

  def _increment(self, item):
    return self.build(item[0]) + "++"

  def _decrement(self, item):
    return self.build(item[0]) + "--"

  def _binary_operator(self, item, operation):
    return ''.join([self.build(item[0]), operation, self.build(item[1])])

  def _this(self, item):
    return 'this'

  def _instanceof(self, item):
    return self._binary_operator(item, " instanceof ")

  def _plus(self, item):
    return self._binary_operator(item, " + ")

  def _minus(self, item):
    return self._binary_operator(item, " - ")

  def _mul(self, item):
    return self._binary_operator(item, " * ")

  def _div(self, item):
    return self._binary_operator(item, " / ")

  def _mod(self, item):
    return self._binary_operator(item, " % ")

  def _eq(self, item):
    return self._binary_operator(item, " == ")

  def _strict_eq(self, item):
    return self._binary_operator(item, " is ")

  def _strict_ne(self, item):
    return self._binary_operator(item, " isnt ")

  def _lsh(self, item):
    return self._binary_operator(item, " << ")

  def _ursh(self, item):
    return self._binary_operator(item, " >> ")

  def _rsh(self, item):
    return self._binary_operator(item, " >> ")

  def _ne(self, item):
    return self._binary_operator(item, " != ")

  def _lt(self, item):
    return self._binary_operator(item, " < ")

  def _le(self, item):
    return self._binary_operator(item, " <= ")

  def _gt(self, item):
    return self._binary_operator(item, " > ")

  def _ge(self, item):
    return self._binary_operator(item, " >= ")

  def _bitwise_and(self, item):
    return self._binary_operator(item, " & ")

  def _bitwise_or(self, item):
    return self._binary_operator(item, " | ")

  def _bitwise_xor(self, item):
    return self._binary_operator(item, " ^ ")

  def _bitwise_not(self, item):
    raise Unsupported("Bitwise not isn't supported by CoffeeScript")

  def _and(self, item):
    return self._binary_operator(item, " and ")

  def _or(self, item):
    return self._binary_operator(item, " or ")

  def _in(self, item):
    return self._binary_operator(item, " in ")

  def _new_with_args(self, item):
    return 'new %s(%s)' % (self.build(item[0]), self.build(item[1]))

  def _delete(self, item):
    return "\n".join([("delete %s" % self.build(i)) for i in item]) + "\n"

  def _unary_minus(self, item):
    return '-%s' % self.build(item[0])

  def _unary_plus(self, item):
    return '+%s' % self.build(item[0])

  def _try(self, item):
    re = Code()
    re += "try"
    re *= self.build(item.tryBlock)
    for clause in item.catchClauses:
      re += self.build(clause)
    return re

  def _catch(self, item):
    re = Code()
    re += "catch %s" % item.varName
    re *= self.build(item.block)
    return re

  def _throw(self, item):
    return 'throw %s' % self.build(item.exception)

  def _null(self, item):
    return "null"

  def _other(self, item):
    return "/*%s*/" % (item.type)

  def _group(self, item):
    return '(' + self.build(item[0]) + ')'

  def _return(self, item):
    if hasattr(item, 'last') and item.value != 'return':
      if item.value.type == "CALL":
        return self._call_statement(item.value) + "\n"
      else:
        return self.build(item.value)

    elif item.value == 'return':
      return "return\n"
    else:
      return "return %s\n" % self.build(item.value)

  def _new(self, item):
    return "new %s" % self.build(item[0])

  def _id(self, str):
    # Account for reserved keywords
    if str in ['off', 'on', 'when', 'not', 'until', '__indexOf']:
      # TODO: issue a warning
      return "%s_" % str
    else:
      return str

  def _identifier(self, item):
    return self._id(item.value)

  def _call(self, item):
    if len(item[1]) == 0:
      # alert()
      return self.build(item[0]) + "()"
    else:
      # alert(2)
      params = self.build(item[1])
      if "\n" in params:
        return "%s(%s\n)" % (self.build(item[0]), params)
      else:
        return "%s(%s)" % (self.build(item[0]), params)

  def _call_statement(self, item):
    # "alert(2);" => "alert 2"
    if len(item[1]) > 0:
      return "%s %s" % (self.build(item[0]), self.build(item[1]))

    else:
      return self._call(item)

  def _list(self, item):
    re = Code()

    first = True
    for i in item:

      if not first: re += ", "
      first = False

      if i.type == "OBJECT_INIT":
        re += self._object_init_short(i)
      else:
        re += self.build(i)

    return re.rstrip()

  def _if_short(self, item, then):
    return "%s if %s\n" % (then.strip(), self.build(item.condition).strip())

  def _if(self, item):
    # Optimize: if the 'then' part isn't much of a block, then compress it
    then = self.build(item.thenPart)
    if not item.elsePart and then.count("\n") <= 1:
      return self._if_short(item, then)

    re = Code()
    re += "if %s" % self.build(item.condition)
    re *= self.build(item.thenPart)
    if item.elsePart:
      re += "else "
      re += self.build(item.elsePart)
    return re

  def _true(self, item):
    return "true"

  def _false(self, item):
    return "false"

  def _typeof(self, item):
    return "typeof(%s)" % ( self.build(item[0]) )

  def _dot(self, item):
    if item[0].type == 'THIS':
      return '@%s' % self.build(item[1])
    else:
      return '%s.%s' % ( self.build(item[0]), self.build(item[1]) )

  def _assign(self, item):
    re = Code()
    re += '%s = ' % self.build(item[0])

    # Optimize: hashes in assignments can skip the brackets
    if item[1].type == "OBJECT_INIT":
      re += self._object_init_short(item[1])
    else:
      re += self.build(item[1])
    return re

  def _index(self, item):
    return '%s[%s]' % ( self.build(item[0]), self.build(item[1]) )

  def _label(self, item):
    raise Unsupported("Labels not supported")

  def _object_init(self, item):
    re = Code()
    items = [self.build(i) for i in item]

    if len(items) == 0:
      re = "{}"
    elif len(items) > 1:
      re += "{"
      re *= "\n".join(items)
      re += "}"
    else:
      re += "{%s}" % ", ".join(items)
    return re

  def _object_init_short(self, item):
    re = Code()
    items = [self.build(i) for i in item]

    if len(items) == 0:
      re = "{}"
    elif len(items) > 1:
      re *= "\n".join(items)
    else:
      re += "{%s}" % ", ".join(items)
    return re

  def _property_init(self, item):
    return '%s: %s' % (self.build(item[0]), self.build(item[1]))

  def _array_init(self, item):
    return "[%s]" % ", ".join([self.build(i) for i in item])

  def _for(self, item):
    re = Code()
    if item.setup:
      re += self.build(item.setup) + "\n"

    cond    = self.build(item.condition) if item.condition else "true"
    update  = self.build(item.update)    if item.update    else ""
    body    = self.build(item.body) + update

    re += "while %s" % cond
    re *= body if len(body.strip()) > 0 else "0"
    return re

  def _for_in(self, item):
    re = Code()
    re += "for %s of %s" % (self.build(item.iterator), self.build(item.object))
    body = self.build(item.body)
    re *= body if len(body.strip()) > 0 else "0"
    return re

  def _not(self, item):
    return "not %s" % self.build(item[0])

  def _comma(self, item):
    return "\n".join([self.build(i) for i in item])

  def _regexp(self, item):
    begins_with = item.value['regexp'][0]

    # Workaround for "/ /g" and "/=/" not being parseable.
    if begins_with in [' ', '=']:
      return "RegExp(%s, %s)" % (repr(item.value['regexp']), repr(item.value['modifiers']))

    else:
      return '/%s/%s' % (item.value['regexp'], item.value['modifiers'])

  def _while(self, item):
    re = Code()
    re += "while %s" % self.build(item.condition)
    body = self.build(item.body)
    re *= body if len(body.strip()) > 0 else "0"
    return re

  def _break(self, item):
    return "break\n"

  def _continue(self, item):
    return "continue\n"

  def _switch(self, item):
    disc = self.build(item.discriminant)
    re = Code()
    else_ = ""
    for case in item.cases:
      if hasattr(case, 'caseLabel'):
        re += "%sif %s == %s" % (else_, self.build(case.caseLabel), disc)
        else_ = "else "
      elif case.type == 'DEFAULT':
        re += 'else'
      re *= self._script(case.statements, no_break=True).strip()
    return re

  def _hook(self, item):
    return "(if %s then %s else %s)" % (self.build(item[0]), self.build(item[1]), self.build(item[2]))

  def _void(self, item):
    return '`void 0`'

  def _do(self, item):
    re = Code()
    re += "while true"

    sub = Code()
    sub += self.build(item.body)
    sub += "break unless %s" % self.build(item.condition)

    re *= sub
    return re
