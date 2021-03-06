from utils import Enum
import sys


class Scanner(object):
    token = {
        'code': False,
        'lex': "",
        'ln': 1,
        'cl': 1,
        'qtd': -1
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

    def cont_line(self):
        if self.c == '\n' or self.c == '\r':
            self.token['cl'] = 1
            self.token['ln'] += 1
        elif self.c == '\t':
            self.token['cl'] += 4
        else:
            self.token['cl'] += 1

    def is_valid(self):
        if self.is_blank() or self.c.isalpha() or self.c == '_' or self.c.isdigit() or self.c == '<' or self.c == '>' or self.c == '<=' or self.c == '>=' or self.c == '==' or self.c == '!=' or self.c == '+' or self.c == '-' or self.c == '*' or self.c == '/' or self.c == '=' or self.c == '(' or self.c == ')' or self.c == '{' or self.c == '}' or self.c == ',' or self.c == ';' or self.is_reserved_word() or self.c == '\'' or self.c == '.' or self.c == '':
            response = True
        else:
            response = False
        return response

    def print_error(self, msg):
        self.push_lex()
        print("ERRO na linha {0}, coluna {1}, ultimo token lido '{2}': {3}".format(self.token['ln'], self.token['cl'], self.token['lex'], msg))
        sys.exit(1)

    def is_special(self):
        if self.c == '(':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            self.create_token(Enum.Tparenteses_opn)
            response = True
        elif self.c == ')':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            self.create_token(Enum.Tparenteses_cls)
            response = True
        elif self.c == '{':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            self.create_token(Enum.Tchaves_opn)
            response = True
        elif self.c == '}':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            self.create_token(Enum.Tchaves_cls)
            response = True
        elif self.c == ';':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            self.create_token(Enum.Tponto_virgula)
            response = True
        elif self.c == ',':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            self.create_token(Enum.Tvirgula)
            response = True
        else:
            response = False
        return response

    @property
    def comment(self):
        flag = True
        if self.c == '/':  # One-line Comment
            self.cont_line()
            self.c = self.get_c()
            while self.c != "\n":  # Line-break
                self.cont_line()
                self.c = self.get_c()
            response = True
        elif self.c == '*':  # Multi
            self.cont_line()
            self.c = self.get_c()
            while flag:
                if self.c == '*':  # Multiline Comment
                    self.cont_line()
                    self.c = self.get_c()
                    if self.c == '/':
                        self.cont_line()
                        self.c = self.get_c()
                        response = True
                        flag = False
                elif not self.c: # End of File
                    self.print_error("Comentario multilinha nao fechado!")
                else:
                    self.cont_line()
                    self.c = self.get_c()
        else:
            response = False
        return response

    @property
    def is_op_arithmetic(self):
        if self.c == '+':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            self.create_token(Enum.Tsoma)
            response = True
        elif self.c == '-':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            self.create_token(Enum.Tsub)
            response = True
        elif self.c == '*':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            self.create_token(Enum.Tmult)
            response = True
        elif self.c == '/':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            if not self.comment:  # Check if 'is Comment
                self.create_token(Enum.Tdivi)
                response = True
            else:
                self.token['lex'] = ''
                response = False
        elif self.c == '=':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            if self.c == '=':
                response = False
            else:
                self.create_token(Enum.Tatrib)
                response = True
        else:
            response = False
        return response

    def is_op_relational(self):
        if self.c == '>':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            if self.c == '=':
                self.push_lex()
                self.cont_line()
                self.c = self.get_c()
                self.create_token(Enum.Tmaior_igual)
            else:
                self.create_token(Enum.Tmaior)
            response = True
        elif self.c == '<':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            if self.c == '=':
                self.push_lex()
                self.cont_line()
                self.c = self.get_c()
                self.create_token(Enum.Tmenor_igual)
            else:
                self.create_token(Enum.Tmenor)
            response = True
        elif self.c == '=':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            self.create_token(Enum.Tigual)
            response = True
        elif self.c == '!':
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            if self.c == '=':
                self.push_lex()
                self.cont_line()
                self.c = self.get_c()
                self.create_token(Enum.Tdiferente)
            else:
                self.push_lex()
                self.cont_line()
                self.print_error("Operador Relacional Diferente mal formado.")
                sys.exit()
            response = True
        else:
            response = False
        return response

    def is_reserved_word(self):
        if self.token['lex'] == 'main':
            self.create_token(Enum.Tmain)
            response = True
        elif self.token['lex'] == 'if':
            self.create_token(Enum.Tif)
            response = True
        elif self.token['lex'] == 'else':
            self.create_token(Enum.Telse)
            response = True
        elif self.token['lex'] == 'while':
            self.create_token(Enum.Twhile)
            response = True
        elif self.token['lex'] == 'do':
            self.create_token(Enum.Tdo)
            response = True
        elif self.token['lex'] == 'for':
            self.create_token(Enum.Tfor)
            response = True
        elif self.token['lex'] == 'int':
            self.create_token(Enum.Tint)
            response = True
        elif self.token['lex'] == 'float':
            self.create_token(Enum.Tfloat)
            response = True
        elif self.token['lex'] == 'char':
            self.create_token(Enum.Tchar)
            response = True
        else:
            response = False
        return response

    def verify_float(self):
        self.push_lex()
        self.cont_line()
        self.c = self.get_c()
        if self.c.isdigit():
            self.push_lex()
            self.cont_line()
            self.c = self.get_c()
            while self.c.isdigit():  # Iterate Int
                self.push_lex()
                self.cont_line()
                self.c = self.get_c()
            if self.c == '.':
                self.push_lex()
                self.print_error("Float mal formado")
            else:
                return self.create_token(Enum.Tdigfloat)
        else:
            self.push_lex()
            self.print_error("Float mal formado")

    def scan_file(self):
        self.token['lex'] = ""
        while self.c:  # Iterate the Archive
            while self.is_blank():  # Skip the blank (not tokens)
                self.cont_line()
                self.c = self.get_c()
            if self.c.isdigit():  # Digit Int
                self.push_lex()
                self.cont_line()
                self.c = self.get_c()
                while self.c.isdigit():  # Iterate while Int
                    self.push_lex()
                    self.cont_line()
                    self.c = self.get_c()
                if self.c == '.':  # Float
                    return self.verify_float()
                return self.create_token(Enum.Tdigint)
            elif self.c == '.':  # Float
                return self.verify_float()
            elif self.is_op_arithmetic:  # Arithmetic Operator
                return self.token
            elif self.c.isalpha() or self.c == '_':  # identifier (Letters or _ ) Or Reserved Word
                self.push_lex()
                self.cont_line()
                self.c = self.get_c()
                while self.c.isalnum() or self.c == '_':  # (Alphanumeric or _ )
                    self.push_lex()
                    self.cont_line()
                    self.c = self.get_c()
                if self.is_reserved_word():  # Verify is it's a Reserved Word
                    return self.token
                else:
                    return self.create_token(Enum.Tid)
            elif self.is_op_relational():  # Relational Operator
                return self.token
            elif self.is_special():
                return self.token
            elif self.c == '\'':
                self.push_lex()
                self.cont_line()
                self.c = self.get_c()
                self.push_lex()
                self.cont_line()
                self.c = self.get_c()
                if self.c != '\'':
                    self.print_error("Caracter mal formado.")
                else:
                    self.push_lex()
                    self.cont_line()
                    self.c = self.get_c() 
                    return self.create_token(Enum.Tdigchar)
            elif not self.is_valid():
                print("Lexema: {}\nCharacter: {}".format(self.token['lex'], self.c))
                self.print_error("Token nao pertence a linguagem.")
            else:    
                self.cont_line()
                self.c = self.get_c()
        return self.create_token(Enum.Tfeof)
