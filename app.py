import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# ---- Page Config ----
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# ---- Custom Styling ----
st.markdown("""
    <style>
        .main {
            background-color: #0f172a;
            color: white;
        }
        .stButton>button {
            background-color: #6366f1;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #4f46e5;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar ----
with st.sidebar:
    st.title("⚙️ Options")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

# ---- Initialize Chat History ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- Title ----
st.title("🎥 Indian Movie Recommender")
st.write("Select your preferences and get a perfect movie suggestion!")

# ---- Inputs ----
col1, col2, col3 = st.columns(3)

with col1:
    mood = st.selectbox(
        "Mood",
        ["romantic", "happy", "sad", "exciting", "thrilling"]
    )

with col2:
    genre = st.selectbox(
        "Genre Preference",
        ["romance", "action", "comedy", "drama", "thriller"]
    )

with col3:
    actor = st.selectbox(
        "Favorite Actor",
        ["Shah Rukh Khan", "Salman Khan", "Aamir Khan", "Ranbir Kapoor", "Deepika Padukone"]
    )

# ---- Prompt Setup ----
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant that answers questions about movies. "
     "Recommend an Indian movie for these options: {mood}, {genre_preference}, and {favorite_actor}. "
     "Only return the movie name, nothing else."),
    ("human", "Suggest a movie based on the given preferences.")
])

# ---- Model ----
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="AIzaSyDGGF9cfSxmTRm3hmNdsi6xIf6m7uBzbsY",
    temperature=0.2,
    max_output_tokens=150
)

parser = StrOutputParser()
chain = prompt | model | parser

# ---- Button ----
if st.button("🎬 Get Recommendation"):
    response = chain.invoke({
        "mood": mood,
        "genre_preference": genre,
        "favorite_actor": actor
    })

    # Store in chat history
    st.session_state.chat_history.append({
        "user": f"{mood}, {genre}, {actor}",
        "bot": response
    })

# ---- Chat Display ----
st.subheader("💬 Recommendations")

for chat in reversed(st.session_state.chat_history):
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**🎥 Movie:** {chat['bot']}")
    st.markdown("---")
