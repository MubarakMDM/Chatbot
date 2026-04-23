import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers questions about movies, Recommend a Indian movie for these options {mood}, {genre_preference} and {favorite_acter}"),
    ("human", "Suggest a movie")
])

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    max_output_tokens=100
)

parse = StrOutputParser()
chain = prompt | model | parse

st.title("🎬 Movie Recommender")

mood = st.selectbox("Select Mood", ["romantic", "happy", "sad", "action", "motivational"])

genre_preference = st.selectbox("Select Genre", ["romance", "comedy", "drama", "thriller", "action"])

favorite_acter = st.selectbox(
    "Select Actor",
    ["Shah Rukh Khan", "Salman Khan", "Aamir Khan", "Akshay Kumar", "Hrithik Roshan"]
)

if st.button("Recommend Movie"):
    response = chain.invoke({
        "mood": mood,
        "genre_preference": genre_preference,
        "favorite_acter": favorite_acter
    })
    st.write(response)