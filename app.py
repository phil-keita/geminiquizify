import streamlit as st
from QuizManager import QuizManager

st.title('Quizify')

with st.form('generator'):
    st.write("Upload a PDF file for ingestion, the quiz topic, and click Generate! (v2 will allow multiple docs)")
    uploaded_file = st.file_uploader("Choose file", type=['.pdf'])
    topic = st.text_input('Enter the quiz topic:')
    num_questions = st.slider('Select the number of questions:', 1, 5)
    submit_button = st.form_submit_button(label='Generate Quiz')
    if submit_button:
            if uploaded_file:
                with st.spinner("Generating Questions..."):
                    try:
                        quiz = QuizManager(file=uploaded_file, topic=topic, num_questions=num_questions)
                        st.session_state['questions'] = quiz.questions
                    except Exception as e:
                        st.error(e)
            else:
                st.error("Make sure to upload a document!")

if 'questions' in st.session_state:
    for i, question in enumerate(st.session_state['questions']):
        if 'question' not in question:
            st.write("Question generation issue. Please retry")
        else:
            with st.container():
                with st.form("question" + str(i)):
                    answer = st.radio(label=question['question'], options=question['options'])
                    submit_button = st.form_submit_button(label="Submit")
                    if submit_button:
                        if answer == question['correct_answer']:
                            st.success("Correct!\n")
                            st.write(question['explanation'])
                        else:
                            st.error("Wrong!")