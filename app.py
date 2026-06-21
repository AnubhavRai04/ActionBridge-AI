import streamlit as st
from pypdf import PdfReader
from groq import Groq


client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

st.title("ActionBridge AI")

st.set_page_config(
    page_title="ActionBridge AI",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0f172a;
}

/* Main text */
h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}

/* Text area */
textarea {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #1e293b;
    border: 2px dashed #3b82f6;
    border-radius: 15px;
    padding: 20px;
}

/* Buttons */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}

/* Button hover */
.stButton > button:hover {
    background-color: #1d4ed8;
}

</style>
""", unsafe_allow_html=True)

st.info("""
📄 Document / Situation

⬇️

🧠 AI Analysis

⬇️

✅ Clear Guidance & Next Steps
""")

# -----------------------------
# INPUTS
# -----------------------------

col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader(
        "📄 Upload Document",
        type=["pdf"]
    )

with col2:
    user_input = st.text_area(
        "❓ What are you confused about?",
        height=180,
        placeholder="""
Examples:

• Am I eligible for this scholarship?

• What documents do I need?

• What should I do next?

• Is there an important deadline?

• I don't understand this notice.
"""
    )


document_text = ""

if uploaded_file:

    st.success("Document uploaded successfully")

    try:
        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                document_text += page_text + "\n"

        MAX_CHARS = 15000

        if len(document_text) > MAX_CHARS:
            document_text = document_text[:MAX_CHARS]

            st.warning(
                "Large document detected. Only the first part of the document will be analyzed."
            )

        with st.expander("View Extracted Text"):
            st.text_area(
                "Document Content",
                document_text,
                height=300
            )

    except Exception as e:
        st.error(f"Error reading PDF: {e}")


if st.button("🚀 Get Guidance", use_container_width=True):
    
    if not document_text and not user_input.strip():

        st.warning(
            "Please upload a document, describe a situation, or do both."
        )

        st.stop()

    content = ""

    if document_text:
        content += f"""
DOCUMENT:

{document_text}

"""

    if user_input.strip():
        content += f"""
USER CONCERN:

{user_input}

"""
    elif document_text:
        content += """
The user uploaded a document and wants help understanding it.
"""

    with st.spinner("🧠 Understanding your situation..."):

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are ActionBridge AI.

Your purpose is to help people understand confusing
documents, notices, requirements, instructions,
support resources, and real-world situations.

The user may provide:
- A document
- A description of their situation
- Both

Your job is to:

1. Understand what the user is confused about.
2. Explain information in simple language.
3. Answer the user's concern directly.
4. Suggest practical next steps when appropriate.
5. Mention support resources when relevant.

Do not behave like a general chatbot.

Do not answer requests about:
- entertainment
- gaming
- jokes
- dating
- random casual conversation

If the request is unrelated to understanding
a document, situation, decision, requirement,
or support need, politely explain that
ActionBridge AI is designed to help people
understand important information and determine
next steps.

Keep responses natural.

Avoid rigid templates like:
- Situation Summary
- What This Means
- Recommended Actions

Only use headings if they genuinely improve clarity.
"""
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )

            answer = response.choices[0].message.content

            st.success("✅ Guidance Ready")
            
            st.markdown(answer)

        except Exception as e:

            st.error(
                f"AI Error: {e}"
            )

            st.divider()

            st.caption(
    "ActionBridge AI • USAII Global AI Hackathon 2026"
)
