from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

# пользовательские классы исключений
class CustomExceptionA(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class CustomExceptionB(Exception):
    def __init__(self, detail: str):
        self.detail = detail

# модели реагирования на ошибки
class ErrorResponse(BaseModel):
    error: str
    message: str

# обработчики исключений
@app.exception_handler(CustomExceptionA)
def handle_custom_exception_a(request: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=400,
        content={"error": "CustomExceptionA", "message": exc.detail},
    )

@app.exception_handler(CustomExceptionB)
def handle_custom_exception_b(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=404,
        content={"error": "CustomExceptionB", "message": exc.detail},
    )

@app.get("/trigger-a")
def trigger_a():
    raise CustomExceptionA("Произошла ошибка типа A")

@app.get("/trigger-b")
def trigger_b():
    raise CustomExceptionB("Ресурс не найден (ошибка типа B)")


@app.get("/standard-error")
def standard_error():
    raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")