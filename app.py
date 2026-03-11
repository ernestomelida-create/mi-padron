import streamlit as st
import pandas as pd

# Configuración para móvil
st.set_page_config(page_title="Buscador Padrón", layout="centered")

# Estilo para mejorar la visualización en celular
st.markdown("""
    <style>
    .main { padding: 10px; }
    .stDataFrame { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    # Cargamos el archivo (asegúrate de que se llame datos.csv)
    df = pd.read_csv("datos.csv", sep=';', encoding='utf-8')
    # Convertimos Matricula a string para que la búsqueda sea más fácil
    df['Matricula'] = df['Matricula'].astype(str)
    return df

st.title("📂 Buscador de Afiliados")

try:
    df = cargar_datos()
    
    # Buscador principal
    opcion = st.radio("Buscar por:", ["Matrícula (DNI)", "Apellido", "Nombre"], horizontal=True)
    
    busqueda = st.text_input(f"Ingresa el/la {opcion}:").strip()

    if busqueda:
        # Lógica de filtrado
        if opcion == "Matrícula (DNI)":
            resultado = df[df['Matricula'].str.contains(busqueda)]
        elif opcion == "Apellido":
            resultado = df[df['Apellido'].str.contains(busqueda, case=False, na=False)]
        else:
            resultado = df[df['Nombre'].str.contains(busqueda, case=False, na=False)]

        if not resultado.empty:
            st.success(f"Se encontraron {len(resultado)} resultados")
            for i in range(len(resultado)):
                fila = resultado.iloc[i]
                with st.expander(f"👤 {fila['Apellido']}, {fila['Nombre']}"):
                    st.write(f"**DNI:** {fila['Matricula']}")
                    st.write(f"**Domicilio:** {fila['Domicilio']}")
                    st.write(f"**Circuito:** {fila['Circuito']}")
                    st.write(f"**Sección:** {fila['Seccion']}")
                    st.write(f"**Clase:** {int(fila['Clase']) if pd.notnull(fila['Clase']) else 'N/A'}")
        else:
            st.error("No se encontraron coincidencias.")
    else:
        st.info("Escribe algo arriba para comenzar la búsqueda.")

except FileNotFoundError:
    st.error("No se encontró el archivo 'datos.csv'. Asegúrate de subirlo al repositorio.")