import streamlit as st

from asistant import ask_database


st.set_page_config(
    page_title="DBAssistant",
    page_icon="🗄️"
)

st.title("🗄️ DBAssistant")

st.write(
    "AI-powered PostgreSQL Database Assistant"
)

question = st.text_area(
    "Ask your database question"
)

if st.button("Ask DBAssistant"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Analyzing database..."
        ):

            try:

                response = ask_database(
                    question
                )

                st.subheader(
                    "Generated SQL"
                )

                st.code(
                    response["sql"],
                    language="sql"
                )

                st.subheader(
                    "Result"
                )

                st.dataframe(
                    response["result"]
                )

            except Exception as e:

                st.error(str(e))

