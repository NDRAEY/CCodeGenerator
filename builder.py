from dataclasses import dataclass
from typing import Any

@dataclass
class CTypeVar:
    type_: str
    name: str

@dataclass
class LROperation:
    left: Any
    right: Any

class Add(LROperation): pass
class Sub(LROperation): pass
class Mul(LROperation): pass
class Div(LROperation): pass
class And(LROperation): pass
class ShLeft(LROperation): pass
class ShRight(LROperation): pass
class Or(LROperation): pass

@dataclass
class Not:
    value: Any

@dataclass
class Number:
    value: Any

def additional_to_str(val: Any) -> str:
    ty = type(val)

    if ty is CTypeVar:
        return val.type_ + " " + val.name
    elif ty is Add:
        return additional_to_str(val.left) + " + " + additional_to_str(val.right)
    elif ty is Sub:
        return additional_to_str(val.left) + " - " + additional_to_str(val.right)
    elif ty is Mul:
        return additional_to_str(val.left) + " *" + additional_to_str(val.right)
    elif ty is Div:
        return additional_to_str(val.left) + " / " + additional_to_str(val.right)
    elif ty is And:
        return additional_to_str(val.left) + " & " + additional_to_str(val.right)
    elif ty is ShLeft:
        return additional_to_str(val.left) + " << " + additional_to_str(val.right)
    elif ty is ShRight:
        return additional_to_str(val.left) + " >> " + additional_to_str(val.right)
    elif ty is Or:
        return additional_to_str(val.left) + " | " + additional_to_str(val.right)
    elif ty is Not:
        return "~" + additional_to_str(val.value)
    elif ty is Number:
        return str(val.value)
    else:
        print("CCodeGenerator: additional_to_str(): String conversion from", type(val), "is not implemented!")
        return val

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
            if type(tree) is Add:
                return "(" + self.eval_binop(tree.left) + " + " + self.eval_binop(tree.right) + ")"
            elif type(tree) is Sub:
                return "(" + self.eval_binop(tree.left) + " - " + self.eval_binop(tree.right) + ")"
            elif type(tree) is Mul:
                return "(" + self.eval_binop(tree.left) + " * " + self.eval_binop(tree.right) + ")"
            elif type(tree) is Div:
                return "(" + self.eval_binop(tree.left) + " / " + self.eval_binop(tree.right) + ")"

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
        
        code += definition.type_ + " " + definition.name

        if value:
            code += " = " + value

        code += ";"

        self.definition_code += code

    def variable_set(self, name: str, value: str):
        self.main_code += name + " = " + value + ";\n"

    def add_function_call(self, name: str, argumnets: list[CTypeVar]):
        ...

    def generate(self):
        return self.preproc_code + "\n" + self.definition_code + "\n" \
               + self.function_code + "\n" + self.main_code

if __name__ == "__main__":
    code = CCode()

    code.add_variable_definition(CTypeVar("int", "query_count"), "0")
    code.variable_set("query_count", Number(4))
    code.add_func("int", "hello", [], CCode())

    print(
        code.variable_set(
            "hello",
            code.eval_binop(
                Add(
                    "1",
                    Mul("2", "4")
                )
            )
        )
    )

    print(code.generate())
