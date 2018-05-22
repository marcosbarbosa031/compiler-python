
class Stack(object):
    table = []

    def __init__ (self):
        pass
    
    def push (self, data):
        self.table.append(data)
    
    def pop (self):
        return self.table.pop()

    def printTable (self):
        for t in self.table:
            t.getTable()
    
    def top (self):
        return self.table[-1]

    def searchScope(self, symbolT):
        for t in self.table:
            if (t.scope == symbolT.scope and t.lex == symbolT.lex):
                return True
        return False
    
    def serchAll (self, symbolT):
        for t in self.table:
            if (t.lex == symbolT.lex):
                return True
        return False
    
    def isEmpty (self):
        if not self.table:
            return True
        return False
    
    def removeScope (self, scope):
        self.table = [t for t in self.table if t.scope != scope]
        # return self.table

    def clearTable (self):
        del self.table[:]

    pass