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
    string += f"O caso deve ser avaliado pelo time de Currículo, através de um chamado para Orientação Pedagógica."
    st.markdown(string)


def print_successful_migration(modality: str, curriculum: str, class_: int) -> None:
    modality = modality.replace(":", "\:")

    st.markdown(f"#### A próxima aula do aluno deverá ser:")
    st.markdown(f"## {modality} - {curriculum} C{class_}")


def get_delta(
    src_class: int,
    dst_class: int,
    src_curr: str,
    dst_curr: str,
    src_moda: str,
    dst_moda: str,
) -> list:
    concepts = []

    for concept, values in CONCEPTS[src_curr][src_moda][dst_curr][dst_moda].items():
        if src_class >= values["classes"][0] or dst_class <= values["classes"][1]:
            continue

        description = f"- {values['description']}"
        description += f"\n\t- *(A professora pode utilizar as atividades da aula C{values['classes'][1]} - 1:1 como referência)*"
        concepts.append(description)

    return concepts


def main() -> None:
    st.markdown(
        "<style>.block-container {padding: 2rem 1rem 2rem;} hr {margin: 1em 0px;}</style>",
        unsafe_allow_html=True,
    )

    col1, col2, col3, _, col5, col6 = st.columns(6)

    with col1:
        st.markdown("### Origem")

        subset: dict = MAPPING
        src_curr = st.selectbox("Currículo", subset.keys(), key="src_curr")

    with col2:
        st.markdown("### ⠀")

        subset = subset[src_curr]
        src_moda = st.selectbox("Modalidade", subset.keys(), key="src_moda")

    with col3:
        st.markdown("### ⠀")

        current_class_ = st.number_input(
            "Última aula concluída",
            min_value=1,
            max_value=144,
        )

    with col5:
        st.markdown("### Destino")

        subset = subset[src_moda]
        dst_curr = st.selectbox("Currículo", subset.keys(), key="dst_curr")

    with col6:
        st.markdown("### ⠀")

        subset = subset[dst_curr]
        dst_moda = st.selectbox("Modalidade", subset.keys(), key="dst_moda")

    st.divider()

    subset = subset[dst_moda]
    for src_class, dst_class in subset:
        if src_class == current_class_ and dst_class:
            print_successful_migration(dst_moda, dst_curr, dst_class)

            concepts = get_delta(
                src_class,
                dst_class,
                src_curr,
                dst_curr,
                src_moda,
                dst_moda,
            )

            if concepts:
                st.warning("É necessário uma aula BOOSTER.", icon="⚠️")
                st.markdown("#### A professora deve revisar os seguintes conceitos:")
                st.markdown("\n".join(concepts))
            else:
                st.success("Não há necessidade de aula BOOSTER.", icon="✅")

            break
    else:
        print_unavailable_migration()


if __name__ == "__main__":
    main()
