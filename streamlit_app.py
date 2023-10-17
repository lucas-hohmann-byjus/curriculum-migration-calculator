import streamlit as st

from consts import *

st.set_page_config(
    page_title="Curriculum Migration",
    page_icon="⏩",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Dados do Aluno")
curriculum = st.selectbox("Currículo", ["BEG", "INT", "ADV", "PRO"])
direction = st.selectbox("Direção", ["1:M para 1:1"])
class_number = st.number_input("Última aula concluída", min_value=1, max_value=144)


# Find destination
for src, dst in TABLE[curriculum]:
    if src == class_number:
        break
else:
    dst = None

if dst:
    st.header(f"A próxima aula do aluno deverá ser a '1:M {curriculum} C{dst}'")
else:
    st.title("AULA INVÁLIDA")
