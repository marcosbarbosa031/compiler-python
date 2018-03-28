from utils import Enum


class Parser(object):
    token = None

    def __init__ (self, scanner):
        self.Scanner = scanner

    def program (self):
        self.token = self.Scanner.scan_file()
        if self.token == Enum.Tint:
            self.token = self.Scanner.scan_file()
            if self.token == Enum.Tmain:
                self.token = self.Scanner.scan_file()
                if self.token == Enum.Tparenteses_opn:
                    self.token = self.Scanner.scan_file()
                    if self.token == Enum.Tparenteses_cls:
                        self.token = self.Scanner.scan_file()
                        if self.token == Enum.Tchaves_opn:
                            self.token = self.Scanner.scan_file()
                        else:
                            print ('error')
                    else:
                        print ('error')
                else:
                    print ('error')
            else:
                print ('error')
        else:
            print ('error')