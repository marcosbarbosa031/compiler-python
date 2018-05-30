from enum import Enum

class CodeGenerator(object):
    op_count = 0
    l_count = 0
    t_count = 0

    def __init__(self):
        pass

    def generate_code (self, op1, op2, op):
        print('$t{} = {}'.format(self.t_count, op1['lex'])),     # $t0 = x
        # if op1['qtd'] >= 0:
        #     print('{}'.format(op1['qtd'])),
        print('{}'.format(op)),                                 # *
        if op == Enum.Tdiferente:                                # !=
            print('='),
        print(' {}'.format(op2['lex'])),                         # y
        # if op2['qtd'] >= 0:
        #     print('{}'.format(op2['qtd']))
        print('')
        op1['qtd'] = self.t_count
        self.t_count += 1
        op1['lex'] = '$t'+str(self.t_count - 1)
        return op1

    def gen_int_to_float(self, op):
        print('$t{} = (float){}'.format(self.t_count, op['lex'])),
        # if op['qtd'] >= 0:
        #     print('{}'.format(op['qtd']))
        print('')
        op['qtd'] = self.t_count
        self.t_count += 1
        op['lex'] = '$t'+str(self.t_count - 1)

    def if_while_generator (self, op):
        print('if {}'.format(op['lex'])),
        l_aux = self.l_count
        self.l_count += 1
        print(' == 0 then goto L{}'.format(self.l_count))
        return l_aux
    
    def end_while_generator (self, l_aux):
        print('goto L{}'.format(l_aux))
        print('L{}'.format(self.l_count))
        self.l_count += 1

    def if_generator (self, op):
        print('if {}'.format(op['lex'])),
        # if op['qtd'] >= 0:
        #     print(op['qtd']),
        print(' == 0 goto L{}'.format(self.l_count))
        l_aux = self.l_count
        self.l_count += 1
        return l_aux

    def else_generator (self, l_aux):
        print('goto L{}'.format(self.l_count))
        print(' L{}'.format(l_aux))
        l_aux2 = self.l_count
        self.l_count += 1
        return l_aux2

    def baisc_command_generator (self, op1, op2):
        print('{} = {}'.format(op1['lex'], op2['lex']))

    def iterator_l_generation (self):
        print('L{}'.format(self.l_count))

    pass