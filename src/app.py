from fastapi import FastAPI
from routes import router 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(debug=1)
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Update this with your HTML page origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

if __name__=="__main__":
    import uvicorn 
    uvicorn.run("app:app", port=5000, reload=True)