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
        pass

    def block(self):
        if self.token['code'] == Enum.Tchaves_opn:  # "{"
            self.token = self.Scanner.scan_file()
            while self.is_var_dec():  # {<decl_var>}*
                self.var_decl()
                self.token = self.Scanner.scan_file()
            while self.is_command():  # {<comando>}*
                self.command()
                self.token = self.Scanner.scan_file()
            if self.token['code'] == Enum.Tchaves_cls:  # "}"
                self.token = self.Scanner.scan_file()
            else:
                PrintErr.print_error(self.token, "Bloco mal formado. Era esperado '}'")
        else:
            PrintErr.print_error(self.token, "Bloco mal formado. Era esperado '{'")

    def program(self):
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
