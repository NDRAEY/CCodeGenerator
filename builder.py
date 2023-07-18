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
        return "\"" + str(self.value) + "\""

class Reference(Single):
    def __str__(self):
        return "&" + str(self.value)

class Dereference(Single):
    def __str__(self):
        return "*" + str(self.value)

class Pointer(Single):
    def __str__(self):
        return str(self.value) + "*"

@dataclass
class TypeCast:
    type_: str
    value: Any

    def __str__(self):
        return "(" + str(self.type_) + ")" + str(self.value)

@dataclass
class Subscript:
    value: Any
    index: Any

    def __str__(self):
        return str(self.value) + "[" + str(self.index) + "]"

@dataclass
class ParameterList:
    arguments: list[CTypeVar]

    def __str__(self):
        temp = [str(i) for i in self.arguments]
        strtemp = ""

        for i in temp:
            strtemp += i + ", "

        return strtemp[:-2]

@dataclass
class ArgumentList:
    arguments: list[Any]

    def __str__(self):
        temp = [str(i) for i in self.arguments]
        strtemp = ""

        for i in temp:
            strtemp += i + ", "

        return strtemp[:-2]

@dataclass
class FunctionCall:
    name: str
    arguments: ArgumentList

    def __str__(self):
        return str(self.name) + "(" + str(self.arguments) + ")"

class CCode:
    def __init__(self):
        self.preproc_code = ""
        self.definition_code = ""
        self.function_code = ""
        self.main_code = ""

    def include_local(self, path: str):
        self.preproc_code += "#include " + "\"" + path + "\"\n"

    def include_global(self, path: str):
        self.preproc_code += "#include " + "<" + path + ">\n"

    def eval_binop(self, tree: Add | Sub | Mul | Div):
        if type(tree) not in (Add, Sub, Mul, Div):
            return tree
        else:
            return str(tree)

    def add_func(self, type_: str | None, name: str, args: ParameterList, code_, static: bool = False):  # code_: CCode
        type_ = type_ or "void"

        if static:
            type_ = "static " + type_
    
        code = type_ + " "
        code += name + "("

        code += str(args)
        
        code += ") {\n"
        
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

        self.definition_code += code + "\n"

    def variable_set(self, name: str, value: str):
        self.main_code += name + " = " + str(value) + ";\n"

    def call_func(self, fc: FunctionCall):
        self.main_code += str(fc) + ";\n"

    def generate(self):
        return self.preproc_code + "\n" + self.definition_code + "\n" \
               + self.function_code + "\n" + self.main_code

if __name__ == "__main__":
    code = CCode()
    main = CCode()

    code.include_global("stdio.h")

    main.add_variable_definition(
        CTypeVar("char*", "pokemon"),
        String("Pikachu")
    )

    main.call_func(
        FunctionCall(
            "printf",
            ArgumentList([
                String(r"%p\n"),
                "pokemon"
            ])
        )
    )
    
    code.add_func("int", "main", ParameterList([]), main)

    print(code.generate())
