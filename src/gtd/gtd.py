
import logging
from random import randint
logger = logging.getLogger(__name__)

symbol_table = {}


class Gtd(object):
    def __init__(self, db = None):
        global gdb
        self.db = db
        gdb = db
        print('class Gtd initialized')

    def take_server_object(self, server_obj):
        self.server = server_obj

    # take_data - used by the server to push the data it got from teh client
    # to the proc/gtd for processing
    def take_data(self,data):
        print("the proc got this data: {}".format(data))
        ############## just for the sake of testing
        if r"start @" in data:
            # get a list of task and project ids
            l1 = list(gdb.dfp.index.values)
            l2 = list(gdb.dft.index.values)
            l3 = l1+l2
            if len(l3) == 0:
                raise ValueError('for some reason, got an empty list in @0000 replacement')
            r = randint(0,len(l3))
            #gdb.use_this_ID_for_ref = l3[r]
            data = data.replace('00000000',str(l3[r]))#.zfill(8))
            logger.debug('command after replacement: {}'.format(data))
        elif r'stop @' in data:
            #list(g[g.State == 'Closed']['ID'])
            l1 =  list(gdb.dfa[gdb.dfa.State == 'Started'].index)
            l1 += list(gdb.dft[gdb.dft.State == 'Open'].index)
            l1 += list(gdb.dfp[gdb.dfp.State == 'Started'].index)
            l2 =  list(gdb.dfa[gdb.dfa.State == 'OnHold'].index)
            l2 += list(gdb.dft[gdb.dft.State == 'OnHold'].index)
            l2 += list(gdb.dfp[gdb.dfp.State == 'OnHold'].index)
            l3 = l1 + l2
            if len(l3) == 0:
                raise ValueError('for some reason, got an empty list in @0000 replacement')
            r = randint(0,len(l3)-1)
            data = data.replace('00000000', str(l3[r]))#.zfill(8))
            logger.debug('command after replacement: {}'.format(data))
        elif r'cont @' in data:
            #list(g[g.State == 'Closed']['ID'])
            l1 =  list(gdb.dfa[gdb.dfa.State == 'Ended'].index)
            l1 += list(gdb.dft[gdb.dft.State == 'Closed'].index)
            l1 += list(gdb.dfp[gdb.dfp.State == 'Ended'].index)
            l2 =  list(gdb.dfa[gdb.dfa.State == 'OnHold'].index)
            l2 += list(gdb.dft[gdb.dft.State == 'OnHold'].index)
            l2 += list(gdb.dfp[gdb.dfp.State == 'OnHold'].index)
            l3 = l1 + l2
            if len(l3) == 0:
                raise ValueError('for some reason, got an empty list in @0000 replacement')
            r = randint(0,len(l3)-1)
            data = data.replace('00000000', str(l3[r]))#.zfill(8))
            logger.debug('command after replacement: {}'.format(data))
        elif r'halt @' in data:
            #list(g[g.State == 'Closed']['ID'])
            l1 =  list(gdb.dfa[gdb.dfa.State == 'Started'].index)
            l1 += list(gdb.dft[gdb.dft.State == 'Open'].index)
            l1 += list(gdb.dfp[gdb.dfp.State == 'Started'].index)
            l2 = []
            l3 = l1 + l2
            if len(l3) == 0:
                raise ValueError('for some reason, got an empty list in @0000 replacement')
            r = randint(0,len(l3)-1)
            data = data.replace('00000000', str(l3[r]))#.zfill(8))
            logger.debug('command after replacement: {}'.format(data))
        elif r'list @' in data:
            #list(g[g.State == 'Closed']['ID'])
            l1 = list(gdb.dfm.index.values)
            l2 = list(gdb.dfp.index.values)
            l3 = list(gdb.dft.index.values)
            l4 = list(gdb.dfa.index.values)
            l5 = l1 + l2 + l3 + l4
            if len(l5) == 0:
                raise ValueError('for some reason, got an empty list in @0000 replacement')
            r = randint(0,len(l5)-1)
            data = data.replace('00000000', str(l5[r]))#.zfill(8))
            logger.debug('command after replacement: {}'.format(data))

        ############## just for the sake of testing
        self.current_data = data
        logger.debug('stored new data:{}'.format(self.current_data))
        return True

    # process function does/start the heavy lifting of interpreting
    # the request from teh client and pusing the info to the database
    def process(self):
        print('processing data from the client')
        logger.debug('data from c: %s',self.current_data)
        if not self.sanitize_input():
            #raise UserWarning
            return False
        try:
            res = parse(self.current_data)
        except SyntaxError:
            logger.debug("parse exception: {}".format(res.__repr__()))
        # at this point, the
        res1 = gdb.do_transaction()
        return True

    # get_message_back_to_client - method used by
    def get_message_back_to_client(self):
        #return_message = 'proc2client: ' + self.current_data # (just echo for now)
        logger.debug('this is the return_message: {}'.format(self.db.return_message))
        return gdb.return_message

    # this function cleans the input to parsing from things that may be operatoprs
    # like = -,=,!,@ etc
    def sanitize_input(self):
        # some syntax checks and expantions
        ################################
        # check that "list" follows a "list" command
        if ((self.current_data.replace(' ', '') == 'list') and ('list' not in gdb.transaction_type)):
            return False


        #############################################
        # ci and co messages
        if self.current_data == 'ci':
            self.current_data = 'start @48 | checking in - start work'
        if self.current_data == 'co':
            self.current_data = 'start @48 | checking out - home'

        ##############################################
        # check if context need to be kept, and if not - clean it up
        if self.current_data.replace(' ', '') != 'list':
            gdb.clean_context()

        ##############################################
        # since teh tokenizer is not dealing well with the '|'
        # use this piece of code to handle that part
        if '|' in self.current_data:
            (t1,t2, t3) = self.current_data.partition('|')
            gdb.set_trans_description(t3)

        ##############################################
        # prepare a today | .... assuming
        # that there is a project called 'today' which is number
        # 48 (the number is what is important)
        temp1 = self.current_data.partition('|')
        if temp1[0].replace(' ', '') == 'today':
            self.current_data = 'start @48 |' + temp1[2]
        ##############################################
        return True


##########################################################
##########################################################

def expression(rbp=0):
    global token
    t = token
    token = next(mnext)
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next(mnext)
        left = t.led(left)
    return left

def tokenize_weekly(command):
    import tokenize
    from io import BytesIO
    #from io import StringIO as StringIO
    type_map = {
        tokenize.NUMBER: "(literal)",
        tokenize.STRING: "(literal)",
        tokenize.OP: "(operator)",
        tokenize.NAME: "(name)",
    }
    #for t in tokenize.generate_tokens(StringIO(command).next):
    logger.debug('I am in tokenize_weekly %s', command)
    #readline = StringIO("x+1").readline
    g = tokenize.tokenize(BytesIO(command.encode('utf-8')).readline)
    for t in g:
    #for t in tokenize.tokenize(BytesIO("x+1".encode('utf-8')).readline):
        logger.debug("tokenize_weekly, {}".format(t))
        if t[0] == 59: # this is the 'first' thing tokenize returns, which is the encoding
            continue
        try:
            yield type_map[t[0]], t[1]
        except KeyError:
            if t[0] == tokenize.ENDMARKER:
                break
            else:
                raise SyntaxError("Syntax error")
    yield "(end)", "(end)"

def tokenize(command):
    logger.debug('I am in tokenize %s', command)
    for id, value in tokenize_weekly(command):
        #logger.debug('id, value: %s , $s',id, value)
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
            elif id == "(operator)":
                symbol = symbol_table[id]
                s = symbol()
                s.value = value
            else:
                raise SyntaxError("Unknown operator (%r)" % id)
        yield s


def symbol(id, bp=0):
    #global symbol_table
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

def parse(command):
    global token, mnext
    logger.debug('I am in parse %s',command)
    mnext = tokenize(command)
    token = next(mnext)
    return expression()

def advance(id=None):
    global token
    if id and token.id != id:
        raise SyntaxError("Expected %r" % id)
    token = next(mnext)



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

def infix(id, bp):
    def led(self, left):
        self.first = left
        self.second = expression(bp)
        return self
    symbol(id, bp).led = led

def prefix(id, bp):
    def nud(self):
        self.first = expression(bp)
        self.second = None
        return self
    symbol(id).nud = nud


def infix_r(id, bp):
    def led(self, left):
        self.first = left
        self.second = expression(bp-1)
        return self
    symbol(id, bp).led = led

# # language definitions
symbol('(name)')
symbol('(literal)')
symbol("(end)")

symbol("(literal)").nud = lambda self: self
symbol("(name)").nud = lambda self: self
symbol("(operator)").nud = lambda self:self

prefix("create", 20)
prefix("task", 20)
infix_r("@",30)
infix_r("|",30)
prefix("start", 20)
prefix("cont", 20)
prefix("stop", 20)
prefix("halt", 20)
prefix("list", 20)
prefix("field", 20)
prefix("irange", 20)
prefix("drange", 20)
prefix("for", 20)
prefix("limit", 20)
prefix("col", 20)
prefix("is", 20)
prefix("inc", 20)
prefix("ninc", 20)
prefix("not", 20)
prefix("columns", 20)
prefix("states", 20)
prefix("head", 20)
prefix("tail", 20)
prefix("columns", 20)
prefix("states", 20)
prefix("help", 20)
prefix("delete", 20)
prefix("online", 20)
prefix("plus", 20)
symbol(".", 120)


def method(s):
    # decorator
    assert issubclass(s, symbol_base)
    def bind(fn):
        setattr(s, fn.__name__, fn)
    return bind

## extentions
@method(symbol("create"))
def nud(self):
    logger.debug("create nud")
    # creating a project
    if token.value == "project":
        self.id = "create project"
        self.first = next(mnext) # this is the project name
        # tell the gdb that the opration is create process
        gdb.transaction_is(self.id)
        gdb.set_project_name(self.first.value)
        advance() # need to advance to start process the megaproject name
        self.second = expression()
    # creating a megaproject
    if token.value == "megaproject":
        self.id = "create megaproject"
        self.first = next(mnext) # this is the megaproject name
        gdb.transaction_is(self.id)
        gdb.set_megaproject_name(self.first.value)
        advance() # need to advance to start the description
        self.second = expression()
    return self

@method(symbol("@"))
def nud(self):
    logger.debug("@ nud")
    if gdb.transaction_type == "create project":
        gdb.set_megaproject_name(token.value)
        advance()  # to check what is beyond ..
    elif gdb.transaction_type == "create task":
        gdb.set_project_name(token.value)
        advance()  # to check what is beyond ..
    elif gdb.transaction_type == 'start activity':
        # deal with the spacial case where token.value can be 'n'
        gdb.use_this_ID_for_ref = int(token.value) #get the id to relate the task creation to
    elif gdb.transaction_type == "stop something":
        gdb.use_this_ID_for_ref = int(token.value) #get the id to relate the task creation to
    elif gdb.transaction_type == "cont something":
        gdb.use_this_ID_for_ref = int(token.value) #get the id to relate the task creation to
    elif gdb.transaction_type == "halt something":
        gdb.use_this_ID_for_ref = int(token.value)  # get the id to relate the task creation to
    elif gdb.transaction_type == "list id":
        gdb.use_this_ID_for_ref = int(token.value)  # get the id to relate the task creation to
    elif gdb.transaction_type == "delete id":
        gdb.use_this_ID_for_ref = int(token.value)  # get the id to relate the task creation to

    self.first = expression()
    return self


@method(symbol("|"))
def nud(self):
    global token
    logger.debug("| nud")
    # this actually means there is nothing to do more
    # so ending the recursion here
    return self


# task creation
@method(symbol("task"))
def nud(self):
    logger.debug("task nud")
    # creating a task
    self.id = "create task"
    gdb.transaction_is(self.id)
    self.second = expression()
    return self

# activity creation
@method(symbol("start"))
def nud(self):
    logger.debug('start nud')
    gdb.transaction_is('start activity')
    self.second = expression()
    return self

@method(symbol("stop"))
def nud(self):
    logger.debug('stop nud')
    gdb.transaction_is('stop something')
    self.second = expression()
    return self

@method(symbol("cont"))
def nud(self):
    logger.debug('cont nud')
    gdb.transaction_is('cont something')
    self.second = expression()
    return self

@method(symbol("halt"))
def nud(self):
    logger.debug('halt nud')
    gdb.transaction_is('halt something')
    self.second = expression()
    return self

@method(symbol("list"))
def nud(self):
    logger.debug('list nud')
    if token.id == '@':
        gdb.transaction_is('list id')
    elif token.value == 'megaproject':
        gdb.transaction_is('list megaproject')
        advance()
    elif token.value == 'project':
        gdb.transaction_is('list project')
        advance()
    elif token.id == 'task':
        gdb.transaction_is('list task')
        advance()
    elif token.value == 'activity':
        gdb.transaction_is('list activity')
        advance()
    elif token.value == 'search':
        gdb.transaction_is('list search')
        # wrap it up
        return self
    elif token.id == '(end)':
        gdb.keep_context = True

    if token.id != "(end)":
        # if this is listing for ww - need to continue processing
        if token.value and 'ww' in token.value:
            gdb.list_ww = token.value
        else:
            self.second = expression() # continue process
    else:
        pass # do nothing - that is ==> start folding back teh recursion
    return self

@method(symbol("limit"))
def nud(self):
    logger.debug("limit nud")
    gdb.list_resp_has_limit = True
    if (token.value != '(end)'):
        gdb.list_resp_row_limit = int(token.value)
    #advance()
    self.second = expression()
    # this is the end of processing for limit thread
    return self

@method(symbol("col"))
def nud(self):
    logger.debug("col nud")
    gdb.list_col_name = token.value
    advance() # over the column name
    #gdb.list_col_value = token.value # this will be overriden if we have is/inc/not
    self.second = expression()
    return self

@method(symbol("is"))
def nud(self):
    logger.debug("is nud")
    gdb.list_col_value = token.value
    gdb.list_col_rel = 'is'
    #advance() # over the column name
    self.second = expression()
    return self

@method(symbol("inc"))
def nud(self):
    logger.debug("inc nud")
    gdb.list_col_value = token.value
    gdb.list_col_rel = 'inc'
    #advance() # over the column name
    self.second = expression()
    return self

@method(symbol("not"))
def nud(self):
    logger.debug("not nud")
    gdb.list_col_value = token.value
    gdb.list_col_rel = 'not'
    #advance() # over the column name
    self.second = expression()
    return self

@method(symbol("ninc"))
def nud(self):
    logger.debug("ninc nud")
    gdb.list_col_value = token.value
    gdb.list_col_rel = 'ninc'
    #advance() # over the column name
    self.second = expression()
    return self

@method(symbol("irange"))
def nud(self):
    logger.debug('irange nud')
    gdb.list_col_rel = 'irange'
    gdb.list_col_bot = token.value
    advance()
    gdb.list_col_top = token.value
    # this is the end of processing for this type of command
    return self

@method(symbol("drange"))
def nud(self):
    logger.debug('drange nud')
    gdb.list_col_rel = 'drange'
    gdb.list_col_bot = token.value
    if token.value != 'bot': # meaning we need to do some processing for the bottom
        advance()
        gdb.list_col_bot += token.value
        advance()
        if token.id == '.': # need to process a day
            gdb.list_col_bot += '.'
            advance()
            gdb.list_col_bot += token.value
            advance()
        else:
            gdb.list_col_bot += '.Sun' # this is the default
    else:
        advance()

    # now handle the top
    #advance()
    gdb.list_col_top = token.value
    if token.value != 'top':  # meaning we need to do some processing for the bottom
        advance()
        gdb.list_col_top += token.value
        advance()
        if token.id == '.':  # need to process a day
            gdb.list_col_top += '.'
            advance()
            gdb.list_col_top += token.value
        else:
            gdb.list_col_top += '.Sun'  # this is the default
            # now handle the top
    return self

@method(symbol("."))
def led(self, left):
    logger.debug('led .')
    return self


@method(symbol("for"))
def nud(self):
    logger.debug('nud for')
    # replace transaction
    st1,st2,st3 = gdb.transaction_type.partition(' ') #st3 holds the what to list (megaproject, project, etc)
    gdb.transaction_is('list for')
    gdb.list_what_for = st3
    if token.value:
        gdb.list_for_what = token.value
    else:
        gdb.list_for_what = token.id # this is special handling for the case of 'task' that is not processed like others
    advance()
    if gdb.list_for_what == 'task':
        advance()
    gdb.list_for_val = token.value
    #advance()
    #self.second = expression()
    return self

@method(symbol("columns"))
def nud(self):
    logger.debug("nud columns")
    gdb.list_attr = 'columns'
    # that's it. done
    return self

@method(symbol("states"))
def nud(self):
    logger.debug("nud states")
    gdb.list_attr = 'states'
    # that's it. done
    return self

@method(symbol("help"))
def nud(self):
    logger.debug('help nud')
    gdb.transaction_is('help')
    return self

@method(symbol("delete"))
def nud(self):
    logger.debug('deleate nud')
    if token.id == '@':
        gdb.transaction_is('delete id')
    else:
        raise SyntaxError(
            "Unknown token (%r)." % token.id
        )
    self.second = expression()
    return self

@method(symbol("online"))
def nud(self):
    logger.debug('online nud')
    gdb.transaction_is('online')
    return self

@method(symbol("plus"))
def nud(self):
    logger.debug("plus nud")
    return self