import streamlit as st
import pandas as pd

st.title("Teste App 🚀")

st.write("Se você está vendo isso, o app está funcionando")

url = "https://docs.google.com/spreadsheets/d/1eX28N9DyCgR8MTD6Ol8MtHOJQ1e3GPamw5KMGRxJnmU/gviz/tq?tqx=out:csv&sheet=Dados"

try:
    df = pd.read_csv(url)
    # FILTRO POR EMPRESA
empresa = st.selectbox("Filtrar por empresa", ["Todas"] + list(df["Empresa"].dropna().unique()))

if empresa != "Todas":
    df = df[df["Empresa"] == empresa]
    st.write("Dados carregados com sucesso ✅")
    st.dataframe(df)

except Exception as e:
    st.error("Erro ao carregar dados ❌")
    st.write(e)
