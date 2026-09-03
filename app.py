import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)

st.title("✍️ AI Content Assistant")
st.write("Create ready-to-post content with AI in a few clicks.")

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.info(
        "Add your Groq API key in Streamlit Cloud under "
        "Settings → Secrets."
    )

# Inputs
content_type = st.selectbox(
    "1. Content Type",
    [
        "Social Media Post",
        "Promotional Post",
        "Educational Post",
        "Product Description",
        "LinkedIn Post",
        "Instagram Caption",
        "TikTok Caption",
        "Blog Introduction"
    ]
)

platform = st.selectbox(
    "2. Platform",
    [
        "Instagram",
        "Facebook",
        "LinkedIn",
        "TikTok",
        "X (Twitter)",
        "Pinterest",
        "Website/Blog"
    ]
)

topic = st.text_input(
    "3. Topic",
    placeholder="Example: Benefits of digital products"
)

target_audience = st.text_input(
    "4. Target Audience",
    placeholder="Example: Small business owners"
)

tone = st.selectbox(
    "5. Tone",
    [
        "Professional",
        "Friendly",
        "Educational",
        "Persuasive",
        "Casual",
        "Inspirational",
        "Creative"
    ]
)

extra_instructions = st.text_area(
    "Optional instructions",
    placeholder="Example: Include a strong hook and a call to action."
)

generate = st.button("🚀 Generate Content", use_container_width=True)

if generate:
    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    if not target_audience.strip():
        st.warning("Please enter your target audience.")
        st.stop()

    # Read API key from Streamlit secrets
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        st.error(
            "Groq API key not found. Add GROQ_API_KEY to "
            "Streamlit Cloud Secrets."
        )
        st.stop()

    client = Groq(api_key=api_key)

    prompt = f"""
You are a professional AI content writer.

Create a complete piece of content using these requirements:

Content type: {content_type}
Platform: {platform}
Topic: {topic}
Target audience: {target_audience}
Tone: {tone}
Extra instructions: {extra_instructions}

Return the answer in exactly this structure:

TITLE:
Write a short title.

POST:
Write the complete ready-to-post content.

CAPTION:
Write a short engaging caption.

HASHTAGS:
Provide 8-12 relevant hashtags.

CTA:
Write one clear call-to-action.

Rules:
- Make the content original and useful.
- Match the selected platform.
- Keep the language natural and easy to read.
- Do not explain your process.
"""

    with st.spinner("Creating your content..."):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional social media and content writing assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1200
            )

            result = response.choices[0].message.content

            st.success("Content generated successfully!")

            st.subheader("📝 Your Content")
            st.text_area(
                "Generated Content",
                value=result,
                height=500
            )

            st.download_button(
                label="⬇️ Download Content",
                data=result,
                file_name="ai_content.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.divider()
st.caption("AI Content Assistant • Built with Streamlit + Groq")
