import streamlit as st
from google import genai

# ---------------------------------------------------------
# AI Learning Buddy — "Professor Neuron"
# Topic: Neural Networks Basics
# ---------------------------------------------------------

st.set_page_config(page_title="AI Learning Buddy — Professor Neuron", page_icon="🧠")

# ---- API key setup ----
# Add your Gemini API key in Streamlit Cloud under:
# App settings -> Secrets ->  GEMINI_API_KEY = "your-key-here"
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Gemini API key not found. Add GEMINI_API_KEY in Streamlit secrets to run this app.")
    st.stop()

MODEL = "gemini-2.5-flash"

PERSONA_PROMPT = """You are Professor Neuron, an AI Learning Buddy that teaches {topic} to a
complete beginner learner. Your tone is warm, patient, and encouraging, but precise — you never
give vague praise. Always:
1. Explain concepts in plain, jargon-light language using everyday analogies before introducing
   technical terms.
2. Follow every explanation with one concrete real-life example.
3. When asked to quiz, ask clear, well-scoped questions.
4. When evaluating a learner's answer, say exactly what they got right, correct any misconception
   specifically, and give one memorable tip. Never just say "correct" or "good job" without
   explaining why.
Keep responses focused — no more than 2-3 short paragraphs unless generating a quiz.
"""

TEMPLATES = {
    "Explain the topic": (
        "Explain {topic} to a complete beginner in simple, everyday language. Avoid jargon; "
        "if you must use a technical term, define it immediately in one short sentence. Use an "
        "analogy from daily life to anchor the idea. Keep it to 2 short paragraphs."
    ),
    "Give a real-life example": (
        "Give one clear, real-life example of {topic} in action — something a beginner would "
        "recognize from daily life or a well-known app/technology. Explain in 3-4 sentences how "
        "the example maps back to the concept."
    ),
    "Generate a 5-question quiz": (
        "Generate 5 quiz questions to test a beginner's understanding of {topic}. Include a mix "
        "of conceptual (why/what) and applied (which scenario) questions. List the 5 questions "
        "first without answers, then provide the correct answers with a one-line explanation "
        "each, clearly separated under an 'Answers' heading."
    ),
    "Get feedback on my answer": (
        "The quiz question was: '{question}'. My answer is: '{answer}'. Evaluate my answer: say "
        "specifically what I got right, correct any misconception with a brief explanation, and "
        "give one memorable tip so I retain the correct idea. Be encouraging but precise."
    ),
}

st.title("🧠 AI Learning Buddy — Professor Neuron")
st.caption("Topic: Neural Networks Basics")

topic = st.text_input("Topic", value="Neural Networks Basics")

activity = st.radio(
    "What would you like to do?",
    list(TEMPLATES.keys()),
)

question_input, answer_input = "", ""
if activity == "Get feedback on my answer":
    question_input = st.text_area("Quiz question", placeholder="Paste the quiz question here")
    answer_input = st.text_area("Your answer", placeholder="Type your answer here")

if st.button("Ask Professor Neuron", type="primary"):
    with st.spinner("Professor Neuron is thinking..."):
        user_prompt = TEMPLATES[activity].format(
            topic=topic, question=question_input, answer=answer_input
        )
        try:
            interaction = client.interactions.create(
                model=MODEL,
                system_instruction=PERSONA_PROMPT.format(topic=topic),
                input=user_prompt,
            )
            st.markdown("### Response")
            st.write(interaction.output_text)
        except Exception as e:
            st.error(f"Something went wrong calling the Gemini API: {e}")

st.divider()
st.caption(
    "Built as part of the AI Learning Buddy assignment. Persona, prompt templates, and this "
    "app all teach the same topic so the deliverables stay consistent."
)
