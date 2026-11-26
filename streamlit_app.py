
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="CraftLens",
    page_icon="🧶",
    layout="wide"
)

# API URL
API_URL = "http://127.0.0.1:8000/analyze-craft"

# Custom styling
st.markdown("""
<style>
.main {
    background-color: #fffaf7;
}
h1 {
    color: #9b4564;
}
.stButton > button {
    background-color: #9b4564;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🧶 CraftLens")
st.subheader("Turn your craft inspiration into reality!")
st.write(
    "Upload a craft image and let CraftLens analyze "
    "its materials, tools, difficulty and instructions."
)

st.divider()

# Image uploader
uploaded_file = st.file_uploader(
    "Upload your craft image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file is not None:

    image_bytes = uploaded_file.getvalue()

    # Display uploaded image
    col1, col2 = st.columns(2)

    with col1:
        st.image(
            image_bytes,
            caption="Your uploaded craft",
            use_container_width=True
        )

    with col2:
        st.write("### Ready to analyze?")
        st.write("Click below to discover your craft details.")

        if st.button("Analyze My Craft", use_container_width=True):

            with st.spinner("CraftLens is analyzing your image..."):

                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            image_bytes,
                            uploaded_file.type
                        )
                    }

                    response = requests.post(
                        API_URL,
                        files=files,
                        timeout=120
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.success("Craft analysis completed!")

                        st.session_state["result"] = result

                    else:
                        st.error(
                            f"API Error: {response.text}"
                        )

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Cannot connect to FastAPI. "
                        "Please start your backend first."
                    )

                except requests.exceptions.Timeout:
                    st.error(
                        "Analysis is taking too long. Please try again."
                    )

                except Exception as error:
                    st.error(f"Something went wrong: {error}")


# Display analysis results
if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()
    st.header("✨ Craft Analysis")

    craft = result.get("craft_analysis", {})

    st.subheader(
        craft.get("craft_name", "Craft Details")
    )

    st.write(craft.get("description", "No description available."))

    # Difficulty and confidence
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Difficulty",
            craft.get("difficulty", "Unknown")
        )

    with col2:
        st.metric(
            "Confidence",
            craft.get("confidence", "Unknown")
        )

    # Visible objects
    st.subheader("👀 Visible Objects")
    st.write(craft.get("visible_objects", []))

    # Materials
    st.subheader("🧵 Possible Materials")
    st.write(craft.get("possible_materials", []))

    # Wire details
    st.subheader("🔗 Wire Information")

    wire = {
        "Wire Type": craft.get("wire_type", "Unknown"),
        "Wire Material": craft.get("wire_material", "Unknown"),
        "Estimated Thickness": craft.get("estimated_thickness", "Unknown"),
        "Flexibility": craft.get("wire_flexibility", "Unknown")
    }

    st.json(wire)

    # Required tools
    st.subheader("🛠️ Required Tools")
    st.write(craft.get("required_tools", []))

    # Crafting steps
    st.subheader("📋 Step-by-Step Instructions")

    for index, step in enumerate(craft.get("steps", []), start=1):
        st.write(f"**Step {index}:** {step}")

    # OCR
    st.subheader("📝 Extracted Text")
    st.write(result.get("extracted_text", "No text found."))

    # Material analysis
    st.subheader("📦 Material Analysis")
    st.json(result.get("material_analysis", {}))

    st.info(
        "Material quantities are approximate. "
        "Always verify measurements before starting your craft."
    )

    # Download results
    st.download_button(
        label="Download Analysis",
        data=str(result),
        file_name="craftlens_analysis.txt",
        mime="text/plain"
    )
