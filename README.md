# Intérprete de Mini Scheme

Este proyecto desarrolla un intérprete para una versión simplificada del lenguaje funcional Scheme, utilizando Python y ANTLR. Scheme, derivado de Lisp, es conocido por su simplicidad y estructura basada en expresiones. Este intérprete permite ejecutar programas con funcionalidades clave como operaciones básicas, definiciones de funciones, manejo de listas y estructuras condicionales.

## Características principales

1. **Operaciones básicas**:

   - Soporte para operaciones aritméticas (`+`, `-`, `*`, `/`, `mod`), lógicas (`and`, `or`, `not`) y relacionales (`<`, `<=`, `>`, `>=`, `=`).

2. **Definición de funciones y constantes**:

   - Definición global de funciones mediante `define`.
   - Declaración de constantes inmutables.

3. **Manejo de listas**:

   - Operaciones como `car`, `cdr`, `cons` y `null?` para manipular listas.

4. **Estructuras de control**:

   - Condicionales simples (`if`) y múltiples (`cond`).

5. **Entrada y salida**:

   - Lectura de datos con `read` y escritura con `display` y `newline`.

6. **Variables locales**:

   - Soporte para declaraciones locales mediante `let`.

7. **Recursión**:

   - Capacidad para implementar funciones recursivas.

## Gramática utilizada

La gramática en formato ANTLR utilizada para procesar el lenguaje Scheme es la siguiente:

```antlr
grammar scheme;

root : expr* EOF;

expr
    : ( '\'(' | '(' ) expr* ')' #expression
    | BOOLEAN #bool
    | NUMBER #num
    | IDENTIFIER #id
    | OPERATOR #op
    | STRING #str
    ;

OPERATOR: '+'|'-'|'*'|'/'|'<'|'>'|'='|'<='|'>='|'and'|'or'|'not'|'mod';
IDENTIFIER: [a-zA-Z][a-zA-Z0-9\-]* '?'?;
NUMBER : '-'? [0-9]+ ;
BOOLEAN : '#t' | '#f';
STRING : '"' .*? '"';
WS  : [ \t\n\r]+ -> skip;
COMMENT: ';' .*? '\n' -> skip;
```

## Implementación

El intérprete está implementado en Python con las siguientes clases clave:

### Clases principales

1. **`Function`**:

   - Representa funciones definidas por el usuario, incluyendo parámetros y cuerpo.

2. **`Environment`**:

   - Maneja el ámbito de las funciones y constantes, permitiendo la evaluación contextual.

3. **`EvalVisitor`**:

   - Es el componente central que evalúa las expresiones. Recorre el árbol sintáctico generado por ANTLR y ejecuta las operaciones necesarias según el tipo de nodo.

### Detalles sobre `EvalVisitor`

#### Visión General

`EvalVisitor` es el núcleo del intérprete, responsable de traducir y ejecutar cada elemento del árbol sintáctico generado por ANTLR. Incluye funcionalidades para evaluar expresiones, realizar cálculos, manejar listas, y ejecutar estructuras de control.

#### Funcionalidades Clave

1. **Llamadas a funciones definidas por el usuario**:
   `EvalVisitor` permite ejecutar funciones creadas con `define`. Cuando se llama a una función definida por el usuario:
   - Se crea un entorno local para los parámetros de la función.
   - Se evalúa el cuerpo de la función en este entorno.
   - Se devuelve el resultado de la última expresión evaluada.

2. **Llamadas a funciones predefinidas**:
   Estas funciones están integradas en el intérprete y cubren tareas comunes como:
   - `display`: Imprime un valor en la salida estándar.
   - `if`: Evalúa una condición y ejecuta una de las dos ramas.
   - `cond`: Evalúa una lista de condiciones y ejecuta la primera verdadera.
   - Operaciones con listas como `car`, `cdr`, `cons` y `null?`.

3. **Llamadas a operadores aritméticos y booleanos**:
   Los operadores (`+`, `-`, `*`, `/`, `and`, `or`, etc.) se manejan como funciones predefinidas. Cada operador toma sus argumentos, los evalúa y devuelve el resultado de la operación.

4. **Definición de funciones y constantes**:
   - `function_define`: Guarda funciones en el entorno global.
   - `constant_define`: Asocia un nombre a un valor evaluado una sola vez.

5. **Evaluación de expresiones**:
   Determina el tipo de expresión y delega su evaluación al método correspondiente. Esto incluye:
   - Operaciones básicas.
   - Llamadas a funciones predefinidas.
   - Llamadas a funciones definidas por el usuario.

6. **Manejo de variables locales con `let`**:
   Permite definir variables temporales en un nuevo entorno. Este entorno se destruye al finalizar la evaluación.

7. **Entrada y salida**:
   - `read`: Solicita entrada del usuario y devuelve el resultado como una expresión evaluada.
   - `newline`: Imprime una nueva línea.

#### Organización del Entorno

El entorno es una estructura jerárquica que permite manejar variables y funciones, tanto globales como locales. Cada nivel del entorno se crea temporalmente al llamar a una función o al declarar un `let`, y se destruye cuando la evaluación finaliza.

## Juegos de prueba

El directorio `tests` incluye varios casos para validar el funcionamiento del intérprete:

1. **`complex_operations`**: Valida operaciones matemáticas complejas.
2. **`dynamic_calculation`**: Evalúa cálculos dinámicos basados en entrada del usuario.
3. **`filter_numbers`**: Prueba funciones de filtrado de listas.
4. **`read_and_display`**: Prueba las funciones de entrada y salida.
5. **`boolean_tests`**: Valida expresiones booleanas.
6. **`map_and_sum`**: Verifica transformaciones y acumulaciones en listas.
7. **`foldl`**: Evalúa acumulaciones con listas anidadas.

Cada prueba incluye:

- Archivo `.scm` con el código.
- Archivos `.inp` y `.out` con datos de entrada y salida esperada.

## Limitaciones

1. Las funciones deben definirse de forma global.
2. No se soportan funciones anónimas (`lambda`).

## Conclusión

Este proyecto demuestra cómo construir un intérprete funcional utilizando herramientas modernas como ANTLR y Python. Permite ejecutar programas en Mini Scheme y sirve como base para explorar más características de lenguajes funcionales.
