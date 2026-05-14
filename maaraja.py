import streamlit as st
import pandas as pd
import os

# --- 1. LEHE SEADISTUS ---
st.set_page_config(
    page_title="Eesti sooneostaimede eoste määraja", 
    page_icon="🌿", 
    layout="wide"
)

# --- 2. CSS VÄLIMUSE JAOKS ---
st.markdown("""
    <style>
    /* Põhipaigutuse vahed */
    [data-testid="stHorizontalBlock"] { gap: 2rem !important; }
    h1 { color: #2e7d32 !important; }
    
    /* Peapildi suuruse piirang tulemustes, et see ei veniks */
    [data-testid="stImage"] img {
        max-width: 450px !important;
        height: auto !important;
        border-radius: 8px;
    }

    /* Külgmenüü pisipiltide suurus */
    [data-testid="stSidebar"] [data-testid="stImage"] img {
        max-width: 100% !important; 
    }

    /* Slaiderite visuaalne puhastus */
    div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"],
    div[data-baseweb="typo-caption-12"], .st-emotion-cache-1ghh6m9 { 
        display: none !important; 
    }
    
    /* Edu-teate värv */
    .stSuccess { background-color: #e8f5e9; border-color: #2e7d32; color: #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNKTSIOONID ---
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
    """Vormindab nime nii, et sulgudes olev ladina keel läheb kaldkirja."""
    raw_str = str(raw_name)
    if "(" in raw_str and ")" in raw_str:
        parts = raw_str.split("(")
        return f"{parts[0].strip()} (*{parts[1].replace(')', '').strip()}*)"
    return raw_str

# --- 4. PEALKIRI ---
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

# --- 5. PÕHIPROGRAMM ---
try:
    df_full = load_data()
    df = df_full.copy()

    # === KÜLGMENÜÜ: FILTRID ===
    st.sidebar.header("Määramistunnused")
    
    # --- KUJU ---
    with st.sidebar.expander("Kuju", expanded=False):
        # Bilateraalne
        if 'shape_bilateral' in df.columns:
            c1, c2 = st.columns([2, 1], vertical_alignment="center")
            with c1:
                if st.checkbox("Bilateraalne", key="chk_bilat"): 
                    df = df[df['shape_bilateral'] == 1]
            with c2:
                if os.path.exists("pildid/bilateral.png"):
                    st.image("pildid/bilateral.png", use_container_width=True)
                else: st.write("💊")
        
        # Tetraeedriline
        if 'shape_tetra' in df.columns:
            c1, c2 = st.columns([2, 1], vertical_alignment="center")
            with c1:
                if st.checkbox("Tetraeedriline", key="chk_tetra"): 
                    df = df[df['shape_tetra'] == 1]
            with c2:
                if os.path.exists("pildid/tetra.png"):
                    st.image("pildid/tetra.png", use_container_width=True)
                else: st.write("🔼")
        
        # Sfääriline
        if 'shape_spherical' in df.columns:
            c1, c2 = st.columns([2, 1], vertical_alignment="center")
            with c1:
                if st.checkbox("Sfääriline", key="chk_sphere"): 
                    df = df[df['shape_spherical'] == 1]
            with c2:
                if os.path.exists("pildid/spherical.png"):
                    st.image("pildid/spherical.png", use_container_width=True)
                else: st.write("⚪")

    # --- PERISPOOR ---
    with st.sidebar.expander("Perispoor", expanded=False):
        if 'perine_absent' in df.columns:
            if st.checkbox("Perispoor puudub", key='p_abs'): df = df[df['perine_absent'] == 1]
            if st.checkbox("Perispoor olemas", key='p_pres'): df = df[df['perine_absent'] == 0]

    # --- PINNASTRUKTUUR ---
    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        if 'surf_reticulate' in df.columns:
            c1, c2 = st.columns([2, 1], vertical_alignment="center")
            with c1:
                if st.checkbox("Retikulaarne (reticulate)", key="chk_retic"): 
                    df = df[df['surf_reticulate'] == 1]
            with c2:
                if os.path.exists("pildid/reticulate.png"):
                    st.image("pildid/reticulate.png", use_container_width=True)
                else: st.write("🕸️")
        
        st.divider()
        muud_pinnad = {
            "Ogaline (echinate)": "surf_echinate", 
            "Peeneogaline (microechinate)": "surf_microechinate",
            "Tüükaline (verrucate)": "surf_verrucate", 
            "Lohuline (lophate)": "surf_lophate",
            "Harjaline (cristate)": "surf_cristate",
            "Kurruline (rugulate)": "surf_rugulate",
            "Konksuline (hamulate)": "surf_hamulate",
            "Granulaarne (granulate)": "surf_granulate",
            "Peenkare (scabrate)": "surf_scabrate",
            "Sile (psilate)": "surf_psilate",
            "Auguline (foveolate)": "surf_foveolate",
            "Voldiline (folded)": "surf_folded"
        }
        for silt, veerg in muud_pinnad.items():
            if veerg in df.columns and st.checkbox(silt, key=f"chk_{veerg}"):
                df = df[df[veerg] == 1]

    # --- SUURUSED (P ja E) ---
    if 'P_mean' in df.columns:
        p_data = df_full['P_mean'].dropna()
        if not p_data.empty:
            with st.sidebar.expander("Polaartelg (µm)", expanded=False):
                p_min, p_max = float(p_data.min()), float(p_data.max())
                if p_min == p_max: p_min -= 1.0; p_max += 1.0
                v_p = st.slider("P", p_min, p_max, (p_min, p_max), key="s_p")
                df = df[(df['P_mean'].between(v_p[0], v_p[1])) | (df['P_mean'].isna())]

    if 'E_mean' in df.columns:
        e_data = df_full['E_mean'].dropna()
        if not e_data.empty:
            with st.sidebar.expander("Ekvatoriaaldiameeter (µm)", expanded=False):
                e_min, e_max = float(e_data.min()), float(e_data.max())
                if e_min == e_max: e_min -= 1.0; e_max += 1.0
                v_e = st.slider("E", e_min, e_max, (e_min, e_max), key="s_e")
                df = df[(df['E_mean'].between(v_e[0], v_e[1])) | (df['E_mean'].isna())]

    # === TULEMUSED ===
    vastete_arv = len(df)
    if vastete_arv == 0:
        st.warning("Valitud tunnustega vasteid ei leitud.")
    else:
        st.success(f"Leitud vasteid: {vastete_arv}")
        for _, row in df.iterrows():
            f_name = format_species_name(row['species'])
            with st.expander(f_name):
                st.markdown(f"### {f_name}")
                
                # Paigutus: tekst vasakul (2 osa), pilt paremal (1 osa)
                col_text, col_img = st.columns([2, 1], gap="large")
                
                with col_text:
                    st.write("**Eose kirjeldus:**")
                    st.write(row.get('description', 'Kirjeldus puudub.'))
                    st.divider()
                    # P ja E korrektselt üksteise all
                    st.write(f"📐 **Polaartelg:** {row.get('P_mean', '-')} µm")
                    st.write(f"📐 **Ekvatoriaaldiameeter:** {row.get('E_mean', '-')} µm")
                    
                with col_img:
                    if 'image_url' in row and pd.notna(row['image_url']) and str(row['image_url']).strip() != "":
                        try:
                            st.image(row['image_url'], use_container_width=True)
                        except:
                            st.caption("📸 Pilti ei leitud")

except Exception as e:
    st.error(f"Viga rakenduse töös: {e}")
