from utils.enum import Enum


class Scanner(object):
    token = {
        'code': False,
        'lex': "",
        'ln': 1,
        'cl': 1
    }

    def __init__(self, arq):
        self.arq = arq

    def get_c(self):
        return self.arq.read(1)

    def create_token(self, code, lex):
        self.token['code'] = code
        self.token['lex'] = lex
        return self.token

    def scan_file(self):
        c = self.get_c()
        while c != '}':
            print("token = " + c)
            print("line = " + str(self.token['ln']))
            print("Column = " + str(self.token['cl']))
            c = self.get_c()
            self.token['cl'] += 1
            if c == "\n":
                self.token['ln'] += 1
                self.token['cl'] = 0


