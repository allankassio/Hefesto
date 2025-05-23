import os, re, uuid
import streamlit as st

from gdd import GameDesignDocument
from persistence import HefestoPersistence

safe_room = os.getenv("SAFE_ROOM")
persistence = HefestoPersistence()

st.set_page_config(page_title="Hefesto Game Lab",
                   page_icon='🛠️',
                   layout='centered',
                   initial_sidebar_state='collapsed')

hide_streamlit_style = """
    <style>
    /* Esconde o botão "Deploy" */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Esconde o menu de três pontinhos */
    [data-testid="stToolbar"] {
        visibility: hidden;
        height: 0px;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center;'>🛠️ Hefesto Game Lab 🛠️</h1>"
    "<h3 style='text-align: center;'>Gerador de GDD de Jogos para o Ensino de Pensamento Computacional<h3>"
    "<div style='text-align: center;'>Não esqueça de responder o questionário: <a href='https://forms.gle/8LvBzjJqsraZ796u5' target='_blank'>https://forms.gle/8LvBzjJqsraZ796u5</a></div>",
    unsafe_allow_html=True
)

if safe_room is not None:
    # Adiciona uma verificação de senha simples
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("### 🔐 Área Protegida")
        password = st.text_input("Digite a senha para acessar:", type="password")
        if password is None: password = "";
        if password == safe_room:
            st.session_state.authenticated = True
            st.rerun()  # Recarrega a página com acesso liberado
        elif password:
            st.error("Senha incorreta. Tente novamente.")
        st.stop()

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Inicializa o estado da aplicação
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.prev_step = 1

def enhance_gdd_step(pillar, mechanic, public):
    st.session_state.selected_pillar = pillar
    st.session_state.selected_mechanic = mechanic
    st.session_state.selected_public = public
    st.session_state.step = 2


def code_step():
    st.session_state.step = 3


def artifact_step():
    st.session_state.step = 4

def reset_all():
    session_id = st.session_state.session_id
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.step = 1

    parts = session_id.split("__")
    if len(parts) > 1:
        version = int(parts[1]) + 1
        session_id = parts[0]
    else:
        version = 1
    st.session_state.session_id = session_id + "__" + str(version)
    st.session_state.authenticated = True


options_pillars = ['Abstraction', 'Pattern Recognition', 'Algorithm', 'Decomposition']

options_mechanic = {
    'Abstraction': ['Puzzle', 'Strategy', 'Construction', 'Sandbox', 'Board Game', 'Simulation',
                    'Memory', 'Visual Logic', 'Narrative', 'Symbolic Representation'],
    'Pattern Recognition': ['Puzzle', 'Strategy', 'Memory', 'Visual Logic',
                            'Sequencing, Sorting, or Categorizing', 'Wayfinding', 'Matching', 'Tile-based'],
    'Algorithm': ['Puzzle', 'Strategy', 'Construction', 'Sandbox', 'Board Game', 'Escape Room',
                  'Resource Management', 'Sequencing, Sorting, or Categorizing',
                  'Wayfinding', 'Programming and Coding'],
    'Decomposition': ['Puzzle', 'Strategy', 'Construction', 'Sandbox', 'Simulation', 'Escape Room',
                      'Resource Management', 'Level-based']
}

options_public = [
    '1st Semester Computer Science Students',
    '2nd Semester Computer Science Students',
    '3rd Semester Computer Science Students',
    '4th Semester Computer Science Students',
    '5th to 9th Semester Computer Science Students',
    # 'Children aged 7 to 11',
    # 'Children aged 12 to 16'
]

if st.session_state.step > 1:
    cols = st.columns([2, 2, 2, 2])  # Última coluna maior para espaçamento ou conteúdo adicional
    with cols[0]:
        st.button("🔄 Recomeçar", on_click=reset_all)
    with cols[1]:
        if st.session_state.step != 2:
            st.button("📄 GDD", on_click=lambda: st.session_state.update(step=2))
    with cols[2]:
        if st.session_state.step != 3:
            st.button("💻 Código", on_click=lambda: st.session_state.update(step=3))
    with cols[3]:
        if st.session_state.step != 4:
            st.button("🧩 Artefato", on_click=lambda: st.session_state.update(step=4))

# Front Page
if st.session_state.step == 1:
    print(st.session_state.step)
    selected_pillar = st.selectbox('Escolha o pilar do Pensamento Computacional:', options_pillars, index=0)
    selected_mechanic = ""
    if selected_pillar:
        selected_mechanic = st.selectbox('Escolha a mecânica:', options_mechanic[selected_pillar], index=0)
    selected_public = st.selectbox('Escolha o público:', options_public, index=0)
    st.button("Gerar GDD", on_click=lambda: enhance_gdd_step(selected_pillar, selected_mechanic, selected_public))


# GDD Generation
if st.session_state.step == 2:
    print(st.session_state.step)

    # Se já tiver GDD salvo, usa ele — senão, gera e salva
    if 'ggd_result' in st.session_state:
        ggd_cleaned = st.session_state.ggd_result
    else:
        gdd = GameDesignDocument(
            pillar=st.session_state.selected_pillar,
            mechanic=st.session_state.selected_mechanic,
            public=st.session_state.selected_public
        )
        with st.spinner("🔄 Gerando GDD com o LLM..."):
            raw_result = gdd.deploy_gdd()
        ggd_cleaned = re.sub(r"<think>.*?</think>", "", raw_result, flags=re.DOTALL).strip()
        st.session_state.ggd_result = ggd_cleaned
        persistence.salvar_gdd(
            session_id=st.session_state.session_id,
            pillar=st.session_state.selected_pillar,
            mechanic=st.session_state.selected_mechanic,
            public=st.session_state.selected_public,
            ggd_result=ggd_cleaned
        )

    # Exibe o conteúdo gerado
    st.markdown("### 📄 GDD Generated")
    st.markdown(ggd_cleaned, unsafe_allow_html=True)

    # Botão de download (não altera estado)
    if st.download_button(
        label="📥 Baixar GDD como Markdown",
        data=ggd_cleaned,
        file_name="game_design_document.md",
        mime="text/markdown",
        key="download-gdd"
    ):
        persistence.marcar_gdd_baixado(session_id=st.session_state.session_id)

    # Botões de navegação
    st.button("Gerar Código", on_click=code_step)
    st.button("Gerar Artefato Desplugado", on_click=artifact_step)

# Code Generation
elif st.session_state.step == 3:
    print(st.session_state.step)

    # Botão para regenerar
    if st.button("🔁 Gerar Código Novamente"):
        st.session_state.pop("code_result", None)

    # Gera o código apenas se ainda não tiver salvo
    if 'code_result' in st.session_state:
        code_cleaned = st.session_state.code_result
    else:
        gdd = GameDesignDocument(
            pillar=st.session_state.selected_pillar,
            mechanic=st.session_state.selected_mechanic,
            public=st.session_state.selected_public
        )
        ggd_result = st.session_state.ggd_result

        with st.spinner("💻 Gerando código JavaScript..."):
            code_result_raw = gdd.deploy_code(ggd_result)

        # Extrai apenas o código entre os blocos ```javascript ... ```
        match = re.search(r"```javascript\s*(.*?)```", code_result_raw, flags=re.DOTALL)
        code_cleaned = match.group(1).strip() if match else code_result_raw #"// No JavaScript code found."
        #if code_cleaned == "// No JavaScript code found.":
        #    st.session_state.pop("code_result", None)

        st.session_state.code_result = code_cleaned

        persistence.salvar_code(
            session_id=st.session_state.session_id,
            code_result=st.session_state.code_result
        )

    # Exibe o código
    st.markdown("### 💻 JavaScript Code")
    st.code(body=code_cleaned, language="javascript", line_numbers=True)

    # Botão de download
    if st.download_button(
        label="📥 Baixar Código como .js",
        data=code_cleaned,
        file_name="game_code.js",
        mime="application/javascript",
        key="download-js"
    ):
        persistence.marcar_codigo_baixado(session_id=st.session_state.session_id)


# Artifact Generation
elif st.session_state.step == 4:
    print(st.session_state.step)

    # Botão para regenerar
    if st.button("🔁 Gerar Artefato Novamente"):
        st.session_state.pop("artifact_result", None)

    # Só gera se ainda não tiver no estado
    if 'artifact_result' in st.session_state:
        artifact_result_cleaned = st.session_state.artifact_result
    else:
        gdd = GameDesignDocument(
            pillar=st.session_state.selected_pillar,
            mechanic=st.session_state.selected_mechanic,
            public=st.session_state.selected_public
        )
        ggd_result = st.session_state.ggd_result
        with st.spinner("💻 Gerando artefato desplugado..."):
            artifact_result = gdd.deploy_artifact(ggd_result)
        artifact_result_cleaned = re.sub(r"<think>.*?</think>", "", artifact_result, flags=re.DOTALL).strip()
        st.session_state.artifact_result = artifact_result_cleaned
        persistence.salvar_artefato(
            session_id=st.session_state.session_id,
            artifact_result=st.session_state.artifact_result
        )

    # Exibe o conteúdo
    st.markdown("### 🧩 Artefato Desplugado")
    st.markdown(artifact_result_cleaned)

    # Botão de download (.txt)
    if st.download_button(
        label="📥 Baixar Artefato como .txt",
        data=artifact_result_cleaned,
        file_name="offline_artifact.txt",
        mime="text/plain",
        key="download-artifact"
    ):
        persistence.marcar_artefato_baixado(session_id=st.session_state.session_id)



