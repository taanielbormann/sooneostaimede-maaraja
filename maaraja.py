import streamlit as st
import pandas as pd
import os

# 1. LEHE SEADISTUS
st.set_page_config(
    page_title="Eesti sooneostaimede eoste määraja", 
    page_icon="🌿", 
    layout="wide"
)

# --- CSS: SLAIDERID, LOGO JA VÄLIMUS ---
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] {
        gap: 2rem !important;
    }
    
    h1 { 
        color: #2e7d32 !important; 
    }

    /* Pildi suuruse piiramine */
    [data-testid="stImage"] img {
        max-width: 450px !important;
        height: auto !important;
        border-radius: 10px;
    }

    /* Slaiderite puhastus (numbrite peitmine) */
    div[data-testid="stTickBarMin"], 
    div[data-testid="stTickBarMax"],
    div[data-baseweb="typo-caption-12"],
    .st-emotion-cache-1ghh6m9 { 
        display: none !important; 
    }
    
    .stSuccess { background-color: #e8f5e9; border-color: #2e7d32; color: #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTSIOONID ---
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

def format_species_name(raw_name):
    raw_str = str(raw_name)
    if "(" in raw_str and ")" in raw_str:
        parts = raw_str.split("(")
        return f"{parts[0].strip()} (*{parts[1].replace(')', '').strip()}*)"
    return raw_str

# --- PEALKIRI ---
logo_path = "pildid/fern.png"
col_logo, col_title = st.columns([1, 10]) 
with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=80)
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
    
    # 1. KUJU
    with st.sidebar.expander("Kuju", expanded=False):
        if 'shape_bilateral' in df.columns:
            c1, c2 = st.columns([4, 1])
            if c1.checkbox("Bilateraalne", key="chk_bilat"): df = df[df['shape_bilateral'] == 1]
            if os.path.exists("pildid/bilateral.png"): c2.image("pildid/bilateral.png")
        
        if 'shape_tetra' in df.columns:
            c1, c2 = st.columns([4, 1])
            if c1.checkbox("Tetraeedriline", key="chk_tetra"): df = df[df['shape_tetra'] == 1]
            if os.path.exists("pildid/tetra.png"): c2.image("pildid/tetra.png")

    # 2. PERISPOOR
    with st.sidebar.expander("Perispoor", expanded=False):
        if 'perine_absent' in df.columns:
            if st.checkbox("Perispoor puudub", key='p_abs'): df = df[df['perine_absent'] == 1]
            if st.checkbox("Perispoor olemas", key='p_pres'): df = df[df['perine_absent'] == 0]

    # 3. PINNASTRUKTUUR
    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        if 'surf_reticulate' in df.columns:
            c1, c2 = st.columns([4, 1])
            if c1.checkbox("Retikulaarne (reticulate)", key="chk_retic"): df = df[df['surf_reticulate'] == 1]
            if os.path.exists("pildid/reticulate.png"): c2.image("pildid/reticulate.png")
        
        st.divider()
        muud_pinnad = {
            "Ogaline (echinate)": "surf_echinate", 
            "Peeneogaline (microechinate)": "surf_microechinate",
            "Tüükaline (verrucate)": "surf_verrucate", 
            "Konksuline (hamulate)": "surf_hamulate",
            "Sile (psilate)": "surf_psilate",
            "Kurruline (rugulate)": "surf_rugulate",
            "Harjaline (cristate)": "surf_cristate"
        }
        for silt, veerg in muud_pinnad.items():
            if veerg in df.columns and st.checkbox(silt, key=f"chk_{veerg}"):
                df = df[df[veerg] == 1]

    # 4. SUURUSED
    if 'P_mean' in df.columns:
        with st.sidebar.expander("Polaartelg (µm)", expanded=False):
            p_min, p_max = float(df_full['P_mean'].min()), float(df_full['P_mean'].max())
            v_p = st.slider("P", p_min, p_max, (p_min, p_max), key="s_p")
            df = df[df['P_mean'].between(v_p[0], v_p[1])]

    if 'E_mean' in df.columns:
        with st.sidebar.expander("Ekvatoriaaldiameeter (µm)", expanded=False):
            e_min, e_max = float(df_full['E_mean'].min()), float(df_full['E_mean'].max())
            v_e = st.slider("E", e_min, e_max, (e_min, e_max), key="s_e")
            df = df[df['E_mean'].between(v_e[0], v_e[1])]

    # --- TULEMUSED ---
    vastete_arv = len(df)
    if vastete_arv == 0:
        st.warning("Valitud tunnustega vasteid ei leitud.")
    else:
        st.success(f"Leitud vasteid: {vastete_arv}")
        for _, row in df.iterrows():
            f_name = format_species_name(row['species'])
            with st.expander(f_name):
                st.markdown(f"### {f_name}")
                col_text, col_img = st.columns([2, 1])
                with col_text:
                    st.write("**Eose kirjeldus:**")
                    st.write(row.get('description', 'Kirjeldus puudub.'))
                    st.divider()
                    # Siin on P ja E üksteise all
                    st.write(f"📐 **Polaartelg:** {row.get('P_mean', '-')} µm")
                    st.write(f"📐 **Ekvatoriaaldiameeter:** {row.get('E_mean', '-')} µm")
                with col_img:
                    if pd.notna(row.get('image_url')):
                        st.image(row['image_url'], use_container_width=True)

except Exception as e:
    st.error(f"Viga rakenduse töös: {e}")
