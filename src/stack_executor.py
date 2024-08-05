from core import *

OUTPUT_FLAG = 'X'

class FunctionRunner:
    def __init__(self, functions, vars):
        self.stack = functions
        self.vars = vars
        self.cache = []

    def run(self):
        for function, var in zip(self.stack, self.vars):
            if len(var) != function.__code__.co_argcount: raise ValueError("Number of arguments insufficient")
            tmp = []
            for x in var:
                if x != OUTPUT_FLAG:
                    tmp.append(x)
                else:
                    tmp.extend(self.cache)
            output = function(*tmp)
            self.cache = [output]
        return self.cache

if __name__ == "__main__":
    f = [add, power_function]
    vars = [(12, 1), ("X", 9)]
    x = FunctionRunner(f, vars)
    print(x.run())