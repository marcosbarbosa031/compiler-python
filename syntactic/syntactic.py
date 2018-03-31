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
        pass

    def command(self):
        pass

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
