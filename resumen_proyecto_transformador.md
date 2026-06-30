
# 🧠 Proyecto: Transformador + Estadísticas (Resumen)

## 🚀 Estado General
Sistema web con Flask que:
- Sube archivos Excel
- Transforma datos
- Genera estadísticas automáticas en un template Excel
- Descarga archivos procesados

---

## 🧩 SECCIÓN 1: TRANSFORMADOR

### Flujo
1. Usuario sube Excel (es un html en realidad)
2. Backend lee archivo (pandas + openpyxl)
3. Se ejecuta lógica de limpieza (separar UFI)
4. Se devuelve Excel transformado

### Endpoint
- POST /transformar

### Resultado
✔ Excel descargable limpio

---

## 📊 SECCIÓN 2: ESTADÍSTICAS

### Flujo
1. Usuario sube 3 excels (en frontend futuro)
2. Selecciona mes
3. Backend filtra por:
   - FECHA DE SOLICITUD
   - DEPTO. JUDICIAL
4. Se carga template Excel
5. Se completa:
   - R6:R25 (conteo por departamento)
   - B26:R26 (sumas totales)
6. Se descarga Excel final

### Endpoint
- POST /estadisticas

---

## 📁 TEMPLATE EXCEL

- Archivo base:
  /data/template_estadisticas.xlsx

- Requisito:
  ✔ Debe ser .xlsx (NO .xls)

---

## ⚙️ PROBLEMAS RESUELTOS

### ❌ FastAPI vs Flask
✔ Se eliminó conflicto
✔ Se dejó solo Flask

### ❌ Template no encontrado
✔ Ruta corregida con Path(__file__)

### ❌ Indentación rota
✔ Se reorganizó bloque de estadísticas

### ❌ SUMA fila 26
✔ Implementada B26:R26 correctamente

---

## 🎨 FRONTEND

### Sección 1
✔ Funciona correctamente
❌ CSS básico (sección superior desordenada)

### Sección 2 (en progreso)
- Subida de 3 archivos Excel
- Selección de mes
- Botón "Descargar estadísticas"

---

## 🧠 ARQUITECTURA ACTUAL

Frontend (HTML/JS)
        ↓
Flask API (app.py)
        ↓
Pandas + Openpyxl
        ↓
Excel output

---

## 🚀 PRÓXIMOS PASOS

- Completar PERICIAS / FINALIZADAS
- Mejorar UI (CSS)
- Validación de departamentos
- Dashboard más visual
