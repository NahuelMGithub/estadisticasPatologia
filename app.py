print("🔥 ESTOY EJECUTANDO ESTE APP.PY")

from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from io import BytesIO
import traceback
from openpyxl import load_workbook
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)


# -------------------------
# 🌐 FRONTEND
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# 🧪 TEST
# -------------------------
@app.route("/ping")
def ping():
    return "OK"


# -------------------------
# 🧠 LECTURA INTELIGENTE
# -------------------------
def leer_archivo(file, filename):
    filename = filename.lower()

    try:
        content = file.read()
        file.seek(0)

        contenido_lower = content.lower()
        es_html = (
            b"<html" in contenido_lower
            or b"<table" in contenido_lower
            or b"<style" in contenido_lower
            or b"<!doctype" in contenido_lower
        )

        if es_html:
            html_str = content.decode("utf-8", errors="ignore")
            tables = pd.read_html(html_str)
            return tables[0]

        elif filename.endswith(".xlsx"):
            return pd.read_excel(BytesIO(content), engine="openpyxl")

        elif filename.endswith(".xls"):
            return pd.read_excel(BytesIO(content), engine="xlrd")

        else:
            raise Exception("Formato no soportado")

    except Exception as e:
        print("❌ ERROR LEYENDO ARCHIVO:", str(e))
        raise

# -------------------------
# 🔧 LÓGICA TRANSFORMAR
# -------------------------
def separar_ufi(df):
    df = df.copy()
    i = len(df) - 1

    while i > 0:
        try:
            actual = str(df.iloc[i, 6]).upper()
            anterior = str(df.iloc[i - 1, 6]).upper()

            if "UNIDAD FUNCIONAL" in actual and "MORGUE" in anterior:
                df.iloc[i - 1, 7] = df.iloc[i, 6]
                df = df.drop(df.index[i]).reset_index(drop=True)
                i -= 1

        except Exception as e:
            print("⚠️ Error:", e)

        i -= 1

    return df


# -------------------------
# 🚀 TRANSFORMAR
# -------------------------
@app.route("/transformar", methods=["POST"])
def transformar():
    try:
        file = request.files["file"]
        filename = file.filename

        df = leer_archivo(file, filename)
        df = separar_ufi(df)

        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return send_file(output, download_name="transformado.xlsx", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e), "detalle": traceback.format_exc()}), 500


# -------------------------
# 📊 ESTADÍSTICAS
# -------------------------
@app.route("/estadisticas", methods=["POST"])
def estadisticas():
    try:
        file = request.files["expedientes"]
        mes = int(request.form.get("mes"))
        anio = int(request.form.get("anio"))  # 👈 ESTO FALTABA
        df = pd.read_excel(file)

        df["DEPTO. JUDICIAL"] = df["DEPTO. JUDICIAL"].astype(str).str.upper()
        df["FECHA DE SOLICITUD"] = pd.to_datetime(df["FECHA DE SOLICITUD"], errors="coerce")

        df = df[
    (df["FECHA DE SOLICITUD"].dt.month == mes) &
    (df["FECHA DE SOLICITUD"].dt.year == anio)
]

        # -------------------------
        # TEMPLATE
        # -------------------------
        BASE_DIR = Path(__file__).resolve().parent
        template_path = BASE_DIR / "data" / "template_estadisticas.xlsx"

        wb = load_workbook(template_path)
        ws = wb.active

        # -------------------------
        # MAPEO A6:A25 → R6:R25
        # -------------------------
        for row in range(6, 26):
            depto = ws[f"A{row}"].value

            if depto:
                depto = str(depto).upper()
                count = df[df["DEPTO. JUDICIAL"] == depto].shape[0]
                ws[f"R{row}"] = count

        # -------------------------
        # 🔢 SUMA B26:R26
        # -------------------------
        for col in range(2, 19):
            col_letter = ws.cell(row=6, column=col).column_letter

            total = 0
            for row in range(6, 26):
                value = ws[f"{col_letter}{row}"].value
                try:
                    total += float(value)
                except:
                    pass

            ws[f"{col_letter}26"] = total

        # -------------------------
        # OUTPUT
        # -------------------------
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        meses = {
            1: "ENERO", 2: "FEBRERO", 3: "MARZO",
            4: "ABRIL", 5: "MAYO", 6: "JUNIO",
            7: "JULIO", 8: "AGOSTO", 9: "SEPTIEMBRE",
            10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
        }

        nombre_mes = meses.get(mes, "MES")
        año = datetime.now().year

        return send_file(
            output,
            download_name=f"Estadísticas {nombre_mes} {año}.xlsx",
            as_attachment=True
        )

    except Exception as e:
        print("❌ ERROR ESTADÍSTICAS:")
        print(traceback.format_exc())

        return jsonify({
            "error": str(e),
            "detalle": traceback.format_exc()
        }), 500


# -------------------------
# ▶️ RUN
# -------------------------
if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=8000
    )