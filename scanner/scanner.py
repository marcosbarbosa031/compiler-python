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

    def get_blank (self):
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
        if self.c == ' ' or self.c == '\n' or self.c == '\t' or self.c == '\r' or self.c == ';' or self.c == '=' or self.c == '!' or self.c == '+' or self.c == '-' or self.c == '*' or self.c == '/' or self.c == '>' or self.c == '<' or self.c == '<=' or self.c == '>=' or self.c == '(' or self.c == ')' or self.c == '{' or self.c == '}' or not self.c:
            response = True
        else:
            response = False
        return response

    def scan_file(self):
        self.c = self.get_c()
        self.token['lex'] = ""
        while self.c:
            # print ("token: "+self.c)
            # print ("line: "+str(self.token['ln']))
            # print ("Column: "+ str(self.token['cl']))
            # print ("\n")
            while self.is_blank():
                self.get_blank()
                self.c = self.get_c()
            if self.is_digit():
                self.push_lex()
                self.get_blank()
                self.c = self.get_c()
                while self.is_digit():
                    self.push_lex()
                    self.get_blank()
                    self.c = self.get_c()
                if self.is_valid():
                    return self.create_token(Enum.Tdigint)
            
            self.get_blank()
            self.c = self.get_c()
        # print("Lexema: "+ self.token['lex'])
        

                


