
arithmetic_operators = {
    "+": lambda a,b: a+b,
    "-": lambda a,b: a-b,
    "^": lambda a,b: a**b,
    "/": lambda a,b: a.__div__(b),
    "//": lambda a,b: a//b,
    "*": lambda a,b: a*b
}

variables = {
    "imprimir": lambda x: print(*x),
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