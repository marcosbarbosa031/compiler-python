from utils import Stack
from utils import SymbolTable

s = Stack()
t = SymbolTable("8.25", "float", 0)

if(s.isEmpty()):
  print('vazio')


s.push(t)

t = SymbolTable("5", "int", 0)

s.push(t)

t = SymbolTable("a", "char", 1)

s.push(t)

print('antes')
s.printTable()

s.removeScope(0)
# s.clearTable()

print('depois')

s.printTable()