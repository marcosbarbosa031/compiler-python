import sys
from syntactic import Syntactic
from scanner import Scanner
from io import open

args = len(sys.argv)

if args < 2:
    print ("Insira o caminho do arquivo a ser aberto")
elif args == 2:
    filename = sys.argv[1]
    with open(filename, 'r') as arq:
        s = Scanner(arq)
        s.c = s.get_c()
        p = Syntactic(s)
        if p.program():
            print("Compilado com sucesso!")
        #token = s.scan_file()
        #while token:
        #    print ("Lexema: "+token['lex'])
        #    print ("token: "+ str(token['code']))
        #    print ('')
        #    token = s.scan_file()
else:
    print ("Argumentos invalidos. Insira apenas o caminho do arquivo a ser aberto")
