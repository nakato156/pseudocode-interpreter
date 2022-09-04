from src.Lexer import Tokenizer, Token
from src.Stack import Stack
from src.Env import variables, arithmetic_operators, operaciones_igualdad

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
    pgma.tokens = tks

    if next(pgma).texto != ";": exit("EOF ERROR")
    return expr


def exec_function(this, params, code):
    locales = dict(zip(this, *params))
    tk = Tokenizer([])
    tk.tmp_iter(code)
    return run(tk, scope_vars=locales, Func=True)

def call_function(func:str, tokens:Tokenizer, scope_vars=variables):
    tmp_tokens = []
    if func in scope_vars or func in variables:
        place = scope_vars if func in scope_vars else variables
        args, pre_args, END, tk = [], [], 1, True
        for tk in tokens:
            if tk.texto == ";" and tk.tipo is None: exit("Sintaxis Inválida")
            if tk.texto == "(": END+=1
            elif tk.texto == ")": END-=1
            if END==0 and tk.texto == ")": 
                tmp_tokens = pre_args[:]
                if tmp_tokens: 
                    args.append(eval_expresion(iter(tmp_tokens), scope_vars))
                break
            elif tk.texto!=",": pre_args.append(tk)
            elif tk.texto == "," and END==1: 
                tmp_tokens = pre_args[:]
                args.append(eval_expresion(iter(tmp_tokens), scope_vars))
        else: exit("EOF Error")
        r= place[func](args)
        return r
    else:
        raise NameError(f"No se ha declarado la función {func}")



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

def asignacion(token:Token, val:Tokenizer, scope_vars=variables)->None:
    scope_vars[token.texto] = eval_expresion(val)

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
 