## To do:

 *  Compiler settings
 *  Issue warnings

### Optimizations to do:

 *  `delete x, y` => `delete x` `delete y`
 *  `if (x) y = a; else y = b` => `y = if x; a; else b`

### Done:

 *  `alert(lol(2))` => `alert lol(2)` (safe omission of call parentheses)
 *  `alert({x:2, y:2})` => `alert;  x: 2;  y: 2` (safe omission of hash braces)
 *  omit the last return
 *  Empty blocks like `for (;;) { }`
 *  `if x == y; return` => `return if x == y`

