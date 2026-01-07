"""
UI Components for Fashion Search Engine
Separate file for styling and layout components
"""
import streamlit as st


def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* Global Styles */
        .main {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(to bottom, #f8f9fa, #ffffff);
        }
        
        /* Header Styles */
        .main-header {
            font-size: 3.5rem;
            font-weight: 700;
            text-align: center;
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #FFA726 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            padding: 1rem 0;
        }
        
        .sub-header {
            font-size: 1.3rem;
            text-align: center;
            color: #495057;
            margin-bottom: 2.5rem;
            font-weight: 400;
        }
        
        /* Search Box Styling */
        .stTextInput > div > div > input {
            font-size: 1.05rem;
            padding: 0.95rem 1.8rem;
            border-radius: 12px;
            border: 1.5px solid #e1e4e8;
            transition: all 0.25s ease;
            background: #fafbfc;
            font-weight: 400;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #FF6B6B;
            background: #ffffff;
            box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.08), 0 3px 12px rgba(0, 0, 0, 0.08);
            outline: none;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #6c757d;
            font-weight: 400;
            opacity: 0.7;
        }
        
        /* Button Styling */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #FF6B6B 0%, #FF5252 100%);
            color: white;
            font-size: 0.95rem;
            padding: 0.95rem 2.5rem;
            border-radius: 12px;
            border: none;
            font-weight: 600;
            transition: all 0.25s ease;
            box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);
            letter-spacing: 0.3px;
            text-transform: uppercase;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #FF5252 0%, #FF6B6B 100%);
            box-shadow: 0 4px 14px rgba(255, 107, 107, 0.3);
            transform: translateY(-1px);
        }
        
        .stButton>button:active {
            transform: translateY(0);
            box-shadow: 0 2px 6px rgba(255, 107, 107, 0.25);
        }
        
        /* Result Card Styling */
        .result-card {
            border-radius: 20px;
            padding: 1rem;
            background: white;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
            transition: all 0.4s ease;
            border: 2px solid #f1f3f5;
        }
        
        .result-card:hover {
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 16px 32px rgba(255, 107, 107, 0.15);
            border-color: #FF6B6B;
        }
        
        /* Score Badge */
        .score-badge {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            display: inline-block;
            margin: 4px 2px;
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #fff5f5 0%, #ffffff 100%);
        }
        
        /* Info Box */
        .stAlert {
            border-radius: 16px;
            border-left: 5px solid #FF6B6B;
            background: #fff5f5;
        }
        
        /* Divider */
        hr {
            margin: 2.5rem 0;
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #FFB4B4, #FF6B6B, #FFB4B4, transparent);
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            font-weight: 600;
            border-radius: 12px;
            background: #fff5f5;
        }
        
        /* Download Button */
        .stDownloadButton>button {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
            color: white;
            font-weight: 600;
            border-radius: 25px;
            padding: 1rem 2rem;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stDownloadButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
        }
        
        /* Image Container */
        .stImage {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .stImage:hover {
            box-shadow: 0 8px 20px rgba(255, 107, 107, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the main header"""
    st.markdown('<div class="main-header">✨ Fashion Search Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Discover your perfect style with AI-powered visual search</div>', unsafe_allow_html=True)


def render_sidebar(config, config_path):
    """Render the sidebar with settings"""
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        st.markdown("---")
        
        # Results slider
        st.markdown("**📊 Number of Results**")
        top_k = st.slider(
            "Results to Display",
            min_value=1,
            max_value=20,
            value=config['search']['top_k'],
            step=1,
            label_visibility="collapsed"
        )
        
        # Update config if changed
        if top_k != config['search']['top_k']:
            import yaml
            config['search']['top_k'] = top_k
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f)
        
        st.markdown("---")
        st.markdown("**💡 Example Queries:**")
        st.markdown("""
        - *Person in yellow raincoat*
        - *Black evening dress*
        - *Casual summer outfit*
        - *Formal business attire*
        """)
        
        return top_k


def render_search_box():
    """Render the search input box"""
    st.divider()
    
    # Search input full width
    query = st.text_input(
        "Enter your fashion search query:",
        placeholder="e.g., Person wearing elegant black dress...",
        label_visibility="collapsed",
        key="search_query"
    )
    
    # Center the search button below
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)
    
    return query, search_button


def render_results(results, query, dataset_dir, results_per_row):
    """Render search results in a grid"""
    from PIL import Image
    import os
    
    st.divider()
    
    # Results header
    st.markdown(f"### 🎯 Results for *'{query}'*")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display results in grid
    for i in range(0, len(results), results_per_row):
        cols = st.columns(results_per_row)
        
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(results):
                result = results[idx]
                
                with col:
                    # Container for card effect
                    with st.container():
                        # Load and display image
                        img_path = result['image_path']
                        
                        try:
                            img = Image.open(img_path)
                            st.image(img, use_container_width=True)
                        
                        except Exception as e:
                            st.error(f"❌ Error loading image: {e}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)


def render_export_button(results, query):
    """Render the export results button"""
    # Export functionality disabled
    pass


def render_welcome_message(dataset_dir):
    """Render welcome message with example images"""
    from PIL import Image
    import os
    
    # Show example images
    st.divider()
    st.subheader("📸 Example Images from Dataset")
    
    if os.path.exists(dataset_dir):
        image_files = [f for f in os.listdir(dataset_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if image_files:
            cols = st.columns(min(5, len(image_files)))
            for i, col in enumerate(cols):
                if i < len(image_files):
                    with col:
                        img_path = os.path.join(dataset_dir, image_files[i])
                        img = Image.open(img_path)
                        st.image(img)
                        st.caption(image_files[i])
