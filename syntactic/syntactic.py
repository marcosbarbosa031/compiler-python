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
        pass

    def arit_expr(self):
        pass

    def attribution(self):
        if self.token['code'] == Enum.Tid:
            self.token = self.Scanner.scan_file()
            if self.token['code'] == Enum.Tigual:
                self.token = self.Scanner.scan_file()
                self.arit_expr()
            else:
                PrintErr.print_error(
                    self.token, "Atribuicao mal formada. Era esperado um '='")
        else:
            PrintErr.print_error(self.token, "Atribuicao mal formada. Era esperado um Identificador.")

    def basic_command(self):
        if self.token['code'] == Enum.Tid:
            self.attribution()
        elif self.token['code'] == Enum.Tchaves_opn:
            self.block()
        else:
            PrintErr.print_error(self.token, "Comando mal formado. Era esperado Atribuicao ou Bloco.")

    def command(self):
        if self.token['code'] == Enum.Tid or self.token['code'] == Enum.Tchaves_opn:
            self.basic_command()
        elif self.token['code'] == Enum.Twhile or self.token['code'] == Enum.Tdo:
            self.iteration()
        elif self.token['code'] == Enum.Tif:
            pass
        else:
            PrintErr.print_error(self.token, "Comando mal formado.")

    def var_decl(self):
        if self.is_var_dec():  # <tipo>
            self.token = self.Scanner.scan_file()
            if self.token['code'] == Enum.Tid:  # <id>
                self.token = self.Scanner.scan_file()
                while self.token['code'] == Enum.Tvirgula:  # {,<id>}*
                    self.token = self.Scanner.scan_file()
                    if self.token['code'] == Enum.Tid:
                        self.token = self.Scanner.scan_file()
                    else:
                        PrintErr.print_error(self.token, "Declaracao de variavel mal formada. era esperado um Identificador.")
                if self.token['code'] == Enum.Tponto_virgula:  #  ";"
                    self.token = self.Scanner.scan_file()
                else:
                    PrintErr.print_error(self.token, "Declaracao de variavel mal formada. era esperado um ';'")
            else:
                PrintErr.print_error(self.token, "Declaracao de variavel mal formada. era esperado um Identificador.")
        else:
            PrintErr.print_error(self.token, "Declaracao de variavel mal formada. era esperado um Tipo (Int, Float, Char)")    

    def block(self):
        if self.token['code'] == Enum.Tchaves_opn:  # "{"
            self.token = self.Scanner.scan_file()
            while self.is_var_dec():  # {<decl_var>}*
                self.var_decl()
            while self.is_command():  # {<comando>}*
                self.command()
            if self.token['code'] == Enum.Tchaves_cls:  # "}"
                self.token = self.Scanner.scan_file()
            else:
                PrintErr.print_error(self.token, "Bloco mal formado. Era esperado '}'")
        else:
            PrintErr.print_error(self.token, "Bloco mal formado. Era esperado '{'")

    def programm(self):
        self.token = self.Scanner.scan_file()
        if self.token['code'] == Enum.Tint:
            self.token = self.Scanner.scan_file()
            if self.token['code'] == Enum.Tmain:
                self.token = self.Scanner.scan_file()
                if self.token['code'] == Enum.Tparenteses_opn:
                    self.token = self.Scanner.scan_file()
                    if self.token['code'] == Enum.Tparenteses_cls:
                        self.token = self.Scanner.scan_file()
                        self.block()
                        return True
                    else:
                        PrintErr.print_error(self.token, "Programa mal formado. Era esperado )")
                else:
                    PrintErr.print_error(self.token, "Programa mal formado. Era esperado (")
            else:
                PrintErr.print_error(self.token, "Programa mal formado. Era esperado a palavra reservada 'main'")
        else:
            PrintErr.print_error(self.token, "Programa mal formado. Era esperado a palavra reservada 'int'")
