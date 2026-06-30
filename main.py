from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from estadisticas_engine import procesar_expedientes

app = FastAPI()


@app.post("/estadisticas")
async def estadisticas(
    expedientes: UploadFile = File(...),
    mes: str = Form(...)
):

    # Ejecutar motor
    output_path = procesar_expedientes(expedientes.file, mes)

    # Nombre dinámico del archivo
    from datetime import datetime

    meses = {
        "1": "ENERO", "2": "FEBRERO", "3": "MARZO",
        "4": "ABRIL", "5": "MAYO", "6": "JUNIO",
        "7": "JULIO", "8": "AGOSTO", "9": "SEPTIEMBRE",
        "10": "OCTUBRE", "11": "NOVIEMBRE", "12": "DICIEMBRE"
    }

    mes_nombre = meses.get(mes, "MES")
    año = datetime.now().year

    filename = f"Estadísticas {mes_nombre} {año}.xlsx"

    return FileResponse(
        output_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )