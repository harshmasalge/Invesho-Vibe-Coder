import streamlit as st
from scraper import get_sample_data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from matplotlib.colors import LinearSegmentedColormap

# Set Streamlit page config
st.set_page_config(page_title="Invesho Vibe Coder Tool", layout="wide")

# Custom CSS: glassmorphic sidebar, responsive UI, tag pills, footer
st.markdown("""
    <style>
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="collapsedControl"] {
            display: block !important;
        }
    }
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
        padding: 2rem 1.5rem;
        width: 320px !important;
    }
    [data-testid="stSidebar"] h1 {
        font-size: 1.4rem !important;
        font-weight: bold;
        color: white !important;
    }
    .tag {
        display: inline-block;
        background: linear-gradient(to right, #38ef7d, #11998e);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 2px 6px 6px 0;
    }
    .footer {
        font-size: 0.9rem;
        color: #aaa;
        text-align: center;
        margin-top: 3rem;
        padding: 1rem 0;
        border-top: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# Hero section
st.title("🔍 Product Hunt Trends Analyzer")
st.markdown("Explore top-performing products, popular tags, and engagement metrics to craft a data-driven launch strategy.")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["📊 Trending Products", "🏷️ Tag Frequency Analysis"])

# Maintain product limit state
if "post_limit" not in st.session_state:
    st.session_state.post_limit = 5

# Caching data based on limit
@st.cache_data
def fetch_data(limit):
    return get_sample_data(limit)

data = fetch_data(st.session_state.post_limit)

# Trending products page
if page == "📊 Trending Products":
    if not data:
        st.warning("❌ No data received from Product Hunt API.")
    else:
        for product in data:
            st.subheader(product["name"])
            st.markdown(f"*{product['tagline']}*")

            col1, col2 = st.columns([1, 4])
            with col1:
                st.metric("Upvotes", product["upvotes"])
                st.metric("Comments", product["comments"])

            with col2:
                st.markdown("**Tags:**")
                if product["tags"]:
                    for tag in product["tags"]:
                        st.markdown(f"<span class='tag'>{tag}</span>", unsafe_allow_html=True)
                else:
                    st.write("N/A")

            st.markdown("---")

        # Show 'Fetch More' if under 100
        if st.session_state.post_limit < 100:
            if st.button("Fetch More Products"):
                with st.spinner("🔄 Loading more..."):
                    st.session_state.post_limit += 5
                    st.rerun()
        else:
            st.info("✅ You've reached the maximum limit of 100 products.")

# Tag frequency page
elif page == "🏷️ Tag Frequency Analysis":
    st.subheader("Tag Frequency Analysis")

    if not data:
        st.error("❌ No data available.")
    else:
        all_tags = [tag for product in data for tag in product["tags"]]
        if not all_tags:
            st.warning("No tags found to analyze.")
        else:
            tag_counts = pd.Series(all_tags).value_counts()
            top_n = st.slider("Select number of top tags to display", 5, min(20, len(tag_counts)), 10)
            top_tags = tag_counts.head(top_n)

            cmap = LinearSegmentedColormap.from_list("green_red", ["#38ef7d", "#ff6b6b", "#c2185b"])
            norm = plt.Normalize(top_tags.min(), top_tags.max())
            colors = [cmap(norm(value)) for value in top_tags.values]

            fig, ax = plt.subplots(figsize=(10, 5))
            bars = ax.bar(top_tags.index, top_tags.values, color=colors, edgecolor='#333', linewidth=0.7, alpha=0.85)
            ax.set_facecolor('#111')
            fig.patch.set_facecolor('#111')
            ax.set_title("Most Common Tags", color='white', fontweight='bold')
            ax.set_ylabel("Frequency (number of occurrences in the fetched products)", color='white')
            ax.set_xlabel("Tag", color='white')
            ax.tick_params(axis='x', colors='white', rotation=45)
            ax.tick_params(axis='y', colors='white')
            ax.grid(True, alpha=0.2)

            st.pyplot(fig)

# Footer
st.markdown("<div class='footer'>© 2025 Invesho. Built with ❤️ using Product Hunt API and Streamlit.</div>", unsafe_allow_html=True)
