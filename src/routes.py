from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from model import Model
from stack_executor import FunctionRunner, OUTPUT_FLAG
from inspect import signature
import core

model = Model()
FUNCTIONS = {name: attr for name, attr in vars(core).items() if callable(attr)}
TYPES = {"str": str, "int": int, "float": float}
to_type = lambda d, type: d if d == OUTPUT_FLAG else TYPES[type](d)
function_info = lambda _: [[name, str(signature(f))] for name, f in FUNCTIONS.items()]

def parse_vars(var_str):
    # 1_int:2_int 3_int
    vars = []
    for v in var_str.split(" "):
        tmp = []
        for j in v.split(":"):
            data, type = j.split("_")
            tmp.append(to_type(data, type))
        vars.append(tmp)
    return vars

router = APIRouter()

@router.get("/info")
async def read_finfo():
    return JSONResponse(content={"info": function_info(0)}, status_code=200)

@router.post("/generate_code")
async def generate_code(prompt: str=Body(..., embed=True)):
    try:
        model.run(prompt)
        FUNCTIONS = {name: attr for name, attr in vars(core).items() if callable(attr)}
        return JSONResponse(content={"message": "Success"}, status_code=200) 
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/run_code")
async def run_code(code: str=Body(...), vars: str=Body(...)):
    code = [FUNCTIONS[x] for x in code.split(" ") if x in FUNCTIONS.keys()]
    if not code:
        return JSONResponse(content={"message": "Failed", "output": "No code given"}, status_code=400)
    vars = parse_vars(vars)
    x = FunctionRunner(code, vars)
    try:
        return JSONResponse(content={"message": "Success", "output": x.run()}, status_code=200)
    except:
        return JSONResponse(content={"message": "Failed", "output": "Couldn't run the code provided"}, status_code=400)
    
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})