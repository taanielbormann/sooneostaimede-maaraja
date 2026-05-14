import streamlit as st
import pandas as pd
import os

# 1. LEHE SEADISTUS
st.set_page_config(
    page_title="Eesti sooneostaimede eoste määraja", 
    page_icon="🌿", 
    layout="wide"
)

# --- CSS: DISAINI PARANDUSED ---
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    h1 { 
        color: #2e7d32 !important; 
    }
    /* Pildi suuruse kontroll, et see ei veniks */
    [data-testid="stImage"] img {
        max-width: 400px !important;
        border-radius: 8px;
    }
    /* Slaiderite visuaalne puhastus */
    div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"],
    div[data-baseweb="typo-caption-12"], .st-emotion-cache-1ghh6m9 { 
        display: none !important; 
    }
    .stSuccess { background-color: #e8f5e9; border-color: #2e7d32; color: #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# --- ANDMETE LAADIMINE (VAHEMÄLUS) ---
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
    name_str = str(name)
    if "(" in name_str:
        parts = name_str.split("(")
        return f"{parts[0].strip()} (*{parts[1].replace(')', '').strip()}*)"
    return name_str

# --- PÄIS ---
col_logo, col_title = st.columns([1, 8]) 
with col_logo:
    if os.path.exists("pildid/fern.png"):
        st.image("pildid/fern.png", width=80)
    else:
        st.write("🌿")
with col_title:
    st.title("Eesti sooneostaimede eoste määraja")

st.divider()

try:
    df_full = load_data()
    df = df_full.copy()

    # --- SIDEBAR: FILTRID ---
    st.sidebar.header("Määramistunnused")
    
    # KUJU
    with st.sidebar.expander("Kuju", expanded=False):
        if 'shape_bilateral' in df.columns:
            c1, c2 = st.columns([3, 1])
            if c1.checkbox("Bilateraalne", key="c_bil"): df = df[df['shape_bilateral'] == 1]
            if os.path.exists("pildid/bilateral.png"): c2.image("pildid/bilateral.png")
            
        if 'shape_tetra' in df.columns:
            c1, c2 = st.columns([3, 1])
            if c1.checkbox("Tetraeedriline", key="c_tet"): df = df[df['shape_tetra'] == 1]
            if os.path.exists("pildid/tetra.png"): c2.image("pildid/tetra.png")

    # PINNASTRUKTUUR
    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        if 'surf_reticulate' in df.columns:
            c1, c2 = st.columns([3, 1])
            if c1.checkbox("Retikulaarne", key="c_ret"): df = df[df['surf_reticulate'] == 1]
            if os.path.exists("pildid/reticulate.png"): c2.image("pildid/reticulate.png")
        
        st.divider()
        muud = {"Ogaline": "surf_echinate", "Tüükaline": "surf_verrucate", "Konksuline": "surf_hamulate", "Sile": "surf_psilate"}
        for silt, veerg in muud.items():
            if veerg in df.columns:
                if st.checkbox(silt, key=f"ch_{veerg}"): df = df[df[veerg] == 1]

    # SUURUS
    if 'P_mean' in df.columns:
        with st.sidebar.expander("Polaartelg (P)", expanded=False):
            p_val = st.slider("P µm", float(df_full['P_mean'].min()), float(df_full['P_mean'].max()), 
                             (float(df_full['P_mean'].min()), float(df_full['P_mean'].max())), key="s_p")
            df = df[df['P_mean'].between(p_val[0], p_val[1])]

    # --- TULEMUSED ---
    if len(df) == 0:
        st.warning("Vasteid ei leitud.")
    else:
        st.success(f"Leitud vasteid: {len(df)}")
        for _, row in df.iterrows():
            display_name = format_name(row['species'])
            with st.expander(display_name):
                st.markdown(f"### {display_name}")
                col1, col2 = st.columns([2, 1], gap="medium")
                with col1:
                    st.write("**Eose kirjeldus:**")
                    st.write(row.get('description', 'Kirjeldus puudub.'))
                    st.write(f"📐 **P:** {row.get('P_mean', '-')} µm | **E:** {row.get('E_mean', '-')} µm")
                with col2:
                    if pd.notna(row.get('image_url')):
                        st.image(row['image_url'], use_container_width=True)

except Exception as e:
    st.error(f"Viga: {e}")
