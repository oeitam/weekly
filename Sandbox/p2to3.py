import re

# token_pat = re.compile("\s*(?:(\d+)|(.))")
token_pat = re.compile("\s*(?:(\d+)|(\*\*|.))")

def expression(rbp=0):
    #print "rbp: %d" % rbp
    global token
    #print "1 this is token %s" % token.value
    t = token
    token = next()
    #print "->t    :" + str(t.value)
    #print "->token:" + str(token.value)
    left = t.nud()
    #print left
    while rbp < token.lbp:
        t = token
        token = next()
        #print "->t    :" + str(t.value)
        #print "->token:" + str(token.value)
        #print "2 this is token %s" % token.value
        left = t.led(left)
    #print "expression returning left: %s" % left
    return left

class symbol_base(object):

    id = None # node/token type name
    value = None # used by literals
    first = second = third = None # used by tree nodes

    def nud(self):
        raise SyntaxError(
            "Syntax error (%r)." % self.id
        )

    def led(self, left):
        raise SyntaxError(
            "Unknown operator (%r)." % self.id
        )

    def __repr__(self):
        if self.id == "(name)" or self.id == "(literal)":
            return "(%s %s)" % (self.id[1:-1], self.value)
        out = [self.id, self.first, self.second, self.third]
        out = map(str, filter(None, out))
        return "(" + " ".join(out) + ")"

#def tokenize(program):
#    for number, operator in token_pat.findall(program):
#        if number:
#            symbol = symbol_table["(literal)"]
#            s = symbol()
#            s.value = number
#            yield s
#        else:
#            symbol = symbol_table.get(operator)
#            if not symbol:
#                raise SyntaxError("Unknown operator")
#            yield symbol()
#    symbol = symbol_table["(end)"]
#   yield symbol()

def tokenize_python(program):
    import tokenize
    from io import StringIO
    from io import BytesIO

    type_map = {
        tokenize.NUMBER: "(literal)",
        tokenize.STRING: "(literal)",
        tokenize.OP: "(operator)",
        tokenize.NAME: "(name)",
        }

    #for t in tokenize.generate_tokens(StringIO(program).readline):
    for t in tokenize.generate_tokens(BytesIO(b"x+1").readline):
        try:
            yield type_map[t[0]], t[1]
        except KeyError:
            if t[0] == tokenize.ENDMARKER:
                break
            else:
                raise SyntaxError("Syntax error")
    yield "(end)", "(end)"

def tokenize(program):
    for id, value in tokenize_python(program):
        if id == "(literal)":
            symbol = symbol_table[id]
            s = symbol()
            s.value = value
        else:
            # name or operator
            symbol = symbol_table.get(value)
            if symbol:
                s = symbol()
            elif id == "(name)":
                symbol = symbol_table[id]
                s = symbol()
                s.value = value
            else:
                raise SyntaxError("Unknown operator (%r)" % id)
        yield s

symbol_table = {}

def symbol(id, bp=0):
    try:
        s = symbol_table[id]
    except KeyError:
        class s(symbol_base):
            pass
        s.__name__ = "symbol-" + id # for debugging
        s.id = id
        s.lbp = bp
        symbol_table[id] = s
    else:
        s.lbp = max(bp, s.lbp)
    return s


symbol("(literal)")
symbol("+", 10); symbol("-", 10)
symbol("*", 20); symbol("/", 20)
symbol("**", 30)
symbol("(end)")

#print symbol_table

def infix(id, bp):
    def led(self, left):
        self.first = left
        self.second = expression(bp)
        return self
    symbol(id, bp).led = led

infix("+", 10); infix("-", 10)
infix("*", 20); infix("/", 20)

def prefix(id, bp):
    def nud(self):
        self.first = expression(bp)
        self.second = None
        return self
    symbol(id).nud = nud

prefix("+", 100); prefix("-", 100)

def infix_r(id, bp):
    def led(self, left):
        self.first = left
        self.second = expression(bp-1)
        return self
    symbol(id, bp).led = led

infix_r("**", 30)

symbol("(literal)").nud = lambda self: self

def parse(program):
    global token, next
    next = next(tokenize(program))
    token = next()
    #print "->t    :" + str(token.value)
    #print "->token:" + str(token.value)
    return expression()

symbol("lambda", 20)
symbol("if", 20) # ternary form

infix_r("or", 30); infix_r("and", 40); prefix("not", 50)

infix("in", 60); infix("not", 60) # in, not in
infix("is", 60) # is, is not
infix("<", 60); infix("<=", 60)
infix(">", 60); infix(">=", 60)
infix("<>", 60); infix("!=", 60); infix("==", 60)

infix("|", 70); infix("^", 80); infix("&", 90)

infix("<<", 100); infix(">>", 100)

infix("+", 110); infix("-", 110)

infix("*", 120); infix("/", 120); infix("//", 120)
infix("%", 120)

prefix("-", 130); prefix("+", 130); prefix("~", 130)

infix_r("**", 140)

symbol(".", 150); symbol("[", 150); symbol("(", 150)

symbol("(literal)").nud = lambda self: self
symbol("(name)").nud = lambda self: self
symbol("(end)")

def nud(self):
    expr = expression()
    advance(")")
    return expr
symbol("(").nud = nud

def advance(id=None):
    global token
    if id and token.id != id:
        raise SyntaxError("Expected %r" % id)
    token = next()

symbol(")")

def led(self, left):
    self.first = left
    self.second = expression()
    try:
        advance("else")
    except:
        SyntaxError
    else:
        self.third = expression()
    return self
symbol("if").led = led

symbol("else")

def led(self, left):
    if token.id != "(name)":
        SyntaxError("Expected an attribute name.")
    self.first = left
    self.second = token
    advance()
    return self
symbol(".").led = led

symbol("]")

def led(self, left):
    self.first = left
    self.second = expression()
    advance("]")
    return self
symbol("[").led = led

def method(s):
    assert issubclass(s, symbol_base)
    def bind(fn):
        setattr(s, fn.__name__, fn)
    return bind

#symbol(")");
symbol(",")

@method(symbol("("))
def led(self, left):
    self.first = left
    self.second = []
    if token.id != ")":
        while 1:
            self.second.append(expression())
            if token.id != ",":
                break
            advance(",")
    advance(")")
    return self

symbol(":")

@method(symbol("lambda"))
def nud(self):
    self.first = []
    if token.id != ":":
        argument_list(self.first)
    advance(":")
    self.second = expression()
    return self

def argument_list(list):
    while 1:
        if token.id != "(name)":
            SyntaxError("Expected an argument name.")
        list.append(token)
        advance()
        if token.id != ",":
            break
        advance(",")


def constant(id):
    @method(symbol(id))
    def nud(self):
        self.id = "(literal)"
        self.value = id
        return self

constant("None")
constant("True")
constant("False")

@method(symbol("not"))
def led(self, left):
    if token.id != "in":
        raise SyntaxError("Invalid syntax")
    advance()
    self.id = "not in"
    self.first = left
    self.second = expression(60)
    return self

@method(symbol("is"))
def led(self, left):
    if token.id == "not":
        advance()
        self.id = "is not"
    self.first = left
    self.second = expression(60)
    return self

@method(symbol("("))
def nud(self):
    self.first = []
    comma = False
    if token.id != ")":
        while 1:
            if token.id == ")":
                break
            self.first.append(expression())
            if token.id != ",":
                break
            comma = True
            advance(",")
    advance(")")
    if not self.first or comma:
        return self # tuple
    else:
        return self.first[0]

symbol("]")

@method(symbol("["))
def nud(self):
    self.first = []
    if token.id != "]":
        while 1:
            if token.id == "]":
                break
            self.first.append(expression())
            if token.id != ",":
                break
            advance(",")
    advance("]")
    return self

symbol("}"); symbol(":")

@method(symbol("{"))
def nud(self):
    self.first = []
    if token.id != "}":
        while 1:
            if token.id == "}":
                break
            self.first.append(expression())
            advance(":")
            self.first.append(expression())
            if token.id != ",":
                break
            advance(",")
    advance("}")
    return self


