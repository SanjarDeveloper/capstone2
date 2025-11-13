# app.py
import streamlit as st
import io
import tempfile
from openai import OpenAI

st.set_page_config(page_title="Voice to Image App")
st.title("Voice to Image App")

# Sidebar for API key input
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key here.")

if not api_key:
    st.info("Please enter your OpenAI API key in the sidebar to get started.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Main content
st.header("Upload Your Voice Message")
supported_formats = ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']
uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=supported_formats,
    help=f"Record a short voice message describing the image you want (e.g., 'A serene mountain landscape at sunset'). Supported formats: {', '.join(supported_formats)}"
)

def transcribe_with_bytesio(uploaded_file):
    """Try transcribing by passing a BytesIO that has a .name attribute (so API can detect format)."""
    audio_bytes = uploaded_file.read()
    audio_file = io.BytesIO(audio_bytes)
    # IMPORTANT: set a name so the server can infer format from filename extension
    audio_file.name = uploaded_file.name
    audio_file.seek(0)
    return client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",
        language="en"
    )

def transcribe_with_tempfile(uploaded_file):
    """Robust fallback: write to a temporary file with correct suffix and reopen."""
    audio_bytes = uploaded_file.read()
    ext = uploaded_file.name.split('.')[-1] if '.' in uploaded_file.name else ''
    suffix = f".{ext}" if ext else ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        tmp_name = tmp.name
    with open(tmp_name, "rb") as f:
        return client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text",
            language="en"
        )

if uploaded_file is not None:
    # Check extension
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension not in supported_formats:
        st.error(f"Unsupported file format: {file_extension}. Please use one of: {', '.join(supported_formats)}")
        st.stop()

    # Display file details
    file_details = {"Filename": uploaded_file.name, "File size": f"{uploaded_file.size} bytes", "Format": file_extension.upper()}
    st.write("**Uploaded File Details:**")
    for key, value in file_details.items():
        st.write(f"{key}: {value}")

    if st.button("Transcribe and Generate Image"):
        # Transcription
        transcript = None
        with st.spinner("Transcribing your voice message..."):
            try:
                # First try: pass uploaded_file directly (Streamlit file-like object has .name)
                try:
                    # uploaded_file is a BytesIO-like object with .name; rewind first
                    uploaded_file.seek(0)
                    transcript_resp = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=uploaded_file,
                        response_format="text",
                        language="en"
                    )
                except Exception as e1:
                    # If the direct pass fails (some environments), try BytesIO with .name
                    try:
                        uploaded_file.seek(0)
                        transcript_resp = transcribe_with_bytesio(uploaded_file)
                    except Exception as e2:
                        # Fallback: write to a tempfile and re-open
                        uploaded_file.seek(0)
                        transcript_resp = transcribe_with_tempfile(uploaded_file)

                # The SDK may return the transcription text directly or wrapped.
                # Try to extract string safely:
                if isinstance(transcript_resp, str):
                    transcript = transcript_resp
                else:
                    # If an object-like response, attempt common attribute access
                    transcript = getattr(transcript_resp, "text", None) or \
                                 getattr(transcript_resp, "transcript", None) or \
                                 getattr(transcript_resp, "data", None) or \
                                 transcript_resp

                # Ensure it's a string for display
                if not isinstance(transcript, str):
                    transcript = str(transcript)

                st.success("Transcription completed.")
            except Exception as e:
                # Show helpful debug information
                st.error(f"Transcription failed: {e}")
                st.stop()

        # Display transcript
        st.subheader("📝 Recorded Message Transcript")
        st.write(transcript)
        st.session_state.transcript = transcript

        # Generate image prompt using an LLM
        with st.spinner("Converting to detailed image prompt..."):
            try:
                prompt_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert prompt engineer for image generation. Convert the user's spoken description into a highly detailed, vivid prompt optimized for DALL-E 3. Make it creative, specific, and include style, lighting, composition details where appropriate."
                        },
                        {
                            "role": "user",
                            "content": f"User's voice description: {transcript}\n\nGenerate a detailed DALL-E prompt based on this."
                        }
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                image_prompt = prompt_response.choices[0].message.content.strip()
            except Exception as e:
                st.error(f"Prompt generation failed: {e}")
                st.stop()

        st.subheader("🎨 Generated Image Prompt")
        st.write(image_prompt)
        st.session_state.image_prompt = image_prompt

        # Generate image using DALL-E 3
        with st.spinner("Generating your image..."):
            try:
                image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                # Different SDKs/versions may return url or b64. Try several ways:
                image_url = None
                if hasattr(image_response, "data") and image_response.data:
                    first = image_response.data[0]
                    image_url = first.get("url") if isinstance(first, dict) else getattr(first, "url", None)
                    b64 = first.get("b64_json") if isinstance(first, dict) else getattr(first, "b64_json", None)
                    if not image_url and b64:
                        # write base64 to temp file for display
                        import base64, os
                        img_bytes = base64.b64decode(b64)
                        tmp_path = os.path.join(tempfile.gettempdir(), "generated_image.png")
                        with open(tmp_path, "wb") as f:
                            f.write(img_bytes)
                        st.image(tmp_path, caption="Your voice-inspired image", use_container_width=True)
                    elif image_url:
                        st.image(image_url, caption="Your voice-inspired image", use_container_width=True)
                    else:
                        st.error("Image response format unexpected. Inspect console for details.")
                else:
                    st.error("No image returned from API.")
            except Exception as e:
                st.error(f"Image generation failed: {e}")
                st.stop()

        # Summary of intermediates
        with st.expander("🔍 View Full Workflow Summary"):
            st.write("**Models Used:**")
            st.write("- Speech-to-Text: Whisper-1")
            st.write("- LLM for Prompt: GPT-3.5-Turbo")
            st.write("- Image Generation: DALL-E 3")
            st.write("**Intermediate Data:**")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Transcript:**")
                st.code(transcript)
            with col2:
                st.write("**Prompt:**")
                st.code(image_prompt)
else:
    st.info("👆 Upload an audio file above and click 'Transcribe and Generate Image' to start!")
