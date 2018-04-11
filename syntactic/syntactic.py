from utils import Enum
from utils import PrintErr


class Syntactic(object):
    token = None

    def __init__ (self, scanner):
        self.Scanner = scanner

    def is_var_dec(self):
        if self.token['code'] == Enum.Tint or self.token['code'] == Enum.Tfloat or self.token['code'] == Enum.Tchar:
            response = True
        else:
            response = False
        return response

    def is_command(self):
        if self.token['code'] == Enum.Tid or self.token['code'] == Enum.Tchaves_opn or self.token['code'] == Enum.Twhile or self.token['code'] == Enum.Tdo or self.token['code'] == Enum.Tif:
            response = True
        else:
            response = False
        return response

    def iteration(self):
        if self.token['code'] == Enum.Twhile:                                           # while
            self.token = self.Scanner.scan_file()
            if self.token['code'] == Enum.Tparenteses_opn:                              # "("
                self.token = self.Scanner.scan_file()
                self.rel_expr()                                                         # <expr_relacional>
                if self.token['code'] == Enum.Tparenteses_cls:                          # ")"
                    self.token = self.Scanner.scan_file()
                    self.command()                                                      # <comando>
                else:
                    PrintErr.print_error(self.token, "Iteracao mal formada. Era esperado: ')'")
            else:
                PrintErr.print_error(self.token, "Iteracao mal formada. Era esperado: '('")
        elif self.token['code'] == Enum.Tdo:                                            # do
            self.token = self.Scanner.scan_file()
            self.command()                                                              # <comando>
            if self.token['code'] == Enum.Twhile:                                       # while
                self.token = self.Scanner.scan_file()
                if self.token['code'] == Enum.Tparenteses_opn:                          # "("
                    self.token = self.Scanner.scan_file()
                    self.rel_expr()                                                     # <expr_relacional>
                    if self.token['code'] == Enum.Tparenteses_cls:                      # ")" 
                        self.token = self.Scanner.scan_file()
                        if self.token['code'] == Enum.Tponto_virgula:                   # ";"
                            self.token = self.Scanner.scan_file()
                        else:
                            PrintErr.print_error(self.token, "Iteracao mal formada. Era esperado: ';'")
                    else:
                        PrintErr.print_error(self.token, "Iteracao mal formada. Era esperado: ')'")
                else:
                    PrintErr.print_error(self.token, "Iteracao mal formada. Era esperado: '('")
            else:
                PrintErr.print_error(self.token, "Iteracao mal formada. Era esperado: 'while'")
        else:
            PrintErr.print_error(self.token, "Iteracao mal formada.")

    def factor(self):
        if self.token['code'] == Enum.Tid or self.token['code'] == Enum.Tdigint or self.token['code'] == Enum.Tdigfloat or self.token['code'] == Enum.Tdigchar:
            self.token = self.Scanner.scan_file()
        elif self.token['code'] == Enum.Tparenteses_opn:
            self.token = self.Scanner.scan_file()
            self.expr()
            if self.token['code'] == Enum.Tparenteses_cls:
                self.token = self.Scanner.scan_file()
            else:
                PrintErr.print_error(self.token, "Fator mal formado. Era esperado: ')'")
        else:
            PrintErr.print_error(self.token, "Fator mal formado. Era esperado: Identificador, numero inteiro, real ou caracter")

    def arit_term(self):
        if self.token['code'] == Enum.Tmult or self.token['code'] == Enum.Tdivi:        # "*"  | "/"
            self.token = self.Scanner.scan_file()
            self.factor()
            self.arit_term()

    def term(self):
        self.factor()                                                                   # <F>
        self.arit_term()                                                                # <T'>

    def arit_expr(self):
        if self.token['code'] == Enum.Tsoma or self.token['code'] == Enum.Tsub:         # "+"  | "-" 
            self.token = self.Scanner.scan_file()
            self.term()                                                                 # <T>
            self.arit_expr()                                                            # <E'>

    def expr(self):
        self.term()                                                                     # <T>
        self.arit_expr()                                                                # <E'>

    def rel_expr(self):
        self.expr()
        if self.token['code'] == Enum.Tigual or self.token['code'] == Enum.Tdiferente or self.token['code'] == Enum.Tmaior or self.token['code'] == Enum.Tmenor or self.token['code'] == Enum.Tmaior_igual or self.token['code'] == Enum.Tmenor_igual:
            self.token = self.Scanner.scan_file()
            self.expr()
        else:
            PrintErr.print_error(self.token, "Expressao mal formada. Era esperado: Operador Relacional.")

    def attribution(self):      #OK
        if self.token['code'] == Enum.Tid:                                              # <id>
            self.token = self.Scanner.scan_file()
            if self.token['code'] == Enum.Tatrib:                                       # "="
                self.token = self.Scanner.scan_file()
                self.expr()                                                             # <expr_arit>
                if self.token['code'] == Enum.Tponto_virgula:                           # ";"
                    self.token = self.Scanner.scan_file()
                else:
                    PrintErr.print_error(self.token, "Atribuicao mal formada. Era esperado: ';'")
            else:
                PrintErr.print_error(
                    self.token, "Atribuicao mal formada. Era esperado: '='")
        else:
            PrintErr.print_error(self.token, "Atribuicao mal formada. Era esperado: Identificador.")

    def basic_command(self):    #OK
        if self.token['code'] == Enum.Tid:                                              # <atribuicao>
            self.attribution()
        elif self.token['code'] == Enum.Tchaves_opn:                                    # <bloco>
            self.block()
        else:
            PrintErr.print_error(self.token, "Comando mal formado. Era esperado: Atribuicao ou Bloco.")

    def command(self):          #OK
        if self.token['code'] == Enum.Tid or self.token['code'] == Enum.Tchaves_opn:    # <comando_basico>
            self.basic_command()
        elif self.token['code'] == Enum.Twhile or self.token['code'] == Enum.Tdo:       # <iteracao>
            self.iteration()
        elif self.token['code'] == Enum.Tif:                                            # if
            self.token = self.Scanner.scan_file()
            if self.token['code'] == Enum.Tparenteses_opn:                              # "("
                self.token = self.Scanner.scan_file()
                self.rel_expr()                                                         # <expr_relacional>
                if self.token['code'] == Enum.Tparenteses_cls:                          # ")" 
                    self.token = self.Scanner.scan_file()
                    self.command()                                                      # <comando>
                    if self.token['code'] == Enum.Telse:                                # {else <comando>}?
                        self.token = self.Scanner.scan_file()
                        self.command()
                    # self.token = self.Scanner.scan_file()
                else:
                    PrintErr.print_error(self.token, "Comando mal formada. Era esperado: ')'")
            else:
                PrintErr.print_error(self.token, "Comando mal formada. Era esperado: '('")
        else:
            PrintErr.print_error(self.token, "Comando mal formado.")

    def var_decl(self):         #OK
        if self.is_var_dec():                                                           # <tipo>
            self.token = self.Scanner.scan_file()
            if self.token['code'] == Enum.Tid:                                          # <id>
                self.token = self.Scanner.scan_file()
                while self.token['code'] == Enum.Tvirgula:                              # {,<id>}*
                    self.token = self.Scanner.scan_file()
                    if self.token['code'] == Enum.Tid:
                        self.token = self.Scanner.scan_file()
                    else:
                        PrintErr.print_error(self.token, "Declaracao de variavel mal formada. era esperado um Identificador.")
                if self.token['code'] == Enum.Tponto_virgula:                           #  ";"
                    self.token = self.Scanner.scan_file()
                else:
                    PrintErr.print_error(self.token, "Declaracao de variavel mal formada. era esperado um ';'")
            else:
                PrintErr.print_error(self.token, "Declaracao de variavel mal formada. era esperado um Identificador.")
        else:
            PrintErr.print_error(self.token, "Declaracao de variavel mal formada. era esperado um Tipo (Int, Float, Char)")    

    def block(self):            #OK
        if self.token['code'] == Enum.Tchaves_opn:                                      # "{"
            self.token = self.Scanner.scan_file()
            while self.is_var_dec():                                                    # {<decl_var>}*
                self.var_decl()
            while self.is_command():                                                    # {<comando>}*
                self.command()
            if self.token['code'] == Enum.Tchaves_cls:                                  # "}"
                self.token = self.Scanner.scan_file()
            else:
                PrintErr.print_error(self.token, "Bloco mal formado. Era esperado '}'")
        else:
            PrintErr.print_error(self.token, "Bloco mal formado. Era esperado '{'")

    def programm(self):         #OK
        self.token = self.Scanner.scan_file()
        if self.token['code'] == Enum.Tint:                                             # int
            self.token = self.Scanner.scan_file()
            if self.token['code'] == Enum.Tmain:                                        # main
                self.token = self.Scanner.scan_file()
                if self.token['code'] == Enum.Tparenteses_opn:                          # "("
                    self.token = self.Scanner.scan_file()
                    if self.token['code'] == Enum.Tparenteses_cls:                      # ")"
                        self.token = self.Scanner.scan_file()
                        self.block()                                                    # <bloco>
                        return True
                    else:
                        PrintErr.print_error(self.token, "Programa mal formado. Era esperado )")
                else:
                    PrintErr.print_error(self.token, "Programa mal formado. Era esperado (")
            else:
                PrintErr.print_error(self.token, "Programa mal formado. Era esperado a palavra reservada 'main'")
        else:
            PrintErr.print_error(self.token, "Programa mal formado. Era esperado a palavra reservada 'int'")

