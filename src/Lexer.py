from src.Env import variables

def check_float(texto:str)->str:
    texto = texto.replace(",",".")
    if texto.count(".")!=1 or len(texto)<2: return
    for ch in texto:
        if not (ch.isnumeric() or ch == "."): return 
    return texto

operadores = "=(),+-*/<>[];:!~"
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
    BOOLEAN = 12
    NADA = 13

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
        texto = texto.replace("'", '"')
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
        elif texto[0] == '"':
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
                    yield Token(car)
                    i += 1

                elif car in "'\"":
                    inicio = i
                    i += 1
                    while i < largo and linea[i] != car:
                        i += 1
                    yield Token(linea[inicio:i+1])
                    i += 1

                else:
                    inicio = i
                    i += 1
                    while i < largo and linea[i] not in operadores and linea[i] != ' ':
                        i += 1
                    yield Token(linea[inicio:i])
    
    def skip_tokens(self, skip)->Token:
        try:
            for _ in range(skip):
                next(self.tokens)
                if not self.tokens: break
            n = next(self.tokens)
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