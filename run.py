import sys
from scanner.scanner import Scanner

args = len(sys.argv)

if args < 2:
    print ("Insira caminho doa rquivo a ser aberto")
elif args == 2:
    filename = sys.argv[1]
    # filename = 'input.txt'
    with open(filename, 'r') as arq:
        s = Scanner(arq)
        token = s.scan_file()
        while token:
            print ("Lexema: "+token['lex'])
            print ("token: "+ str(token['code']))
            token = s.scan_file()
    


else:
    print ("Argumentos invalidos. Insira apenas o caminho doa rquivo a ser aberto")
