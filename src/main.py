# src/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.calculator import add, subtract, multiply, divide

app = FastAPI(title="Python Testing API")


class CalculationRequest(BaseModel):
    operation: str
    a: float
    b: float


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app": "python-testing"}


@app.post("/calculate")
def calculate_endpoint(request: CalculationRequest):
    """Calculates result based on operation."""
    op = request.operation.lower()

    if op == "add":
        res = add(request.a, request.b)
    elif op == "subtract":
        res = subtract(request.a, request.b)
    elif op == "multiply":
        res = multiply(request.a, request.b)
    elif op == "divide":
        try:
            res = divide(request.a, request.b)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported operation: {request.operation}")

    return {"operation": request.operation, "result": res}
