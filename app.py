import streamlit as st
from QuizManager import QuizManager

st.title('Quizify')

with st.form('generator'):
    st.write("Upload a file(s), the quiz topic, and click \"Generate Quiz\"!")
    uploaded_files = st.file_uploader("Choose file", accept_multiple_files=True, type=['pdf', 'docx'])
    topic = st.text_input(label='Enter the quiz topic:')
    num_questions = st.slider('Select the number of questions:', 1, 5)
    submit_button = st.form_submit_button(label='Generate Quiz')
    if submit_button:
        print("- User submitted the form.")
        if uploaded_files and topic and topic.strip() != "":
            print("- Generating questions ...")
            st.write("Generating Questions...")
            quiz = QuizManager(files=uploaded_files, topic=topic, num_questions=num_questions)
            st.session_state['questions'] = quiz.questions
            print("- Questions stored in session state.")
        else:
            error_message = "Make sure to upload a file(s)" if not uploaded_files else "Make sure to enter a topic"
            st.error(error_message)
            

if 'questions' in st.session_state:
    seen = set()
    for i, question in enumerate(st.session_state['questions']):
        if 'question' not in question:
            print("- Question was empty.")
            st.warning("Something went wrong.")
        elif question['question'] in seen:
            print("- Question was repeated.")
            st.warning("I couldn't generate enough questions.")
            break
        else:
            with st.container():
                with st.form("question" + str(i)):
                    print("- Displaying question.")
                    seen.add(question['question'])
                    answer = st.radio(label=question['question'], options=question['options'])
                    submit_button = st.form_submit_button(label="Submit")
                    if submit_button:
                        if answer == question['correct_answer']:
                            st.success("Correct!\n")
                            st.write(question['explanation'])
                        else:
                            st.error("Wrong!")