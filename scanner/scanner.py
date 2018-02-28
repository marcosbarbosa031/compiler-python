from utils.enum.enum import Enum

class Scanner(object):
    ln = 1
    cl = 1

    def __init__(self, arq):
        self.arq = arq

    def getc(self):
        return self.arq.read(1)

    def scan_file(self):
        c = self.getc()
        while(c != '}'):
            print ("token = " + c)
            print ("line = " + str(self.ln))
            print ("line = " + str(self.cl))
            c = self.getc()
            self.ln += 1
            if (c == "\n"):
                self. cl += 1


