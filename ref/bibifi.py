
#################################
# Team 0xCC
# BIBIFI 2016 Coursera Capstone
# Server program
# Release 1.0
#################################
#
# This is the base for the team 0xCC Program Parser. It is based off the Vaughan Pratt 
# improvement to recursive-descent parsing. The description of the algorithm 
# and original code can be found at:
# http://effbot.org/zone/simple-top-down-parsing.htm
# The syntax definitions have been modeled after the Fall 2016 Bibifi challenge 
# description. 

import sys
import re
import json

CONTEXT = "anyone" # replaced by the as principal call at the start of the prog
DEFAULT_DELEGATOR = "anyone"
SHUTDOWN = False
DEBUG = True

# symbol (token type) registry
symbol_table = {}
reserved_words = [
    "all", "append", "as", "change", "create", "delegate", "default", "delete",
    "admin", "exit", "delegator", "delegation", "in", "local", "foreach",
    "password", "principal", "read", "replacewith", "return", "set", "to", "write",
    "***", "split", "concat", "tolower", "notequal", "filtereach", 
    "with", "let"
]

### In-Memory Context sensitive Program Manager ###
global_variable_table = {}
principal_table = {"admin":"admin","anyone":""}
local_variable_change_buffer = {}  # updated by local x = y calls dumped at end of program
global_variable_change_buffer = {} # all other variables
principal_change_buffer = {} #
OUTPUT_ROWS = []

gcount = 0


# oe debug functions
def debug_status_report(where = "NO WHERE"):
    if DEBUG:
        print "*************** %s: START DEBUG REPORT ***************" % where
        print "DEBUG:   Principals: ", principal_table
        print "DEBUG:   Globals: ", global_variable_table
        print "DEBUG:   LCB: ", local_variable_change_buffer
        print "DEBUG:   GCB: ", global_variable_change_buffer
        print "DEBUG:   PCB: ", principal_change_buffer
        print "CURRENT: CONTEXT: %s" % CONTEXT
        print "CURRENT: DEFAULT DELEGATOR: %s" % DEFAULT_DELEGATOR
        print "*************** %s: END DEBUG REPORT *****************" % where
    return
        
def print_token(t, level = "HEAD"):
    if DEBUG:
        print "*************** LEVEL %s: START TOKEN REPORT *****************" % level
        print "this is t at level %s:" % level
        if hasattr (t, "id"):
            print "id is: %s" % t.id
        if hasattr (t, "value"):
            print "value is: %s" % t.value
        if hasattr (t, "first"):
            print "first is: %s" % t.first
            print_token(t.first,"FIRST")
        if hasattr (t, "second"):
            print "second is: %s" % t.second
            print_token(t.second,"SECOND")
        if hasattr (t, "third"):
            print "third is: %s" % t.third
            print_token(t.third,"THIRD")
        # now - recursively can call some of the above!!
        
        print "*************** LEVEL %s: END TOKEN REPORT *******************" % level
    return        

# used to clear change cache at the end of the program
def flush_changes(success= False):
    global OUTPUT_ROWS
    global DEBUG
    global CONTEXT
    global local_variable_change_buffer
    global global_variable_change_buffer
    global principal_change_buffer
    if success:
        print "Saving variables to persist"
        for p in principal_change_buffer.keys():
            principal_table[p] = principal_change_buffer[p]
        for v in global_variable_change_buffer.keys():
            global_variable_table[v] = global_variable_change_buffer[v]
    if DEBUG:
        print "============== FROM FLUSH: success is %s  ====================" % success
        print "DEBUG Principals: ", principal_table
        print "DEBUG Globals: ", global_variable_table
        print "DEBUG LCB: ", local_variable_change_buffer
        print "DEBUG GCB: ", global_variable_change_buffer
        print "DEBUG PCB: ", principal_change_buffer
        print "CURRENT CONTEXT: %s" % CONTEXT
        print "CURRENT DEFAULT DELEGATOR: %s" % DEFAULT_DELEGATOR
        print "=================================== ===================="
    else:
        print "Failure Flushes Changes"
    local_variable_change_buffer = {}  
    global_variable_change_buffer = {}
    principal_change_buffer = {}
    results = OUTPUT_ROWS
    CONTEXT = "anyone"
    #print global_variable_table
    #print principal_table
    if DEBUG:
        print results
        print
        return results

### Principal management functions 
def add_principal(principal, password):
    global OUTPUT_ROWS
    global DEBUG
    global CONTEXT
    global local_variable_change_buffer
    global global_variable_change_buffer
    global principal_change_buffer

    debug_status_report("add principal #1")
    if CONTEXT != "admin":
        if DEBUG:
            print "Cannot add principal if not admin"
        OUTPUT_ROWS.append("DENIED")
        flush_changes()
        return False
    if principal in principal_table.keys():
        if DEBUG:
            print "Principal Already Exists"
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return False
    password = password.strip("\"")
    principal_change_buffer[principal] = password
    debug_status_report("add principal #2")
    add_delegation("all", principal, CONTEXT)
    debug_status_report("add principal #3")
    return True
    
def change_principal_password(principal, password):
    global OUTPUT_ROWS
    global DEBUG
    global CONTEXT
    global local_variable_change_buffer
    global global_variable_change_buffer
    global principal_change_buffer
    if "\"" in password:
        password = password.replace("\"","")
    if CONTEXT != "admin" and CONTEXT != principal:
        if DEBUG:
            print "%s cannot change the password for %s" %(CONTEXT, principal)
        OUTPUT_ROWS.append("DENIED")
        flush_changes()
        return False
    if principal not in principal_table.keys() and principal not in principal_change_buffer.keys():
        if DEBUG:
            print "Principal not in table or change buffer"
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return False
    principal_change_buffer[principal] = password
    
    return True

def principal_exists(principal):
    return ((principal in principal_table.keys()) or (principal in principal_change_buffer.keys()))
    
### Variable management functions
def variable_exists(variable):
    if (variable not in global_variable_table.keys() and variable not in global_variable_change_buffer.keys() and variable not in local_variable_change_buffer.keys()):     
        return False
    return True

def has_delegation(target, principal, delegation):
    global OUTPUT_ROWS
    global CONTEXT
    global DEBUG
    global local_variable_change_buffer
    global global_variable_change_buffer
    global principal_change_buffer
    if not variable_exists(target):
        return False
    if target in global_variable_change_buffer.keys():
        var_table = global_variable_change_buffer
    elif target in global_variable_table.keys():
         var_table = global_variable_table
    elif target in local_variable_change_buffer.keys():
         var_table = local_variable_change_buffer

    var = var_table[target]
    perms = var["access_control"]
    if principal in perms.keys():
        if delegation in perms[principal]:
            return True
    return False

def delete_delegation(target, principal, from_principal, delegation="R"):
    global OUTPUT_ROWS
    global DEBUG
    global CONTEXT
    global local_variable_change_buffer
    global global_variable_change_buffer
    global principal_change_buffer
    if CONTEXT != "admin" and CONTEXT != principal or (from_principal == "admin"):
        if DEBUG:
            print "%s cannot remove %s %s %s -> %s" % (CONTEXT, target, principal, delegation, from_principal)
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return False
    if not principal_exists(principal) or not principal_exists(from_principal):
        if DEBUG:
            print "One of the principals doesn't exist"
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return False
    if target is "all":
        for v in local_variable_change_buffer.keys():
            var = local_variable_change_buffer[v]
            perms = var["access_control"]
            if CONTEXT in perms.keys():
                if "D" in perms[CONTEXT]:
                    if from_principal in perms.keys():
                        perm_str = perms[from_principal].replace(delegation,"")
                        perms[from_principal] = perm_str
                        if perm_str == "":
                            del perms[from_principal]
                        if DEBUG:
                            print "perms ", perms
                        local_variable_change_buffer[target] = {"value":var["value"],"access_control":perms}
                        return True
                    else:
                        if DEBUG:
                            print "principal you are trying to remove the delegation from does not exist"
                        OUTPUT_ROWS.append("FAILED")
                        flush_changes()
                        return False
                else: 
                    if DEBUG:
                        print " %s cannot change delegation on %s" % (CONTEXT. target)
                    OUTPUT_ROWS.append("DENIED")
                    flush_changes()
                    return False
            else:
                if DEBUG:
                    print " %s cannot access %s" % (CONTEXT. target)
                OUTPUT_ROWS.append("DENIED")
                flush_changes()
                return False
        for v in global_variable_change_buffer.keys():
            var = global_variable_change_buffer[v]
            perms = var["access_control"]
            if CONTEXT in perms.keys():
                if "D" in perms[CONTEXT]:
                    if DEBUG:
                        print "resetting ",delegation, " for", from_principal
                    if from_principal in perms.keys():
                        perm_str = perms[from_principal].replace(delegation,"")
                        perms[from_principal] = perm_str
                        if perm_str == "":
                            del perms[from_principal]
                        global_variable_change_buffer[target] = {"value":var["value"],"access_control":perms}
                        return True
                    else:
                        if DEBUG:
                            print "principal you are trying to remove the delegation from does not exist"
                        OUTPUT_ROWS.append("FAILED")
                        flush_changes()
                        return False
                else: 
                    if DEBUG:
                        print " %s cannot change delegation on %s" % (CONTEXT. target)
                    OUTPUT_ROWS.append("DENIED")
                    flush_changes()
                    return False
            else: 
                if DEBUG:
                    print " %s cannot access %s" % (CONTEXT. target)
                OUTPUT_ROWS.append("DENIED")
                flush_changes()
                return False
        for v in global_variable_table.keys():
            var = global_variable_table[v]
            perms = var["access_control"]
            if CONTEXT in perms.keys():
                if "D" in perms[CONTEXT]:
                    if from_principal in perms.keys():
                        perm_str = perms[from_principal].replace(delegation,"")
                        perms[from_principal] = perm_str
                        if perm_str == "":
                            del perms[from_principal]
                        global_variable_change_buffer[target] = {"value":var["value"],"access_control":perms}
                        return True
                    else:
                        if DEBUG:
                            print "principal you are trying to remove the delegation from does not exist"
                        OUTPUT_ROWS.append("FAILED")
                        flush_changes()
                        return False
                else: 
                    if DEBUG:
                        print " %s cannot change delegation on %s" % (CONTEXT. target)
                    OUTPUT_ROWS.append("DENIED")
                    flush_changes()
                    return False
            else: 
                if DEBUG:
                    print " %s cannot access %s" % (CONTEXT. target)
                OUTPUT_ROWS.append("DENIED")
                flush_changes()
                return False
    else:
        the_table = "l"
        if target in local_variable_change_buffer.keys():
             var_table = local_variable_change_buffer
        elif target in global_variable_change_buffer.keys():
            var_table = global_variable_change_buffer
            the_table = "g"
        elif target in global_variable_table.keys():
             var_table = global_variable_table
             the_table = "g"
        
        var = var_table[target]
        perms = var["access_control"]
        if CONTEXT in perms.keys():
            if "D" in perms[CONTEXT]:
                if DEBUG:
                    print "resetting ",delegation, " for", from_principal
                if from_principal in perms.keys():
                    perm_str = perms[from_principal].replace(delegation,"")
                    perms[from_principal] = perm_str
                    if perm_str == "":
                        del perms[from_principal]
                    if DEBUG:
                        print "perms ", perms
                    global_variable_change_buffer[target] = {"value":var["value"],"access_control":perms}
                    debug_status_report("inside delete delegation #1")
                    return True
                else:
                    if DEBUG:
                        print "principal you are trying to remove the delegation from does not exist"
                    OUTPUT_ROWS.append("FAILED")
                    flush_changes()
                    return False
            else: 
                if DEBUG:
                    print " %s cannot access %s" % (CONTEXT. target)
                OUTPUT_ROWS.append("DENIED")
                flush_changes()
                return False
        else: 
            if DEBUG:
                print " %s cannot access %s" % (CONTEXT. target)
            OUTPUT_ROWS.append("DENIED")
            flush_changes()
            return False

def add_delegation(target, principal, from_principal, delegation="R"):
    global OUTPUT_ROWS
    global DEBUG
    global CONTEXT
    global local_variable_change_buffer
    global global_variable_change_buffer
    global principal_change_buffer

    debug_status_report("add delegation #1")
    if target is "all":
        for v in global_variable_table.keys():
            if v not in global_variable_change_buffer.keys():
                # check if it meets the criteria for a change
                var = global_variable_table[v]
                perms = var["access_control"]
                if CONTEXT in perms.keys():
                    if "D" in perms[CONTEXT]:
                        # add it to the change buffer
                        global_variable_change_buffer[v] = global_variable_buffer[v]

        # step 2
        for v in global_variable_change_buffer.keys():
            var = global_variable_change_buffer[v]
            perms = var["access_control"]
            if CONTEXT in perms.keys():
                if "D" in perms[CONTEXT]:
                    # add delegation for principal
                    perms[principal] = delegation

                    global_variable_change_buffer[v]["access_control"][principal] = delegation 
                    
        return True
                    
                    
                    
        
##        for v in global_variable_table.keys():
##            # here no check if this var has a changed value in the change buffer
##            var = global_variable_table[v]
##            perms = var["access_control"]
##            if CONTEXT in perms.keys(): # if the current principal (CP) has permissions on this variable
##                if "D" in perms[CONTEXT]: # and if the permisions CP has include delegation
##                    perms[principal] = delegation
##                    debug_status_report("add delegation #2")

##                    global_variable_change_buffer[v] = {"value":var["value"],"access_control":perms}

##                    debug_status_report("add delegation #3")
    else:
        if not principal_exists(principal) or not principal_exists(from_principal):
            OUTPUT_ROWS.append("FAILED")
            flush_changes()
            return
        if CONTEXT != "admin":
            if CONTEXT != from_principal:
                OUTPUT_ROWS.append("DENIED")
                flush_changes()
                return False
            if not has_delegation(target, from_principal, "D"):
                OUTPUT_ROWS.append("DENIED")
                flush_changes()
                return False
        
        if not variable_exists(target):
            OUTPUT_ROWS.append("FAILED")
            flush_changes()
            return False
        the_table = "l"
        if target in local_variable_change_buffer.keys():
             var_table = local_variable_change_buffer
        elif target in global_variable_change_buffer.keys():
            var_table = global_variable_change_buffer
            the_table = "g"
        elif target in global_variable_table.keys():
             var_table = global_variable_table
             the_table = "g"
        var = var_table[target]
        perms = var["access_control"]
        #perms[principal] = delegation # need to add, not replace

        if principal not in perms.keys(): #add it
            perms[principal] = delegation 
        if delegation not in perms[principal]: # add it
            perms[principal] = perms[principal] + delegation
        var = {"value":var["value"],"access_control":perms}
        if the_table == "g":
            debug_status_report("add delegation #4")
            global_variable_change_buffer[target] = var
            debug_status_report("add delegation #5")
        else:
            local_variable_change_buffer[target] = var
        return True
                    
def lookup_variable_access_perms(name):
    global OUTPUT_ROWS
    global CONTEXT
    global DEBUG
    global local_variable_change_buffer
    global global_variable_change_buffer
    global principal_change_buffer
    if variable_exists(name):
        if name in global_variable_change_buffer.keys():
            var_table = global_variable_change_buffer
        elif name in global_variable_table.keys():
             var_table = global_variable_table
        elif name in local_variable_change_buffer.keys():
             var_table = local_variable_change_buffer
        else:
            return False
        return var_table[name]["access_control"]
   
def lookup_variable_value(name,field=None):
    global OUTPUT_ROWS
    global DEBUG
    global CONTEXT
    global local_variable_change_buffer
    global global_variable_change_buffer
    global principal_change_buffer
    if variable_exists(name):
        
        if name in local_variable_change_buffer.keys():
             var_table = local_variable_change_buffer
        elif name in global_variable_change_buffer.keys():
            var_table = global_variable_change_buffer
        elif name in global_variable_table.keys():
             var_table = global_variable_table
        else:
            OUTPUT_ROWS.append("FAILED")
            flush_changes()
            return False
        
        access_perms = var_table[name]["access_control"]
        if DEBUG:
            print "Permissions for %s " % name , access_perms
        if CONTEXT not in access_perms:
            OUTPUT_ROWS.append("DENIED")
            flush_changes()
            return False
        if "R" not in access_perms[CONTEXT]:
            OUTPUT_ROWS.append("DENIED")
            flush_changes()
            return False
        if field is None:
            return var_table[name]["value"]
        else:
            if type(var_table[name]["value"]) == type({}):
                if field not in var_table[name]["value"].keys():
                    OUTPUT_ROWS.append("FAILED")
                    flush_changes()
                    return False
                elif type(var_table[name]["value"]) == type([]):
                    if int(field) >= len(var_table[name]["value"].keys()):
                        OUTPUT_ROWS.append("FAILED")
                        flush_changes()
                        return False
                    field = int(field)
            return var_table[name]["value"][field]
    else:
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return False

def add_global(name, value,from_here = ""):
    global OUTPUT_ROWS
    global DEBUG
    global CONTEXT
    global local_variable_change_buffer
    global global_variable_change_buffer
    global principal_change_buffer
    access_perms = {}

    if DEBUG:
        print "adding global of type: %s" % type(value)
    if type(value) == type({}):
        for k in value:
            if type(value[k]) != type({}):
                value[k] = value[k].replace("\"","")
            else:
                keys_op = getattr(value[k], "keys", None)
                if callable(keys_op):
                    for m in value[k].keys():
                        value[k][m] = value[k][m].replace("\"","")
                else:
                    for m in range(0, len(value[k])):
                        value[k][m] = value[k][m].replace("\"","")
    elif type(value) == type([]):
        for k in range(0,len(value)):
            if type(value[k]) != type({}):
                value[k] = value[k].replace("\"","")
            else:
                keys_op = getattr(value[k], "keys", None)
                if callable(keys_op):
                    for m in value[k].keys():
                        value[k][m] = value[k][m].replace("\"","")
                else:
                    for m in range(0, len(value[k])):
                        value[k][m] = value[k][m].replace("\"","")
    elif type(value) == type(" ") and value != "":
        value = value.replace("\"","")

    if variable_exists(name) and value != None:
        if DEBUG:
            print "%s exists checking permissions for %s" % (name, CONTEXT)

        has_write =  has_delegation(name, CONTEXT, 'W')
        has_append = has_delegation(name, CONTEXT, 'A')
        if from_here == "append" and has_append :
            has_permission = 1
        #elif from_here == "append" and has_write:
        #    has_permission = 1
        elif from_here != "append" and has_write:
            has_permission = 1
        else:
            has_permission = 0
            
        if not has_permission:
            if DEBUG:
                print "%s cannot write to %s" % (CONTEXT, name)
            OUTPUT_ROWS.append("DENIED")
            flush_changes()
            return False
        access_perms = lookup_variable_access_perms(name)

    else:
        if DEBUG:
            print "Creating global variable %s with RWAD permissions for %s" % (name, CONTEXT)
        access_perms[CONTEXT] = "RWAD"  # Read, Write, Append, Delegate for creator
        if DEBUG:
            print "Access after creating", access_perms

            
    global_variable_change_buffer[name] = {"value":value,"access_control":access_perms}
    debug_status_report("add_global")
    return True
    
def add_local(name, value):
    global OUTPUT_ROWS
    global DEBUG
    global CONTEXT
    global local_variable_change_buffer
    global global_variable_change_buffer
    global principal_change_buffer
    access_perms = {}
    if DEBUG:
        print "adding local of type: %s" % type(value)

    if type(value) == type({}):
        for k in value:
            if type(value[k]) != type({}):
                value[k] = value[k].replace("\"","")
            else:
                keys_op = getattr(value[k], "keys", None)
                if callable(keys_op):
                    for m in value[k].keys():
                        value[k][m] = value[k][m].replace("\"","")
                else:
                    for m in range(0, len(value[k])):
                        value[k][m] = value[k][m].replace("\"","")
    elif type(value) == type([]):
        for k in range(0,len(value)):
            if type(value[k]) != type({}):
                value[k] = value[k].replace("\"","")
            else:
                keys_op = getattr(value[k], "keys", None)
                if callable(keys_op):
                    for m in value[k].keys():
                        value[k][m] = value[k][m].replace("\"","")
                else:
                    for m in range(0, len(value[k])):
                        value[k][m] = value[k][m].replace("\"","")
    elif "\"" in str(value):
        value = value.replace("\"","")
    if variable_exists(name) and value != None:
        if not has_delegation(name, CONTEXT, 'W'):
            OUTPUT_ROWS.append("DENIED")
            flush_changes()
            return
        access_perms = lookup_variable_access_perms(name)
    else:
        access_perms[CONTEXT] = "RWAD"  # Read, Write, Append, Delegate for creator
    local_variable_change_buffer[name] = {"value":value,"access_control":access_perms}
                        
### make sure the principal running the prog exists.
def validate_context(principal,password):
    global OUTPUT_ROWS
    global DEBUG
    global CONTEXT
    global local_variable_change_buffer
    global global_variable_change_buffer
    global principal_change_buffer
    global principal_table
    
    #print principal_table
    if "\"" in password:
        password = password.replace("\"","")
    if principal is "anyone":
        CONTEXT = "anyone"
    else:
        if principal not in principal_change_buffer.keys() and principal not in principal_table.keys():
            print "%s not in either table" % principal
            print principal_table
            print principal_change_buffer
            OUTPUT_ROWS.append("DENIED")
            return False
        if principal in principal_table:
            the_table = principal_table
        else:
            the_table = principal_change_buffer
        if password != the_table[principal]:
            print "pass incorrect %s %s" % (password, )
            OUTPUT_ROWS.append("DENIED")
            return False
        if DEBUG:
            print "Changing context to %s" % str(principal)
            print "+++++++++++++++++++++"
        CONTEXT = principal
    return True
        
        
        
### definition of program syntax parsing code ###
class symbol_base(object):

    id = None
    value = None
    first = second = third = None

    def nud(self):
        raise SyntaxError("Syntax error (%r)." % self.id)

    def led(self, left):
        raise SyntaxError("Unknown operator (%r)." % self.id)

    def __repr__(self):
        if self.id == "(name)" or self.id == "(literal)":
            return "(%s %s)" % (self.id[1:-1], self.value)
        out = [self.id, self.first, self.second, self.third]
        out = map(str, filter(None, out))
        return "(" + " ".join(out) + ")"

def symbol(id, bp=0):
    try:
        s = symbol_table[id]
    except KeyError:
        class s(symbol_base):
            pass
        s.__name__ = "symbol-" + id # for debugging
        s.id = id
        s.value = None
        s.lbp = bp
        symbol_table[id] = s
    else:
        s.lbp = max(bp, s.lbp)
    return s

# helpers

def infix(id, bp):
    def led(self, left):
        self.first = left
        self.second = expression(bp)
        return self
    symbol(id, bp).led = led

def infix_r(id, bp):
    def led(self, left):
        self.first = left
        self.second = expression(bp-1)
        return self
    symbol(id, bp).led = led

def prefix(id, bp):
    def nud(self):
        self.first = expression(bp)
        return self
    symbol(id).nud = nud

def advance(id=None):
    global token
    if id and token.id != id:
        raise SyntaxError("Expected %r" % id)
    token = next()

def method(s):
    # decorator
    assert issubclass(s, symbol_base)
    def bind(fn):
        setattr(s, fn.__name__, fn)
    return bind

# BIBIFI expression program syntax
prefix("create", 50);
prefix("as", 150);
symbol("change"); 
symbol("append", 150);
symbol("set", 150); 
symbol("local");
symbol("foreach", 150);
symbol("delete");
symbol("default", 20);
symbol("do", 20);
symbol("exit"); symbol("return");
infix("is", 60); 
infix("to", 60);

infix("delegation", 60);
infix("delegator", 60);
infix("->", 60)
symbol("replacewith", 80);

# General language constructs for expressions
symbol("if", 20); symbol("else"); 

infix_r("or", 30); infix_r("and", 40); prefix("not", 50)
symbol("**")

infix("in", 60); infix("not", 60) # not in
infix("<", 60); infix("<=", 60)
infix(">", 60); infix(">=", 60)
infix("<>", 60); infix("!=", 60); infix("==", 60)
infix("|", 70); infix("^", 80); infix("&", 90)
infix("<<", 100); infix(">>", 100)
infix("+", 110); infix("-", 110)
infix("*", 120); infix("/", 120); infix("//", 120)
infix("%", 120)
# infix("{", 120) do we need this?
prefix("-", 130); prefix("+", 130); prefix("~", 130)
symbol("[");
symbol(".", 150);  symbol("(", 150)
symbol(":"); symbol("=")
symbol("(name)").nud = lambda self: self



symbol("(literal)").nud = lambda self: self


symbol("(end)")

symbol("]")
symbol("}")
symbol("{") # ????? do we need this one also?
symbol(")"); symbol(",")


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
            try:
                advance(",")
            except:
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
    try:
        advance(")")
    except:
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return
    if not self.first or comma:
        return self # tuple
    else:
        return self.first[0]

@method(symbol("do"))
def led(self, left):
    self.first = left
    t = token.id
    out = [t]
    t = True
    while t:
        try:
            t = next()
            if t.id in ["(name)","(literal)"]:
                out.append(t.value)
            else:
                out.append(t.id)
        except Exception as e:
            t = False
    cmd_str = " ".join(out)
    self.second = cmd_str
    parse(cmd_str)  
    return self

@method(symbol("in"))
def nud(self):
    self.first = token
    self.second = expression(300)
    return self

@method(symbol("if"))
def led(self, left):
    self.first = left
    self.second = expression()
    try:
        advance("else")
    except:
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return
    self.third = expression()
    return self

@method(symbol("foreach"))
def nud(self):
    # global DEBUG
    record_list = []
    tmp_varname = token.value

    if variable_exists(tmp_varname):
        if tmp_varname not in local_variable_change_buffer:
            if DEBUG:
                print "Global Variable %s already exists.Cant declare local" % tmp_varname
            OUTPUT_ROWS.append("FAILED")
            flush_changes()
            return
    
    advance()
    advance('in')
    look_in = token.value

    if not variable_exists(look_in):
        if DEBUG:
            print "Variable %s doesn't exists." % look_in
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return

    vcontent = lookup_variable_value(look_in)

    
    if DEBUG:
        print "Variable %s contents: "% look_in, vcontent
    if not vcontent:
        if DEBUG:
            print "Couldnt lookup value for %s." % look_in
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return
    if type(vcontent) != type([]):
        if DEBUG:
            print "Variable %s not a list." % look_in
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return
    # determine if there is a subfield in replace scenario
    add_local(tmp_varname,vcontent)
    mainvar = expression(300).value

    advance()
    
    send_me = 300
    
    exp = expression(send_me) # grabs the next sub-expression

    #print "Expression foreach: ", exp

    # analyze 
    
    if type(exp) == type({}): # we are replacing with each part of 'x'
                              # with a record
        need_replacement = 0
        for k in exp.keys():
            if "\"" in exp[k]:
                need_replacement = 1
            if type(exp[k]) != type(" "):
                if DEBUG:
                    print "%s cannot init a non-string var" % look_in
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
        # iterate
        new_value = [] # create a new list
        for r in vcontent:
            local_new = dict(exp)
            if (need_replacement):
                for k in exp.keys():
                    if "\"" not in exp[k]: # this is a variable name
                        local_new[k] = r

            try:
                new_value.append(local_new)
            except:
                if DEBUG:
                    print "field %s not in item " % look_in, vcontent
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
        # new_value = exp
    elif token.id == ".":
        advance()
        field = token.value # the subfield of the record
        new_value = []
        if DEBUG:
            print "Found subfield to replace with"
        for r in vcontent:
            try:
                new_value.append(r[field])
            except:
                if DEBUG:
                    print "field %s not in item " % look_in, vcontent
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
    else:
        if DEBUG:
            print "No Sub-field Grabbing whole entries"
        advance()

    if DEBUG:
        print "Setting %s to " % look_in, new_value
    if look_in in local_variable_change_buffer.keys():
        var_table = "l"
    else:
        var_table = "g"
    
    if var_table == "l":
        add_local(look_in,new_value)
    else:
        add_global(look_in,new_value)
    self.first = tmp_varname
    self.second = look_in
    self.third = new_value
    OUTPUT_ROWS.append("FOREACH")
    return self 

# ==>1
@method(symbol("."))
def led(self, left):  
    if token.id != "(name)":
        SyntaxError("Expected an attribute name.")
    #vname = left.first
    vname = left.value
    #field = left.second
    field = token.value

    #print "DOT LOOKUP %s.%s" % (vname, field)
    record = lookup_variable_value(vname, field)
    #print "Got ", record
    if record:
        self.first = vname
        self.second = record
    return self


@method(symbol("("))
def led(self, left):
    self.first = left
    self.second = []
    if token.id != ")":
        while 1:
            self.second.append(expression())
            if token.id != ",":
                break
            try:
                advance(",")
            except:
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
    try:
        advance(")")
    except:
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return
    return self

@method(symbol("exit"))
def nud(self):
    global DEBUG
    success = False
    if CONTEXT == "admin":
        if DEBUG:
            print "Exit routines" #
        OUTPUT_ROWS.append("EXITING")
        success = True
    else:
        if DEBUG:
            print "Silly %s exits for admins" % CONTEXT
        OUTPUT_ROWS.append("DENIED")
    return flush_changes(success)

def argument_list(list):
    while 1:
        if token.id != "(name)":
            SyntaxError("Expected an argument name.")
        list.append(token)
        advance()
        if token.id == "=":
            advance()
            list.append(expression())
        else:
            list.append(None)
        if token.id != ",":
            break
        try:
            advance(",")
        except:
            OUTPUT_ROWS.append("FAILED")
            flush_changes()
            return
def constant(id):
    @method(symbol(id))
    def nud(self):
        self.id = "(literal)"
        self.value = id
        return self

# Constants some basics for language support
constant("None")
constant("True")
constant("False")
# and the rights principals may hold
constant("read")
constant("write")
constant("delegate")

# multitoken operators
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

@method(symbol("create"))
def nud(self):
    debug_status_report("create principal #1")
    if token.value == "principal":
        self.id = "create principal"
        self.first = next().value
        self.second = next().value
        debug_status_report("create principal #2")
        print_token(self)
        if add_principal(self.first,self.second):
            OUTPUT_ROWS.append("CREATE_PRINCIPAL")

    debug_status_report("create principal #3")
    return self

@method(symbol("as"))
def nud(self):
    if token.value == "principal":
        self.id = "as principal"
        self.first = next().value
        advance() 
        password = next()
        if hasattr(password, "id"):
            if password.id == "do":
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
        self.second = password.value
        if validate_context(self.first,self.second):
            CONTEXT = self.first
            # advance()
        else:
            OUTPUT_ROWS.append("DENIED")  
            flush_changes()
            return
    else:        
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return
    return self

@method(symbol("append"))
def nud(self):
    if token.id == "to":
        advance()
        self.first = token.value
        advance()
        advance()
        self.second = expression()
        if not variable_exists(self.first):
            OUTPUT_ROWS.append("FAILED")
            return
        
        curval = lookup_variable_value(self.first)

        debug_status_report("append")
        
        #oe
        
        adding_a_variable = 0
        adding_a_constant = 0
        adding_a_field    = 0
        # want to find out if we have to add a variable to curval,
        # or we are adding a constant
        if (hasattr(self.second,"id") and self.second.id == "(name)") :
            # we have a variable
            adding_a_variable = 1
            adding_a_field    = 0
            adding_a_constant = 0
        elif (hasattr(self.second,"id") and self.second.id == ".") : # adding a record field value
            adding_a_variable = 0
            adding_a_field    = 1
            adding_a_constant = 0
        else:
            # if this is not a name of a variable or a field, then we are adding a constant
            adding_a_variable = 0
            adding_a_field    = 0
            adding_a_constant = 1

        if (adding_a_variable == 1) :
            add_val = lookup_variable_value(self.second.value)
        if (adding_a_field == 1) :
            add_val = self.second.second
        if (adding_a_constant == 1):        
            add_val = self.second

        # find if we are adding a string, set add_val to this string value
        if hasattr(add_val,'id') :
            if add_val.id == "(literal)" : # meaning - we are adding a string
                add_val = add_val.value

        # note - this is not used anywhere
        curperms = lookup_variable_access_perms(self.first)
         
        nextval = curval

        if type(curval) != type([]):
            ## MUST append to a list !!
            OUTPUT_ROWS.append("FAILED")
            flush_changes()
            return
        elif type(curval) == type([]): # of course ... but leave it lie that
            if type(add_val) == type([]):
                for i in range(0,len(add_val)):
                    nextval.append(add_val[i])
            elif type(add_val) == type({}):
                nextval.append(add_val)
            elif type(add_val) == type(" "): # we must be adding a string then, right?
                nextval.append(add_val)
            else: # not corrct type found ...
                if DEBUG:
                    print "append to couldnt determine what to do with ", type(curval)
                    OUTPUT_ROWS.append("FAILED")
                    flush_changes()
                    return

        if self.first in local_variable_change_buffer.keys():
             var_table = "l"
        else:
            var_table = "g"
        if var_table == "l":
            add_local(self.first,nextval)
        else:
            add_global(self.first,nextval,"append")
    OUTPUT_ROWS.append("APPEND")
    return self


@method(symbol("change"))
def nud(self):
    if token.value == "password":
        self.first = next().value
        self.second = next().value
        if change_principal_password(self.first, self.second):
            OUTPUT_ROWS.append("CHANGE_PASSWORD")
        self.id = "change password"
    return self

@method(symbol("local"))
def nud(self):
    lvname = token.value
    advance()
    print "Adding %s as local" % lvname
    advance('=')
    
    val = expression(300)

    print "%s to have the value of %s" % (lvname , val.value)
    

    if hasattr(val,'id'): 
        if val.id == "(literal)": # setting the local to a constand
            value = val.value
        elif val.id == "(name)": # setting the local to a variable
            value = lookup_variable_value(val.value)
        if value:
            add_local(lvname, value)
    else:
        add_local(lvname, val.value)
    OUTPUT_ROWS.append("LOCAL")
    return self
            
@method(symbol("set"))
def nud(self):
    debug_status_report("set #1")

    if token.id == "delegation":
        print_token(self)
        self.id = "set delegation"
        advance()
        varname = token.value
        advance()
        whos_delegating = token.value
        advance()
        level = token.id
        advance()
        advance()
        advance()
        delegate_to = token.value
        advance()
        w = False
        if level == "read":
            w = add_delegation(varname, delegate_to, whos_delegating, "R")
        elif level == "write":
            w = add_delegation(varname, delegate_to, whos_delegating, "W")
        elif level == "append":
            w = add_delegation(varname, delegate_to, whos_delegating, "A")
        elif level == "delegate":
            w = add_delegation(varname, delegate_to, whos_delegating, "D")
        if w:
            OUTPUT_ROWS.append("SET_DELEGATION")

        debug_status_report("set #2")
        return 
    
    elif token.id == "(name)":
        # setting a variable to a value. Value maybe a literal, expression, or record type object
        self.first = token.value
        if self.first in reserved_words:
            print "%s is a reserved word" % self.first
            OUTPUT_ROWS.append("FAILED")
            flush_changes()
            return
        advance()
        advance('=')
        expr = []
        self.second = expression()

        debug_status_report("set #3")
            
        w = False
        if hasattr(self.second, "value"):
            if DEBUG:
                print "SETTING %s to %s" % (self.first, str(self.second.value))
            if add_global(self.first, self.second.value):
                if DEBUG:
                    print "SET %s to %s" % (self.first, str(self.second.value))
                OUTPUT_ROWS.append("SET")
            else:
                if DEBUG:
                    print "SET w/ value failed %s = %s" % (self.first, self.second.value)
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
        else:
            if add_global(self.first, self.second):
                if DEBUG:
                    print "SET %s to %s" % (self.first, self.second)
                OUTPUT_ROWS.append("SET")
            else:
                if DEBUG:
                    print "SET w/o value failed %s = %s" % (self.first, self.second)
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
    else:
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return

    debug_status_report("set #3")

    return self

@method(symbol("delete"))
def nud(self):
    debug_status_report("delete #1")
    
    if token.id == "delegation":
        advance()
        self.id = "delete delegation"
    self.first = token.value # variable being effected
    var_name = self.first
    advance()
    self.second = token.value
    for_who = CONTEXT
    principal = self.second
    advance()
    level = token.id
    advance()
    advance()
    advance()
    for_principal = token.value
    if level == "read":
        delegation = "R"
    elif level == "write":
        delegation = "W"
    elif level == "append":
        delegation = "A"
    elif level == "delegate":
        delegation = "D"
    if delete_delegation(var_name, principal, for_principal, delegation):
        OUTPUT_ROWS.append("DELETE_DELEGATION")
        
    debug_status_report("delete #2")
    return self

@method(symbol("default"))
def nud(self,):
    if token.id == "delegator":
        advance()
        self.id = "default delegator"
    self.first = next()
    
    if CONTEXT == "admin":
        if principal_exists(self.first.value):
            DEFAULT_DELGATOR = self.first.value
            OUTPUT_ROWS.append("DEFAULT_DELEGATOR")
        else:
            OUTPUT_ROWS.append("FAILED")
            flush_changes(False)
            return
    else:
        OUTPUT_ROWS.append("DENIED")
        flush_changes(False)
        return
    debug_status_report("default delegator #1")
    return self

# at the start of a line this should indicate the next token is also * and
# we have reached the end of the program.
@method(symbol("**"))
def nud(self):
    global principal_table
    global global_variable_table
    
    if token.id == "*":
        advance()
        success = True
        if "FAILED" in OUTPUT_ROWS or "DENIED" in OUTPUT_ROWS:
            success = False
        self.id = "(end)"
        flush_changes(success)

        if DEBUG:
            print "DEBUG: Pricipal Table: %s" % principal_table
            print "DEBUG: Global Variable Table %s" % global_variable_table
            print 
    return self

# when not at the start, if next symbol is * then this is the end of 
# the program otherwise this is an exponentiation operation
@method(symbol("**"))
def led(self, left):
    if token.id == "*":
        OUTPUT_ROWS.append("FAILED")
        flush_changes(False)
        return
    else:
        self.first = left
        if hasattr(left, 'id'):
            if left.id == "(name)":
                left_val = lookup_variable_value(left.value)
                if not left_val:
                    return 
            else:
                left_val = left.value
        else:
            left_val = left
        self.second = expression(40)
        try:
            if self.second.id == "(literal)":
                return float(left_val)+float(self.second.value)
            elif self.second.id == "(name)":
                right_val = lookup_variable_value(self.second.value)
            return float(left_val)+float(right_val)
        except Exception as e:
            return float(left_val)+float(self.second)

@method(symbol("return"))
def nud(self):
    debug_status_report("return")
    print_token(self)
    
    if token.value == "\"\"":
        OUTPUT_ROWS.append("RETURNING \"\"")
        return self
    self.first = token.value
    if DEBUG:
        print "Returning with token: ", self.first
    exp = expression(200)
    val = ''
    if hasattr(exp,'id'):
        if DEBUG:
            print "Returning Expression: ", exp
        vname = exp.value
        
        if token.id != "(end)":
            nxt = next()
            self.second = nxt.value
            if DEBUG:
                print "Returning Sub-field: ", self.second
            if nxt.id == "(literal)":
                index = int(nxt.value)
                if DEBUG:
                    print "Looking up (literal) %s index: " % vname, index
                val = lookup_variable_value(vname, index)
                if not val:
                    val = nxt.value
                if DEBUG:
                    print "Got: ", val
                OUTPUT_ROWS.append("RETURNING %s" % str(val))
                advance()
            elif nxt.id == "(name)":
                index = str(nxt.value)
                if DEBUG:
                    print "Looking up (name) index: ", index
                val = lookup_variable_value(vname, index)
                if val:
                    if DEBUG:
                        print "Got: ", val
                    OUTPUT_ROWS.append("RETURNING %s" % json.dumps(val))
                else:
                    return
                advance()
        else:
            if DEBUG:
                print "No Sub Fields Present for: ", exp.value
            if "\"" in exp.value:
                if DEBUG:
                    print "Cleaning up string for return: %s" % exp.value
                val = exp.value.replace("\"","")
            else:
                val = lookup_variable_value(exp.value)
            if val:
                if DEBUG:
                    print "Got: ", val
                OUTPUT_ROWS.append("RETURNING %s" % json.dumps(val))
            elif DEBUG:
                print "Failed to lookup: ", exp.value
    return


# displays

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
            try:
                advance(",")
            except:
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
    try:
        advance(")")
    except:
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return
    if not self.first or comma:
        return self # tuple
    else:
        return self.first[0]

symbol("]")
@method(symbol("["))
def nud(self):
    record_item = []
    if token.id != "]":
        while 1:
            if token.id == "]":
                break
            v = expression()
            if v.id == "(name)":
                v = lookup_variable_value(v.value)
            else:
                v = v.value
            record_item.append(v)
            if token.id != ",":
                break
            try:
                advance(",")
            except:
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
    try:
        advance("]")
    except:
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return
    return record_item

# symbol("}") WHY WAS IT HERE?

@method(symbol("{"))
def nud(self):
    record_item = {}
    if token.id != "}":
        while 1:
            if token.id == "}":
                break
            k = expression().value
            try:
                advance("=")
            except:
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
            v = expression()
            # oe: replace with the content only in case is a string
            if v.id == "(name)":
                v1 = lookup_variable_value(v.value)
                if type(v1) != type(' '): # meaning - not a string
                    v = v.value
                else:
                    v = v1.value
            else:
                v = v.value

            record_item[k] = v
            if token.id != ",":
                break
            try:
                advance(",")
            except:
                OUTPUT_ROWS.append("FAILED")
                flush_changes()
                return
    try:
        advance("}")
    except:
        OUTPUT_ROWS.append("FAILED")
        flush_changes()
        return
    return record_item

# python tokenizer

def tokenize_program(program):
    import tokenize
    from cStringIO import StringIO
    program = program.strip().replace("\n", "")
    type_map = {
        tokenize.NUMBER: "(literal)",
        tokenize.STRING: "(literal)",
        tokenize.OP: "(operator)",
        tokenize.NAME: "(name)"
        }
    for t in tokenize.generate_tokens(StringIO(program).next):
        try:
            yield type_map[t[0]], t[1]
        except KeyError:
            if t[0] == tokenize.NL:
                continue
            if t[0] == tokenize.ENDMARKER:
                break
            else:
                OUTPUT_ROWS.append("FAILED")
                flush_changes(False)
                return
    yield "(end)", "(end)"

def tokenize(program):
    global OUTPUT_ROWS
    if isinstance(program, list):
        source = program
    else:
        source = tokenize_program(program)
    for id, value in source:
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
                OUTPUT_ROWS.append("FAILED")
                flush_changes(False)
                return
        yield s

# parser engine
def expression(rbp=0):
    global token

    t = token
    token = next()

    left = t.nud()
        
    while rbp < token.lbp:
        t = token
        token = next()
        left = t.led(left)


    return left

def parse_line(program):
    global token, next
    try:
        next = tokenize(program).next
        token = next()
        return expression()
    except:
        OUTPUT_ROWS.append('FAILED')
        flush_changes(False)
        return
    
def parse(program):
    global token, next, OUTPUT_ROWS, CONTEXT, SHUTDOWN
    lines = program.split("\n")
    expressions = []
    for line in lines:
        if "DENIED" in OUTPUT_ROWS:
            if DEBUG:
                print "Security Violation: Stopping."
            OUTPUT_ROWS = []
            return {"status":"DENIED"}
        elif "FAILED" in OUTPUT_ROWS:
            if DEBUG:
                print "Program Failure: Stopping."
            OUTPUT_ROWS = []
            return {"status":"FAILED"}
        if DEBUG:
            print ">> Processing: %s" % line.strip()
        expressions.append(parse_line(line))
    if DEBUG:
        print "Adding ROWS to Output: ", OUTPUT_ROWS
    ret_json = {}
    out = []
    for stat in OUTPUT_ROWS:
        ret_json = {}
        if DEBUG:
            print "Adding %s to Output" % stat
        if "RETURNING" in stat:
            if DEBUG:
                print "Found Return call"
            ret_json["status"] = "RETURNING"
            tk = stat.split(" ")
            val = ' '.join(tk[1:])
            ret_json["output"] = val
            out.append(ret_json)
            
            if DEBUG:
                print "Return %s" % val
                print "Current out after return ", out
                
        elif stat == "EXITING":
            ret_json["status"] = stat
            SHUTDOWN = True
            out.append(ret_json)

        else :
            ret_json["status"] = stat
            out.append(ret_json)

        #out.append(ret_json)
    OUTPUT_ROWS = []
    if DEBUG:
        print "\nFinal Output \n", out
        print "EXPRESSION DEBUG: ", expressions
        print
    return out

def test(program):
    global DEBUG
    DEBUG = True
    lines = program.split("\n")
    print "Processing %d lines" % len(lines)
    print ">>>", program
    return parse(program)


#
# --------------------------------------------------------
# SERVER
# --------------------------------------------------------


import socket # Socket for server
import signal # sigterm - server startup and shutdown
import sys # exit etc

### Check SIGTERM and exit with the correct return code - see Server startup and shutdown
def SIGTERMhandler(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, SIGTERMhandler)

ADMIN = ''
ERRORKO = False
HOST = None # Symbolic name meaning all available interfaces

def deflector_shield(testprog):
    global ERRORKO
    testsplit = testprog.lstrip().rstrip().split('\n')
    # Remove comment
    newline = []
    for line in testsplit:
        if line.count('//') > 0:
            if line [0:2] != '//': # comment inside the line - drop line that begins with //
                line = line.split('//')[0]  
                newline.append(' '.join(line.split())) # eliminate all not needed spaces
        else:
            newline.append(' '.join(line.split())) # eliminate all not needed spaces
    # check first word for fast exit
    grammar = ["append", "as", "change", "create", "default", "delete", "exit", "local", "foreach", "return", "set", "***"]
    for line in newline:
        if len(line) == 0:
            ERRORKO = True # find an empty lines
        else: 
            row = line.split()
            #print "row = ", row[0] # for debug
            if row[0] not in grammar:
                ERRORKO = True
            else:
                if row[0] == "set" and len(row) >= 4 and row[2] == "=":
                    if len(row[3]) > 65535:
                        ERRORKO = True
    return newline

### Sanitize command line
#print 'Number of arguments:', len(sys.argv), 'arguments.' # for debug
#print 'Argument List:', str(sys.argv) # for debug
# no argument
if len(sys.argv) < 2:
    sys.exit(255)
# lenght of argument greater than 4096 or more than 2 argument
for i in range(1, len(sys.argv)):
    len_sys_argv_i = len(sys.argv[i])
    if i == 1: # port number
        if sys.argv[i][0]=='0': # port number begins with 0
            sys.exit(255)
    if i == 2: # password for admin
        ADMIN = str(sys.argv[i])
        principal_table["admin"] = str(sys.argv[i])
        #print "admin =", ADMIN for debug
    if len_sys_argv_i > 4096 or i > 2:
        sys.exit(255)
# port integer and between 1024 and 65535
if not sys.argv[1].isdigit():
    sys.exit(255)
else:
    PORT = int(sys.argv[1])
    if (PORT < 1024) or (PORT > 65535):
        sys.exit(255)

### Initialize socket
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(0) # one connectionat a time - see Overview
    except KeyboardInterrupt:
        sys.exit(0)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    # print 'could not open socket' # for debug
    sys.exit(63) # Port taken - see Server startup and shutdown

### Accept and close connections
while not SHUTDOWN:
    try:
        conn, addr = s.accept()
        conn.settimeout(None) # timeout 30 sec if not ***
        #print 'Connected by', addr # for debug
        progline = []
        cleanprogline = []
        prog = ""
        returnparser = ""
        endcon = True
        while endcon:
            try:
                data = conn.recv(4096) 
                conn.settimeout(30) # timeout
                if data.find("***") != -1: # ADDED IGNORE AFTER ***
                    conn.settimeout(None)
                    #progline.append(data.lstrip().strip("\n")) # strip leading spaces and newlines
                    #progline.append(data.lstrip()) # strip leading spaces 
                    progline.append(data)
                    #cleanprogline = (deflector_shield("\n".join(progline)))
                    cleanprogline = (deflector_shield("".join(progline))) # MR
                    prog = "\n".join(cleanprogline)
                    if len(prog) > 1000000 or ERRORKO:
                        #print "lenght progr: ", len(prog), " errorko= ", ERRORKO # for debug
                        data = "{\"status\": \"FAILED\"}\n"
                        ERRORKO = False
                    else:
                        #print "call parser program: ", prog # for debug
                        returnparser = parse(prog)
                        data = ''
                        if len (returnparser) > 1:
                            if type(returnparser) == type([]):
                                for ret in returnparser:
                                    data += str(ret).replace("'", '"').replace('""', '"') + "\n"
                            else:
                                data = str(returnparser).replace("'", '"').replace('""', '"') + "\n"
                        else:
                            data = str(returnparser).replace("'", '"').replace('""', '"').replace('[','').replace(']','') + "\n"
                    data = data.replace("\"[","[").replace("]\"","]")
                    data = data.replace("\"{","{").replace("}\"","}")
                    
                    progline = []
                    cleanprogline = []
                    print "RETURNING: ", data
                    conn.send(data)
                    endcon = False # data ended, close connection
                    if SHUTDOWN: 
                        conn.close()
                        sys.exit(0) # - see Command (<cmd>)
                else:
                    progline.append(data) # single rows input
            except socket.timeout:
                data = '{"status": "TIMEOUT"}\n'
                conn.send(data)
                progline = []
                cleanprogline = []
                conn.settimeout(None)
                endcon = False
            except KeyboardInterrupt:
                conn.close()
                sys.exit(0) # - see Server startup and shutdown
        conn.close()
    except KeyboardInterrupt:
        sys.exit(0) # - see Server startup and shutdown
sys.exit(0) # - see Command (<cmd>)


