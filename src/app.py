# Para a execução no streamlit executar o seguinte no terminal:
# streamlit run src/app.py
# Para verificar o app, utilizar o seguinte elemento:
# Network URL: http://192.168.0.182:8501
# Para realizar o deploy, ler: https://docs.streamlit.io/en/stable/deploy_streamlit_app.html


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Feito para deixar as bases armazenadas em cache
@st.cache
def load_data(caminho):
    dados = pd.read_csv(caminho)
    return dados

def grafico_comparativo(df_2019, df_2020, causa = 'TODAS', estado = "BRASIL"):
    
    if estado == 'BRASIL':
        total_2019 = df_2019.groupby('tipo_doenca').sum()
        total_2020 = df_2020.groupby('tipo_doenca').sum()
        if causa == 'TODAS':
            lista = [total_2019['total'].sum(), total_2020['total'].sum()]
        else:
            lista = [int(total_2019.loc[causa]), int(total_2020.loc[causa])]

    else:
        total_2019 = df_2019.groupby(['uf','tipo_doenca']).sum()
        total_2020 = df_2020.groupby(['uf','tipo_doenca']).sum()
        if causa == 'TODAS':
            lista = [int(total_2019.loc[estado].sum()), int(total_2020.loc[estado].sum())]
        else:
            lista = [int(total_2019.loc[estado, causa]), int(total_2020.loc[estado, causa])]

    dados = pd.DataFrame({'Total':lista,
                         'Ano': [2019, 2020]})


    fig, ax = plt.subplots()
    ax = sns.barplot(y = 'Ano', x = 'Total', data = dados, orient = 'h')
    ax.set_title('Óbitos por {} - {}'.format(causa, estado))
    plt.xticks(rotation = 45)
    ax.set_xlabel('Quantia de óbitos causados por {}'.format(causa))
    ax.set_ylabel('Ano de verificação')
    
    return fig


def main():
    obitos_2019 = load_data('Dados/obitos-2019.csv')
    obitos_2020 = load_data('Dados/obitos-2020.csv')
    tipo_doenca = obitos_2020['tipo_doenca'].unique()
    unidade_federativa = np.append(obitos_2020['uf'].unique(), 'BRASIL')

    st.title('Análise de óbitos \n Período de: 2019 e 2020')
    st.markdown('## Dados adquiridos através do site: https://transparencia.registrocivil.org.br/especial-covid')
    st.markdown('### O foco do projeto é verificar os óbitos que ocorreram e quais doenças o causaram nos anos de 2019 e 2020')

    opcao_1 = st.sidebar.selectbox('Selecione o tipo de doença',
                tipo_doenca)

    opcao_2 = st.sidebar.selectbox('Selecione o estado', 
                unidade_federativa)

    figura = grafico_comparativo(obitos_2019, obitos_2020, opcao_1, opcao_2)
    
    st.pyplot(figura)
    #st.dataframe(obitos_2019)

if __name__ == "__main__":
    main()