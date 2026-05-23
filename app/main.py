
---

# 8️⃣ app/main.py

```python
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


def matrix_to_html(matrix):
    html = "<table class='table table-bordered text-center'>"

    for row in matrix:
        html += "<tr>"
        for value in row:
            html += f"<td>{round(value,2)}</td>"
        html += "</tr>"

    html += "</table>"

    return html


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": None
        }
    )


@app.post("/", response_class=HTMLResponse)
async def calculate(
    request: Request,

    a11: float = Form(...),
    a12: float = Form(...),
    a13: float = Form(...),

    a21: float = Form(...),
    a22: float = Form(...),
    a23: float = Form(...),

    a31: float = Form(...),
    a32: float = Form(...),
    a33: float = Form(...)
):

    A = np.array([
        [a11, a12, a13],
        [a21, a22, a23],
        [a31, a32, a33]
    ])

    determinant = np.linalg.det(A)

    transpose = A.T

    negative = -A

    inverse = None
    multiplication = None

    if determinant != 0:
        inverse = np.linalg.inv(A)
        multiplication = np.dot(A, inverse)

    result = {
        "original": matrix_to_html(A),
        "determinant": round(determinant, 2),
        "transpose": matrix_to_html(transpose),
        "negative": matrix_to_html(negative),
        "inverse": matrix_to_html(inverse) if inverse is not None else "Não possui inversa",
        "multiplication": matrix_to_html(multiplication) if multiplication is not None else "Não disponível"
    }

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result
        }
    )
