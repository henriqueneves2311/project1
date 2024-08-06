import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt

# Configuração do tema escuro do Altair
alt.themes.enable('dark')

# Carregar o arquivo Excel
file_path = 'cancelamento1.xlsx'
df = pd.read_excel(file_path, sheet_name='GERAL', engine='openpyxl')

# Verificar e limpar nomes das colunas
df.columns = df.columns.str.strip()

# Função para gerar o gráfico de barras
def generate_bar_chart(df, analista):
    filtered_df = df[df['Analista'] == analista]
    processos_counts = filtered_df.groupby('Analista')['N° PROCESSO'].count()

    fig = px.bar(x=processos_counts.index, y=processos_counts.values,
                 labels={'x': 'Analista', 'y': 'Quantidade de Processos'},
                 title=f'Quantidade de Processos para {analista}',
                 text=processos_counts.values)

    fig.update_layout(
        font=dict(family='Arial', color='white'),
        title_font=dict(color='white', size=20),
        xaxis_title_font=dict(color='white'),
        yaxis_title_font=dict(color='white'),
        xaxis=dict(
            tickfont=dict(color='white'),
            title_font=dict(color='white')
        ),
        yaxis=dict(
            tickfont=dict(color='white'),
            title_font=dict(color='white')
        )
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='white', mirror=True)
    fig.update_traces(
        textposition='inside',
        textfont=dict(size=14, color='white', family='Arial', weight='bold')
    )

    return fig

# Função para gerar o quadro de resultados
def generate_results_table(df, analista):
    filtered_df = df[df['Analista'] == analista]
    analisados = filtered_df['Data início Análise'].notna().sum()
    nao_analisados = filtered_df['Data início Análise'].isna().sum()
    diligencias = filtered_df['Data de envio de diligência'].notna().sum()
    total = len(filtered_df)

    data = [
        {'Categoria': 'Analisados', 'Quantidade': analisados},
        {'Categoria': 'Não Analisados', 'Quantidade': nao_analisados},
        {'Categoria': 'Em Diligência', 'Quantidade': diligencias},
        {'Categoria': 'Total', 'Quantidade': total}
    ]

    return pd.DataFrame(data)

# Layout do dashboard
st.set_page_config(page_title="Dashboard de Processos", layout="wide", page_icon=":bar_chart:")
st.title("Dashboard de Processos")

# Dividir em colunas
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.header("Seleção de Analista")
    st.write("Escolha um analista para ver as informações:")
    analistas = df['Analista'].unique()
    analista_selecionado = st.selectbox("Escolha o Analista", analistas, key='analista_selecionado')


with col2:
    st.header("Gráfico de Processos")
    fig = generate_bar_chart(df, analista_selecionado)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.header("Quadro de Resultados")
    results_df = generate_results_table(df, analista_selecionado)
    st.dataframe(results_df, use_container_width=True)

