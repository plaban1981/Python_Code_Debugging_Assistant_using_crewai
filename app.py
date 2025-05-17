import streamlit as st
from main import debug_code
import json
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import time

# Set page configuration
st.set_page_config(
    page_title="Code Debugging Assistant",
    page_icon="🐛",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .output-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .code-container {
        background-color: #1e1e1e;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .error-text {
        color: #ff4b4b;
        font-weight: bold;
    }
    .fix-text {
        color: #00cc00;
        font-weight: bold;
    }
    .header-text {
        color: #0083B8;
        font-weight: bold;
    }
    """ + HtmlFormatter().get_style_defs('.highlight') + """
</style>
""", unsafe_allow_html=True)

# Header
st.title("🐛 Code Debugging Assistant")
st.markdown("""
<p style='font-size: 1.2em; color: #666;'>
    Upload your Python code and let our AI-powered assistant help you identify and fix errors.
</p>
""", unsafe_allow_html=True)

# Code input
st.markdown("<h3 class='header-text'>📝 Your Code</h3>", unsafe_allow_html=True)
code_input = st.text_area(
    "Enter your Python code here:",
    height=200,
    help="Paste your Python code here for analysis",
    key="code_input"
)

# Debug button
if st.button("🔍 Debug Code", type="primary"):
    if code_input.strip():
        with st.spinner("🔄 Analyzing your code..."):
            try:
                # Get debugging results
                result = debug_code(code_input)
                
                # Extract the Pydantic model data
                if hasattr(result, 'pydantic'):
                    debug_data = result.pydantic
                    
                    # Create three columns for output
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("<h3 class='header-text'>🔍 Analysis Results</h3>", unsafe_allow_html=True)
                        
                        # Display errors if any
                        st.markdown("<h4>Found Errors:</h4>", unsafe_allow_html=True)
                        if debug_data.error and debug_data.error.lower() != "none":
                            st.markdown(f"<div class='error-text'>{debug_data.error}</div>", unsafe_allow_html=True)
                        else:
                            st.success("No errors found in the code!")
                        
                        # Display fixes if any
                        st.markdown("<h4>Applied Fixes:</h4>", unsafe_allow_html=True)
                        if debug_data.fix and debug_data.fix.lower() != "none":
                            st.markdown(f"<div class='fix-text'>{debug_data.fix}</div>", unsafe_allow_html=True)
                        else:
                            st.info("No fixes were necessary.")
                    
                    with col2:
                        st.markdown("<h3 class='header-text'>✨ Corrected Code</h3>", unsafe_allow_html=True)
                        
                        # Display the corrected code with syntax highlighting
                        highlighted_code = highlight(
                            debug_data.rectifiled_code,
                            PythonLexer(),
                            HtmlFormatter(style='monokai')
                        )
                        st.markdown(f"<div class='code-container'>{highlighted_code}</div>", unsafe_allow_html=True)
                        
                        # Add copy button for the corrected code
                        st.code(debug_data.rectifiled_code, language="python")
                        
                else:
                    st.error("Failed to process the debugging results.")
                    
            except Exception as e:
                st.error(f"An error occurred while debugging: {str(e)}")
    else:
        st.warning("Please enter some code to debug!")

# Footer
st.markdown("""
<div style='margin-top: 50px; text-align: center; color: #666;'>
    <hr>
    <p>Built with ❤️ using Streamlit and CrewAI</p>
</div>
""", unsafe_allow_html=True) 