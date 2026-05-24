from fastapi import FastAPI, Request
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
            html += f"<td>{round(value, 2)}</td>"
        html += "</tr>"
    html += "</table>"
    return html


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, size: int = 3):
    # O tamanho padrão inicial será 3x3, mas aceita qualquer valor via URL (?size=4)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"result": None, "size": size}
    )


@app.post("/", response_class=HTMLResponse)
async def calculate(request: Request):
    # Captura todos os dados do formulário dinamicamente
    form_data = await request.form()
    size = int(form_data.get("size", 3))

    # Monta a lista bidimensional baseada no tamanho escolhido
    matrix_list = []
    for i in range(size):
        row = []
        for j in range(size):
            # Busca o valor usando a máscara de nome que definimos no HTML (ex: a_0_1)
            val = float(form_data.get(f"a_{i}_{j}", 0))
            row.append(val)
        matrix_list.append(row)

    # O NumPy aceita essa lista de qualquer tamanho instantaneamente!
    A = np.array(matrix_list)

    determinant = np.linalg.det(A)
    transpose = A.T
    negative = -A

    inverse = None
    multiplication = None

    # Evita problemas de precisão de ponto flutuante comparando com uma tolerância pequena
    if abs(determinant) > 1e-9:
        inverse = np.linalg.inv(A)
        multiplication = np.dot(A, inverse)
    else:
        determinant = 0.0  # Limpa resíduos floats caso seja numericamente zero

    result = {
        "original": matrix_to_html(A),
        "determinant": round(determinant, 2),
        "transpose": matrix_to_html(transpose),
        "negative": matrix_to_html(negative),
        "inverse": matrix_to_html(inverse) if inverse is not None else "Não possui inversa (Determinante é zero)",
        "multiplication": matrix_to_html(multiplication) if multiplication is not None else "Não disponível"
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"result": result, "size": size}
    )
