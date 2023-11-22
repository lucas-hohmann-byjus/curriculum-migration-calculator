import streamlit as st

from consts import *

# Config
st.set_page_config(
    page_title="Curriculum Migration",
    page_icon="⏩",
    layout="wide",
    initial_sidebar_state="expanded",
)


def print_unavailable_migration() -> None:
    st.error(f"EQUIVALÊNCIA NÃO DISPONÍVEL", icon="🚨")

    string = f"#### "
    string += f"O caso deve ser avaliado pelo time de Currículo através do formulário:"
    st.markdown(string)

    string = f"[Solicitação de Alteração de Currículo - Curso de Programação]"
    string += f"(https://docs.google.com/forms/d/e/1FAIpQLSc_6p8cp8B7b0KtK0sKa_pgYXBuHLSKZK-es9ZudQfeawSQXg/viewform)"
    st.markdown(string)


def print_successful_migration(modality: str, curriculum: str, class_: int) -> None:
    modality = modality.replace(":", "\:")

    st.markdown(f"## A próxima aula do aluno deverá ser:")
    st.markdown(f"# {modality} - {curriculum} C{class_}")
    st.divider()


def print_concepts_delta(
    src_class: int, dst_class: int, curriculum: str, direction: str
) -> None:
    concepts = []

    for concept, values in CONCEPTS[curriculum][direction].items():
        if src_class >= values["classes"][0]:
            continue

        if dst_class <= values["classes"][1]:
            continue

        description = f"- {values['description']}"
        description += f"\n\t- *(A professora pode utilizar as atividades da aula C{values['classes'][1]} - 1:1 como referência)*"
        concepts.append(description)

    if concepts:
        st.warning("É necessário uma aula BOOSTER.", icon="⚠️")
        st.markdown("#### A professora deve revisar os seguintes conceitos:")
        st.markdown("\n".join(concepts))
    else:
        st.success("Não há necessidade de aula BOOSTER.", icon="✅")


def main() -> None:
    with st.sidebar:
        st.markdown("# Origem")
        subset: dict = MAPPING
        src_curr = st.selectbox("Currículo", subset.keys(), key="src_curr")
        subset = subset[src_curr]
        src_moda = st.selectbox("Modalidade", subset.keys(), key="src_moda")
        current_class_ = st.number_input(
            "Última aula concluída",
            min_value=1,
            max_value=144,
        )

        st.markdown("# Destino")
        subset = subset[src_moda]
        dst_curr = st.selectbox("Currículo", subset.keys(), key="dst_curr")
        subset = subset[dst_curr]
        dst_moda = st.selectbox("Modalidade", subset.keys(), key="dst_moda")

    subset = subset[dst_moda]
    for src_class, dst_class in subset:
        if src_class == current_class_:
            print_successful_migration(dst_moda, dst_curr, dst_class)

            if src_curr == dst_curr:
                print_concepts_delta(
                    src_class, dst_class, src_curr, f"{src_moda} > {dst_moda}"
                )

            break
    else:
        print_unavailable_migration()


if __name__ == "__main__":
    main()
