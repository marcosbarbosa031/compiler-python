

class Scanner(object):
    
    def __init__(self, arq):
        self.arq = arq
    
    def file_print(self):
        for i in self.arq:
            print (i)

    