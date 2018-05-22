
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
    
    pass