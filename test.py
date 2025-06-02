import streamlit as st
import pandas as pd
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

# Forçar o tema padrão
#st.set_page_config(page_title="Meu Projeto", layout="wide")

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

# Exibir os dados
st.title("NCM Pesquisa")
# st.dataframe(df, height=500)

# Entrada de texto
user_input = st.text_input("Digite algo:", "")



# Consulta um código NCM específico
if user_input:
    ncm = fetch_ncm.get_codigo_ncm(user_input)
    st.write('Código:', ncm.codigo_ncm)      # '01031000'
    st.write('Descrição:', ncm.descricao_ncm)   # '- Reprodutores de raça pura'
    st.write('Data:', ncm.data_inicio)     # datetime object
    st.write('Número do Ato:' ,ncm.numero_ato)        # Tipo do ato normativo
    st.write('Ano do Ato:' ,ncm.ano_ato)        # Tipo do ato normativo

