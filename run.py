import sys
from scanner.scanner import Scanner

args = len(sys.argv)

if args < 2:
    print ("Insira o caminho do arquivo a ser aberto")
elif args == 2:
    filename = sys.argv[1]
    # filename = 'input.txt'
    with open(filename, 'r') as arq:
        s = Scanner(arq)
        s.c = s.get_c()
        token = s.scan_file()
        while token:
            if token == None:
                exit
            print ("Lexema: "+token['lex'])
            print ("token: "+ str(token['code']))
            print ('')
            # s.c = s.get_c()
            token = s.scan_file()
else:
    print ("Argumentos invalidos. Insira apenas o caminho do arquivo a ser aberto")
