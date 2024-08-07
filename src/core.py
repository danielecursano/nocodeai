def add(a: int, b: int): return a + b
def square_root(number): return number ** 0.5
def subtraction(a: int, b: int) -> int:   return a - b
def power_of_ten(n: int):    return 10**n
def power_function(number, power): return number ** power

def read_file(file_name):
  with open(file_name, 'r') as f:
    content = f.read()
  return content
def multiplication(a, b):  return a * b