import vertexai
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession, GenerationResponse
from datetime import datetime
import json
import random
import streamlit as st


PROJECT_ID = 'quizify-440923'
LOCATION = 'us-central1'
MODEL = 'gemini-pro'

class QuizGenerator:
    def __init__(self):
        vertexai.init(project=PROJECT_ID, location=LOCATION)

        # Configs & Model
        config = generative_models.GenerationConfig(
            temperature=0.4, 
            max_output_tokens=500
        )
        self.model = GenerativeModel(
            MODEL,
            generation_config = config
        )
        # Start llm
        self.llm = self.model.start_chat()

    def generate_questions(self, quiz_topic, vector_store, num_questions):
        # Check if LLM is initialized
        if not self.llm:
            raise ValueError("LLM is not initialized!")

        # Check if vectorstore is initialized
        if not vector_store:
            raise ValueError("Vectorstore is not initialized!")
        
        # Retrieve relevant documents or elements for question generation
        relevant = vector_store.query(query_texts=quiz_topic, n_results=3)
        
        # Retrieval error handling
        if not relevant:
            raise ValueError("No relevant documents found for the quiz topic!")
        
        context = ""
        for doc in relevant["documents"]:
            context += doc[0] + "\n"
        question_bank = []
        for _ in range(num_questions):
            question_bank.append(self.generate_question(quiz_topic, context))
        return question_bank
        
    
    def format_question(self, response):
        if '{' not in response or '}' not in response:
            return "{"+"}"
        response = response.split("{")[1]
        response = response.split("}")[0]
        try:
            question = json.loads("{"+response+"}")
        except Exception as e:
            st.warning("Something went wrong")
        return question

    def generate_question(self, quiz_topic, context):
        # Format the prompt
        prompt = f"Based on the following knowledge:{context}\n\n Generate a quiz question on {quiz_topic}. Respond in json with the 'question', 'options', 'correct_answer' and 'explanation'"
        output = "{"+"}"
        try:
            response = self.llm.send_message(prompt)
            output = response.candidates[0].content.parts[0].text
        except Exception as e:
            log = f"{datetime.now()}\nUser query: {prompt}\nError: Test error\n\n"
            with open("error_log.txt", "a") as file:
                file.write(log)
        question = self.format_question(output)
        return question
