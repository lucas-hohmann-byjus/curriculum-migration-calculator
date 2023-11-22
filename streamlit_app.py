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
    st.markdown("# Tipo")
    migration_type = st.selectbox(
        "Tipo de Migração",
        [
            "Modalidade",
            "Conclusão de Curso",
            "Entre Currículos",
        ],
    )
    st.markdown("# Dados do Aluno")

    if migration_type == "Modalidade":
        curriculum = st.selectbox(
            "Currículo",
            ["BEG", "INT", "ADV", "PRO"],
        )
        direction = st.selectbox(
            "Direção",
            ["1:M para 1:1"],
        )
        class_number = st.number_input(
            "Última aula concluída",
            min_value=1,
            max_value=144,
        )

    elif migration_type == "Conclusão de Curso":
        curriculum = st.selectbox(
            "Currículos",
            ["BEG -> INT", "INT -> ADV", "ADV -> PRO"],
        )
        modality = st.selectbox(
            "Modalidade",
            ["1:1", "1:M"],
        )

    elif migration_type == "Entre Currículos":
        modality = st.selectbox(
            "Modalidade",
            ["1:1", "1:M"],
        )
        src_curriculum = st.selectbox(
            "Origem",
            ["BEG", "INT", "ADV", "PRO"],
        )
        dst_curriculum = st.selectbox(
            "Destino",
            MIGRATIONS_INTER[src_curriculum].keys(),
        )
        class_number = st.number_input(
            "Última aula concluída",
            min_value=1,
            max_value=144,
        )

if migration_type == "Modalidade":
    # Find destination
    for src, dst in MIGRATIONS_INTRA[curriculum]:
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
        st.markdown(
            f"#### O caso deve ser avaliado pelo time de Currículo através do formulário: "
        )
        st.markdown(
            f"[Solicitação de Alteração de Currículo - Curso de Programação](https://docs.google.com/forms/d/e/1FAIpQLSc_6p8cp8B7b0KtK0sKa_pgYXBuHLSKZK-es9ZudQfeawSQXg/viewform)"
        )

elif migration_type == "Conclusão de Curso":
    next_class = CONTINUATIONS[curriculum][modality]
    modality = modality.replace(":", "\:")
    curriculum = curriculum.split()[-1]

    st.markdown(f"## O aluno deve ser migrado para:")
    st.markdown(f"# {modality} - {curriculum} - C{next_class}")
    st.divider()

elif migration_type == "Entre Currículos":
    try:
        for src, dst in MIGRATIONS_INTER[src_curriculum][dst_curriculum][modality]:
            if src >= class_number:
                break
        else:
            raise ValueError

        st.markdown(f"## A próxima aula do aluno deverá ser:")
        st.markdown(f"# {modality} - {dst_curriculum} C{dst}")
        st.divider()

    except (KeyError, ValueError):
        st.error(f"EQUIVALÊNCIA NÃO DISPONÍVEL", icon="🚨")
        st.markdown(
            f"#### O caso deve ser avaliado pelo time de Currículo através do formulário: "
        )
        st.markdown(
            f"[Solicitação de Alteração de Currículo - Curso de Programação](https://docs.google.com/forms/d/e/1FAIpQLSc_6p8cp8B7b0KtK0sKa_pgYXBuHLSKZK-es9ZudQfeawSQXg/viewform)"
        )
