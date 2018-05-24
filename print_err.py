import sys

class PrintErr(object):

    @staticmethod
    def print_error(token, msg):
        print("ERRO na linha {0}, coluna {1}, ultimo token lido '{2}': {3}".format(token['ln'], token['cl'], token['lex'], msg))
        sys.exit(1)