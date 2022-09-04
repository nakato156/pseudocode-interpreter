from sys import argv
from src.Lexer import Tokenizer
from src.Env import variables
from src.Evaluator import run

if __name__ == "__main__":
    file = argv[1] if len(argv)>1 else None
    if file:
        with open(f"{file}") as f:
            pgma = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith("//")]
        pgma = Tokenizer(pgma)
        run(pgman=pgma, scope_vars=variables)
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
                runner = Tokenizer(pgma)
                variables = run(runner)
                continue
            elif entrada and entrada[-1] !=";": 
                print("EOL Error")
                continue
            elif entrada == "exit();": break
            runner = Tokenizer(pgma)
            variables = run(runner)