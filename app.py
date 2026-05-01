import streamlit as st
import pandas as pd
import datetime

st.title("📊 Gestão de Contratos")

url = "https://docs.google.com/spreadsheets/d/1eX28N9DyCgR8MTD6Ol8MtHOJQ1e3GPamw5KMGRxJnmU/gviz/tq?tqx=out:csv&sheet=Dados"

# ======================
# CARREGAR DADOS
# ======================
try:
    df = pd.read_csv(url)
except Exception as e:
    st.error("Erro ao carregar dados")
    st.write(e)
    st.stop()

# ======================
# FILTRO
# ======================
empresa = st.selectbox(
    "Filtrar por empresa",
    ["Todas"] + list(df["Empresa"].dropna().unique())
)

if empresa != "Todas":
    df = df[df["Empresa"] == empresa]

# ======================
# ALERTA
# ======================
if "DataVencimento" in df.columns:
    df["DataVencimento"] = pd.to_datetime(df["DataVencimento"], errors="coerce")
    hoje = datetime.datetime.today()

    vencendo = df[(df["DataVencimento"] - hoje).dt.days <= 30]

    if not vencendo.empty:
        st.warning(f"⚠️ {len(vencendo)} documentos vencendo em até 30 dias")

# LINK PDF
if "Link" in df.columns:
    def link_pdf(x):
        if pd.notna(x):
            return f'<a href="{x}" target="_blank">Abrir PDF</a>'
        return ""

    df["Link"] = df["Link"].apply(link_pdf)

# 🔽 AQUI entra a correção das datas
if "DataInicio" in df.columns:
    df["DataInicio"] = pd.to_datetime(df["DataInicio"], errors="coerce").dt.strftime("%d/%m/%Y")

if "DataVencimento" in df.columns:
    df["DataVencimento"] = pd.to_datetime(df["DataVencimento"], errors="coerce").dt.strftime("%d/%m/%Y")

# 🔽 limpar NaN
df = df.fillna("")

# TABELA (última coisa)
# ======================
# LINK CLICÁVEL (CORREÇÃO)
# ======================
if "Link" in df.columns:
    df["Abrir PDF"] = df["Link"]

    # opcional: remover coluna antiga
    # df = df.drop(columns=["Link"])

# ======================
# MOSTRAR TABELA
# ======================
st.dataframe(df, use_container_width=True)
# ======================
# FORMULÁRIO
# ======================
st.sidebar.header("➕ Novo Registro")

with st.sidebar.form("formulario"):
    empresa_nova = st.text_input("Empresa")
    tipo = st.text_input("Tipo Documento")
    pessoa = st.text_input("Pessoa")
    link = st.text_input("Link PDF")

    enviar = st.form_submit_button("Salvar")

    if enviar:
        st.success("Registro capturado (não salva ainda)")
