import streamlit as st
import pandas as pd
import unicodedata
from ncm.client import FetchNcm
from ncm.entities import Ncm, NcmList



# Inicializa o cliente (carrega automaticamente os dados do cache ou da API)
fetch_ncm = FetchNcm()


# # Obter todos os códigos NCM
# ncm_list = fetch_ncm.get_all()
# st.write(len(ncm_list.ncm_list))  # Quantidade de códigos

# # Obter apenas códigos NCM com 8 dígitos
# fetch_ncm.only_ncm_8_digits=True
# ncm_list_8_digits = fetch_ncm.get_all()

# # Iterar sobre os resultados
# for ncm in ncm_list_8_digits.ncm_list:
#     st.write(f"{ncm.codigo_ncm}: {ncm.descricao_ncm}")


st.set_page_config(page_title="NCM Pesquisa", layout="wide")

# Aplicar fundo personalizado
st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #222222; /* Cor de fundo personalizada */
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Defina o caminho do JSON gerado pela função de atualização
json_file_path = "ncm.json"

# Carregar o JSON e converter para DataFrame
df = pd.read_json(json_file_path)

# Convertendo a coluna JSON para dicionários
df_normalizado = pd.json_normalize(df['Nomenclaturas'])

df_base = df_normalizado[["Codigo", "Descricao"]]

col_left, col_mid, col_right = st.columns([1, 6, 1])

with col_mid:
    
    st.title("NCM Pesquisa")
    
    
    
    # Dois campos de pesquisa mais estreitos usando mais colunas
    col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 3, 3])
    with col1:
        user_input1 = st.text_input("🔍 Pesquisar termo 1:", "", key="input1")
    with col2:
        user_input2 = st.text_input("🔍 Pesquisar termo 2:", "", key="input2")

    def remover_acentos(txt):
        if pd.isnull(txt):
            return ""
        return unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('ASCII')

    # Normaliza as colunas para busca sem acento
    df_base_sem_acento = df_base.applymap(remover_acentos)

    # Normaliza os termos de busca
    user_input1_sem_acento = remover_acentos(user_input1)
    user_input2_sem_acento = remover_acentos(user_input2)

    df_filtrado = df_base.copy()
    if user_input1:
        mask1 = df_base_sem_acento.apply(lambda row: row.str.contains(user_input1_sem_acento, case=False, na=False).any(), axis=1)
        df_filtrado = df_filtrado[mask1]
    if user_input2:
        # Filtra sobre o resultado anterior para manter o AND
        mask2 = df_base_sem_acento.loc[df_filtrado.index].apply(
            lambda row: row.str.contains(user_input2_sem_acento, case=False, na=False).any(), axis=1)
        df_filtrado = df_filtrado.loc[mask2]
        
    st.write(f"Resultados encontrados: {len(df_filtrado)}")


    st.dataframe(
        df_filtrado,
        column_config={
            "Codigo": st.column_config.Column(width="small"),
            "Descricao": st.column_config.Column(width="large"),
        }
    )

# st.dataframe(df_filtrado)


# # Consulta um código NCM específico
# if user_input:
#     ncm = fetch_ncm.get_codigo_ncm(user_input)
#     st.write('Código:', ncm.codigo_ncm)      # '01031000'
#     st.write('Descrição:', ncm.descricao_ncm)   # '- Reprodutores de raça pura'
#     st.write('Data:', ncm.data_inicio)     # datetime object
#     st.write('Número do Ato:' ,ncm.numero_ato)        # Tipo do ato normativo
#     st.write('Ano do Ato:' ,ncm.ano_ato)        # Tipo do ato normativo
