
# Mini Scheme Interpreter

This project develops an interpreter for a simplified version of the functional language Scheme, using Python and ANTLR. Scheme, derived from Lisp, is known for its simplicity and expression-based structure. This interpreter allows the execution of programs with key features like basic operations, function definitions, list management, and conditional structures.

## Key Features

- **Basic Operations**:
  - Support for arithmetic operations (`+`, `-`, `*`, `/`, `mod`), logical operations (`and`, `or`, `not`), and relational operations (`<`, `<=`, `>`, `>=`, `=`).
  
- **Function and Constant Definitions**:
  - Global function definitions using `define`.
  - Immutable constant declarations.
  
- **List Management**:
  - Operations like `car`, `cdr`, `cons`, and `null?` for list manipulation.
  
- **Control Structures**:
  - Simple conditionals (`if`) and multiple conditionals (`cond`).
  
- **Input and Output**:
  - Data reading with `read` and writing with `display` and `newline`.
  
- **Local Variables**:
  - Support for local declarations using `let`.
  
- **Recursion**:
  - Ability to implement recursive functions.

## Grammar Used

The ANTLR grammar used to process the Scheme language is as follows:

```antlr
grammar scheme;

root : expr* EOF;

expr
    : ( ''(' | '(' ) expr* ')' #expression
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
WS  : [ 	

]+ -> skip;
COMMENT: ';' .*? '
' -> skip;
```

## Implementation

The interpreter is implemented in Python with the following key classes:

### Main Classes

- **`Function`**:
  - Represents user-defined functions, including parameters and body.

- **`Environment`**:
  - Manages the scope of functions and constants, enabling contextual evaluation.

- **`EvalVisitor`**:
  - The central component that evaluates expressions. It traverses the syntax tree generated by ANTLR and performs the necessary operations according to the node type.

### Details about `EvalVisitor`

#### Overview

`EvalVisitor` is the core of the interpreter, responsible for translating and executing each element of the syntax tree generated by ANTLR. It includes functionalities for evaluating expressions, performing calculations, managing lists, and executing control structures.

#### Key Features

1. **User-Defined Function Calls**:
   - A local environment is created for the function parameters.
   - The function body is evaluated in this environment.
   - The result of the last evaluated expression is returned.

2. **Built-in Function Calls**:
   - `display`: Prints a value to the standard output.
   - `if`: Evaluates a condition and executes one of the two branches.
   - `cond`: Evaluates a list of conditions and executes the first true one.
   - List operations like `car`, `cdr`, `cons`, and `null?`.

3. **Arithmetic and Boolean Operator Calls**:
   - Operators (`+`, `-`, `*`, `/`, `and`, `or`, etc.) are handled as built-in functions.

4. **Function and Constant Definitions**:
   - `function_define`: Stores functions in the global environment.
   - `constant_define`: Associates a name with a value evaluated only once.

5. **Expression Evaluation**:
   - Determines the type of expression and delegates its evaluation to the corresponding method. This includes:
     - Basic operations.
     - Built-in function calls.
     - User-defined function calls.

6. **Local Variable Handling with `let`**:
   - Allows defining temporary variables in a new environment. This environment is destroyed after evaluation.

7. **Input and Output**:
   - `read`: Requests user input and returns the result as an evaluated expression.
   - `newline`: Prints a new line.

#### Environment Organization

The environment is a hierarchical structure that handles variables and functions, both global and local. Each level of the environment is temporarily created when calling a function or declaring a `let` and is destroyed when the evaluation finishes.

## Test Cases

The `tests` directory includes several cases to validate the interpreter's functionality:

1. **`complex_operations`**: Validates complex mathematical operations.
2. **`dynamic_calculation`**: Evaluates dynamic calculations based on user input.
3. **`filter_numbers`**: Tests list filtering functions.
4. **`read_and_display`**: Tests input and output functions.
5. **`boolean_tests`**: Validates boolean expressions.
6. **`map_and_sum`**: Verifies transformations and accumulations on lists.
7. **`foldl`**: Evaluates accumulations with nested lists.

Each test includes:

- A `.scm` file with the code.
- `.inp` and `.out` files with input data and expected output.

## Limitations

1. Functions must be defined globally.
2. Anonymous functions (`lambda`) are not supported.

## Conclusion

This project demonstrates how to build a functional interpreter using modern tools like ANTLR and Python. It allows the execution of Mini Scheme programs and serves as a foundation for exploring more features of functional languages.
