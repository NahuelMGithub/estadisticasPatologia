
// =======================
// UTILIDADES COMPARTIDAS
// =======================

function descargarArchivo(blob, nombre) {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = nombre;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}

// =======================
// SECCIÓN 1 - TRANSFORMADOR (SIN CAMBIOS LÓGICOS)
// =======================

const fileInput = document.getElementById('fileInput');
const btnSubir = document.getElementById('btnSubir');
const btnTransformar = document.getElementById('btnTransformar');
const estado = document.getElementById('estado');

let archivoCargado = null;

btnSubir.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    archivoCargado = e.target.files[0];
    estado.textContent = `Documento cargado: ${archivoCargado.name}`;
    btnTransformar.disabled = false;
  }
});

btnTransformar.addEventListener('click', async () => {
  if (!archivoCargado) return;

  const formData = new FormData();
  formData.append("file", archivoCargado);

  estado.textContent = "Procesando... ⏳";

  try {
    const response = await fetch("http://127.0.0.1:8000/transformar", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("❌ ERROR BACKEND RAW:", errText);
      estado.textContent = "Error en backend";
      btnDescargarStats.textContent = "Error";
      return;
    }

    const blob = await response.blob();
    descargarArchivo(blob, "transformado.xlsx");

    estado.textContent = "Transformado ✔️";

  } catch (err) {
    console.error(err);
    estado.textContent = "Error de conexión ❌";
  }
});


// =======================
// SECCIÓN 2 - ESTADÍSTICAS (FUNCIONAL)
// =======================

//fecha
let anioSeleccionado = null;
let anioOK = false;

// Archivos
let periciasFile = null;
let medicasFile = null;
let expedientesFile = null;
let mesSeleccionado = null;

// Estado
let periciasOK = false;
let medicasOK = false;
let expedientesOK = false;
let mesOK = false;

// Elementos UI
const btnPericias = document.getElementById("btnPericias");
const btnMedicas = document.getElementById("btnMedicas");
const btnExpedientes = document.getElementById("btnExpedientes");
const btnDescargarStats = document.getElementById("btnDescargarStats");
const mesSelect = document.getElementById("mesSelect");
const anioSelect = document.getElementById("anio");


// Estados visuales
const estadoPericias = document.getElementById("estadoPericias");
const estadoMedicas = document.getElementById("estadoMedicas");
const estadoExpedientes = document.getElementById("estadoExpedientes");

// Inputs ocultos dinámicos
const inputPericias = document.createElement("input");
inputPericias.type = "file";

const inputMedicas = document.createElement("input");
inputMedicas.type = "file";

const inputExpedientes = document.createElement("input");
inputExpedientes.type = "file";


// =======================
// HELPERS
// =======================

function actualizarBotonStats() {

  console.log({
    periciasOK,
    medicasOK,
    expedientesOK,
    mesOK,
    anioOK
  });

  btnDescargarStats.disabled =
    !(periciasOK && mesOK && anioOK);
}

function validarSeleccion() {
  console.log("anioSeleccionado =", anioSeleccionado);

  mesOK = mesSeleccionado !== null && mesSeleccionado !== "";
  anioOK = anioSeleccionado !== null && anioSeleccionado !== "";

  actualizarBotonStats();
}

function setEstado(elemento, texto) {
  if (elemento) elemento.textContent = texto;
}

function cargarAnios() {
  const selectAnio = document.getElementById("anio");
  if (!selectAnio) return;

  selectAnio.innerHTML = "";

  const opcionVacia = document.createElement("option");
  opcionVacia.value = "";
  opcionVacia.textContent = "Seleccionar año";
  selectAnio.appendChild(opcionVacia);

  const anioActual = new Date().getFullYear();
  for (let anio = anioActual; anio >= 2020; anio--) {
    const opcion = document.createElement("option");
    opcion.value = String(anio);
    opcion.textContent = String(anio);
    selectAnio.appendChild(opcion);
  }
}

cargarAnios();

anioSelect.addEventListener("change", (e) => {
  anioSeleccionado = e.target.value;

  console.log("Año seleccionado:", anioSeleccionado);

  validarSeleccion();
});

// =======================
// EVENTO MES Y AÑO
// =======================

mesSelect.addEventListener("change", (e) => {
  mesSeleccionado = e.target.value;
  validarSeleccion();
});

anioSelect.addEventListener("change", (e) => {
  anioSeleccionado = e.target.value;
  validarSeleccion();
});

// =======================
// PERICIAS
// =======================

btnPericias.addEventListener("click", () => {
  inputPericias.click();
});

inputPericias.addEventListener("change", (e) => {
  if (e.target.files.length > 0) {
    periciasFile = e.target.files[0];
    periciasOK = true;
    setEstado(estadoPericias, `✔ ${periciasFile.name}`);
    actualizarBotonStats();
  }
});


// =======================
// MÉDICAS
// =======================

btnMedicas.addEventListener("click", () => {
  inputMedicas.click();
});

inputMedicas.addEventListener("change", (e) => {
  if (e.target.files.length > 0) {
    medicasFile = e.target.files[0];
    medicasOK = true;
    setEstado(estadoMedicas, `✔ ${medicasFile.name}`);
    actualizarBotonStats();
  }
});


// =======================
// EXPEDIENTES
// =======================

btnExpedientes.addEventListener("click", () => {
  inputExpedientes.click();
});

inputExpedientes.addEventListener("change", (e) => {
  if (e.target.files.length > 0) {
    expedientesFile = e.target.files[0];
    expedientesOK = true;
    setEstado(estadoExpedientes, `✔ ${expedientesFile.name}`);
    actualizarBotonStats();
  }
});


// =======================
// BOTÓN FINAL
// =======================


btnDescargarStats.addEventListener("click", async () => {

  const formData = new FormData();

  // ⚠️ IMPORTANTE: nombres deben coincidir con FastAPI
  formData.append("pericias", periciasFile);
  formData.append("mes", mesSeleccionado);
  formData.append("anio", anioSeleccionado);

  if (!mesSeleccionado || !anioSeleccionado) {
    alert("Falta mes o año");
    return;
  }

  btnDescargarStats.disabled = true;
  btnDescargarStats.textContent = "Procesando... ⏳";

  try {
    const response = await fetch("http://127.0.0.1:8000/estadisticas", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error("❌ ERROR BACKEND RAW:", errText);
      estado.textContent = "Error en backend";
      btnDescargarStats.textContent = "Error";
      return;
    }

    const blob = await response.blob();

    // descarga directa
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;

    const hoy = new Date();
    const año = hoy.getFullYear();

    const meses = {
      "1": "ENERO", "2": "FEBRERO", "3": "MARZO",
      "4": "ABRIL", "5": "MAYO", "6": "JUNIO",
      "7": "JULIO", "8": "AGOSTO", "9": "SEPTIEMBRE",
      "10": "OCTUBRE", "11": "NOVIEMBRE", "12": "DICIEMBRE"
    };

    const nombreMes = meses[mesSeleccionado] || "MES";

    a.download = `Estadísticas ${nombreMes} ${año}.xlsx`;

    document.body.appendChild(a);
    a.click();
    a.remove();

    window.URL.revokeObjectURL(url);

    btnDescargarStats.textContent = "Descargar estadísticas ✔️";
    actualizarBotonStats();

  } catch (err) {
    console.error("ERROR FETCH:", err);
    btnDescargarStats.textContent = "Error de conexión ❌";
    actualizarBotonStats();
  }
});
