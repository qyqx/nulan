##############################################################################
#  Strings
##############################################################################
>>> read(r'"foo\bar\n\qux"')
error: unknown escape sequence b
  "foo\b  (line 1, column 6)
       ^

>>> read(r'"foo\\\@\tbar"')
"foo\\\@\tbar"

>>> read(r'"foo\uA00Gbar"')
error: G is not valid hexadecimal
  "foo\uA00G  (line 1, column 10)
           ^

>>> read(r'"foo\ua00fbar"')
error: a is not valid hexadecimal
  "foo\ua  (line 1, column 7)
        ^

>>> read(r'"foo\u0000bar"')
"foo\u0000bar"

>>> read(r'"foo\uA00Fbar"')
"foo\uA00Fbar"

>>> read('"fooÀbar"')
"fooÀbar"

>>> read(r'"foo\u00C0bar"')
"foo\u00C0bar"


>>> read(r'"foo\u0009bar"')
"foo\u0009bar"

>>> read('"foo	bar"')
"foo  bar"

>>> read(r'"foo\tbar"')
"foo\tbar"

>>> read(r'"foo\u000Abar"')
"foo\u000Abar"

>>> read(r'''
...       "foo
...        bar"
...       ''')
"foo
 bar"

>>> read(r'"foo\nbar"')
"foo\nbar"


>>> write(r'"foo@bar\nqux"')
error: invalid character \
  "foo@bar\  (line 1, column 9)
          ^

>>> write(r'"foo@(id bar)\nqux"')
[(&fn str) (&char f) (&char o) (&char o) [(&symbol id) (&symbol bar)] (&char \n) (&char q) (&char u) (&char x)]

>>> write('"foo@barqux"')
[(&fn str) (&char f) (&char o) (&char o) (&symbol barqux)]

>>> write('"foo@"@"bar""qux"')
[(&fn str) (&char f) (&char o) (&char o) [(&fn str) [(&fn str) (&char b) (&char a) (&char r)]] (&char q) (&char u) (&char x)]

>>> write('"foo@(id bar)qux"')
[(&fn str) (&char f) (&char o) (&char o) [(&symbol id) (&symbol bar)] (&char q) (&char u) (&char x)]

>>> read(r'''
...       "foo\t
...        bar"
...       ''')
"foo\t
 bar"

>>> read(r'''
...       "foo
...          bar
...            qux"
...       ''')
"foo
   bar
     qux"

##############################################################################
#  Raw Strings
##############################################################################
>>> read(r'''
...       `fo@o\\bar\\n\qux`
...       ''')
"fo\@o\\\\bar\\\\n\\qux"

>>> write_all(
...       r'''
...       `fo@o\\bar`n:qux`
...       ''')
error: missing ending ` quote
  (line 3, column 6)

>>> read(
...       r'''
...       `fo@o\\bar`n:qux
...       ''')
("fo\@o\\\\bar" n (qux))

>>> read(r'''
...       `fo@o\\bar`
...       n`\qux`
...       ''')
"fo\@o\\\\bar"

>>> read(r'''
...       `foo
...          bar
...            qux`
...       ''')
"foo
         bar
           qux"

##############################################################################
#  Comments
##############################################################################
>>> read(r"#|#|foo|#bar|#qux")
qux

>>> read(r"#||#qux")
qux

>>> write(r'''
... #foo
... bar qux corge
... ''')
[(&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(r'''
... #|foo
... |#bar qux corge
... ''')
[(&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(r'''
...       #|
...         #|
...           foo
...         |#
...       bar
...       |#qux
...       ''')
(&symbol qux)

>>> read(r'''
...       #|
...         #|
...           foo
...         |#
...       bar
...       |#
...       ''')
%eof

>>> write(r'''
...       #foobar
...       qux
...       ''')
(&symbol qux)

>>> write(r'''
...       #
...       qux
...       ''')
(&symbol qux)

>>> read("#foobar")
%eof


>>> write('"foo@#||#qux"')
[(&fn str) (&char f) (&char o) (&char o) (&symbol qux)]


>>> write("foo bar #||# qux")
[(&symbol foo) (&symbol bar) (&symbol qux)]

>>> write("(foo bar #||# qux)")
[(&symbol foo) (&symbol bar) (&symbol qux)]

>>> write("[foo bar #||# qux]")
[(&fn seq) (&symbol foo) (&symbol bar) (&symbol qux)]


>>> write("()")
[]

>>> write("[]")
[]


>>> write("#||#")
%eof

>>> write("(#||#)")
[]

>>> write("[#||#]")
[]


>>> write("foo bar @ #||# qux")
[(&symbol foo) (&symbol bar) [(&fn splice) (&symbol qux)]]

>>> write("(foo bar @ #||# qux)")
[(&symbol foo) (&symbol bar) [(&fn splice) (&symbol qux)]]

>>> write("[foo bar @ #||# qux]")
[(&fn seq) (&symbol foo) (&symbol bar) [(&fn splice) (&symbol qux)]]

##############################################################################
#  Symbols
##############################################################################
>>> write("foo")
(&symbol foo)

>>> write("foo bar")
[(&symbol foo) (&symbol bar)]

>>> write("foo:bar")
[(&symbol foo) [(&symbol bar)]]

>>> write_all(r"foo;bar")
[(&symbol foo) [(&symbol bar)]]

>>> write("foo1")
(&symbol foo1)

>>> write("100foo")
(&symbol 100foo)

##############################################################################
#  Ignore
##############################################################################
>>> write("~")
(&fn %tilde)

>>> write("foo~bar")
[(&symbol foo) (&fn %tilde) (&symbol bar)]

##############################################################################
#  Numbers
##############################################################################
>>> write("100")
(&number 100)

>>> write("100")
(&number 100)

>>> write("100.50")
(&number 100.5)

>>> write(".100")
error: invalid character .
  .  (line 1, column 1)
  ^

>>> write("100.50.70")
error: invalid character .
  100.50.  (line 1, column 7)
        ^

##############################################################################
#  Infix < > <= =>
##############################################################################
>>> write("X < Y")
[(&fn lt?) (&symbol X) (&symbol Y)]

>>> write("(X < Y)")
[(&fn lt?) (&symbol X) (&symbol Y)]

>>> write("[X < Y]")
[(&fn seq) (&fn lt?) (&symbol X) (&symbol Y)]

>>> write("[X > Y]")
[(&fn seq) (&fn gt?) (&symbol X) (&symbol Y)]

>>> write("[X <= Y]")
[(&fn seq) (&fn lte?) (&symbol X) (&symbol Y)]

>>> write("[X => Y]")
[(&fn seq) (&fn gte?) (&symbol X) (&symbol Y)]

>>> write("[X => Y [Z < A]]")
[(&fn seq) [(&fn seq) (&fn gte?) (&symbol X) (&symbol Y)] [(&fn seq) (&fn lt?) (&symbol Z) (&symbol A)]]

>>> write("[X => Y Z < A]")
[(&fn seq) [(&fn seq) (&fn gte?) (&symbol X) (&symbol Y)] [(&fn seq) (&fn lt?) (&symbol Z) (&symbol A)]]

>>> write("{X => Y {Z < A}}")
[(&fn dict) [(&fn gte?) (&symbol X) (&symbol Y)] [(&fn dict) [(&fn lt?) (&symbol Z) (&symbol A)]]]


>>> write("foo<bar")
(&symbol foo<bar)

>>> write("foo<=bar")
(&symbol foo<=bar)

>>> write("foo>bar")
(&symbol foo>bar)

>>> write("foo=>bar")
(&symbol foo=>bar)

>>> write("foo => bar")
[(&fn gte?) (&symbol foo) (&symbol bar)]

>>> write("foo >= bar")
error: >= is invalid (you probably meant to use =>)
  foo >=  (line 1, column 6)
       ^

>>> write("foo = bar")
[(&fn is?) (&symbol foo) (&symbol bar)]

>>> write("foo == bar")
error: == is invalid (you probably meant to use =)
  foo ==  (line 1, column 6)
       ^

>>> write("foo = bar < 5")
[(&fn is?) (&symbol foo) [(&fn lt?) (&symbol bar) (&number 5)]]

>>> write("foo < bar = 5")
[(&fn is?) [(&fn lt?) (&symbol foo) (&symbol bar)] (&number 5)]

>>> write("[foo = bar]")
[(&fn seq) (&fn is?) (&symbol foo) (&symbol bar)]


>>> write("foo =")
error: expected an expression after =
  foo =  (line 1, column 5)
      ^

>>> write("foo ==")
error: == is invalid (you probably meant to use =)
  foo ==  (line 1, column 6)
       ^

>>> write("foo <")
error: expected an expression after <
  foo <  (line 1, column 5)
      ^

>>> write("foo <=")
error: expected an expression after <=
  foo <=  (line 1, column 6)
       ^

>>> write("foo >")
error: expected an expression after >
  foo >  (line 1, column 5)
      ^

>>> write("foo =>")
error: expected an expression after =>
  foo =>  (line 1, column 6)
       ^

>>> write("foo >=")
error: >= is invalid (you probably meant to use =>)
  foo >=  (line 1, column 6)
       ^

>>> write("foo ->")
error: expected an expression after ->
  foo ->  (line 1, column 6)
       ^

>>> write("foo +")
error: expected an expression after +
  foo +  (line 1, column 5)
      ^

>>> write("foo -")
error: expected an expression after -
  foo -  (line 1, column 5)
      ^

>>> write("foo *")
error: expected an expression after *
  foo *  (line 1, column 5)
      ^

>>> write("foo /")
error: expected an expression after /
  foo /  (line 1, column 5)
      ^

>>> write("foo :")
error: expected an expression after :
  foo :  (line 1, column 5)
      ^

>>> write("foo ;")
error: expected an expression after ;
  foo ;  (line 1, column 5)
      ^

>>> write("foo @")
error: expected an expression after @
  foo @  (line 1, column 5)
      ^

##############################################################################
#  Infix Math
##############################################################################
>>> write("(fact X - 1)")
[(&symbol fact) [(&fn sub) (&symbol X) (&number 1)]]

>>> write("fact1 X - 1 X * Acc")
[(&symbol fact1) [(&fn sub) (&symbol X) (&number 1)] [(&fn mul) (&symbol X) (&symbol Acc)]]

>>> write("fact1 X - 1: X * Acc")
[(&symbol fact1) [(&fn sub) (&symbol X) (&number 1)] [(&fn mul) (&symbol X) (&symbol Acc)]]

>>> write("fact1 X - 1; X * Acc")
[(&symbol fact1) [(&fn sub) (&symbol X) (&number 1)] [(&fn mul) (&symbol X) (&symbol Acc)]]

>>> write("fact1; X - 1; X * Acc")
error: can't use ; after ;
  fact1; X - 1;  (line 1, column 13)
              ^

>>> write("fact1: X - 1; X * Acc")
[(&symbol fact1) [(&fn sub) (&symbol X) (&number 1)] [(&fn mul) (&symbol X) (&symbol Acc)]]

>>> write("X * (fact X - 1)")
[(&fn mul) (&symbol X) [(&symbol fact) [(&fn sub) (&symbol X) (&number 1)]]]

>>> write("X * fact X - 1")
[[(&fn mul) (&symbol X) (&symbol fact)] [(&fn sub) (&symbol X) (&number 1)]]


>>> write("+100")
[(&fn add) (&number 100)]

>>> write("-100")
[(&fn sub) (&number 100)]


>>> write("+100.50")
[(&fn add) (&number 100.5)]

>>> write("-100.50")
[(&fn sub) (&number 100.5)]


>>> write("100 + 200")
[(&fn add) (&number 100) (&number 200)]

>>> write("100 - 200")
[(&fn sub) (&number 100) (&number 200)]

>>> write("100 * 200")
[(&fn mul) (&number 100) (&number 200)]

>>> write("100 / 200")
[(&fn div) (&number 100) (&number 200)]


>>> write("(100 +)")
error: expected an expression after +
  (100 +)  (line 1, column 7)
        ^

>>> write("(100 + 200 * 300)")
[(&fn add) (&number 100) [(&fn mul) (&number 200) (&number 300)]]

>>> write("(100 * 200 + 300)")
[(&fn add) [(&fn mul) (&number 100) (&number 200)] (&number 300)]

>>> write("((100 + 200) * 300)")
[(&fn mul) [(&fn add) (&number 100) (&number 200)] (&number 300)]


>>> write("[100 + 200 * 300]")
[(&fn seq) (&fn add) (&number 100) [(&fn seq) (&fn mul) (&number 200) (&number 300)]]

>>> write("[100 * 200 + 300]")
[(&fn seq) (&fn add) [(&fn seq) (&fn mul) (&number 100) (&number 200)] (&number 300)]

>>> write("[[100 + 200] * 300]")
[(&fn seq) (&fn mul) [(&fn seq) (&fn add) (&number 100) (&number 200)] (&number 300)]


>>> write("100 + 200 * 300")
[(&fn add) (&number 100) [(&fn mul) (&number 200) (&number 300)]]

>>> write("(100 + 200) * 300")
[(&fn mul) [(&fn add) (&number 100) (&number 200)] (&number 300)]

>>> write("100 + 200 - 300")
[(&fn sub) [(&fn add) (&number 100) (&number 200)] (&number 300)]

>>> write("100 + (200 - 300)")
[(&fn add) (&number 100) [(&fn sub) (&number 200) (&number 300)]]

>>> write("100 * 200 / 300")
[(&fn div) [(&fn mul) (&number 100) (&number 200)] (&number 300)]

>>> write("100 * (200 / 300)")
[(&fn mul) (&number 100) [(&fn div) (&number 200) (&number 300)]]

##############################################################################
#  Curly
##############################################################################
>>> write("{foo 1 bar 2}")
[(&fn dict) (&symbol foo) (&number 1) (&symbol bar) (&number 2)]

>>> write("{1 + 2 3}")
[(&fn dict) [(&fn add) (&number 1) (&number 2)] (&number 3)]

>>> write("{1 + 2 * 3 4}")
[(&fn dict) [(&fn add) (&number 1) [(&fn mul) (&number 2) (&number 3)]] (&number 4)]

##############################################################################
#  Bar
##############################################################################
>>> write(r'[foo bar qux @ : corge]')
[(&fn seq) (&symbol foo) (&symbol bar) (&symbol qux) [(&fn splice) [(&fn seq) (&symbol corge)]]]

>>> write(r'[foo bar qux @ : corge      ]')
[(&fn seq) (&symbol foo) (&symbol bar) (&symbol qux) [(&fn splice) [(&fn seq) (&symbol corge)]]]

>>> write_all(r'''
... [foo bar qux @ : corge      ]
... nou
... ''')
[(&fn seq) (&symbol foo) (&symbol bar) (&symbol qux) [(&fn splice) [(&fn seq) (&symbol corge)]]]
(&symbol nou)

>>> write_all(r'[foo bar qux @ : corge      ]nou')
[[(&fn seq) (&symbol foo) (&symbol bar) (&symbol qux) [(&fn splice) [(&fn seq) (&symbol corge)]]] (&symbol nou)]

>>> write(r'[foo bar qux @ : corge: nou]')
[(&fn seq) (&symbol foo) (&symbol bar) (&symbol qux) [(&fn splice) [(&fn seq) (&symbol corge) [(&fn seq) (&symbol nou)]]]]

>>> write(r'[foo: bar: qux: corge]')
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol bar) [(&fn seq) (&symbol qux) [(&fn seq) (&symbol corge)]]]]

>>> write(r'[foo: bar: qux: corge;]')
error: expected an expression after ;
  [foo: bar: qux: corge;]  (line 1, column 23)
                        ^

>>> write(r'[foo: bar: qux; corge]')
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol bar) [(&fn seq) (&symbol qux) [(&fn seq) (&symbol corge)]]]]

>>> write(r'[foo: bar: qux @ corge]')
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol bar) [(&fn seq) (&symbol qux) [(&fn splice) (&symbol corge)]]]]

>>> write(r'[foo: bar: qux @ : corge]')
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol bar) [(&fn seq) (&symbol qux) [(&fn splice) [(&fn seq) (&symbol corge)]]]]]

>>> write(r'[foo: bar: qux @ : corge;]')
error: expected an expression after ;
  [foo: bar: qux @ : corge;]  (line 1, column 26)
                           ^

>>> write(r'[foo: bar: qux @ : corge; nou]')
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol bar) [(&fn seq) (&symbol qux) [(&fn splice) [(&fn seq) (&symbol corge) [(&fn seq) (&symbol nou)]]]]]]

>>> write(r'[foo: bar: qux @ : corge: nou]')
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol bar) [(&fn seq) (&symbol qux) [(&fn splice) [(&fn seq) (&symbol corge) [(&fn seq) (&symbol nou)]]]]]]

>>> write(r'[foo: bar: qux @ : corge nou]')
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol bar) [(&fn seq) (&symbol qux) [(&fn splice) [(&fn seq) (&symbol corge) (&symbol nou)]]]]]


>>> write("@foo")
[(&fn splice) (&symbol foo)]

>>> write("(@foo)")
[[(&fn splice) (&symbol foo)]]

>>> write("[@foo]")
[(&fn seq) [(&fn splice) (&symbol foo)]]


>>> write("@foo    ")
[(&fn splice) (&symbol foo)]

>>> write("(@foo    )")
[[(&fn splice) (&symbol foo)]]

>>> write("[@foo    ]")
[(&fn seq) [(&fn splice) (&symbol foo)]]


>>> write("@foo bar qux")
[[(&fn splice) (&symbol foo)] (&symbol bar) (&symbol qux)]

>>> write("(@foo bar qux)")
[[(&fn splice) (&symbol foo)] (&symbol bar) (&symbol qux)]

>>> write("[@foo bar qux]")
[(&fn seq) [(&fn splice) (&symbol foo)] (&symbol bar) (&symbol qux)]


>>> write(r'''
... foo bar @
... qux
... ''')
error: expected an expression after @
  foo bar @  (line 2, column 9)
          ^

>>> write(r'''
... (foo bar @)
... qux
... ''')
error: expected an expression after @
  (foo bar @)  (line 2, column 11)
            ^

>>> write(r'''
... [foo bar @]
... qux
... ''')
error: expected an expression after @
  [foo bar @]  (line 2, column 11)
            ^


>>> write(r'''
... foo bar @
...   qux
... ''')
[(&symbol foo) (&symbol bar) [(&fn splice) (&symbol qux)]]

>>> write(r'''
... (foo bar @
...   qux)
... ''')
[(&symbol foo) (&symbol bar) [(&fn splice) (&symbol qux)]]

>>> write(r'''
... [foo bar @
...   qux]
... ''')
[(&fn seq) (&symbol foo) (&symbol bar) [(&fn splice) (&symbol qux)]]


>>> write("(foo bar @ qux)")
[(&symbol foo) (&symbol bar) [(&fn splice) (&symbol qux)]]

>>> write("foo bar @ qux")
[(&symbol foo) (&symbol bar) [(&fn splice) (&symbol qux)]]

>>> write("[foo bar @ qux]")
[(&fn seq) (&symbol foo) (&symbol bar) [(&fn splice) (&symbol qux)]]


>>> write("Test @ Args:")
error: expected an expression after :
  Test @ Args:  (line 1, column 12)
             ^

>>> write("(Test @ Args:)")
error: expected an expression after :
  (Test @ Args:)  (line 1, column 14)
               ^

>>> write("[Test @ Args:]")
error: expected an expression after :
  [Test @ Args:]  (line 1, column 14)
               ^


>>> write("Test @ Args: Orig @ Args")
[(&symbol Test) [(&fn splice) (&symbol Args)] [(&symbol Orig) [(&fn splice) (&symbol Args)]]]

>>> write("(Test @ Args: Orig @ Args)")
[(&symbol Test) [(&fn splice) (&symbol Args)] [(&symbol Orig) [(&fn splice) (&symbol Args)]]]

>>> write("[Test @ Args: Orig @ Args]")
[(&fn seq) (&symbol Test) [(&fn splice) (&symbol Args)] [(&fn seq) (&symbol Orig) [(&fn splice) (&symbol Args)]]]


>>> write("Test @ Args; Orig @ Args")
[(&symbol Test) [(&fn splice) (&symbol Args)] [(&symbol Orig) [(&fn splice) (&symbol Args)]]]

>>> write("(Test @ Args; Orig @ Args)")
[(&symbol Test) [(&fn splice) (&symbol Args)] [(&symbol Orig) [(&fn splice) (&symbol Args)]]]

>>> write("[Test @ Args; Orig @ Args]")
[(&fn seq) (&symbol Test) [(&fn splice) (&symbol Args)] [(&fn seq) (&symbol Orig) [(&fn splice) (&symbol Args)]]]


>>> write("foo: Test @ Args")
[(&symbol foo) [(&symbol Test) [(&fn splice) (&symbol Args)]]]

>>> write("(foo: Test @ Args)")
[(&symbol foo) [(&symbol Test) [(&fn splice) (&symbol Args)]]]

>>> write("[foo: Test @ Args]")
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol Test) [(&fn splice) (&symbol Args)]]]


>>> write("foo: Test @ Args;")
error: expected an expression after ;
  foo: Test @ Args;  (line 1, column 17)
                  ^

>>> write("(foo: Test @ Args;)")
error: expected an expression after ;
  (foo: Test @ Args;)  (line 1, column 19)
                    ^

>>> write("[foo: Test @ Args;]")
error: expected an expression after ;
  [foo: Test @ Args;]  (line 1, column 19)
                    ^


>>> write("foo: Test @ Args; Orig @ Args")
[(&symbol foo) [(&symbol Test) [(&fn splice) (&symbol Args)] [(&symbol Orig) [(&fn splice) (&symbol Args)]]]]

>>> write("(foo: Test @ Args; Orig @ Args)")
[(&symbol foo) [(&symbol Test) [(&fn splice) (&symbol Args)] [(&symbol Orig) [(&fn splice) (&symbol Args)]]]]

>>> write("[foo: Test @ Args; Orig @ Args]")
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol Test) [(&fn splice) (&symbol Args)] [(&fn seq) (&symbol Orig) [(&fn splice) (&symbol Args)]]]]


>>> write("X @ (join R Y)")
[(&symbol X) [(&fn splice) [(&symbol join) (&symbol R) (&symbol Y)]]]

>>> write("(X @ (join R Y))")
[(&symbol X) [(&fn splice) [(&symbol join) (&symbol R) (&symbol Y)]]]

>>> write("[X @ (join R Y)]")
[(&fn seq) (&symbol X) [(&fn splice) [(&symbol join) (&symbol R) (&symbol Y)]]]


>>> write("X @ [join R Y]")
[(&symbol X) [(&fn splice) [(&fn seq) (&symbol join) (&symbol R) (&symbol Y)]]]

>>> write("(X @ [join R Y])")
[(&symbol X) [(&fn splice) [(&fn seq) (&symbol join) (&symbol R) (&symbol Y)]]]

>>> write("[X @ [join R Y]]")
[(&fn seq) (&symbol X) [(&fn splice) [(&fn seq) (&symbol join) (&symbol R) (&symbol Y)]]]

##############################################################################
#  Colon
##############################################################################
>>> write("zip: map (foo bar): Args cdr")
[(&symbol zip) [(&symbol map) [(&symbol foo) (&symbol bar)] [(&symbol Args) (&symbol cdr)]]]

>>> write("(zip: map [foo bar]: Args cdr)")
[(&symbol zip) [(&symbol map) [(&fn seq) (&symbol foo) (&symbol bar)] [(&symbol Args) (&symbol cdr)]]]


>>> write("zip @ : map Args cdr")
[(&symbol zip) [(&fn splice) [(&symbol map) (&symbol Args) (&symbol cdr)]]]

>>> write("(zip @ : map Args cdr)")
[(&symbol zip) [(&fn splice) [(&symbol map) (&symbol Args) (&symbol cdr)]]]

>>> write("[zip @ : map Args cdr]")
[(&fn seq) (&symbol zip) [(&fn splice) [(&fn seq) (&symbol map) (&symbol Args) (&symbol cdr)]]]


>>> write("zip @ : map Args: cdr")
[(&symbol zip) [(&fn splice) [(&symbol map) (&symbol Args) [(&symbol cdr)]]]]

>>> write("(zip @ : map Args: cdr)")
[(&symbol zip) [(&fn splice) [(&symbol map) (&symbol Args) [(&symbol cdr)]]]]

>>> write("[zip @ : map Args: cdr]")
[(&fn seq) (&symbol zip) [(&fn splice) [(&fn seq) (&symbol map) (&symbol Args) [(&fn seq) (&symbol cdr)]]]]


>>> write("zip @ : map Args cdr; bar")
[(&symbol zip) [(&fn splice) [(&symbol map) (&symbol Args) (&symbol cdr) [(&symbol bar)]]]]

>>> write("(zip @ : map Args cdr; bar)")
[(&symbol zip) [(&fn splice) [(&symbol map) (&symbol Args) (&symbol cdr) [(&symbol bar)]]]]

>>> write("[zip @ : map Args cdr; bar]")
[(&fn seq) (&symbol zip) [(&fn splice) [(&fn seq) (&symbol map) (&symbol Args) (&symbol cdr) [(&fn seq) (&symbol bar)]]]]


>>> write_all(
... r'''
... foo: bar
... qux
... ''')
[(&symbol foo) [(&symbol bar)]]
(&symbol qux)


>>> write("foo: bar: qux")
[(&symbol foo) [(&symbol bar) [(&symbol qux)]]]

>>> write("(foo: bar: qux)")
[(&symbol foo) [(&symbol bar) [(&symbol qux)]]]

>>> write("[foo: bar: qux]")
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol bar) [(&fn seq) (&symbol qux)]]]


>>> write("foo: bar @ qux")
[(&symbol foo) [(&symbol bar) [(&fn splice) (&symbol qux)]]]

>>> write("(foo: bar @ qux)")
[(&symbol foo) [(&symbol bar) [(&fn splice) (&symbol qux)]]]

>>> write("[foo: bar @ qux]")
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol bar) [(&fn splice) (&symbol qux)]]]


>>> write("foo: bar; qux")
[(&symbol foo) [(&symbol bar) [(&symbol qux)]]]

>>> write("(foo: bar; qux)")
[(&symbol foo) [(&symbol bar) [(&symbol qux)]]]

>>> write("[foo: bar; qux]")
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol bar) [(&fn seq) (&symbol qux)]]]


>>> write("foo: bar; qux; corge")
[(&symbol foo) [(&symbol bar) [(&symbol qux)] [(&symbol corge)]]]

>>> write("(foo: bar; qux; corge)")
[(&symbol foo) [(&symbol bar) [(&symbol qux)] [(&symbol corge)]]]

>>> write("[foo: bar; qux; corge]")
[(&fn seq) (&symbol foo) [(&fn seq) (&symbol bar) [(&fn seq) (&symbol qux)] [(&fn seq) (&symbol corge)]]]


>>> write(
... r'''
... (foo:
...   bar:
...     qux)
... ''')
[(&symbol foo) [(&symbol bar) [(&symbol qux)]]]


>>> write(
... r'''
... $let: F: $fn Args: foo
...            bar
...            qux
...   corge
... ''')
[(&symbol $let) [(&symbol F) [(&symbol $fn) (&symbol Args) [(&symbol foo)]]] (&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(
... r'''
... $let: F: $fn Args: foo;
...            bar
...            qux
...   corge
... ''')
[(&symbol $let) [(&symbol F) [(&symbol $fn) (&symbol Args) [(&symbol foo)]]] (&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(
... r'''
... $let: F: $fn Args: foo;
...            bar
...            qux;
...   corge
... ''')
[(&symbol $let) [(&symbol F) [(&symbol $fn) (&symbol Args) [(&symbol foo)]]] [(&symbol bar) (&symbol qux)] [(&symbol corge)]]

>>> write(
... r'''
... $let: F: $fn Args (foo)
...            bar
...            qux;
...   corge
... ''')
[(&symbol $let) [(&symbol F) [(&symbol $fn) (&symbol Args) [(&symbol foo)]]] (&symbol bar) (&symbol qux) [(&symbol corge)]]


>>> write_all(
... r'''
... foo bar;qux ->
...  $let:Orig:eval Name
...       Test:eval Test
...   $let F:corge
...    eval F
... ''')
error: no matching :
  foo bar;  (line 2, column 8)
         ^

>>> write_all(
... r'''
... foo bar;qux ->
...  $let:Orig:eval Name
...      Test:eval Test
...   $let F:corge
...    eval F
... ''')
error: no matching :
  foo bar;  (line 2, column 8)
         ^

>>> write_all(
... r'''
... foo bar;qux ->
...  $let;Orig:eval Name
...      Test:eval Test
...   $let F:corge
...    eval F
... ''')
error: no matching :
  foo bar;  (line 2, column 8)
         ^


>>> write(
... r'''
... any: zip Fns Args; [X Y] ->
...  $if: not: X Y
...   error foo
... ''')
[(&symbol any) [(&symbol zip) (&symbol Fns) (&symbol Args)] [(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&symbol $if) [(&symbol not) [(&symbol X) (&symbol Y)]] [(&symbol error) (&symbol foo)]]]]

>>> write_all(
... r'''
... any (zip Fns Args); [X Y] ->
...  $if: not: X Y
...   error foo
... ''')
[(&symbol any) [(&symbol zip) (&symbol Fns) (&symbol Args)] [(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&symbol $if) [(&symbol not) [(&symbol X) (&symbol Y)]] [(&symbol error) (&symbol foo)]]]]

>>> write_all(
... r'''
... any; [X Y] -> zip: Fns Args
...  $if: not: X Y
...   error foo
... ''')
[(&symbol any) [(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&symbol zip) [(&symbol Fns) (&symbol Args)]] [(&symbol $if) [(&symbol not) [(&symbol X) (&symbol Y)]] [(&symbol error) (&symbol foo)]]]]


>>> write(": X -> : $let @ R; Y")
[[(&vau $fn) [(&fn seq) (&symbol X)] [(&symbol $let) [(&fn splice) (&symbol R)] (&symbol Y)]]]

>>> write("((X -> : $let @ R) Y)")
[[(&vau $fn) [(&fn seq) (&symbol X)] [(&symbol $let) [(&fn splice) (&symbol R)]]] (&symbol Y)]

>>> write("[[X -> : $let @ R] Y]")
[(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn seq) (&symbol $let) [(&fn splice) (&symbol R)]]] (&symbol Y)]


>>> write(": $fn: X; $let @ R; Y")
[(&symbol $fn) [(&symbol X) [(&symbol $let) [(&fn splice) (&symbol R)]] [(&symbol Y)]]]

>>> write("(($fn (X): $let @ R) Y)")
[[(&symbol $fn) [(&symbol X)] [(&symbol $let) [(&fn splice) (&symbol R)]]] (&symbol Y)]

>>> write("[[$fn [X]: $let @ R] Y]")
[(&fn seq) [(&fn seq) (&symbol $fn) [(&fn seq) (&symbol X)] [(&fn seq) (&symbol $let) [(&fn splice) (&symbol R)]]] (&symbol Y)]

##############################################################################
#  Semicolon
##############################################################################
>>> write("[$set! Name: $vau: $quote %Env; Args; case Args @ Fns]")
[(&fn seq) (&symbol $set!) (&symbol Name) [(&fn seq) (&symbol $vau) [(&fn seq) (&symbol $quote) (&symbol %Env) [(&fn seq) (&symbol Args)] [(&fn seq) (&symbol case) (&symbol Args) [(&fn splice) (&symbol Fns)]]]]]


>>> write(
... r'''
... $def! list? $or: cons? X; null? X
... ''')
[(&symbol $def!) (&symbol list?) (&symbol $or) [(&symbol cons?) (&symbol X) [(&symbol null?) (&symbol X)]]]

>>> write(
... r'''
... $def! list? : X -> $or: cons? X; null? X
... ''')
[(&symbol $def!) (&symbol list?) [(&vau $fn) [(&fn seq) (&symbol X) [(&symbol $or) [(&symbol cons?) (&symbol X)] [(&symbol null?) (&symbol X)]]]]]

>>> write(
... r'''
... ($def! list? : X -> $or: cons? X; null? X)
... ''')
[(&symbol $def!) (&symbol list?) [(&vau $fn) [(&fn seq) (&symbol X) (&symbol $or) [(&symbol cons?) (&symbol X)] [(&symbol null?) (&symbol X)]]]]

>>> write(
... r'''
... ($def! list? : X -> ($or: cons? X; null? X))
... ''')
[(&symbol $def!) (&symbol list?) [(&vau $fn) [(&fn seq) (&symbol X) [(&symbol $or) [(&symbol cons?) (&symbol X)] [(&symbol null?) (&symbol X)]]]]]


>>> write_all(
... r'''
... foo; bar
... qux
... ''')
[(&symbol foo) [(&symbol bar)]]
(&symbol qux)u


>>> write(
... r'''
... $def! foo; X ->
...  bar
... ''')
[(&symbol $def!) (&symbol foo) [(&vau $fn) [(&fn seq) (&symbol X)] (&symbol bar)]]

>>> write(
... r'''
... $def! foo; X ->
...  bar
...   qux
... ''')
[(&symbol $def!) (&symbol foo) [(&vau $fn) [(&fn seq) (&symbol X)] [(&symbol bar) (&symbol qux)]]]

>>> write(
... r'''
... $def! foo; X ->
...  bar
...   qux
...  corge
... ''')
[(&symbol $def!) (&symbol foo) [(&vau $fn) [(&fn seq) (&symbol X)] [(&symbol bar) (&symbol qux)] (&symbol corge)]]


>>> write(
... r'''
... $def!
...  foo
...  bar
...  qux
...  corge
... ''')
[(&symbol $def!) (&symbol foo) (&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(
... r'''
... $def! foo
...  bar
...  qux
...  corge
... ''')
[(&symbol $def!) (&symbol foo) (&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(
... r'''
... $def! foo bar
...  qux
...  corge
... ''')
[(&symbol $def!) (&symbol foo) (&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(
... r'''
... $def! foo bar qux
...  corge
... ''')
[(&symbol $def!) (&symbol foo) (&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(
... r'''
... $def! foo bar qux corge
... ''')
[(&symbol $def!) (&symbol foo) (&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(
... r'''
... $def! foo;
...  bar
...  qux
...  corge
... ''')
[(&symbol $def!) (&symbol foo) [(&symbol bar) (&symbol qux) (&symbol corge)]]

>>> write(
... r'''
... $def! foo;bar;
...  qux
...  corge
... ''')
[(&symbol $def!) (&symbol foo) (&symbol bar) [(&symbol qux) (&symbol corge)]]

>>> write(
... r'''
... $def! foo;bar;qux;
...  corge
... ''')
[(&symbol $def!) (&symbol foo) (&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(
... r'''
... $def! foo;bar;qux;corge
... ''')
[(&symbol $def!) (&symbol foo) (&symbol bar) (&symbol qux) (&symbol corge)]


>>> write(
... r'''
... $def! foo;bar
...           qux
...           corge
... ''')
[(&symbol $def!) (&symbol foo) (&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(
... r'''
... $def! ; foo bar
...   qux
...   corge
... ''')
[(&symbol $def!) [(&symbol foo) (&symbol bar) (&symbol qux) (&symbol corge)]]

>>> write(
... r'''
... $def! foo bar
...           qux
...           corge
... ''')
[(&symbol $def!) (&symbol foo) (&symbol bar) (&symbol qux) (&symbol corge)]

>>> write(
... r'''
... $def! foo;bar
...          qux
...           corge
... ''')
[(&symbol $def!) (&symbol foo) [(&symbol bar) (&symbol qux)] (&symbol corge)]

>>> write(
... r'''
... $def! foo;bar qux;corge
... ''')
[(&symbol $def!) (&symbol foo) [(&symbol bar) (&symbol qux)] (&symbol corge)]

>>> write(
... r'''
... $def! foo
...  bar qux
...   corge
... ''')
[(&symbol $def!) (&symbol foo) [(&symbol bar) (&symbol qux) (&symbol corge)]]


>>> write(
... r'''
... $let F: $fn Args: $if-error: Test @ Args; Orig Args
...  eval foo
... ''')
[(&symbol $let) (&symbol F) [(&symbol $fn) (&symbol Args) [(&symbol $if-error) [(&symbol Test) [(&fn splice) (&symbol Args)]]]] [(&symbol Orig) (&symbol Args) [(&symbol eval) (&symbol foo)]]]

>>> write(
... r'''
... $let F: $fn Args: $if-error: Test @ Args; Orig @ Args
...  eval foo
... ''')
error:

>>> write(
... r'''
... $let F: $fn Args: $if-error: Test @ Args
...  Orig @ Args
...   eval foo
... ''')
error:

[(&symbol $let) (&symbol F) [(&symbol $fn) (&symbol Args) [(&symbol $if-error) [(&symbol Test) [(&fn splice) (&symbol Args)]]]] [(&symbol Orig) [(&fn splice) (&symbol Args)]] [(&symbol eval) (&symbol foo)]]

##############################################################################
#  Arrow
##############################################################################
>>> write("foo->bar")
error: invalid character > (line 1, column 5):
  foo->
      ^u

>>> write("foo -> foo")
[(&vau $fn) [(&fn seq) (&symbol foo)] (&symbol foo)]

>>> write("(foo -> foo)")
[(&vau $fn) [(&fn seq) (&symbol foo)] (&symbol foo)]

>>> write("[foo -> foo]")
[(&fn seq) (&vau $fn) [(&fn seq) (&symbol foo)] (&symbol foo)]


>>> write("foo @ bar -> foo")
[(&vau $fn) [(&fn seq) (&symbol foo) [(&fn splice) (&symbol bar)]] (&symbol foo)]

>>> write("(foo @ bar -> foo)")
[(&vau $fn) [(&fn apply) (&fn seq) (&symbol foo) (&symbol bar)] (&symbol foo)]

>>> write("[foo @ bar -> foo]")
[(&fn seq) (&vau $fn) [(&fn apply) (&fn seq) (&symbol foo) (&symbol bar)] (&symbol foo)]


>>> write("@foo -> foo")
[(&vau $fn) [(&fn apply) (&fn seq) (&symbol foo)] (&symbol foo)]

>>> write("(@foo -> foo)")
[(&vau $fn) [(&fn apply) (&fn seq) (&symbol foo)] (&symbol foo)]

>>> write("[@foo -> foo]")
[(&fn seq) (&vau $fn) [(&fn apply) (&fn seq) (&symbol foo)] (&symbol foo)]


>>> write("(foo -a foo)")
[(&symbol foo) (&symbol -a) (&symbol foo)]


>>> write(
... r'''
... x y ->
...  foo
...  bar
... ''')
[(&vau $fn) [(&fn seq) (&symbol x) (&symbol y)] (&symbol foo) (&symbol bar)]

>>> write(
... r'''
... x y -> foo
...        bar
... ''')
[(&vau $fn) [(&fn seq) (&symbol x) (&symbol y)] (&symbol foo) (&symbol bar)]

>>> write("(x y -> foo bar)")
[(&vau $fn) [(&fn seq) (&symbol x) (&symbol y)] (&symbol foo) (&symbol bar)]

>>> write("[x y -> foo bar]")
[(&fn seq) (&vau $fn) [(&fn seq) (&symbol x) (&symbol y)] (&symbol foo) (&symbol bar)]


>>> write("x y -> foo bar")
[(&vau $fn) [(&fn seq) (&symbol x) (&symbol y)] [(&symbol foo) (&symbol bar)]]

>>> write("(x y -> (foo bar))")
[(&vau $fn) [(&fn seq) (&symbol x) (&symbol y)] [(&symbol foo) (&symbol bar)]]

>>> write("[x y -> [foo bar]]")
[(&fn seq) (&vau $fn) [(&fn seq) (&symbol x) (&symbol y)] [(&fn seq) (&symbol foo) (&symbol bar)]]


>>> write("@foo -> foo bar")
[(&vau $fn) [(&fn apply) (&fn seq) (&symbol foo)] [(&symbol foo) (&symbol bar)]]

>>> write("(@foo -> (foo bar))")
[(&vau $fn) [(&fn apply) (&fn seq) (&symbol foo)] [(&symbol foo) (&symbol bar)]]

>>> write("[@foo -> [foo bar]]")
[(&fn seq) (&vau $fn) [(&fn apply) (&fn seq) (&symbol foo)] [(&fn seq) (&symbol foo) (&symbol bar)]]


>>> write("@foo bar -> foo bar")
u

>>> write("(@foo bar -> foo bar)")
u

>>> write("[@foo bar -> foo bar]")
u


>>> write("(X Y -> Y)")
[(&vau $fn) [(&fn seq) (&symbol X) (&symbol Y)] (&symbol Y)]

>>> write(
... r'''
... (X Y ->
... (-> X)
...   (-> Y))
... ''')
[(&vau $fn) [(&fn seq) (&symbol X) (&symbol Y)] [(&vau $fn) [(&fn seq)] (&symbol X)] [(&vau $fn) [(&fn seq)] (&symbol Y)]]

>>> write("(X Y -> -> X -> Y)")
[(&vau $fn) [(&fn seq) (&vau $fn) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X) (&symbol Y)]] (&symbol X)] (&symbol Y)]

>>> write(
... r'''
... (X Y ->
...   -> X
...   -> Y)
... ''')
[(&vau $fn) [(&fn seq) (&vau $fn) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X) (&symbol Y)]] (&symbol X)] (&symbol Y)]


>>> write(
... r'''
... (: [X Y] -> [[X -> [$let @ R]] Y]; X)
... ''')
[[(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)]] [(&symbol X)]]


>>> write(
... r'''
... (([X Y] -> [[X -> [$let @ R]] Y])
...   X)
... ''')
[[(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)]] (&symbol X)]

>>> write(
... r'''
... [X Y] -> [[X -> [$let @ R]] Y]
...  X
... ''')
[(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)] (&symbol X)]

>>> write(
... r'''
... [X Y] -> [[X -> [$let @ R]] Y]
... X
... ''')
[(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)]]

>>> write(
... r'''
... :[X Y] -> [[X -> [$let @ R]] Y]
...  X
... ''')
[[(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)]] (&symbol X)]

>>> write(
... r'''
... :[X Y] -> [[X -> [$let @ R]] Y]
...   X
... ''')
[(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)] (&symbol X)]

>>> write(
... r'''
... [[[X Y] -> [[X -> [$let @ R]] Y]]
...   X]
... ''')
[(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)]] (&symbol X)]


>>> write(
... r'''
... ([X Y] -> [[X -> [$let @ R]] Y]
...   X)
... ''')
[(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)] (&symbol X)]

>>> write(
... r'''
... ([X Y] ->
...   [[X -> [$let @ R]] Y]
...   X)
... ''')
[(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)] (&symbol X)]

>>> write(
... r'''
... [X Y] ->
...  [[X -> [$let @ R]] Y]
...  X
... ''')
[(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)] (&symbol X)]

>>> write(
... r'''
... [[X Y] -> [[X -> [$let @ R]] Y] X]
... ''')
[(&fn seq) (&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)] (&symbol X)]


>>> write(
... r'''
... $def! each
...   [X @ R] F -> (F X) each R F
... ''')
[(&symbol $def!) (&symbol each) [(&vau $fn) [(&fn seq) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol F)] [(&symbol F) (&symbol X)] (&symbol each) (&symbol R) (&symbol F)]]

>>> write(
... r'''
... $def! each
...   [X @ R] F -> (F X) (each R F)
... ''')
[(&symbol $def!) (&symbol each) [(&vau $fn) [(&fn seq) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol F)] [(&symbol F) (&symbol X)] [(&symbol each) (&symbol R) (&symbol F)]]]

>>> write(
... r'''
... $def! each
...   [X @ R] F -> (F X): each R F
... ''')
[(&symbol $def!) (&symbol each) [(&vau $fn) [(&fn seq) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol F)] [(&symbol F) (&symbol X)] [(&symbol each) (&symbol R) (&symbol F)]]]

>>> write(
... r'''
... $def! each
...   [X @ R] F -> (F X); each R F
... ''')
[(&symbol $def!) (&symbol each) [(&vau $fn) [(&fn seq) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol F)] [(&symbol F) (&symbol X)] [(&symbol each) (&symbol R) (&symbol F)]]]

>>> write(
... r'''
... $def! each
...   [X @ R] F -> : F X; each R F
... ''')
[(&symbol $def!) (&symbol each) [(&vau $fn) [(&fn seq) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol F)] [(&symbol F) (&symbol X)] [(&symbol each) (&symbol R) (&symbol F)]]]

>>> write(
... r'''
... $def! each
...   [X @ R] F -> F X; each R F
... ''')
[(&symbol $def!) (&symbol each) [(&vau $fn) [(&fn seq) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol F)] [(&symbol F) (&symbol X)] [(&symbol each) (&symbol R) (&symbol F)]]]

>>> write(
... r'''
... $def! each
...   ([X @ R] F -> (F X); each R F)
... ''')
[(&symbol $def!) (&symbol each) [(&vau $fn) [(&fn seq) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol F)] [(&symbol F) (&symbol X)] [(&symbol each) (&symbol R) (&symbol F)]]]

>>> write(
... r'''
... $def! each
...   ([X @ R] F -> : F X; each R F)
... ''')
[(&symbol $def!) (&symbol each) [(&vau $fn) [(&fn seq) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol F)] [(&symbol F) (&symbol X)] [(&symbol each) (&symbol R) (&symbol F)]]]

##############################################################################
#  Whitespace indentation
##############################################################################
>>> write_all(r'''
... $pref; foo bar; qux yes
...   nou
... ''')
(&symbol $pref)
[(&symbol foo) (&symbol bar)]
[(&symbol qux) (&symbol yes) (&symbol nou)]

>>> write_all(r'''
... $pref; foo bar: qux yes
...   nou
... ''')
(&symbol $pref)
[(&symbol foo) (&symbol bar) [(&symbol qux) (&symbol yes)] (&symbol nou)]

>>> write_all(r'''
... $pref: foo bar; qux yes
...   nou
... ''')
[(&symbol $pref) [(&symbol foo) (&symbol bar)] [(&symbol qux) (&symbol yes)] (&symbol nou)]

>>> write_all(r'''
... $pref: foo bar: qux yes
...   nou
... ''')
[(&symbol $pref) [(&symbol foo) (&symbol bar) [(&symbol qux) (&symbol yes)]] (&symbol nou)]

>>> write_all(r'''
... $pref: foo bar: qux yes:
...   nou
... ''')
[(&symbol $pref) [(&symbol foo) (&symbol bar) [(&symbol qux) (&symbol yes) (&symbol nou)]]]

>>> write_all(r'''
... $pref: foo bar: qux yes:
...   nou
...    ohso
... ''')
[(&symbol $pref) [(&symbol foo) (&symbol bar) [(&symbol qux) (&symbol yes) [(&symbol nou) (&symbol ohso)]]]]

>>> write_all(r'''
... $pref; foo bar; qux yes;
...   nou
... ''')
(&symbol $pref)
[(&symbol foo) (&symbol bar)]
[(&symbol qux) (&symbol yes)]
(&symbol nou)

>>> write_all(r'''
... $pref: foo bar
...        qux yes
...   nou
... ''')
[(&symbol $pref) [(&symbol foo) (&symbol bar)] [(&symbol qux) (&symbol yes)] (&symbol nou)]

>>> write_all(r'''
... $pref; foo bar
...        qux yes
...   nou
... ''')
(&symbol $pref)
[(&symbol foo) (&symbol bar)]
[(&symbol qux) (&symbol yes) (&symbol nou)]

>>> write_all(r'''
... $pref: corge; foo bar
...               qux yes
...   nou
... ''')
[(&symbol $pref) (&symbol corge) [(&symbol foo) (&symbol bar)] [(&symbol qux) (&symbol yes)] (&symbol nou)]


>>> write_all(r'''
... each Args: X -> foo bar
...                 qux corge
...                 yes nou
... ''')
[(&symbol $each) (&symbol Args) [(&vau $fn) [(&fn &list) (&symbol X)] [(&symbol foo) (&symbol bar)] [(&symbol qux) (&symbol corge)] [(&symbol yes) (&symbol nou)]]]

>>> write_all(r'''
... each Args: X -> foo bar
...   qux corge
...   yes nou
... ''')
[(&symbol $each) (&symbol Args) [(&vau $fn) [(&fn &list) (&symbol X)] [(&symbol foo) (&symbol bar)]] [(&symbol qux) (&symbol corge)] [(&symbol yes) (&symbol nou)]]

>>> write_all(r'''
... each Args: X ->
...   foo bar
...   qux corge
...   yes nou
... ''')
[(&symbol $each) (&symbol Args) [(&vau $fn) [(&fn &list) (&symbol X)] [(&symbol foo) (&symbol bar)] [(&symbol qux) (&symbol corge)] [(&symbol yes) (&symbol nou)]]]


>>> write(r'''
...                             # TODO
... $set! any: [X @ R] F -> $or (F X): any R F
... ''')
[(&symbol $set!) (&symbol any) [(&vau $fn) [(&fn seq) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol F)] [(&symbol $or) [(&symbol F) (&symbol X)] [(&symbol any) (&symbol R) (&symbol F)]]]]

>>> write(r'''
... $set! $or; $vau Env [X @ R]
...   $let: X: eval Env X
...     $if X X: eval Env [$or @ R]
...
...                             # TODO
... $set! any: [X @ R] F -> $or (F X): any R F
... ''')
[(&symbol $set!) (&symbol $or) [(&symbol $vau) (&symbol Env) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] [(&symbol $let) [(&symbol X) [(&symbol eval) (&symbol Env) (&symbol X)]] [(&symbol $if) (&symbol X) (&symbol X) [(&symbol eval) (&symbol Env) [(&fn apply) (&fn seq) (&symbol $or) (&symbol R)]]]]]]

>>> write(r'''
... $set! $or; $vau Env [X @ R]
...   $let: X: eval Env X
...     $if X X: eval Env [$or @ R]
...                             # TODO
... $set! any: [X @ R] F -> $or (F X): any R F
... ''')
[(&symbol $set!) (&symbol $or) [(&symbol $vau) (&symbol Env) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] [(&symbol $let) [(&symbol X) [(&symbol eval) (&symbol Env) (&symbol X)]] [(&symbol $if) (&symbol X) (&symbol X) [(&symbol eval) (&symbol Env) [(&fn apply) (&fn seq) (&symbol $or) (&symbol R)]]]]]]


>>> write(r'''
... $set! $or; $vau Env [X @ R]
...   $let: X: eval Env X
...     $if X X: eval Env [$or @ R]
...                             'foo'
... $set! any: [X @ R] F -> $or (F X): any R F
... ''')
[(&symbol $set!) (&symbol $or) [(&symbol $vau) (&symbol Env) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] [(&symbol $let) [(&symbol X) [(&symbol eval) (&symbol Env) (&symbol X)]] [(&symbol $if) (&symbol X) (&symbol X) [(&symbol eval) (&symbol Env) [(&fn apply) (&fn seq) (&symbol $or) (&symbol R)] [(&fn str) (&char f) (&char o) (&char o)]]]]]]


>>> write(r'''
... $set! $or; $vau Env [X @ R]
...   $let: X: eval Env X
...     $if X X: eval Env [$or @ R]
...                             # TODO
...   $set! any: [X @ R] F -> $or (F X): any R F
... ''')
[(&symbol $set!) (&symbol $or) [(&symbol $vau) (&symbol Env) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] [(&symbol $let) [(&symbol X) [(&symbol eval) (&symbol Env) (&symbol X)]] [(&symbol $if) (&symbol X) (&symbol X) [(&symbol eval) (&symbol Env) [(&fn apply) (&fn seq) (&symbol $or) (&symbol R)]]]] [(&symbol $set!) (&symbol any) [(&vau $fn) [(&fn seq) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol F)] [(&symbol $or) [(&symbol F) (&symbol X)] [(&symbol any) (&symbol R) (&symbol F)]]]]]]

>>> write(r'''
... $set! $or; $vau Env [X @ R]
...   $let: X: eval Env X
...     $if X X: eval Env [$or @ R]
...
...                             # TODO
...   $set! any: [X @ R] F -> $or (F X): any R F
... ''')
[(&symbol $set!) (&symbol $or) [(&symbol $vau) (&symbol Env) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] [(&symbol $let) [(&symbol X) [(&symbol eval) (&symbol Env) (&symbol X)]] [(&symbol $if) (&symbol X) (&symbol X) [(&symbol eval) (&symbol Env) [(&fn apply) (&fn seq) (&symbol $or) (&symbol R)]]]] [(&symbol $set!) (&symbol any) [(&vau $fn) [(&fn seq) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol F)] [(&symbol $or) [(&symbol F) (&symbol X)] [(&symbol any) (&symbol R) (&symbol F)]]]]]]


>>> read(
... r'''
... foo
...  bar
...  qux
...  corge
... ''')
(foo bar qux corge)

>>> read(
... r'''
... foo
...  bar
...  qux
...   corge
... ''')
(foo bar (qux corge))

>>> read(
... r'''
... foo
...  bar
...   qux
...    corge
... ''')
(foo (bar (qux corge)))

>>> read(
... r'''
... foo bar
...  qux
...  corge
... ''')
(foo bar qux corge)

>>> read(
... r'''
... foo bar
...  qux
...  corge
... ''')
(foo bar qux corge)

>>> read(
... r'''
... foo bar
...  qux
...   corge
... ''')
(foo bar (qux corge))

# TODO: should this throw an error?
>>> read(
... r'''
... foo bar
...   qux
...  corge
... ''')
(foo bar qux corge)

##############################################################################
#  Code Snippets
##############################################################################
>>> write(
... r'''
... $def! type; $fn Fns
...  $fn Args
...   any: zip Fns Args; [X Y] ->
...    $if: not: X Y
...     error 'type check failed on argument @Y'
... ''')
[(&symbol $def!) (&symbol type) [(&symbol $fn) (&symbol Fns) [(&symbol $fn) (&symbol Args) [(&symbol any) [(&symbol zip) (&symbol Fns) (&symbol Args)] [(&vau $fn) [[(&fn seq) (&symbol X) (&symbol Y)]] [(&symbol $if) [(&symbol not) [(&symbol X) (&symbol Y)]] [(&symbol error) [(&fn str) (&char t) (&char y) (&char p) (&char e) (&char  ) (&char c) (&char h) (&char e) (&char c) (&char k) (&char  ) (&char f) (&char a) (&char i) (&char l) (&char e) (&char d) (&char  ) (&char o) (&char n) (&char  ) (&char a) (&char r) (&char g) (&char u) (&char m) (&char e) (&char n) (&char t) (&char  ) (&symbol Y)]]]]]]]]


>>> write(
... r'''
... $def! foo: type list? any? ; X -> X
... ''')
[(&symbol $def!) (&symbol foo) [(&symbol type) (&symbol list?) (&symbol any?)] [(&vau $fn) [(&fn seq) (&symbol X)] (&symbol X)]]


>>> write(
... r'''
... $def! foo: X -> X
... ''')
[(&symbol $def!) (&symbol foo) [(&vau $fn) [(&fn seq) (&symbol X)] (&symbol X)]]


>>> write(
... r'''
... $defvau! $def-if! ; Name Test @ Fns ->
...   $let; Orig:  eval Name
...         Test:  eval Test
...         F:     $fn Args: $if-error: Test @ Args
...                            Orig @ Args
...     eval [$def! Name F @ Fns]
... ''')
u


>>> write(
... r'''
... $defvau! $def-if! ; Name Test @ Fns ->
...   $let: Orig: eval Name
...         Test: eval Test
...     $let F: $fn Args: $if-error (Test @ Args): Orig @ Args
...       eval [$def! Name F @ Fns]
... ''')
[(&symbol $defvau!) (&symbol $def-if!) [(&vau $fn) [(&symbol Name) (&symbol Test) | (&symbol Fns)] [(&symbol $let) [(&symbol Orig) [(&symbol eval) (&symbol Name)] [(&symbol Test) [(&symbol eval) (&symbol Test)]]] [(&symbol $let) (&symbol F) [(&symbol $fn) (&symbol Args) [(&symbol $if-error) [(&symbol Test) | (&symbol Args)] [(&symbol Orig) | (&symbol Args)]]] [(&symbol eval) [(&fn seq) (&symbol $def!) (&symbol Name) (&symbol F) | (&symbol Fns)]]]]]]


>>> write(
... r'''
... $def-if! stream: type list?
...   X -> $let Env: current-env
...          make-stream
...            -> nil? X
...            -> car X
...            -> $set-in! Env X: cdr X
... ''')
[(&symbol $def-if!) (&symbol stream) [(&symbol type) (&symbol list?)] [(&vau $fn) [(&symbol X)] [(&symbol $let) (&symbol Env) [(&symbol current-env)] [(&symbol make-stream) [(&vau $fn) [] [(&symbol nil?) (&symbol X)]] [(&vau $fn) [] [(&symbol car) (&symbol X)]] [(&vau $fn) [] [(&symbol $set-in!) (&symbol Env) (&symbol X) [(&symbol cdr) (&symbol X)]]]]]]]


>>> write(
... r'''
... $def-if! stream: type list?
...   X -> $let Env: current-env
...          make-stream; -> nil? X
...                       -> car X
...                       -> $set-in! Env X: cdr X
... ''')
[(&symbol $def-if!) (&symbol stream) [(&symbol type) (&symbol list?)] [(&vau $fn) [(&symbol X)] [(&symbol $let) (&symbol Env) [(&symbol current-env)] [(&symbol make-stream) [(&vau $fn) [] [(&symbol nil?) (&symbol X)]] [(&vau $fn) [] [(&symbol car) (&symbol X)]] [(&vau $fn) [] [(&symbol $set-in!) (&symbol Env) (&symbol X) [(&symbol cdr) (&symbol X)]]]]]]]


>>> write(
... r'''
... $def! join: type list? any?
...   [X @ R] Y -> [X @ (join R Y)]
...   [X]     Y -> [X @ Y]
... ''')
[(&symbol $def!) (&symbol join) [(&symbol type) (&symbol list?) (&symbol any?)] [(&vau $fn) [[(&fn apply) (&fn seq) (&symbol X) (&symbol R)] (&symbol Y)] [(&fn apply) (&fn seq) (&symbol X) [(&symbol join) (&symbol R) (&symbol Y)]]] [(&vau $fn) [[(&fn seq) (&symbol X)] (&symbol Y)] [(&fn apply) (&fn seq) (&symbol X) (&symbol Y)]]]


>>> write(
... r'''
... $set! $let; $vau Env [X @ R]
...   eval Env: $if: null? R
...               X
...               # Equivalent to ($let: [X Y] X; ...)
...               :[X Y] -> [[X -> : $let @ R] Y]
...                X
... ''')
[(&symbol $set!) (&symbol $let) [(&symbol $vau) (&symbol Env) [(&fn apply) (&fn seq) (&symbol X) (&symbol R)] [(&symbol eval) (&symbol Env) [(&symbol $if) [(&symbol null?) (&symbol R)] (&symbol X) [[(&vau $fn) [(&fn seq) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]] (&symbol Y)]] (&symbol X)]]]]]


>>> write(
... r'''
... $set! $def! ; $vau Env [Name @ Fns]
...   $let: Args: uniq
...     eval Env [$set! Name: $fn Args: case Args @ Fns]
... ''')
[(&symbol $set!) (&symbol $def!) [(&symbol $vau) (&symbol Env) [(&fn apply) (&fn seq) (&symbol Name) (&symbol Fns)] [(&symbol $let) [(&symbol Args) [(&symbol uniq)]] [(&symbol eval) (&symbol Env) [(&fn seq) (&symbol $set!) (&symbol Name) [(&fn seq) (&symbol $fn) (&symbol Args) [(&fn apply) (&fn seq) (&symbol case) (&symbol Args) (&symbol Fns)]]]]]]]


>>> write(
... r'''
... $set! $let; $vau Env [X @ R]
...   eval Env: $if: null? R
...               X
...               # Equivalent to ($let: [X Y] X; ...)
...               :[X Y] -> [[X -> : $let @ R] Y]
...                X
... ''')
[(&symbol $set!) (&symbol $let) [(&symbol $vau) (&symbol Env) [(&vau &apply
) (&fn seq) (&symbol X) (&symbol R)] [(&symbol eval) (&symbol Env) [(&symbol
$if) [(&symbol null?) (&symbol R)] (&symbol X) [[(&vau $fn) [(&fn seq) [(&
fn &list) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&vau $fn) [(&
fn &list) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let) (&symbol R)]]
(&symbol Y)]] (&symbol X)]]]]]

>>> write(
... r'''
... $set! $let; $vau Env [X @ R]
...   eval Env: $if: null? R
...               X
...               # Equivalent to ($let: [X Y] X; ...)
...               prn :[X Y] -> [[X -> : $let @ R] Y]
...                    X
... ''')
[(&symbol $set!) (&symbol $let) [(&symbol $vau) (&symbol Env) [(&vau &apply
) (&fn seq) (&symbol X) (&symbol R)] [(&symbol eval) (&symbol Env) [(&symbol
$if) [(&symbol null?) (&symbol R)] (&symbol X) [(&symbol prn) [(&vau $fn) [(
&fn &list) [(&fn seq) (&symbol X) (&symbol Y)]] [(&fn seq) [(&fn seq) (&v
au &arrow) [(&fn seq) (&symbol X)] [(&fn apply) (&fn seq) (&symbol $let)
(&symbol R)]] (&symbol Y)]] (&symbol X)]]]]]

>>> write(
... r'''
... $set! $let; $vau Env [X @ R]
...   eval Env: $if: null? R
...               X
...               # Equivalent to ($let: [X Y] X; ...)
...               ([X Y] -> [[X -> : $let @ R] Y]
...                X)
... ''')
u

>>> write(
... r'''
... $set! $let; $vau Env [X @ R]
...   eval Env: $if: null? R
...               X
...               # Equivalent to ($let: [X Y] X; ...)
...               (([X Y] -> [[X -> : $let @ R] Y])
...                X)
... ''')
u
