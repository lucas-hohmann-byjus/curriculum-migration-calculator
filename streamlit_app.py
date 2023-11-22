import streamlit as st

from consts import *

# Config
st.set_page_config(
    page_title="Curriculum Migration",
    page_icon="⏩",
    layout="wide",
    initial_sidebar_state="expanded",
)


def unavailable_migration() -> None:
    st.error(f"EQUIVALÊNCIA NÃO DISPONÍVEL", icon="🚨")

    string = f"#### "
    string += f"O caso deve ser avaliado pelo time de Currículo através do formulário:"
    st.markdown(string)

    string = f"[Solicitação de Alteração de Currículo - Curso de Programação]"
    string += f"(https://docs.google.com/forms/d/e/1FAIpQLSc_6p8cp8B7b0KtK0sKa_pgYXBuHLSKZK-es9ZudQfeawSQXg/viewform)"
    st.markdown(string)


def successful_migration(modality: str, curriculum: str, class_: int) -> None:
    st.markdown(f"## A próxima aula do aluno deverá ser:")
    st.markdown(f"# {modality} - {curriculum} C{class_}")
    st.divider()


def main() -> None:
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
            curriculum = st.selectbox("Currículo", MIGRATIONS_INTRA.keys())
            direction = st.selectbox("Direção", ["1:M para 1:1"])
            current_class_ = st.number_input(
                "Última aula concluída",
                min_value=1,
                max_value=144,
            )

        elif migration_type == "Conclusão de Curso":
            curriculum = st.selectbox("Currículos", CONTINUATIONS.keys())
            modality = st.selectbox("Modalidade", ["1:1", "1:M"])

        elif migration_type == "Entre Currículos":
            modality = st.selectbox("Modalidade", ["1:1", "1:M"])
            src_curr = st.selectbox("Origem", MIGRATIONS_INTER.keys())
            dst_curr = st.selectbox("Destino", MIGRATIONS_INTER[src_curr].keys())
            current_class_ = st.number_input(
                "Última aula concluída",
                min_value=1,
                max_value=144,
            )

    if migration_type == "Modalidade":
        # Find destination
        for src_class, dst_class in MIGRATIONS_INTRA[curriculum]:
            if src_class == current_class_:
                break
        else:
            dst_class = None

        # Compute concepts delta
        concepts = []
        for concept, values in CONCEPTS[curriculum].items():
            if src_class >= values["classes"][0]:
                continue

            if dst_class <= values["classes"][1]:
                continue

            description = "- {values['description']}"
            description += f"\n\t- *(A professora pode utilizar as atividades da aula C{values['classes'][1]} - 1:1 como referência)*"
            concepts.append(description)

        # Outputs

        if dst_class:
            successful_migration("1\:1", curriculum, dst_class)

            if concepts:
                st.warning("É necessário uma aula BOOSTER.", icon="⚠️")
                st.markdown("#### A professora deve revisar os seguintes conceitos:")
                st.markdown("\n".join(concepts))
            else:
                st.success("Não há necessidade de aula BOOSTER.", icon="✅")

        else:
            unavailable_migration()

    elif migration_type == "Conclusão de Curso":
        dst_class = CONTINUATIONS[curriculum][modality]
        modality = modality.replace(":", "\:")
        dst_curr = curriculum.split()[-1]

        successful_migration(modality, dst_curr, dst_class)

    elif migration_type == "Entre Currículos":
        try:
            for src_cls, dst_cls in MIGRATIONS_INTER[src_curr][dst_curr][modality]:
                if src_cls >= current_class_:
                    break
            else:
                raise ValueError

            successful_migration(modality, dst_curr, dst_cls)

        except ValueError:
            unavailable_migration()


if __name__ == "__main__":
    main()
