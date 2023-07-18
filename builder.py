from dataclasses import dataclass
from typing import Any

@dataclass
class CTypeVar:
    type_: str
    name: str

    def __str__(self):
        return self.type_ + " " + self.name

@dataclass
class LROperation:
    left: Any
    right: Any

class Add(LROperation):
    def __str__(self):
        return "(" + str(self.left) + " + " + str(self.right) + ")"

class Sub(LROperation):
    def __str__(self):
        return "(" + str(self.left) + " - " + str(self.right) + ")"

class Mul(LROperation):
    def __str__(self):
        return "(" + str(self.left) + " * " + str(self.right) + ")"

class Div(LROperation): 
    def __str__(self):
        return "(" + str(self.left) + " / " + str(self.right) + ")"

class And(LROperation):
    def __str__(self):
        return "(" + str(self.left) + " & " + str(self.right) + ")"

class ShLeft(LROperation):
    def __str__(self):
        return "(" + str(self.left) + " << " + str(self.right) + ")"

class ShRight(LROperation):
    def __str__(self):
        return "(" + str(self.left) + " >> " + str(self.right) + ")"

class Or(LROperation):
    def __str__(self):
        return "(" + str(self.left) + " | " + str(self.right) + ")"

@dataclass
class Single:
    value: Any

class Not(Single):
    def __str__(self):
        return "(~" + str(self.right) + ")"

@dataclass
class Number:
    value: int

    def __str__(self):
        return str(self.value)

@dataclass
class String:
    value: str

    def __str__(self):
        return "\"" + self.value + "\""

class Reference(Single):
    def __str__(self):
        return "&" + str(self.value)

class Dereference(Single):
    def __str__(self):
        return "*" + str(self.value)

class Pointer(Single):
    def __str__(self):
        return str(self.value) + "*"

class TypeCast:
    type_: str
    value: Any

    def __str__(self):
        return "(" + str(type_) + ")" + str(self.value)

class CCode:
    def __init__(self):
        self.preproc_code = ""
        self.definition_code = ""
        self.function_code = ""
        self.main_code = ""

    def eval_binop(self, tree: Add | Sub | Mul | Div):
        if type(tree) not in (Add, Sub, Mul, Div):
            return tree
        else:
            return str(tree)

    def add_func(self, type_: str | None, name: str, args: list[CTypeVar], code_, static: bool = False):  # code_: CCode
        type_ = type_ or "void"

        if static:
            type_ = "static " + type_
    
        code = type_ + " "
        code += name + "("

        argsstr = ""

        for i in args:
            argsstr += i.type_ + " " + i.name + ", "

        code += argsstr[:-2] + ") {\n"
        
        code += code_.generate()

        code += "\n}"

        self.function_code += code

    def add_variable_definition(self, definition: CTypeVar, value: Any | None, static: bool = False):
        code = ""

        if static:
            code += "static "
        
        code += str(definition)

        if value:
            code += " = " + str(value)

        code += ";"

        self.definition_code += code

    def variable_set(self, name: str, value: str):
        self.main_code += name + " = " + str(value) + ";\n"

    def add_function_call(self, name: str, argumnets: list[CTypeVar]):
        ...

    def generate(self):
        return self.preproc_code + "\n" + self.definition_code + "\n" \
               + self.function_code + "\n" + self.main_code

if __name__ == "__main__":
    code = CCode()

    code.add_variable_definition(CTypeVar("int", "query_count"), Number(0))
    code.variable_set("query_count", Number(4))
    code.add_func("int", "hello", [], CCode())

    print(
        code.variable_set(
            "hello",
            code.eval_binop(
                Add(
                    Number(8),
                    Mul(
                        Number(2),
                        Number(4)
                    )
                )
            )
        )
    )

    print(code.generate())
