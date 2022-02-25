from sys import argv
from typing import Text
"""[summary]
Nota: usare el modulo colorama para el color, que debe ser descargado.
[description]
"""
ANSI_SCAPE={
    "\"":"\"",
    "'":"\'",
    "n":"\n",
    "a":"\a",
    "b":"\b",
    "f":"\f",
    "r":"\r",
    "t":"\t",
    "v":"\v",
    "\\":"\\",
    "?":"?",
    "x":None
};
# arimetic operators
class TOKEN_VARS():
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
    BOOLEAN = 12
    NADA = 13
    LOOPS = 14
    FUNC = 15
    START = 16
    END = 17
    RETORNAR = 18
arithmetic_operators = {
    "+": lambda a,b: a+b,
    "-": lambda a,b: a-b,
    "^": lambda a,b: a**b,
    "/": lambda a,b: a.__div__(b),
    "//": lambda a,b: a//b,
    "*": lambda a,b: a*b
}
"""sintaxis={
    "key_word":{
        "condicionales":{
            key:value for key,value in {"si":0,"sino si":1,"sino":2}
        },
        "loops":{
            key:value for key,value in {"para":0,"mientras":1,"salto":2}
        },
        "operators":{
            "func":TOKEN_VARS.FUNC,
            "START":TOKEN_VARS.START,
            "END":TOKEN_VARS.END,
            "retornar":TOKEN_VARS.RETORNAR
        },
        "booleans":{
            "verdadero":True,
            "falso":False,
            "true":True,
            "false":False
        }
        
    },
    "arithmetic_operators":{#Dudo mucho de este bucle(con respeto a como se ve la sintaxis), cleo que seria mejor eliminarlo y dejarlo como antes.
        key:value for key,value in {"+":lambda x,y: x+y,"-":lambda x,y: x-y,"*":lambda x,y: x*y,"^":lambda x,y:x**y,"/": lambda x,y: x.__div__(y),"//":lambda x,y:x//y}
    },
    "operadores":"=(),+-*/<>[];:!~"
};"""

def check_float(texto:str)->str:
    texto = texto.replace(",",".")
    if texto.count(".")!=1 or len(texto)<2: return
    for ch in texto:
        if not (ch.isnumeric() or ch == "."): return 
    return texto

operadores = "=(),+-*/<>[];:!~"
#For scape_str.test
#scape_str("\\n")
#scape_str("imprimir(\"\\n\\\"\" ")
#scape_str(input());
#imprimir("hola\n mundo\")
def scape_str(str_:str,INIT:int=0,END=None):
    exit_="";
    LEN=END if END else len(str_);
    scape=0;
    i=INIT;
    while i<LEN:
        char=str_[i];
        if char=='\\':#Preparamos para saber si es un signo de scape.
            if i+1<LEN:
                i+=1;
                char=str_[i];
                if char in ANSI_SCAPE:
                    char=ANSI_SCAPE[char];
                    if not isinstance(char,str):#if char: \x* : significa que el usuario quiere ingresar un codigo hexadecimal.
                        int_="";
                        iu=0;
                        for iu in range(i+1,LEN):
                            str_[iu]
                            if not (str_[iu]>="a" and str_[iu]<="f") and not (str_[iu]>='0' and str_[iu]<='9'):#No es hexadecimal.
                                break;
                            int_+=str_[iu];
                        char=chr(int("0x"+int_,16));
                        i=iu-1;
            else: return {"end":False,"str":exit_+char};
        exit_+=char;
        #Ocurre un error cuando hacen: "hola\\""
        i+=1;
    return {"end":False,"str":exit_};
def search_sub_str(str_:str,init:int=0)->str:
    is_str={"type":"","init":False};
    i=init;
    LEN=len(str_);
    THE_END=False;#Para saber si terminó la cadena.
    while i<LEN:
        char=str_[i];
        if char in "\"'":#Si es un string ("",'')
                if is_str["type"]=="":#Es el inicio de la cadena.
                    is_str["type"]='"' if char=='"' else "'";
                    is_str["init"]=True;
                    init=i;
                elif char==is_str["type"]:#Si no es un signo de escape(\" o \') entonces se cierra la cadena.
                    THE_END=True;
                    break;
        if is_str["type"]!="":
            if char=='\\':#Scapamos cualquier caracter.
                i+=1;
        #Ocurre un error cuando hacen: "hola\\""
        i+=1;
    if len(is_str["type"])==0:
        return "";
    return {"init":init,"end":i,"THE_END":THE_END};

class Token(TOKEN_VARS):
    precedencia = {
            1:"+-()",
            2:"~&|",
            3:"*/%^"
    }

    tipos = {
        2: "ENTERO",
        3: "FLOAT",
        6: "STRING",
        9: "ARRAY",
        12: "BOOLEAN",
        13: "NADA"
    }

    def __init__(self, texto:str):
        self.clasf_token(texto)
    
    def clasf_token(self, texto:str):
        #texto = texto.replace("'", '"')#se quita por que sino se puede cambiar el signo del texto anidado: imprimir("hola 'como estas' tu") -> hola "como estas" tu
        self.tipo = None
        self.texto = texto
        if texto in "*^/+-%":
            self.tipo = Token.OPERADOR
            self.precedencia = [k for k,v in Token.precedencia.items() if texto in v][0]
        elif texto in ["None","NADA"]: self.tipo = Token.NADA
        elif texto in ["verdadero", "falso", "True", "False"]:
            self.tipo = Token.BOOLEAN
        elif texto in ["iterar","para"]:
            self.tipo = Token.FOR
        elif texto == "mientras":
            self.tipo = Token.WHILE
        elif texto == "retornar": self.tipo = Token.RETURN
        elif texto in ["si", "o", "sino"]: self.tipo = Token.CONDICION
        elif texto.isnumeric():
            self.tipo = Token.ENTERO
        elif texto[0].isnumeric() or texto[0] in ".,": #numeros flotantes
            texto = check_float(texto)
            if texto: self.tipo = Token.FLOAT
        elif texto.isalnum() and texto[0].isalpha():
            self.tipo = Token.IDENTIFICADOR
        elif texto == "=":
            self.tipo = Token.ASIGNACION
        elif texto[0] in "\"'":
            self.tipo = Token.STRING
            self.texto = texto[1:-1]

    def _get_value(self):
        vals = {
            Token.ENTERO: lambda x: int(x),
            Token.FLOAT: lambda x: float(x),
            Token.ARRAY: lambda x: x[1:-1].split(",")
        }
        return vals[self.tipo](self.texto) if self.tipo in vals.keys() else self.texto

    def get_type(self)->str:
        return Token.tipos[self.tipo] if self.tipo in Token.tipos else self.texto

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
        if type(other) == Token: other = other._get_value()
        return self._get_value() == other

    def __add__(self, other):
        if type(other) == Token: other = other._get_value()
        self.clasf_token(f"{self._get_value() + other}")
        return self

    def __sub__(self, other):
        if type(other) == Token: other = other._get_value()
        self.clasf_token(f"{self._get_value() - other}")
        return self

    def __mul__(self, other):
        if type(other) == Token: other = other._get_value()
        self.clasf_token(f"{self._get_value() * other}")
        return self

    def __div__(self, other)->float:
        if type(other) == Token: other = other._get_value()
        self.clasf_token(f"{self._get_value() / other}")
        return self

    def __floordiv__(self, other)->int:
        if type(other) == Token: other = other._get_value()
        self.clasf_token(f"{self._get_value() // other}")
        return self

    def __pow__(self, other):
        if type(other) == Token: other = other._get_value()
        self.clasf_token(f"{self._get_value() ** other}")
        return self

    def __mod__(self, other):
        if type(other) == Token: other = other._get_value()
        self.clasf_token(f"{self._get_value() % other}")
        return self

    def __lt__(self, other)->bool:
        if type(other) == Token: other = other._get_value()
        return self._get_value() < other

    def __gt__(self, other)->bool:
        if type(other) == Token: other = other._get_value()
        return self._get_value() > other

    def __bool__(self):
        if self.tipo == Token.BOOLEAN:
            return True if self.texto.lower == "verdadero" else False
        return False if self.texto in ["", 0] else True

    def __getitem__(self, i):
        return self.texto[i]
class Tokenizer():
    def __init__(self, pgma:list):
        self.tokens = self._tokenizer(pgma)
    def __iter__(self):
        return self
    
    def __next__(self)->Token:
        return next(self.tokens)

    def _tokenizer(self, pgma)->Token: 
        for line in pgma:
            linea:str = line.strip()
            largo = len(linea)
            i = 0
            while i < largo:
                inicio = i

                while linea[i] == ' ' and i < largo:
                    i += 1
                if i==largo: break

                car = linea[i]
                if linea[i] in operadores:
                    yield Token(car)
                    i+=1;
                elif car in "'\"":
                    tmp=search_sub_str(linea,inicio);
                    yield Token(scape_str(linea[tmp["init"]:tmp["end"]+1])["str"]);
                    i=tmp["end"]+1;
                else:
                    inicio = i
                    i += 1
                    while i < largo and linea[i] not in operadores and linea[i] != ' ':
                        i += 1
                    yield Token(linea[inicio:i])
    
    def skip_tokens(self, skip)->Token:
        try:
            for _ in range(skip):
                self.__next__();
                if not self.tokens: break
            n = self.__next__();
        except StopIteration:
            n = None
        return n

    def tmp_iter(self, iterable:list):
        self._temporal_iterable = iterable.copy()
        self.tokens = iter(self._temporal_iterable[:])

    def __enter__(self):
        tks = []
        try:
            for tk in self.tokens:
                if tk and tk.texto==":": break
                elif not tk: exit("EOF Error")
                tks.append(tk)
        except StopIteration: 
            pass
        self.prov = self.tokens
        tks.append(Token(";"))
        self.tokens = iter(tks)
        return self

    def __exit__(self, *args):
        self.tokens = self.prov
        del self.prov
    
    def __repr__(self):
        return f"{self.tokens}"
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

variables = {
    "imprimir": lambda x: print(*x),
    "print": lambda x:print(*x),
    "tipo": lambda x: x[0].get_type(),
    "leer": lambda x: input(*x)
}

operaciones_igualdad = {
    "=": lambda x,y: x==y,
    ">=": lambda x,y: x>=y,
    "<=": lambda x,y: x<=y,
    ">": lambda x,y: x>y,
    "<": lambda x,y: x<y
}
###############################################For commint:
class ERROR_Function_Not_Define(Exception):#Para identificar las excepciones que se lazan.
    def __init__(self,msg="Funcion sin declarar."):
        self.message=msg;
#imprimir("hola mundo\n\"//dsad");//No debe aparecer
def call_function(func:str, tokens:Tokenizer, scope_vars=variables):
    tmp_tokens = []
    if func in scope_vars or func in variables:
        place = scope_vars if func in scope_vars else variables
        args, pre_args, END, tk = [], [], 1, True
        for tk in tokens:
            if tk.texto == ";" and tk.tipo is None: exit("Sintaxis Inválida")
            if tk.texto == "(": END+=1
            elif tk.texto == ")":
                END-=1
                if END==0: 
                    tmp_tokens = pre_args[:]
                    if tmp_tokens: 
                        args.append(eval_expresion(iter(tmp_tokens), scope_vars))
                    break
            elif tk.texto!=",": pre_args.append(tk)
            elif tk.texto == "," and END==1: 
                tmp_tokens = pre_args[:]
                args.append(eval_expresion(iter(tmp_tokens), scope_vars))
        else: exit("Sintaxis invalida: Falta cerrar el parentesis.");
        r= place[func](args)
        return r
    else:
        raise ERROR_Function_Not_Define(f"No se ha declarado la función {func}")

def proc_array(exp:Tokenizer, scope_vars=variables)->Token:
    args = []
    tokens = []
    for n_tk in exp:
        if n_tk is None: break
        elif n_tk.texto == ",":
            if tokens: args.append(eval_expresion(iter(tokens), scope_vars))
            continue
        elif n_tk.texto == "[":
            n_tk = proc_array(exp)
            args.append(n_tk)
            continue
        elif n_tk.texto == "]": 
            if tokens: args.append(eval_expresion(iter(tokens), scope_vars))
            break
        tokens.append(n_tk)
    
    tk = Token("")
    tk.tipo = Token.ARRAY
    tk.texto = args
    return tk

def eval_expresion(exp:Tokenizer, scope_vars=variables):
    my_Stack = Stack(exp, scope_vars)
    flag, maybe = None, None
    try:
        for tk in exp:
            if maybe and tk.texto=="(":
                my_Stack.valores.pop(-1)
                my_Stack.add_valores(call_function(maybe[1].texto, exp, scope_vars))
                maybe = False
            else:
                if tk.texto == ";" and tk.tipo == None: break
                elif tk.texto == "[": 
                    arr = proc_array(exp, scope_vars)
                    my_Stack.add_valores(arr)
                elif flag:
                    f = flag
                    flag = False
                    if f[1] == "=":
                        if tk.texto == "=":
                            ant = arithmetic_operators[my_Stack.operadores[-1][0]](*my_Stack.valores) if len(my_Stack.valores)!=1 else my_Stack.valores[-1]
                            val = ant == eval_expresion(exp, scope_vars)
                            return val
                        raise SyntaxError(f"Token inesperado {tk}")
                    elif f[1] in "!~ ": return not tk
                    elif f[1] in "<>":
                        ant = arithmetic_operators[my_Stack.operadores[-1][0]](*my_Stack.valores) if\
                            len(my_Stack.valores)!=1 else my_Stack.valores[-1]
                        
                        if tk.texto == "=": 
                            val = operaciones_igualdad[f"{f[1]}="](ant,next(exp)._get_value())
                        else: val = operaciones_igualdad[f"{f[1]}"](ant,tk._get_value())
                        return val
                        
                    else: raise SyntaxError(tk)
                else:
                    r = my_Stack.def_precedencia(tk)
                    if r: flag = True,tk.texto
                    if tk.tipo == Token.IDENTIFICADOR: maybe=True,tk

    except StopIteration:
        pass

    vals,ops = my_Stack.get_Stack()
    res = arithmetic_operators[ops[-1][0]](*vals) if len(vals)>=1 and len(ops)>=1 else vals[-1]

    if type(res)!=Token: res = Token(f"{res}")
    return res
        
def asignacion(token:Token, val:Tokenizer, scope_vars=variables)->None:
    scope_vars[token.texto] = eval_expresion(val)

def exec_function(this, params, code):
    locales = dict(zip(this, *params))
    tk = Tokenizer([])
    tk.tmp_iter(code)
    return run(tk, scope_vars=locales, Func=True)

def proc_for(pgma:Tokenizer, scope_vars=variables)->tuple:
    control_var = next(pgma)
    code = []
    n = next(pgma)
    if n.texto == "en": 
        with pgma as loop:
            iterable = eval_expresion(loop, scope_vars)
        n = next(pgma)
    elif n.texto == "desde":
        with pgma as loop:
            inicio = next(pgma).texto
            next(pgma)
            fin = next(pgma).texto
            paso = 1 if next(pgma).texto == ":" else pgma.skip_tokens(1)
            paso = int(1 if paso is None else paso )
        iterable = range(int(inicio),int(fin), paso)
    n = next(pgma)
    try:
        END = 1
        for n in pgma:
            if n.texto == "START": END += 1  
            elif n.texto == "END": END-=1
            if END==0:break
            code.append(n)
    except AttributeError:
        exit("EOF Error")
    except StopIteration:
        pass
    return control_var, iterable, code

def create_func(pgma:Tokenizer, n:Token, scope_vars=variables)->None:
    args, code = [],[]
    name = n.texto
    for n in pgma:
        if n.texto ==":": break
        elif n.tipo: args.append(n.texto)
    pgma.skip_tokens(1)
    END = 1
    for n in pgma:
        if n.texto == "START" : END +=1
        elif n.texto == "END": END -=1
        if n and END!=0: code.append(n)
        elif n.texto=="END" and END==0: break
    scope_vars[name] = lambda *x: exec_function(this=args, params=x, code=code.copy())

def proc_cond(pgma:Tokenizer, tk:Token, scope_vars:dict, Func=None)->bool:
    if tk.texto != "si": exit("Sentencia inválida;")
    with pgma as condition:
        expr = eval_expresion(condition, scope_vars)

    tokens = []
    pgma.skip_tokens(1)
    for tk in pgma:
        if tk.texto == "END":break
        elif tk is None: exit("EOF ERROR")
        tokens.append(tk)
    
    tks = pgma.tokens
    pgma.tmp_iter(tokens)
    if expr: expr=run(pgma, Func=Func)
    pgma.tokens = tks;
    #Cuando se anidan los "si", pgma se vuelve una lista y no un generator, por lo que no debes llamar a la funcion next(pgma)
    for i in pgma:
        if i.texto!=';': exit("EOF ERROR");
        next(pgma);
        break;
    return expr

def proc_while(pgma:Tokenizer)->tuple:
    with pgma as condition:
        while_condition = [x for x in condition]
    pgma.skip_tokens(1)
    
    code, END = [], 1
    for n in pgma:
        if n.texto == "START": END += 1  
        elif n.texto == "END": END-=1
        if END == 0 or not n: break
        code.append(n)
    if next(pgma).texto != ";": exit("EOL Error")
    return while_condition, code

def run(pgman:Tokenizer = None, scope_vars=variables, Func=None, continue_for=None):
    for tkn in pgman:
        if continue_for: 
            if tkn.texto in ["o","sino"] and tkn.tipo == Token.CONDICION: 
                if not result_cond and tkn.texto == "o": 
                    scope_vars = proc_cond(pgman, next(pgman), scope_vars, Func=Func)
                elif not result_cond and tkn.texto == "sino": 
                    if next(pgman).texto!=":": exit("EOL Error")
                    scope_vars = run(pgman, scope_vars, Func=Func)
                else:
                    for tk in pgman:
                        for tk in pgman:
                            if tk.texto=="END": break
                        if tk.texto =="o":break
                    scope_vars=result_cond
            continue_for=None
            continue
        if tkn is None: break
        elif tkn.tipo == Token.IDENTIFICADOR:
            n = next(pgman)
            if n.tipo == Token.ASIGNACION:
                asignacion(tkn, pgman, scope_vars)
            elif n.texto == "(":
                call_function(tkn.texto, pgman, scope_vars)
            elif n.texto == "[": #setitem array
                i,args = 1,[]
                while i!=0:
                    n_tk = next(pgman)
                    if n_tk =="[": 
                        i+=1
                        continue
                    elif n_tk=="]": 
                        i-=1
                        continue
                    args.append(tk)
                n = next(pgman)
                if n.tipo != Token.ASIGNACION: raise SyntaxError(f"error de sintaxis en {n.texto}")
                asignacion(tk[args[0]], pgman)
            elif n.tipo == Token.IDENTIFICADOR and tkn.texto == "func":
                create_func(pgman, n,scope_vars)
        elif tkn.tipo == Token.FOR:
            control_variable, iterable, code = proc_for(pgman, scope_vars)
            temp_tk = Tokenizer([])
            for x in iterable:
                temp_tk.tmp_iter(code)
                scope_vars[control_variable.texto] = x
                scope_vars = run(temp_tk, scope_vars, Func=Func)
        elif tkn.tipo == Token.WHILE:
            condition_while, codec = proc_while(pgman)
            temp_tk = Tokenizer([])
            while eval_expresion(iter(condition_while.copy()), scope_vars):
                temp_tk.tmp_iter(codec)
                scope_vars = run(temp_tk, scope_vars, Func=Func)
        elif tkn.tipo == Token.CONDICION:
            if continue_for == None: 
                result_cond = proc_cond(pgman, tkn, scope_vars, Func=Func)
                continue_for = True
        elif tkn.tipo == Token.RETURN:    
            if Func: return eval_expresion(pgman, scope_vars)
            exit("retornar no está dentro de una función")
    return scope_vars if not Func else Token("None") if type(scope_vars)==dict else scope_vars

def deleted_comment_line(str_:str,is_mult_lineas=False) -> str:
    """Descripción:
        [Funcion que pide una cadena y elimina todos los comentarios de esa cadena: del # in str_, pero deja intacto los comentarios dentro de la sub-cadena: imprimir("hola#mundo");#no aparecera -> imprimir("hola#mundo");]
    
    Arguments:
        str_ {str} -- [trozo de codigo para eliminar los comentarios.]
    
    Keyword Arguments:
        is_mult_lineas {bool} -- [Permite decidir si se quiere analizar varias lineas o solo una, esto asegura velocidad cuando no es necesario varias lineas.] (default: {False})
    
    Returns:
        str -- [Trozo de codigo sin comentarios○.]
    """
    init_comment=False;
    exit_="";
    i=0;
    MAX_LEN=len(str_);
    init_exit=0;
    while i < MAX_LEN:
        char=str_[i];
        if init_comment:
            if not is_mult_lineas:#Si no necesitamos ver mas de una linea entonces eliminamos.
                break;
            
            if char=='\n':#Si llegamos al final de linea entonces comenzamos otra vez, pero sin reiniciar el bucle.
                init_comment=False;
                init_exit=i;
        else:#Si no es un comentario:
            if char=='#':#Vemos si es un digito.
                init_comment=True;
                exit_+=str_[init_exit:i];#Como tenemos el inicio y el fin de la cadena sin los comentarios, lo aprevechamos.
                i+=1;
                continue;
            
            if char in "\"'":#Si es un string ("",'')
                i=search_sub_str(str_,i)["end"];#Solo necesitamos saber donde termina la linea para no tratar la cadena pasada por el usuario.
        i+=1;
    return exit_ if init_comment else exit_+str_[init_exit:i+1];
if __name__ == "__main__":
    file = argv[1] if len(argv)>1 else None
    if file:
        with open(f"{file}") as f:
            pgma = [deleted_comment_line(line.strip()) for line in f.readlines()]
        pgma = Tokenizer(pgma)
        run(pgman=pgma, scope_vars=variables)
    else:
        def starts_with(cadena:str, iterable:list):
            return any(cadena.startswith(x) for x in iterable)
        while True:
            pgma = []
            entrada = deleted_comment_line(input(">>> ").strip());#Primero eliminamos los comentarios.
            pgma.append(entrada)
            if starts_with(entrada, ["si", "sino", "mientras", "func", "iterar", "para"]) and entrada[-1] == ":":
                level=0;
                while True:
                    #Le damos una vista al usuario sobre el nivel de profundidad.
                    entrada = deleted_comment_line(input((' '*level)+"... ").strip());
                    tmp=entrada.upper();
                    #Distingimos el nivel de en que se encuentra.
                    if tmp.startswith("START"):#Se queda porque así podemos saber facilmente si es el inicio del codigo o nó, despues veo si puedo usar ":"
                        level+=1;
                        entrada=tmp;#Me pareció incomodo siempre tener que escribir en mayuscula esto.
                    elif tmp.startswith("END"):
                        level-=1;
                        entrada=tmp;
                        if level==0:#Ya llegamos a la superficie.
                            pgma.append(entrada);
                            break;
                    pgma.append(entrada)
                runner = Tokenizer(pgma)
                variables = run(runner)
                continue
            elif entrada and entrada[-1] !=";": 
                print("EOL Error")
                continue
            elif entrada == "exit();": break
            runner = Tokenizer(pgma)
            variables = run(runner)