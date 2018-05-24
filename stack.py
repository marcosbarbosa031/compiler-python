from symbol_table import SymbolTable

class Stack(object):
    stack = []

    def __init__ (self):
        pass

    def push (self, lex, tipo, scope):
        self.table = SymbolTable(lex, tipo, scope)
        self.stack.append(self.table)

    def pop (self):
        return self.stack.pop()

    def printTable (self):
        for t in self.stack:
            t.getTable()
        print('---------------------------------')

    def top (self):
        return self.stack[-1]

    def searchScope(self, lex, scope):
        for t in self.stack:
            if (t.scope == scope and t.lex == lex):
                return t
        return False

    def searchAll (self, lex):
        for t in self.stack:
            if (t.lex == lex):
                return t
        return False

    def isEmpty (self):
        if not self.stack:
            return True
        return False

    def removeScope (self, scope):
        self.stack = [s for s in self.stack if s.scope != scope]
        # return self.table

    def clearTable (self):
        del self.stack[:]

    pass