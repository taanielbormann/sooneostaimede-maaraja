import streamlit as st
import pandas as pd
import os

# 1. LEHE SEADISTUS
st.set_page_config(
    page_title="Eesti sooneostaimede eoste määraja", 
    page_icon="🌿", 
    layout="wide"
)

# --- CSS: SLAIDERID JA PEALKIRJA POSITSIOON ---
st.markdown("""
    <style>
    /* 1. PEALKIRJA JA LOGO LÄHENDAMINE */
    /* Kaotame tulpade vahelise tühiku ja joondame sisu */
    [data-testid="stHorizontalBlock"] {
        gap: 0rem !important;
        align-items: center !important;
    }
    
    h1 { 
        color: #2e7d32 !important; 
        margin-left: -20px !important; /* Toob teksti pildile lähemale */
        padding-top: 0px !important;
    }

    /* 2. SLAIDERI PUHASTUS: Peidame ainult alumised numbrid ja kastid */
    div[data-testid="stTickBarMin"], 
    div[data-testid="stTickBarMax"],
    div[data-baseweb="typo-caption-12"],
    .st-emotion-cache-1ghh6m9, 
    .st-emotion-cache-16idsys,
    .st-emotion-cache-p5mre8,
    .st-emotion-cache-1kyf5f6 { 
        display: none !important; 
    }
    
    /* Tagame, et ülemised väärtused (punased/rohelised) jäävad nähtavale */
    div[data-testid="stThumbValue"] { 
        font-weight: bold !important;
    }

    /* Expanderite päised küljel */
    .st-emotion-cache-p4m61c p { color: #1b5e20 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- PEALKIRI KOOS LOGOGA ---
logo_path = "pildid/fern.png"
# Muutsime suhet [1, 10], et pealkiri ei oleks surutud kaugele paremale
col_logo, col_title = st.columns([1, 10]) 

with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    else:
        st.write("🌿")

with col_title:
    st.title("Eesti sooneostaimede eoste määraja")

st.divider()

try:
    # --- ANDMETE LAADIMINE ---
    try:
        df = pd.read_csv('Fixed_Spore_Data.csv', encoding='cp1252')
    except:
        df = pd.read_csv('Fixed_Spore_Data.csv', encoding='latin-1')
    
    df.columns = df.columns.str.strip()
    
    # --- FILTRID KÜLJEPEAL ---
    st.sidebar.header("Määramistunnused")
    
    # Kuju, Perispoor ja Pinnastruktuur (standardne kood)
    with st.sidebar.expander("Kuju", expanded=False):
        # ... (siin on sinu olemasolev kuju valiku kood) ...
        pass

    # --- SUURUSE SLAIDERID ---
    # Polaartelg
    if 'P_mean' in df.columns:
        with st.sidebar.expander("Polaartelg (µm)", expanded=False):
            p_data = df['P_mean'].dropna()
            if not p_data.empty:
                p_min, p_max = float(p_data.min()), float(p_data.max())
                # label_visibility="collapsed" eemaldab slaideri sisese sildi, hoides vaate puhtana
                v_p = st.slider("Polaartelg", p_min, p_max, (p_min, p_max), key="s_p", label_visibility="collapsed")
                df = df[(df['P_mean'].between(v_p[0], v_p[1])) | (df['P_mean'].isna())]

    # Ekvatoriaaldiameeter
    if 'E_mean' in df.columns:
        with st.sidebar.expander("Ekvatoriaaldiameeter (µm)", expanded=False):
            e_data = df['E_mean'].dropna()
            if not e_data.empty:
                e_min, e_max = float(e_data.min()), float(e_data.max())
                v_e = st.slider("Ekvatoriaaldiameeter", e_min, e_max, (e_min, e_max), key="s_e", label_visibility="collapsed")
                df = df[(df['E_mean'].between(v_e[0], v_e[1])) | (df['E_mean'].isna())]

    # --- TULEMUSTE KUVAMINE ---
    vastete_arv = len(df)
    st.success(f"Leitud vasteid: {vastete_arv}")

    for _, row in df.iterrows():
        species_raw = str(row['species'])
        eesti = species_raw.split("(")[0].strip()
        with st.expander(eesti):
            st.write(row.get('description', 'Kirjeldus puudub.'))
            st.write(f"📐 Polaartelg: {row.get('P_mean', '-')} µm")
            st.write(f"📐 Ekvatoriaaldiameeter: {row.get('E_mean', '-')} µm")

except Exception as e:
    st.error(f"Viga: {e}")
    
