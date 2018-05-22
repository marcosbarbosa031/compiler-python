from utils import Stack
from utils import SymbolTable

s = Stack()
t = SymbolTable("8.25", "float", 0)

s.push(t)

t = SymbolTable("5", "int", 0)

s.push(t)

s.printTable()
x = s.pop()

s.printTable()


s.top().getTable()

x.getTable()
