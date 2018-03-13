from utils import Enum


class Scanner(object):
    token = {
        'code': False,
        'lex': "",
        'ln': 1,
        'cl': 1
    }
    lexqtd = 1
    c = ""

    def __init__(self, arq):
        self.arq = arq

    def get_c(self):
        return self.arq.read(1)

    def create_token(self, code):
        self.token['code'] = code
        return self.token
    
    def push_lex(self):
        self.token['lex'] = self.token['lex'][:self.lexqtd] + self.c
        self.lexqtd += 1

    def is_blank(self):
        if self.c == ' ' or self.c == '\n' or self.c == '\r' or self.c == '\t':
            response = True
        else:
            response = False
        return response

    def cont_line (self):
        if self.c == '\n' or self.c == '\r':
            self.token['cl'] = 1
            self.token['ln'] += 1
        elif self.c == '\t':
            self.token['cl'] += 4
        else:
            self.token['cl'] += 1

    def is_digit(self):
        if self.c >= '0' and self.c <= '9':
            response =  True
        else:
            response = False
        return response

    def is_valid(self):
        if self.c == ' ' or self.c == '\n' or self.c == '\t' or self.c == '\r' or self.c == ';' or self.c == '=' or self.c == '!' or self.c == '+' or self.c == '-' or self.c == '*' or self.c == '/' or self.c == '>' or self.c == '<' or self.c == '<=' or self.c == '>=' or self.c == '(' or self.c == ')' or self.c == '{' or self.c == '}' or not self.c or self.is_digit() or self.c == '.':
            response = True
        else:
            response = False
        return response

    def verify_float(self):
        self.push_lex()
        self.cont_line()
        self.c = self.get_c()
        if self.is_digit():
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            while self.is_digit():  # Iterate Int
                self.push_lex()
                self.cont_line()
                self.c = self.get_c()
            return self.create_token(Enum.Tdigfloat)
        else:
            self.push_lex()
            print("Erro: Float mal formado\nLinha: {0}\nColuna: {1}\nÚltimo token Lido: {2}".format(
                self.token['ln'], self.token['cl'], self.token['lex']))
            return None

    def scan_file(self):
        self.token['lex'] = ""
        while self.c: #Iterate the Archive
            while self.is_blank(): # Skip the blank (not tokens)
                self.cont_line()
                self.c = self.get_c()
            if not self.is_valid(): # Verify if is a valid token
                self.push_lex()
                print("Erro: Token inválido\nLinha: {0}\nColuna: {1}\nÚltimo token Lido: {2}".format(
                    self.token['ln'], self.token['cl'], self.token['lex']))
                return None
            elif self.is_digit(): # Digit Int
                self.push_lex()
                self.cont_line()
                self.c = self.get_c()
                while self.is_digit(): # Iterate while Int
                    self.push_lex()
                    self.cont_line()
                    self.c = self.get_c()
                if self.c == '.': # Float
                    f = self.verify_float()
                    return f
                elif self.is_valid():
                    return self.create_token(Enum.Tdigint)
            elif self.c == '.': # Float
                f = self.verify_float()
                return f  
            elif self.c == '+':
                self.push_lex()
                self.c = self.get_c()
                return self.create_token(Enum.Tsoma)
            self.cont_line()
            self.c = self.get_c()
        # print("Lexema: "+ self.token['lex'])
        

                


