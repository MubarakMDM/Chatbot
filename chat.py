from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import  StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers questions about movies, Recommend a Indian movie for thse options {mood}, {genre_preference} and {favorite_acter}, just give a movie name, don't give any thing extra."),
    ("human", "Suggest a movie based on the given preferences.")
])


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                               temperature=0.2, max_output_tokens=500) 

parse = StrOutputParser()
chain = prompt | model | parse
response = chain.invoke({ "mood": "romantic", 
                          "genre_preference": "romance", 
                          "favorite_acter": "Shah Rukh Khan"})
print(response)
