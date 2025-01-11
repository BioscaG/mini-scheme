from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import ParseCancellationException
import sys
from schemeLexer import schemeLexer
from schemeParser import schemeParser
from schemeVisitor import schemeVisitor


# -------------------------------
# 1. ErrorListener personalizado
# -------------------------------
class MyErrorListener(ErrorListener):
    """
    Listener personalizado para manejar errores de sintaxis durante el parseo.
    """
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ParseCancellationException("")


# -------------------------------
# 2. Clases de entorno y funciones
# -------------------------------
class Function:
    """
    Representa una función definida por el usuario con parámetros y cuerpo.
    """
    def __init__(self, params, body):
        """
        Inicializa una instancia de Function.

        :param params: Lista de nombres de parámetros
        :param body: Lista de expresiones que representan el cuerpo de la función
        """
        self.params = params
        self.body = body

class Environment:
    """
    Administra el alcance de variables y funciones.
    """
    def __init__(self, parent=None):
        """
        Inicializa una instancia de Environment.

        :param parent: Entorno padre para ámbitos anidados
        """
        self.parent = parent
        self.functions = {}
        self.constants = {}

    def define_function(self, name, value):
        """
        Define una nueva función en el entorno.

        :param name: Nombre de la función
        :param value: Instancia de la función
        """
        self.functions[name] = value

    def define_constant(self, name, value):
        """
        Define una nueva constante en el entorno.

        :param name: Nombre de la constante
        :param value: Valor de la constante
        """
        self.constants[name] = value

    def lookup_constant(self, name):
        """
        Busca una constante en el entorno.

        :param name: Nombre de la constante
        :return: Valor de la constante o el nombre si no se encuentra
        """
        if name in self.constants:
            return self.constants[name]
        elif self.parent:
            return self.parent.lookup_constant(name)
        else:
            return name

    def lookup_function(self, name):
        """
        Busca una función en el entorno.

        :param name: Nombre de la función
        :return: Instancia de la función o el nombre si no se encuentra
        """
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.lookup_function(name)
        else:
            return name


def custom_print(value):
    """
    Función de impresión personalizada para formatear y mostrar valores.

    :param value: Valor a imprimir
    """
    if isinstance(value, list):
        formatted_list = '({})'.format(' '.join(map(str, value)))
        print(formatted_list, end='')
    elif isinstance(value, bool):
        print('#t' if value else '#f', end='')
    elif isinstance(value, float):
        if value.is_integer():
            print(int(value), end='')
        else :
            print(value, end='')
    else:
        print(value, end='')


# -------------------------------
# 3. Visitante (EvalVisitor)
# -------------------------------
class EvalVisitor(schemeVisitor):
    """
    Clase visitante para evaluar el código Scheme parseado.
    """
    def __init__(self):
        """
        Inicializa una instancia de EvalVisitor.
        """
        self.env = [Environment()]
        self.basic_operations = {
            '+':  lambda x, y: x + y,
            '-':  lambda x, y: x - y,
            '*':  lambda x, y: x * y,
            '**': lambda x, y: x ** y,
            '/':  lambda x, y: x / y,
            '<':  lambda x, y: x < y,
            '>':  lambda x, y: x > y,
            '=':  lambda x, y: x == y,
            '<=': lambda x, y: x <= y,
            '>=': lambda x, y: x >= y,
            'not': lambda x: not x,
            'and': lambda x, y: x and y,
            'or':  lambda x, y: x or y,
            'mod': lambda x, y: x % y
        }
        self.basic_functions = [
            'if', 'cond', 'display', 'car', 'cdr', 'cons',
            'null?', 'let', 'read', 'newline'
        ]

    def visitRoot(self, ctx):
        """
        Inicia el proceso de evaluación.

        :param ctx: Contexto del árbol de parseo
        :return: Lista de resultados de evaluar los hijos
        """
        results = [self.visit(child) for child in ctx.getChildren()]
        self.function_call('main', [])
        return results

    def if_aux(self, cond, args):
        """
        Función auxiliar para evaluar expresiones 'if'.

        :param cond: Condición a evaluar
        :param args: Lista de expresiones para las ramas 'then' y 'else'
        :return: Resultado de la rama evaluada
        """
        return self.visit(args[0]) if cond else self.visit(args[1])

    def function_define(self, childs):
        """
        Define una nueva función.

        :param childs: Lista de nodos hijos que representan la definición de la función
        """
        func_info = list(childs[0].getChildren())
        func_name = func_info[1].getText()
        params = [param.getText() for param in func_info[2:-1]]
        body = childs[1:]
        func = Function(params, body)
        self.env[-1].define_function(func_name, func)

    def constant_define(self, childs):
        """
        Define una nueva constante.

        :param childs: Lista de nodos hijos que representan la definición de la constante
        """
        name = childs[0].getText()
        value = self.visit(childs[1])
        self.env[-1].define_constant(name, value)

    def function_call(self, func_name, args):
        """
        Ejecuta una función definida por el usuario.

        :param func_name: Nombre de la función a llamar
        :param args: Lista de argumentos para la función
        :return: Resultado de la ejecución de la función
        """
        function = self.env[-1].lookup_function(func_name)
        args = [self.visit(arg) for arg in args]
        local_env = Environment(self.env[0])
        for param, arg in zip(function.params, args):
            local_env.define_constant(param, arg)
        self.env.append(local_env)
        result = None
        for expr in function.body:
            result = self.visit(expr)
        self.env.pop()
        return result

    def handle_let(self, args):
        """
        Maneja expresiones 'let'.

        :param args: Lista de argumentos para la expresión 'let'
        :return: Resultado de la evaluación de la expresión 'let'
        """
        local_env = Environment(self.env[-1])
        variables = list(args[0].getChildren())[1:-1]
        for var in variables:
            var2 = list(var.getChildren())[1:-1]
            local_env.define_constant(var2[0].getText(), self.visit(var2[1]))
        self.env.append(local_env)
        result = None
        for expr in args[1:]:
            result = self.visit(expr)
        self.env.pop()
        return result

    def list_aux(self, args):
        """
        Función auxiliar para evaluar expresiones de lista.

        :param args: Lista de argumentos a evaluar
        :return: Lista de argumentos evaluados
        """
        return [self.visit(param) for param in args]

    def basic_function_call(self, func_name, args):
        """
        Ejecuta una función básica.

        :param func_name: Nombre de la función básica a llamar
        :param args: Lista de argumentos para la función
        :return: Resultado de la ejecución de la función
        """
        if func_name == 'if':
            return self.if_aux(self.visit(args[0]), args[1:])
        elif func_name == 'cond':
            for arg in args:
                childs = list(arg.getChildren())
                cond = self.visit(childs[1])
                if cond:
                    return self.visit(childs[2])
        elif func_name == 'display':
            custom_print(self.visit(args[0]))
            return
        elif func_name == 'car':
            return self.visit(args[0])[0]
        elif func_name == 'cdr':
            return self.visit(args[0])[1:]
        elif func_name == 'cons':
            return [self.visit(args[0])] + self.visit(args[1])
        elif func_name == 'null?':
            return self.visit(args[0]) == []
        elif func_name == 'let':
            return self.handle_let(args)
        elif func_name == 'read':
            return int(input())
        elif func_name == 'newline':
            print()
            return

    def visitExpression(self, ctx):
        """
        Visita un nodo de expresión en el árbol de parseo.

        :param ctx: Contexto del árbol de parseo
        :return: Resultado de la expresión evaluada
        """
        childs = list(ctx.getChildren())
        start = childs[0].getText()
        childs = childs[1:-1]

        if start == '(':
            operation = self.visit(childs[0])
            if operation == 'define':
                if childs[1].getText().startswith('('):
                    self.function_define(childs[1:])
                else:
                    self.constant_define(childs[1:])
            elif operation in self.basic_operations:
                return self.basic_operations[operation](
                    self.visit(childs[1]),
                    self.visit(childs[2])
                )
            elif operation in self.basic_functions:
                return self.basic_function_call(operation, childs[1:])
            else:
                return self.function_call(operation, childs[1:])
        elif start == '\'(':
            return [self.visit(param) for param in childs]

    def visitBool(self, ctx):
        """
        Visita un nodo booleano en el árbol de parseo.

        :param ctx: Contexto del árbol de parseo
        :return: Valor booleano
        """
        return list(ctx.getChildren())[0].getText() == '#t'

    def visitNum(self, ctx):
        """
        Visita un nodo numérico en el árbol de parseo.

        :param ctx: Contexto del árbol de parseo
        :return: Valor entero
        """
        return int(list(ctx.getChildren())[0].getText())

    def visitOp(self, ctx):
        """
        Visita un nodo de operador en el árbol de parseo.

        :param ctx: Contexto del árbol de parseo
        :return: Operador como cadena
        """
        return list(ctx.getChildren())[0].getText()

    def visitId(self, ctx):
        """
        Visita un nodo de identificador en el árbol de parseo.

        :param ctx: Contexto del árbol de parseo
        :return: Valor del identificador desde el entorno
        """
        id = list(ctx.getChildren())[0].getText()
        #Si el identificador es una constante, se busca en el entorno. Si no, se retorna el identificador.
        return self.env[-1].lookup_constant(id)

    def visitStr(self, ctx):
        """
        Visita un nodo de cadena en el árbol de parseo.

        :param ctx: Contexto del árbol de parseo
        :return: Valor de la cadena sin comillas
        """
        return list(ctx.getChildren())[0].getText()[1:-1]


# -------------------------------
# 4. Código principal (main)
# -------------------------------
if len(sys.argv) < 2:
    print("Usage: python3 scheme.py <input_file>")
    sys.exit(1)

program = sys.argv[1]

input_stream = FileStream(program, encoding="utf-8")

lexer = schemeLexer(input_stream)
lexer.removeErrorListeners()
lexer.addErrorListener(MyErrorListener())

token_stream = CommonTokenStream(lexer)

parser = schemeParser(token_stream)
parser.removeErrorListeners()
parser.addErrorListener(MyErrorListener())

try:
    tree = parser.root()

    visitor = EvalVisitor()

    visitor.visit(tree)

except ParseCancellationException as pce:
    print(f"\033[31mSe encontró un error de sintaxis {pce}\033[0m")
    sys.exit(1)