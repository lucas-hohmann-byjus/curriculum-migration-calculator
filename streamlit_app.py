import streamlit as st

from consts import *

# Config
st.set_page_config(
    page_title="Curriculum Migration",
    page_icon="⏩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inputs
with st.sidebar:
    st.markdown("# Dados do Aluno - 1\:M")
    curriculum = st.selectbox("Currículo", ["BEG", "INT", "ADV", "PRO"])
    class_number = st.number_input("Última aula concluída", min_value=1, max_value=144)

# Find destination
for src, dst in MAPPING[curriculum]:
    if src == class_number:
        break
else:
    dst = None

# Compute concepts delta
concepts = []
for concept, values in CONCEPTS[curriculum].items():
    if src >= values["classes"][0]:
        continue

    if dst <= values["classes"][1]:
        continue

    description = f"- {values['description']}"
    description += f"\n\t- *(A professora pode utilizar as atividades da aula C{values['classes'][1]} - 1:1 como referência)*"
    concepts.append(description)


# Outputs

if dst:
    st.markdown(f"## A próxima aula do aluno deverá ser:")
    st.markdown(f"# 1\:1 - {curriculum} C{dst}")
    st.divider()

    if concepts:
        st.warning("É necessário uma aula BOOSTER.", icon="⚠️")
        st.markdown(f"#### A professora deve revisar os seguintes conceitos:")
        st.markdown("\n".join(concepts))
    else:
        st.success("Não há necessidade de aula BOOSTER.", icon="✅")


else:
    st.error(f"EQUIVALÊNCIA NÃO DISPONÍVEL", icon="🚨")
