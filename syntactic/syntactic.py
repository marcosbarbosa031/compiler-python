from utils import Enum
from utils import PrintErr


class Syntactic(object):
    token = None
    scope = 0

    def __init__ (self, scanner, stack):
        self.Scanner = scanner
        self.Stack = stack

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
        if self.token['code'] == Enum.Tdigint or self.token['code'] == Enum.Tdigfloat or self.token['code'] == Enum.Tdigchar:
            self.token = self.Scanner.scan_file()
            return self.token
        elif self.token['code'] == Enum.Tid:
            op = self.Stack.searchAll(self.token['lex'])
            if not op: # Variavel nao declarada
                PrintErr.print_error(self.token, "Variavel '" + self.token['lex'] + "' nao declarada.")
            self.token = self.Scanner.scan_file()
            return { 'code': op.tipo, 'lex': op.lex }
        elif self.token['code'] == Enum.Tparenteses_opn:
            self.token = self.Scanner.scan_file()
            op = self.expr()
            if self.token['code'] == Enum.Tparenteses_cls:
                self.token = self.Scanner.scan_file()
                return op
            else:
                PrintErr.print_error(self.token, "Fator mal formado. Era esperado: ')'")

        else:
            PrintErr.print_error(self.token, "Fator mal formado. Era esperado: Identificador, numero inteiro, real ou caracter")

    # def arit_term(self):
    #     if self.token['code'] == Enum.Tmult or self.token['code'] == Enum.Tdivi:        # "*"  | "/"
    #         self.token = self.Scanner.scan_file()
    #         self.factor()
    #         self.arit_term()

    def term(self):
        op1 = self.factor()                                                                   # <F>
        while self.token['code'] == Enum.Tmult or self.token['code'] == Enum.Tdivi:
            op2 = self.factor()
            if op2['code'] == Enum.Tdigint or op2['code'] == Enum.Tdigfloat or op2['code'] == Enum.Tdigchar:
                if op1['code'] == Enum.Tdigchar and op2['code'] != Enum.Tdigchar:
                    PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Char so podem ser operadas com variaveis do tipo Char.")
                if op1['code'] == Enum.Tdigint and op2['code'] == Enum.Tdigchar:
                    PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Int podem ser operadas apenas com variaveis do tipo Int ou Float.")
                if op1['code'] == Enum.Tdigfloat and op2['code'] == Enum.Tdigchar:
                    PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Float podem ser operadas apenas com variaveis do tipo Int ou Float.")
                if (op1['code'] == Enum.Tdigint and op2['code'] == Enum.Tdigfloat) or (op1['code'] == Enum.Tdigfloat and op2['code'] == Enum.Tdigint):
                    op1['code'] = Enum.Tdigfloat
                if self.token['lex'] == Enum.Tdivi and op1['code'] == Enum.Tdigint and op2['code'] == Enum.Tdigint:
                    op1['code'] = enum.Tdigfloat
        self.token = self.Scanner.scan_file()
        return op1

    def arit_expr(self):
        if self.token['code'] == Enum.Tsoma or self.token['code'] == Enum.Tsub:         # "+"  | "-"
            self.token = self.Scanner.scan_file()
            op1 = self.term()                                                                 # <T>
            op2 = self.arit_expr()                                                            # <E'>
            if op2['code'] == Enum.Tdigint or op2['code'] == Enum.Tdigfloat or op2['code'] == Enum.Tdigchar:
                if op1['code'] == Enum.Tdigchar and op2['code'] != Enum.Tdigchar:
                    PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Char so podem ser operadas com variaveis do tipo Char.")
                if op1['code'] == Enum.Tdigint and op2['code'] == Enum.Tdigchar:
                    PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Int podem ser operadas apenas com variaveis do tipo Int ou Float.")
                if op1['code'] == Enum.Tdigfloat and op2['code'] == Enum.Tdigchar:
                    PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Float podem ser operadas apenas com variaveis do tipo Int ou Float.")
                if (op1['code'] == Enum.Tdigint and op2['code'] == Enum.Tdigfloat) or (op1['code'] == Enum.Tdigfloat and op2['code'] == Enum.Tdigint):
                    op1['code'] = Enum.Tdigfloat
            return op1

    def expr(self):
        op1 = self.term()                                                                     # <T>
        op2 = self.arit_expr()                                                                # <E'>
        if op2['code'] == Enum.Tdigint or op2['code'] == Enum.Tdigfloat or op2['code'] == Enum.Tdigchar:
            if op1['code'] == Enum.Tdigchar and op2['code'] != Enum.Tdigchar:
                PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Char so podem ser operadas com variaveis do tipo Char.")
            if op1['code'] == Enum.Tdigint and op2['code'] == Enum.Tdigchar:
                PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Int podem ser operadas apenas com variaveis do tipo Int ou Float.")
            if op1['code'] == Enum.Tdigfloat and op2['code'] == Enum.Tdigchar:
                PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Float podem ser operadas apenas com variaveis do tipo Int ou Float.")
            if (op1['code'] == Enum.Tdigint and op2['code'] == Enum.Tdigfloat) or (op1['code'] == Enum.Tdigfloat and op2['code'] == Enum.Tdigint):
                op1['code'] = Enum.Tdigfloat
        return op1

    def rel_expr(self):
        op1 = self.expr()
        if self.token['code'] == Enum.Tigual or self.token['code'] == Enum.Tdiferente or self.token['code'] == Enum.Tmaior or self.token['code'] == Enum.Tmenor or self.token['code'] == Enum.Tmaior_igual or self.token['code'] == Enum.Tmenor_igual:
            self.token = self.Scanner.scan_file()
            op2 = self.expr()
            if op2['code'] == Enum.Tdigint or op2['code'] == Enum.Tdigfloat or op2['code'] == Enum.Tdigchar:
                if op1['code'] == Enum.Tdigchar and op2['code'] != Enum.Tdigchar:
                    PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Char so podem ser operadas com variaveis do tipo Char.")
                if op1['code'] == Enum.Tdigint and op2['code'] == Enum.Tdigchar:
                    PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Int podem ser operadas apenas com variaveis do tipo Int ou Float.")
                if op1['code'] == Enum.Tdigfloat and op2['code'] == Enum.Tdigchar:
                    PrintErr.print_error(self.token, "Variaveis incompativeis. Variaveis Float podem ser operadas apenas com variaveis do tipo Int ou Float.")
                if (op1['code'] == Enum.Tdigint and op2['code'] == Enum.Tdigfloat) or (op1['code'] == Enum.Tdigfloat and op2['code'] == Enum.Tdigint):
                    op1['code'] = Enum.Tdigfloat
        else:
            PrintErr.print_error(self.token, "Expressao mal formada. Era esperado: Operador Relacional.")

    def attribution(self):      #OK
        if self.token['code'] == Enum.Tid:                                              # <id>
            self.token = self.Scanner.scan_file()
            if self.token['code'] == Enum.Tatrib:                                       # "="
                self.token = self.Scanner.scan_file()
                op = self.expr()                                                        # <expr_arit>
                if self.token['code'] == Enum.Tponto_virgula:                           # ";"
                    self.token = self.Scanner.scan_file()
                    return op
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
                        self.command()#*
                    # self.token = self.Scanner.scan_file()
                else:
                    PrintErr.print_error(self.token, "Comando mal formada. Era esperado: ')'")
            else:
                PrintErr.print_error(self.token, "Comando mal formada. Era esperado: '('")
        else:
            PrintErr.print_error(self.token, "Comando mal formado.")

    def var_decl(self):         #OK
        if self.is_var_dec():                                                           # <tipo>
            tipo = self.token['code']
            self.token = self.Scanner.scan_file()
            if self.token['code'] == Enum.Tid:                                          # <id>
                if not self.Stack.searchScope(self.token['lex'], self.scope): # Variavel ainda nao criada no escopo
                    self.Stack.push(self.token['lex'], tipo, self.token) # empilha na tabela de simbolos
                self.token = self.Scanner.scan_file()
                while self.token['code'] == Enum.Tvirgula:                              # {,<id>}
                    if not self.Stack.searchScope(self.token['lex'], self.scope): # Variavel ainda nao criada no escopo
                        self.Stack.push(
                            self.token['lex'], tipo,
                            self.token)  # empilha na tabela de simbolos
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
            self.scope += 1 # Incrementa escopo
            self.token = self.Scanner.scan_file()
            while self.is_var_dec():                                                    # {<decl_var>}*
                self.var_decl()
            while self.is_command():                                                    # {<comando>}*
                self.command()
            if self.token['code'] == Enum.Tchaves_cls:                                  # "}"
                self.scope -= 1 # Decrementa escopo
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
                        self.block() #*                                                   # <bloco>
                        if self.token['code'] == Enum.Tfeof:
                            return True
                        else:
                            PrintErr.print_error(self.token, "Programa mal formado. Era esperado Fim de arquivo apos termino do metodo main.")
                    else:
                        PrintErr.print_error(self.token, "Programa mal formado. Era esperado )")
                else:
                    PrintErr.print_error(self.token, "Programa mal formado. Era esperado (")
            else:
                PrintErr.print_error(self.token, "Programa mal formado. Era esperado a palavra reservada 'main'")
        else:
            PrintErr.print_error(self.token, "Programa mal formado. Era esperado a palavra reservada 'int'")
