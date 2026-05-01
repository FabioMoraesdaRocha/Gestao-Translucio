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
    def link_pdf(url):
    if pd.notna(url):
        return f'<a href="{url}" target="_blank">Abrir PDF</a>'
    return ""

df["Link"] = df["Link"].apply(link_pdf)

st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

except Exception as e:
    st.error("Erro ao carregar dados ❌")
    st.write(e)
import datetime

df["DataVencimento"] = pd.to_datetime(df["DataVencimento"], errors="coerce")

hoje = datetime.datetime.today()

vencendo = df[(df["DataVencimento"] - hoje).dt.days <= 30]

if not vencendo.empty:
    st.warning(f"⚠️ {len(vencendo)} documentos vencendo em até 30 dias")
    st.sidebar.header("Novo Registro")

with st.sidebar.form("form"):
    empresa = st.text_input("Empresa")
    tipo = st.text_input("Tipo Documento")
    pessoa = st.text_input("Pessoa")
    link = st.text_input("Link PDF")

    enviar = st.form_submit_button("Salvar")

    if enviar:
        st.success("Registro capturado (falta salvar na planilha)")
