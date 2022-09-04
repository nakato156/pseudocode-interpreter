from src.Lexer import Tokenizer, Token
from src.Env import variables, operaciones_igualdad, arithmetic_operators

class Stack():
    def __init__(self, tokens:Tokenizer, scope_vars:dict):
        self.pgma = tokens
        self.vars = scope_vars
        self.actual = None
        self.op = None
        self.valores = []
        self.operadores = []

    def add_valores(self, value, pos=None):
        if not pos:self.valores.append(value)
        else: self.valores[pos]= value
    def add_operadores(self, op):
        self.operadores.append(op)

    def def_precedencia(self, op:Token):
        if op.tipo != Token.OPERADOR:
            if op.tipo != Token.ENTERO and op.texto in "=~!<>": return True
            var_dict = self.vars if op.texto in self.vars else variables
            op = Token(f"{var_dict[op.texto]}") if op.tipo == Token.IDENTIFICADOR else op
            self.add_valores(op)

        elif op.tipo == Token.OPERADOR:
            prece = op.precedencia
            self.operadores.append((op.texto,prece))

            if len(self.operadores)==1: return
            else:
                ultimo_op = self.operadores[-2][1]
                if prece>ultimo_op:
                    nxt = next(self.pgma)
                    nxt = next(self.pgma) if nxt.texto == "/" else nxt
                    res = arithmetic_operators[op.texto](self.valores[-1], nxt)
                    del self.operadores[-1]
                    self.add_valores(res,-1)
                else: 
                    if self.operadores[-2:] == [("/",3),("/",3)]:
                        nxt = next(self.pgma)
                        if  not nxt in [Token.ENTERO,Token.FLOAT]: exit("No se puede operar con una cadena de texto")
                        self.add_valores(nxt,0)
                        return
                    
                    res = arithmetic_operators[self.operadores[-2][0]](self.valores[-2], self.valores[-1])
                    del self.valores[:3]
                    self.add_valores(res,0)
            self.operadores = [self.operadores[-1]]

    def get_Stack(self)->tuple:
        return self.valores, self.operadores
