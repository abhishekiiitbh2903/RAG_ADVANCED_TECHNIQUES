import streamlit as st
from onlineKBHandler import PrepareVectorDBOnline
import tempfile
from finalAnswerHandler import AnswerGenerator

def process_documents(uploaded_file):
    """Save the uploaded file to a temporary location."""
    temp_file = tempfile.NamedTemporaryFile("wb", suffix=".pdf", delete=False)
    temp_file.write(uploaded_file.read())
    temp_file.close()
    return temp_file.name


def side_bar():
    with st.sidebar:
        st.markdown("## 📝 Note")
        st.info("The **Vector DB for Bluebook** has already been prepared using advanced techniques.")
        
        uploaded_file = st.file_uploader("**📑 Upload PDF files for QnA**", type=["pdf"], accept_multiple_files=False)

        if uploaded_file is not None: 
            st.write("**📑 Selected PDF:**", uploaded_file.name)
            # ? Can we provide a preview of the uploaded PDF here? 
            # ? Generate a link which will open the PDF in a new tab
            
             
             
            doc_confidentiality = st.selectbox(
                "**🔒 Is the document confidential?**",
                options=["Select an option", "Confidential", "Not Confidential"],
                index=0
            )
            st.session_state["doc_confidentiality"] = doc_confidentiality

            if doc_confidentiality == "Confidential":
                st.warning("⚠️ Please note that you have selected a Confidential so you may expect some delay in the response.")
            elif doc_confidentiality == "Not Confidential":
                st.warning("⚠️ Please note that you have selected a Non-Confidential, your request will be served on Llama ,You may expect faster response but it won't be confidential.")
                

        generate_disabled = uploaded_file is None or st.session_state.get("doc_confidentiality") == "Select an option"
        st.markdown("---")

        generate_button = st.button("⚡️ Generate", disabled=generate_disabled)

        if generate_button:
            st.success(f"Processing your {'confidential' if st.session_state['doc_confidentiality'] == 'Confidential' else 'not confidential'} document!")
            try:
                pdf_path = process_documents(uploaded_file)
                loader = PrepareVectorDBOnline(pdf_path, is_confidential=(st.session_state["doc_confidentiality"] == "Confidential"))
                vectordb = loader.prepare_and_save_vectordb()
                st.success("✅ Vector DB Created Successfully,No. of vectors in vectordb: {}".format(vectordb.count()))
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

        st.markdown("---")
        st.markdown("👨‍💻 **Author**: DI ANALYTICS")
    return st.session_state.get("doc_confidentiality")




def main():
    
    st.set_page_config(page_title="RAG Question Answer", layout="wide")
    st.title("📘 RAG-GPT")
    st.markdown("---")
    st.markdown("### Do you have a question from Bluebook:")

    is_bluebook=st.selectbox("Do you have a question from Bluebook?",["Yes","No"],index=0)

    if is_bluebook == "Yes":
        st.markdown("### Enter your question:")
        query = st.text_input("Enter your question:")
        ask_button = st.button("Ask Question")

        if query and ask_button:
            st.markdown("### Answer:")
            answer_generator = AnswerGenerator(query,is_confidential=False)
            answer = answer_generator.get_answer()
            if isinstance(answer, str):
                st.write(answer)
            else:
                for chunk in answer:
                    st.write(chunk, end="")

            st.markdown("---")
    else:
        doc_confidential=side_bar()
        st.markdown("### Enter your question:")
        query = st.text_input("Enter your question:")
        ask_button = st.button("Ask Question")

        if query and ask_button:
            st.markdown("### Answer:")
            answer_generator = AnswerGenerator(query,is_confidential=(doc_confidential == "Confidential"))
            answer = answer_generator.get_answer()
            if isinstance(answer, str):
                st.write(answer)
            else:
                for chunk in answer:
                    st.write(chunk, end="")

            st.markdown("---")


if __name__ == "__main__":
    main()
