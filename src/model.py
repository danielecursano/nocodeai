import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def build(code:str):
    """The string code passed is written in a file using python standard functions. DO NOT UTILIZE \n char to go to the next line"""
    with open("core.py", "a") as file:
        file.write(code)
        file.write("\n")
    return 0

INSTRUCTION = """Your task is to compose Python code using the BUILD tool.
                IMPORTANT: You have access to every Python library. Please follow Python indentation rules.
                Compose the Python code using the provided tool. DO NOT utilize special characters to go to the next line.
                Use simples names for functions.
                OUTPUT: Please, You should return only the alphabetic name of the function you wrote."""
    
class Model:
    def __init__(self, model_name="models/gemini-1.5-pro-latest", instruction=INSTRUCTION, tools=[build]):
        try:
            self.model = genai.GenerativeModel(model_name, system_instruction=instruction, tools=tools)
            self.chat = self.model.start_chat(enable_automatic_function_calling=True)
        except:
            raise ValueError("Couldn't load Gemini model")
        
    def run(self, prompt):
        return self.chat.send_message(f"The problem: {prompt}")
    
if __name__ == "__main__":
    model = Model()
    response = model.run("Write a function to add 2 numbers")
    print(response.text)
    response = model.run("Write a function that calculate the square root of input")
    print(response.text)    