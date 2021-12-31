**Table of Contents**

[TOCM]

## Características
- Es de tipado dinámico
- Combinación de un Parser y Lexer capaz de ejecutar instrucciones básicas
- Basado en Python y en un sistema de generadores e iteradores
- Posee un modo Interactivo

```
imprimir("Hola Mundo :D");
```
### Características Internas　
La implementación de este lenguaje se basa en Python y sus generadores e iteradores que permiten obtener o procesar valores según se requieran lo que minimiza el uso de memoria. 
Un archivo de texto con extención `.psc` es recibido y primeramente pre-procesado para eliminar los comentarios indicados con `//` al inicio de una línea. El archivo se convierte en una lista donde cada línea representa un elemento en una lista Python para un posterior procesamiento de cada instrucción. 

El procesamiento se basa en la conversión de una serie de caracteres a *Tokens* gracias a un *tokenizer* implementado en una clase `Tokenizer` que genera *Token* a *Token*  y se devuelve según se necesite, esto se logra implementando el método `__iter__` para tratar a la clase como un iterador que basa su funcionamiento en el método `_tokenizer` que es un generador que devuelve un objeto de tipo `Token`. Este objeto continene la información mínima necesaria para indicar una acción. Un objeto `Token` se compone de dos atributos:
1. El tipo: De acuerdo a la secuencia de caracteres dada se analiza y se determina un tipo para esa secuencia. Ir a la sección Tipos de token para saber más
2. El valor: Es la secuencia de caracteres dada.

#### Tipos de token
Al analizar una secuencia de caracteres esta posteriormente se convierte en un *Token* que indicará un comportamiento específico para poder procesar la(s) sentencia(s). Los tokens pueden ser clasificados en:

* **OPERADOR**: Si llega a ser un operador aritmético, es decir, que el caracter sea cualquiera de los siguientes caracteres `*^/+-%`.

* **ENTERO**: En caso se determine que es un número entero.

* **FLOAT**: En caso se determine que es un número flotante o decimal. Los números decimales pueden ser expresados tanto con `.` ó `,` como separador decimal. SIn embargo **NO** se recomiendo usar `,` como indicador al estar contenido en un array ya que causará un mal procesamiento del array.

* **IDENTIFICADOR**: Los identificadores son las secuencias de caracteres que llegan a almacenar algún valor, se les denomina identificadores ya que son como un alias para indicar la posición en memoria que llega a tener un objeto, estos llegan a ser los nombre de variables y funciones. Se identifican ya que no llegan a ser números y comienzan con una letra sin estar encerrados en comillas lo que descarta ser Strings.

* **ASIGNACION**: Es el caracter `=`, esto representa la operación de asignación, la cual asocia un identificador con un objeto/valor.

* **STRING**:  En caso la secuencia de tokens este encerrada en comillas (dobles o simples) se determina como un String.

* **For**: Indica que la secuencia de caracteres llega a ser la sentencias `iterar` o `para`, que indican la iteración en un determinado rango de veces.

* **WHILE**: Indica que la secuencia de caracteres es igual a la sentecnia `mientras` que indica una iteración mientras una codición se cumpla.

* **ARRAY**: Indica que la secuencia de caracteres es un array, por defecto esto no se detecta, sino que es asignado al momento de procesar un token, en caso un token contenga como valor un corchete de apertura `[` se ejecuta una función para procesar el array y devuelve un Token cuyo tipo es **ARRAY** y el valor es una lista de Python.

* **RETURN**: En caso la secuencia de caracteres sea `retornar` se define que será una devolución para una función. En caso se encuentre fuera de una función se detiene la ejecución con un error `retornar no está dentro de una función`.

* **CONDICION**: Si la secuencia de caracteres coincide con alguna de las siguientes palabras `si`, `o`, `sino` entonces se determina que se trata de una condición.

------------

## Sintaxis
Al ser de tipado dinámico su sintaxis se hace bastante sencilla y es muy similara a muchos lenguajes. **Todas** las lineas deben tener como indicador de fin el caracter `;` **excepto** las sentencias que especifican un bloque de código, como por ejemplo la declaración de funciones, condicionales y ciclos que deberán terminar con `:`. En caso no se cumpla esto se aboratará la ejecución del programa y se genera un `EOL Error` (End Of Line Error) o `EOF Error` (End Of File Error).

### Datos
Los tipos de datos existentes son los siguientes:
- Strings: Son cadenas de texto, se indican con las comillas (simples o dobles) y dentro de ellas la cadena que se desea, por ejemplo, `"holas"`

- Enteros: Son números enteros, no se necesita de ningún caracter para especificar que se trata de uno, se puede simplemente escribir `10` y asignar esto a una variable

- Flotantes: Son números con parte decimal, pueden estar representados de la forma `10.4` ó `10,4`, es decir, usando tanto el `.` como `,`, sin embargo no se recomienda usar `,` para cuando se encuentran dentro de un array.

- Arrays: Es una estructura de dato que en la cual se puede almacenar varios valores, no se requiere especificar el tamaño del array ni que tipo de datos contendrá. Sus posiciones son indexadas desde el `0`.

**Nota**
Hasta esta versión no se soporta la asignación en los arrays, es decir, hacer `array[0] = "algo";` conllevará a algún error.

### Asignación
La asignacións se hace de igual manera en que se haría en todo lenguaje de programación pero sin especificar el tipo de dato que será o espera la variable. Un ejemplo:

    //asignanado a la variable a el entero 10
    a = 10;
	// asignando un string a una variable
	cadena = "una cadena de texto";
	//asignando un float a una variable
	f = 10.7;
	//creando un array
	arr = ["hola", "soy", "c.", 16];

La asignación responde a la sintaxis 

	<nombre_variable> = <valor>

### SIntaxis de bloques
Los bloques son sentencias que conllevan a la ejecución de un determinado código, es decir una sentencia se asocia a un pedazo de código posterior. Los bloques de código se encuentran al momento de declarar una función, ya que al llamar a la función se ejecutará el código correspondiente, también se encuentran en las condiciones, ya que se debe de ejecutar un pedazo de código según el resultado de evaluar la condición y lo mismo para los ciclos. **Todas** las sentencias que necesiten bloques de código terminan con `:`. Por lo que **Todas** las sentencias que indiquen condiciones, ciclos o funciones terminan con `:` en vez de `;`. Además en la línea siguiente debe de ir la palabra reservada `START;` para indicar el comienzo de la sentencia y `END;` para finalizarla. Estas palabras son como las llaves `{}` de JavaScript u otro lenguaje para indicar que el código pertenece a tal parte.
```
//ejemplo en condición
z = 1;
si z==1:
START;
	imprimir("es igual");
END;

//ejemplo en ciclo
iterar x desde 1 hasta 3:
START;
	imprimir(x);
END;
```

### Ciclos
Los sinclos son sentencias que repiten una acción por determinado tiempo o veces. Se tiene dos clase de tipos, los `for` y `while`. Los `for` se implementan como `iterar` o `para` y los `while` como `mientras`.

#### Iterar
Estos ciclos iteran en un iterable o en un rango, los objetos iterables con los arrays y strings. Existen dos forma de escribir este ciclo, la sintaxis de la primiera es la siguiente:

    iterar <variable_de_control> desde <inicio> hasta <final> con paso <paso>:
	START;
		//codigo
	END;

El paso se puede omitir y por efecto será `1`, lo que significa que la sentencia puede quedar tal que así:

    iterar <variable_de_control> desde <inicio> hasta <final>:
	START;
		//codigo
	END;

La sintaxis de la segunda forma es:

    para <variable_de_control> en <obj_iterable>:
	START;
		//code
	END;

Esta forma permite iterar en un iterable como lo son los arrays o strings, para esta forma **no existe paso**.