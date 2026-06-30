import pandas as pd

def separar_ufi(df):
    """
    Replica el macro VBA:
    - Busca 'UNIDAD FUNCIONAL' en columna G
    - Si fila anterior en G contiene 'MORGUE'
      -> copia G actual a H anterior
      -> elimina fila actual
    """

    # Aseguramos nombres simples por posición tipo Excel:
    # Columna G = índice 6
    # Columna H = índice 7

    df = df.copy()

    ultima_fila = len(df)

    # Recorremos de abajo hacia arriba
    i = ultima_fila - 1

    while i > 0:
        try:
            valor_actual = str(df.iloc[i, 6]).upper()   # Columna G
            valor_anterior = str(df.iloc[i - 1, 6]).upper()

            if "UNIDAD FUNCIONAL" in valor_actual:
                if "MORGUE" in valor_anterior:

                    # Copiar G actual -> H anterior
                    df.iloc[i - 1, 7] = df.iloc[i, 6]

                    # Eliminar fila actual
                    df = df.drop(df.index[i])
                    df = df.reset_index(drop=True)

                    # saltamos una fila hacia arriba (ya cambió el índice)
                    i -= 1
        except Exception:
            pass

        i -= 1

    return df


def procesar_archivo(input_file, output_file):
    """
    Lee archivo tipo Excel o HTML exportado desde Excel
    y lo convierte en DataFrame
    """

    # Si es HTML de Excel
    if input_file.endswith(".html") or input_file.endswith(".htm"):
        dfs = pd.read_html(input_file)
        df = dfs[0]  # normalmente la primera tabla
    else:
        df = pd.read_excel(input_file)

    # Aplicar transformación
    df = separar_ufi(df)

    # Guardar resultado
    df.to_excel(output_file, index=False)

    print("Transformación completada ✔️")
    print(f"Archivo guardado en: {output_file}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Uso: python transformar.py input_file output_file")
        sys.exit(1)

    procesar_archivo(sys.argv[1], sys.argv[2])