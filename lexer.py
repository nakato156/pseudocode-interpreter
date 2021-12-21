from sys import argv
# arimetic operators 
arithmetic_operators = {
    "+": lambda a,b: a+b,
    "-": lambda a,b: a-b,
    "^": lambda a,b: a**b,
    "/": lambda a,b: a/b,
    "//": lambda a,b: a//b,
    "*": lambda a,b: a*b
}

def check_float(texto:str)->str:
    texto = texto.replace(",",".")
    if texto.count(".")!=1 or len(texto)<2: return
    for ch in texto:
        if not (ch.isnumeric() or ch == "."): return 
    return texto

operadores = "=(),+-*/<>[];:!~"
def my_tokenizer(stream)->str:
    for line in stream:
        linea:str = line.strip()
        if linea.count("=")==1 and linea[-1] !=";": exit("EOL Error")
        largo = len(linea)
        i = 0
        while i < largo:
            inicio = i

            while linea[i] == ' ' and i < largo:
                i += 1

            if i == largo: break
            
            car = linea[i]
            if linea[i] in operadores:
                yield car
                i += 1

            elif car in "'\"":
                inicio = i
                i += 1
                while i < largo and linea[i] != car:
                    i += 1
                yield linea[inicio:i+1]
                i += 1

            else:
                inicio = i
                i += 1
                while i < largo and linea[i] not in operadores and linea[i] != ' ':
                    i += 1
                yield linea[inicio:i]

class Token():
    OPERADOR = 1
    ENTERO = 2
    FLOAT = 3
    IDENTIFICADOR = 4
    ASIGNACION = 5
    STRING = 6
    FOR = 7
    WHILE = 8
    ARRAY = 9
    RETURN = 10
    CONDICION = 11

    precedencia = {
            1:"+-()",
            2:"~&|",
            3:"*/%^"
    }

    def __init__(self, texto:str):
        texto = texto.replace("'", '"')
        self.tipo = None
        self.texto = texto
        if texto in "*^/+-%":
            self.tipo = Token.OPERADOR
            self.precedencia = [k for k,v in Token.precedencia.items() if texto in v][0]
        elif texto in ["iterar","para"]:
            self.tipo = Token.FOR
        elif texto == "mientras":
            self.tipo = Token.WHILE
        elif texto == "retornar": self.tipo = Token.RETURN
        elif texto in ["si", "o", "sino"]: self.tipo = Token.CONDICION
        elif texto.isnumeric():
            self.tipo = Token.ENTERO
            self.texto = int(texto)
        elif texto[0].isnumeric() or texto[0] in ".,": #numeros flotantes
            texto = check_float(texto)
            if texto:
                self.tipo = Token.FLOAT
                self.texto = float(texto)
        elif texto.isalnum() and texto[0].isalpha():
            self.tipo = Token.IDENTIFICADOR
        elif texto == "=":
            self.tipo = Token.ASIGNACION
        elif texto[0] == '"':
            self.tipo = Token.STRING
            self.texto = texto[1:-1]

    def __str__(self):
        return f"{self.texto}"

    def __int__(self):
        if self.tipo in [Token.ENTERO, Token.FLOAT]:
            return int(self.texto) if Token.ENTERO else float(self.texto)
        elif self.tipo == Token.IDENTIFICADOR:
            return variables[self.texto]
        else: raise ValueError(f"No se puede convertir {self.texto} a entero")
        
    def __repr__(self):
        return f"({self.tipo}, {self.texto})"
    
    def __eq__(self, other):
        if type(other) == str:
            return self.texto[1:-1] == other
        else:
            return self.texto == other.texto and self.tipo == other.tipo

    def __getitem__(self, i):
        return self.texto[i]

class Tokenizer():
    def __init__(self, pgma):
        self.tokens = [Token(x) for x in pgma] if type(pgma) !=list else pgma 

    def get_token(self)->Token:
        return self.tokens.pop(0) if self.tokens else None
    
    def skip_tokens(self, skip)->Token:
        for _ in range(skip):
            if not self.tokens: break
            self.tokens.pop(0)
        return self.get_token()
    
    def copy(self):
        return Tokenizer(self.tokens[:])

    def __enter__(self):
        tks = []
        while True:
            tk = self.get_token()
            if tk and tk.texto==":": break
            elif not tk: exit("EOF Error")
            tks.append(tk)
        self.prov = self.tokens.copy()
        tks.append(Token(";"))
        self.tokens = tks
        return self

    def __exit__(self, type, x, traceback):
        self.tokens = self.prov
        del self.prov

    def __len__(self):
        return len(self.tokens)
    
    def __repr__(self):
        return f"{self.tokens}"

    def insert(self, index, other):
        self.tokens.insert(index, other)
        return self
class Stack():
    def __init__(self, tokens:Tokenizer) -> None:
        self.pgma = tokens
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
            op = Token(f"{variables[op.texto]}") if op.tipo == Token.IDENTIFICADOR else op
            self.add_valores(op.texto)

        elif op.tipo == Token.OPERADOR:
            prece = op.precedencia
            self.operadores.append((op.texto,prece))

            if len(self.operadores)==1: return
            else:
                ultimo_op = self.operadores[-2][1]
                if prece>ultimo_op:
                    next = self.pgma.get_token().texto
                    next = self.pgma.get_token().texto if next == "/" else next
                    res = arithmetic_operators[op.texto](self.valores[-1], next)
                    del self.operadores[-1]
                    self.add_valores(res,-1)
                else: 
                    if self.operadores[-2:] == [("/",3),("/",3)]:
                        next = self.pgma.get_token().texto
                        if  type(next) != int: exit("No se puede operar con una cadena de texto")
                        self.add_valores(next,0)
                        return
                    
                    res = arithmetic_operators[self.operadores[-2][0]](self.valores[-2], self.valores[-1])
                    del self.valores[:3]
                    self.add_valores(res,0)
            self.operadores = [self.operadores[-1]]

    def get_Stack(self)->tuple:
        return self.valores, self.operadores

variables = {
    "imprimir": lambda x: print(*x),
    "tipo": lambda x: type(x[0]),
    "leer": lambda x: input(*x)
}

operaciones_igualdad = {
    "=": lambda x,y: x==y,
    ">=": lambda x,y: x>=y,
    "<=": lambda x,y: x<=y,
    ">": lambda x,y: x>y,
    "<": lambda x,y: x<y
}

def call_function(func, tokens:Tokenizer, scope_vars=variables):
    tmp_tokens = Tokenizer([])
    if func in scope_vars or func in variables:
        place = scope_vars if func in scope_vars else variables
        args, pre_args, END, tk = [], [], 1, True
        while tk:
            tk = tokens.get_token()
            if tk.texto == "(": END+=1
            elif tk.texto == ")": END-=1
            if END==0 and tk.texto == ")": 
                tmp_tokens.tokens = pre_args
                if tmp_tokens.tokens: args.append(eval_expresion(tmp_tokens, scope_vars))
                break
            elif tk.texto!=",": pre_args.append(tk)
            elif tk.texto == ",": 
                tmp_tokens.tokens = pre_args
                args.append(eval_expresion(tmp_tokens, scope_vars))
        else: exit("EOF Error")
        return place[func](args)
    else:
        raise NameError(f"No se ha declarado la función {func}")

def proc_array(exp:Tokenizer, scope_vars=variables)->Token:
    args = []
    tk = Tokenizer([])
    tk.tokens = []
    while True:
        n_tk = exp.get_token()
        if n_tk is None: break
        elif n_tk.texto == ",":
            if tk.tokens: args.append(eval_expresion(tk, scope_vars))
            continue
        elif n_tk.texto == "[":
            n_tk = proc_array(exp)
            args.append(n_tk)
            continue
        elif n_tk.texto == "]": 
            if tk.tokens: args.append(eval_expresion(tk, scope_vars))
            break
        tk.tokens.append(n_tk)
    tk = Token("")
    tk.tipo = Token.ARRAY
    tk.texto = args
    return tk

def eval_expresion(exp:Tokenizer, scope_vars=variables):
    my_Stack = Stack(exp)
    tk = exp.get_token()
    if not tk: return tk
    if len(exp.tokens)<2: return scope_vars[tk.texto] if tk.tipo == Token.IDENTIFICADOR else tk.texto
    flag, func = None, None
    while tk:
        if tk.texto == ";": break
        elif tk.texto == "[": 
            arr = proc_array(exp, scope_vars)
            my_Stack.add_valores(arr)
            tk = exp.get_token()
        elif flag:
            f = flag
            flag = False
            if f[1] == "=":
                if tk.texto == "=":
                    print(my_Stack.valores)
                    ant = arithmetic_operators[my_Stack.operadores[-1][0]](*my_Stack.valores) if len(my_Stack.valores)!=1 else my_Stack.valores[-1]
                    val = ant == eval_expresion(exp, scope_vars)
                    return val
                raise SyntaxError(f"Token inesperado {tk.texto}")
            elif f[1] in "!~ ": return not tk
            elif f[1] in "<>":
                ant = arithmetic_operators[my_Stack.operadores[-1][0]](*my_Stack.valores) if len(my_Stack.valores)!=1 else my_Stack.valores[-1]
                
                if tk.texto == "=": 
                    val = operaciones_igualdad[f"{f[1]}="](ant,exp.get_token().texto)
                else: val = operaciones_igualdad[f"{f[1]}"](ant,tk.texto)
                return val
                
            else: raise SyntaxError(tk)
        else:
            r = my_Stack.def_precedencia(tk)
            if r: flag = True,tk.texto
            if tk.tipo == Token.IDENTIFICADOR: func=True,tk
            tk = exp.get_token()
            func = func if tk.texto == "(" else False
        if func:
            my_Stack.add_valores(call_function(func[1].texto, exp, scope_vars))
            func = False
            tk = exp.get_token()

    vals,ops =my_Stack.get_Stack()
    return arithmetic_operators[ops[-1][0]](*vals) if len(vals)>=1 and len(ops)>=1 else vals[-1]
        
def asignacion(token:Token, val:Tokenizer, scope_vars=variables)->None:
    scope_vars[token.texto] = eval_expresion(val)

def exec_function(this, params, code):
    locales = dict(zip(this, *params))
    tk = Tokenizer(code)
    return run(tk, scope_vars=locales, Func=True)

def proc_for(pgma:Tokenizer, scope_vars=variables)->tuple:
    control_var = pgma.get_token()
    code = []
    n:Token = pgma.get_token()
    if n.texto == "en": 
        with pgma as loop:
            iterable = eval_expresion(loop, scope_vars)
        n = pgma.get_token()
    elif n.texto == "desde":
        with pgma as loop:
            inicio = pgma.get_token().texto
            pgma.get_token()
            fin = pgma.get_token().texto
            paso = 1 if pgma.get_token().texto == ":" else pgma.skip_tokens(1)
            paso = int(1 if paso is None else paso )
        iterable = range(int(inicio),int(fin), paso)
    n = pgma.get_token()
    try:
        END = 1
        while END!=0 and n:
            code.append(n)
            n = pgma.get_token()
            if n.texto == "START": END += 1  
            elif n.texto == "END": END-=1
    except AttributeError:
        exit("EOF Error")
    pgma.tokens = code[1:]
    return [control_var, iterable, pgma]

def create_func(pgma:Tokenizer, n:Token, scope_vars=variables)->None:
    args, code = [],[]
    name = n.texto
    n = pgma.get_token()
    while n.texto !=":":
        if n.tipo: args.append(n.texto)
        n = pgma.get_token()
    n = pgma.get_token()
    while True:
        if n and not n.texto in ["START","END"]: code.append(n)
        elif not n or n.texto=="END": break
        n = pgma.get_token()
    scope_vars[name] = lambda *x: exec_function(this=args, params=x, code=code.copy())

def proc_cond(pgma:Tokenizer, tk:Token, scope_vars:dict)->bool:
    if tk.texto != "si": print(tk);exit("Sentencia inválida;")
    with pgma as condition:
        expr = eval_expresion(condition, scope_vars)

    tokens = []
    while True:
        tk = pgma.get_token()
        if tk.texto == "END":break
        elif tk is None: exit("EOF ERROR")
        tokens.append(tk)
    
    tks = pgma.tokens.copy()
    pgma.tokens = tokens
    if expr: run(pgma)
    pgma.tokens = tks
    
    if pgma.get_token().texto != ";": exit("EOL ERROR")
    tk = pgma.get_token()
    if tk.tipo == Token.CONDICION:
        if not expr and tk.texto == "o":return proc_cond(pgma, pgma.get_token(), scope_vars)
        elif not expr and tk.texto == "sino": 
            if pgma.get_token().texto!=":": exit("EOL Error")
            run(pgma, scope_vars)
        else:
            while tk and tk.texto !="o":
                while tk and tk.texto!="END":
                    tk = pgma.get_token()
                pgma.get_token()
                tk = pgma.get_token()
    return expr

def proc_while(pgma:Tokenizer):
    with pgma as condition:
        while_condition = condition.copy()    
    pgma.skip_tokens(1)
    
    n = pgma.get_token()
    code, END = [], 1
    while END!=0 and n:
        code.append(n)
        n = pgma.get_token()
        if n.texto == "START": END += 1  
        elif n.texto == "END": END-=1
    if pgma.get_token().texto != ";": exit("EOL Error")
    
    return while_condition, Tokenizer(code)

def run(pgma:Tokenizer, scope_vars=variables, Func=None):
    while True:
        tk = pgma.get_token()
        if tk is None: break
        elif tk.tipo == Token.IDENTIFICADOR:
            n = pgma.get_token()
            if n.tipo == Token.ASIGNACION:
                asignacion(tk, pgma, scope_vars)
            elif n.texto == "(":
                call_function(tk.texto, pgma, scope_vars)
            elif n.texto == "[": #setitem array
                i,args = 1,[]
                while i!=0:
                    n_tk = pgma.get_token()
                    if n_tk =="[": 
                        i+=1
                        continue
                    elif n_tk=="]": 
                        i-=1
                        continue
                    args.append(tk)
                n = pgma.get_token()
                if n.tipo != Token.ASIGNACION: raise SyntaxError(f"error de sintaxis en {n.texto}")
                asignacion(tk[args[0]], pgma)
            elif n.tipo == Token.IDENTIFICADOR and tk.texto == "func":
                create_func(pgma, n,scope_vars)
        elif tk.tipo == Token.FOR:
            control_variable, iterable, code= proc_for(pgma, scope_vars)
            codec = code.tokens
            for x in iterable:
                code.tokens = codec.copy()
                scope_vars[control_variable.texto] = x
                scope_vars = run(code, scope_vars)
        elif tk.tipo == Token.WHILE:
            condition_while, codec = proc_while(pgma)

            while eval_expresion(condition_while.copy(), scope_vars):
                scope_vars = run(codec.copy())
        elif tk.tipo == Token.CONDICION:
            proc_cond(pgma, tk, scope_vars)
        elif Func and tk.tipo == Token.RETURN: 
            return eval_expresion(pgma)  
    return scope_vars if not Func else None

if __name__ == "__main__":
    file = argv[1] if len(argv)>1 else None
    if file:
        with open(f"{file}") as f:
            pgma = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("//")]
        pgma = Tokenizer(my_tokenizer(pgma))
        run(pgma)
    else:
        def starts_with(cadena:str, iterable:list):
            return any(cadena.startswith(x) for x in iterable)
        while True:
            pgma = []
            entrada = input(">>> ").strip()
            pgma.append(entrada)
            if starts_with(entrada, ["si", "sino", "mientras", "func", "iterar", "para"]) and entrada[-1] == ":":
                entrada = input("... ").strip()
                while entrada:
                    pgma.append(entrada)
                    entrada = input("... ").strip()
                runner = Tokenizer(my_tokenizer(pgma))
                variables = run(runner)
                continue
            elif entrada and entrada[-1] !=";": 
                print("EOL Error")
                continue
            elif entrada == "exit();": break
            runner = Tokenizer(my_tokenizer(pgma))
            variables = run(runner)
