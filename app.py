"""
Streamlit Interface for Fashion Search Engine

A beautiful, user-friendly interface for searching fashion images
"""
import streamlit as st
import yaml
import os
import sys

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
retrieval_dir = os.path.join(current_dir, 'Retrieval_Pipeline')
sys.path.insert(0, retrieval_dir)

from retrieval_pipeline import RetrievalPipeline
from ui.ui_components import (
    apply_custom_css,
    render_header,
    render_sidebar,
    render_search_box,
    render_results,
    render_export_button,
    render_welcome_message
)

# Page config
st.set_page_config(
    page_title="Fashion Search Engine",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()


@st.cache_resource
def load_pipeline():
    """Load retrieval pipeline (cached)"""
    config_path = os.path.join(current_dir, 'Retrieval_Pipeline', 'config', 'retrieval.yaml')
    pipeline = RetrievalPipeline(config_path)
    return pipeline


def main():
    # Header
    render_header()
    
    # Load config
    config_path = os.path.join(current_dir, 'Retrieval_Pipeline', 'config', 'retrieval.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Sidebar with settings
    top_k = render_sidebar(config, config_path)
    
    # Search section
    query, search_button = render_search_box()
    
    # Search execution
    if search_button or (query and 'last_query' in st.session_state and st.session_state.last_query != query):
        if query.strip():
            st.session_state.last_query = query
            
            with st.spinner("🔄 Searching... This may take a few seconds..."):
                try:
                    # Load pipeline
                    pipeline = load_pipeline()
                    
                    # Update search parameters
                    pipeline.top_n = config['search']['top_n']  # Use config value for top_n
                    pipeline.top_k = top_k
                    
                    # Perform search
                    results = pipeline.search(query)
                    
                    # Store results in session state
                    st.session_state.results = results
                    st.session_state.query = query
                    
                except Exception as e:
                    st.error(f"❌ Error during search: {str(e)}")
                    st.exception(e)
        else:
            st.warning("⚠️ Please enter a search query")
    
    # Display results
    if 'results' in st.session_state and st.session_state.results:
        dataset_dir = os.path.join(current_dir, 'Dataset')
        results_per_row = config['ui']['results_per_row']
        
        render_results(st.session_state.results, st.session_state.query, dataset_dir, results_per_row)
        render_export_button(st.session_state.results, st.session_state.query)
    
    elif 'results' in st.session_state and not st.session_state.results:
        st.info("🔍 No results found. Try a different query!")
    
    else:
        # Welcome message
        dataset_dir = os.path.join(current_dir, 'Dataset')
        render_welcome_message(dataset_dir)


if __name__== "__main__":
    main()
