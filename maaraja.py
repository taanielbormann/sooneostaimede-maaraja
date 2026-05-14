import streamlit as st
import pandas as pd
import os

# 1. LEHE SEADISTUS
st.set_page_config(
    page_title="Eesti sooneostaimede eoste määraja", 
    page_icon="🌿", 
    layout="wide"
)

# --- CSS: DISAIN JA KOMPAKTSUS ---
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] {
        align-items: start !important;
    }
    
    h1 { 
        color: #2e7d32 !important; 
        margin-left: -20px !important; 
    }

    /* Pildi suuruse kontroll */
    [data-testid="stImage"] img {
        max-width: 100% !important;
        height: auto !important;
        border-radius: 8px;
    }

    /* Slaiderite puhastus */
    div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"],
    div[data-baseweb="typo-caption-12"], .st-emotion-cache-1ghh6m9 { 
        display: none !important; 
    }
    
    .stSuccess { background-color: #e8f5e9; border-color: #2e7d32; color: #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# --- ANDMETE LAADIMINE (CACHE) ---
@st.cache_data
def load_data():
    file_path = 'Fixed_Spore_Data.csv'
    try:
        data = pd.read_csv(file_path, encoding='cp1252')
    except:
        data = pd.read_csv(file_path, encoding='latin-1')
    
    data.columns = data.columns.str.strip()
    if 'description' in data.columns:
        data['description'] = data['description'].str.replace('\x96', '–', regex=True).str.replace('\xad', '-', regex=True)
    return data

def format_name(name):
    if "(" in str(name):
        parts = name.split("(")
        return f"{parts[0].strip()} (*{parts[1].replace(')', '').strip()}*)"
    return name

# --- PÄIS ---
col_logo, col_title = st.columns([1, 10]) 
with col_logo:
    st.image("pildid/fern.png", width=90) if os.path.exists("pildid/fern.png") else st.write("🌿")
with col_title:
    st.title("Eesti sooneostaimede eoste määraja")

st.divider()

try:
    df = load_data().copy()

    # --- SIDEBAR FILTRID ---
    st.sidebar.header("Määramistunnused")
    
    with st.sidebar.expander("Kuju", expanded=False):
        for shape, img in [("shape_bilateral", "bilateral.png"), ("shape_tetra", "tetra.png")]:
            if shape in df.columns:
                c1, c2 = st.columns([4, 1])
                if c1.checkbox(shape.split('_')[1].capitalize(), key=f"chk_{shape}"):
                    df = df[df[shape] == 1]
                if os.path.exists(f"pildid/{img}"): c2.image(f"pildid/{img}")

    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        # Retikulaarne esiletooduna
        if 'surf_reticulate' in df.columns:
            c1, c2 = st.columns([4, 1])
            if c1.checkbox("Retikulaarne", key="chk_retic"): df = df[df['surf_reticulate'] == 1]
            if os.path.exists("pildid/reticulate.png"): c2.image("pildid/reticulate.png")
        
        st.divider()
        surfaces = {"Ogaline": "surf_echinate", "Tüükaline": "surf_verrucate", "Konksuline": "surf_hamulate", "Sile": "surf_psilate"}
        for label, col in surfaces.items():
            if col in df.columns and st.checkbox(label, key=f"chk_{col}"):
                df = df[df[col] == 1]

    # --- TULEMUSED ---
    if len(df) == 0:
        st.warning("Vasteid ei leitud.")
    else:
        st.success(f"Leitud vasteid: {len(df)}")
        for _, row in df.iterrows():
            fname = format_name(row['species'])
            with st.expander(fname):
                st.markdown(f"### {fname}")
                # gap="large" teeb paigutuse puhtamaks
                t_col, i_col = st.columns([2, 1], gap="large")
                with t_col:
                    st.write("**Kirjeldus:**")
                    st.write(row.get('description', 'Puudub.'))
                    st.write(f"📐 **P:** {row.get('P_mean', '-')} µm | **E:** {row.get('E_mean', '-')} µm")
                with i_col:
                    if pd.notna(row.get('image_url')):
                        st.image(row['image_url'], use_container_width=True)

except Exception as e:
    st.error(f"Viga: {e}")
