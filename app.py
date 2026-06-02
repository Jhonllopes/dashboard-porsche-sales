import pandas as pd
import streamlit as st
import plotly.express as px

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Dashboard Porsche",
    page_icon="🚗",
    layout="wide"
)

# =========================
# CARREGAMENTO DOS DADOS
# =========================
@st.cache_data
def carregar_dados():
    return pd.read_excel(
        "8683bed0-cc33-4e06-bca9-04db9c31f9e2.xlsx"
    )

df = carregar_dados()

# =========================
# SIDEBAR - FILTROS
# =========================
st.sidebar.header("Filtros")

modelos = st.sidebar.multiselect(
    "Modelo Porsche",
    options=sorted(df["PorscheModelSanitized"].unique()),
    default=sorted(df["PorscheModelSanitized"].unique())
)

estados = st.sidebar.multiselect(
    "Estado",
    options=sorted(df["StateSanitized"].unique()),
    default=sorted(df["StateSanitized"].unique())
)

df_filtrado = df[
    (df["PorscheModelSanitized"].isin(modelos)) &
    (df["StateSanitized"].isin(estados))
]

# =========================
# TÍTULO
# =========================
st.title("🚗 Dashboard Porsche Sales")
st.markdown("Análise de vendas de veículos Porsche")

# =========================
# MÉTRICAS
# =========================
col1, col2, col3, col4 = st.columns(4)

total_vendas = len(df_filtrado)
faturamento = df_filtrado["SalesPriceSanitized"].sum()
preco_medio = df_filtrado["SalesPriceSanitized"].mean()
km_medio = df_filtrado["VehicleMileageSanitized"].mean()

col1.metric("Total de Vendas", f"{total_vendas}")
col2.metric("Faturamento", f"${faturamento:,.0f}")
col3.metric("Preço Médio", f"${preco_medio:,.0f}")
col4.metric("KM Médio", f"{km_medio:,.0f}")

st.divider()

# =========================
# GRÁFICOS 1
# =========================
col1, col2 = st.columns(2)

with col1:
    faturamento_modelo = (
        df_filtrado
        .groupby("PorscheModelSanitized")["SalesPriceSanitized"]
        .sum()
        .reset_index()
        .sort_values("SalesPriceSanitized", ascending=False)
    )

    fig_modelo = px.bar(
        faturamento_modelo,
        x="PorscheModelSanitized",
        y="SalesPriceSanitized",
        title="Faturamento por Modelo"
    )

    st.plotly_chart(fig_modelo, use_container_width=True)

with col2:
    fig_estado = px.pie(
        df_filtrado,
        names="StateSanitized",
        title="Distribuição de Vendas por Estado"
    )

    st.plotly_chart(fig_estado, use_container_width=True)

# =========================
# GRÁFICOS 2
# =========================
col3, col4 = st.columns(2)

with col3:
    vendas_vendedor = (
        df_filtrado
        .groupby("salesperson")
        .size()
        .reset_index(name="Quantidade")
        .sort_values("Quantidade", ascending=False)
    )

    fig_vendedor = px.bar(
        vendas_vendedor,
        x="salesperson",
        y="Quantidade",
        title="Vendas por Vendedor"
    )

    st.plotly_chart(fig_vendedor, use_container_width=True)

with col4:
    fig_pagamento = px.pie(
        df_filtrado,
        names="PayMethodSanitized",
        title="Métodos de Pagamento"
    )

    st.plotly_chart(fig_pagamento, use_container_width=True)

# =========================
# EVOLUÇÃO DAS VENDAS
# =========================
st.subheader("📈 Evolução das Vendas")

vendas_data = (
    df_filtrado
    .groupby("SaleDateSanitized")["SalesPriceSanitized"]
    .sum()
    .reset_index()
)

fig_linha = px.line(
    vendas_data,
    x="SaleDateSanitized",
    y="SalesPriceSanitized",
    markers=True,
    title="Faturamento ao Longo do Tempo"
)

st.plotly_chart(fig_linha, use_container_width=True)

# =========================
# TABELA
# =========================
st.subheader("📋 Dados Detalhados")

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=400
)

# =========================
# TOP 10 VENDAS
# =========================
st.subheader("🏆 Top 10 Maiores Vendas")

top10 = (
    df_filtrado
    .sort_values("SalesPriceSanitized", ascending=False)
    .head(10)
)

st.dataframe(
    top10[
        [
            "customer_name",
            "PorscheModelSanitized",
            "SalesPriceSanitized",
            "salesperson",
            "StateSanitized"
        ]
    ],
    use_container_width=True
)