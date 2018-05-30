class SymbolTable(object):
    def __init__(self, lex, tipo, scope):
        self.lex = lex
        self.tipo = tipo
        self.scope = scope

    def getLex(self):
        return self.lex

    def getTipo(self):
        return self.tipo

    def getScope(self):
        return self.scope

    def getTable(self):
        print('{')
        print(' lex: '+ str(self.lex))
        print(' tipo: '+ str(self.tipo))
        print(' scope: '+ str(self.scope))
        print('}')

    pass