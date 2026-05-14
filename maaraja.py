import streamlit as st
import pandas as pd
import os

# --- 1. LEHE SEADISTUS ---
st.set_page_config(
    page_title="Eoste määraja / Spore Identifier", 
    page_icon="🌿", 
    layout="wide"
)

# --- 2. KEELE SEISUNDI HALDUS ---
if 'lang' not in st.session_state:
    st.session_state.lang = "Eesti"

# --- 3. TÕLKED ---
t = {
    "Eesti": {
        "title": "Eesti sooneostaimede eoste määraja",
        "sidebar_head": "Määramistunnused",
        "shape": "Kuju",
        "perine": "Perispoor",
        "p_absent": "Perispoor puudub",
        "p_present": "Perispoor olemas",
        "surface": "Pinnastruktuur",
        "p_axis": "Polaartelg (µm)",
        "e_diam": "Ekvatoriaaldiameeter (µm)",
        "results": "Leitud vasteid",
        "no_results": "Valitud tunnustega vasteid ei leitud.",
        "desc": "Eose kirjeldus",
        "none": "Puudub",
        "p_label": "Polaartelg",
        "e_label": "Ekvatoriaaldiameeter"
    },
    "English": {
        "title": "Estonian Spore Identifier",
        "sidebar_head": "Identification Keys",
        "shape": "Shape",
        "perine": "Perispore",
        "p_absent": "Perispore absent",
        "p_present": "Perispore present",
        "surface": "Surface Structure",
        "p_axis": "Polar axis (µm)",
        "e_diam": "Equatorial diameter (µm)",
        "results": "Matches found",
        "no_results": "No matches found with selected traits.",
        "desc": "Spore description",
        "none": "None",
        "p_label": "Polar axis",
        "e_label": "Equatorial diameter"
    }
}[st.session_state.lang]

# --- 4. CSS DISAIN ---
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] { gap: 1.5rem !important; align-items: center !important; }
    h1 { color: #2e7d32 !important; font-size: 2.5rem !important; }
    
    /* Peapildi suurus ja piirang */
    [data-testid="stImage"] img {
        max-width: 450px !important;
        border-radius: 8px;
    }
    
    /* Külgmenüü pildid */
    [data-testid="stSidebar"] [data-testid="stImage"] img {
        max-width: 100% !important;
    }

    /* Slaiderite puhastus */
    div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"],
    div[data-baseweb="typo-caption-12"], .st-emotion-cache-1ghh6m9 { display: none !important; }
    
    .stSuccess { background-color: #e8f5e9; border-color: #2e7d32; color: #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ANDMETE LAADIMINE ---
@st.cache_data
def load_data():
    file_path = 'Fixed_Spore_Data.csv'
    try:
        data = pd.read_csv(file_path, encoding='cp1252')
    except:
        data = pd.read_csv(file_path, encoding='latin-1')
    data.columns = data.columns.str.strip()
    return data

def format_species_name(raw_name):
    raw_str = str(raw_name)
    if "(" in raw_str and ")" in raw_str:
        parts = raw_str.split("(")
        return f"{parts[0].strip()} (*{parts[1].replace(')', '').strip()}*)"
    return raw_str

# --- 6. PÄIS JA KEELEVALIK ---
col_logo, col_title, col_lang = st.columns([1, 8, 2], vertical_alignment="center")

with col_logo:
    if os.path.exists("pildid/fern.png"):
        st.image("pildid/fern.png", width=80)
    else:
        st.write("🌿")

with col_title:
    st.title(t["title"])

with col_lang:
    # Lisame lipud valikusse
    options = {"Eesti": "🇪🇪 Eesti", "English": "🇬🇧 English"}
    
    chosen_label = st.selectbox(
        "Language", 
        options=list(options.values()), 
        index=0 if st.session_state.lang == "Eesti" else 1,
        label_visibility="collapsed"
    )
    
    # Leiame võtme (Eesti või English) vastavalt valitud sildile
    new_lang = "Eesti" if chosen_label == "🇪🇪 Eesti" else "English"
    
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()

st.divider()

# --- 7. PÕHIPROGRAMM ---
try:
    df_full = load_data()
    df = df_full.copy()

    # SIDEBAR: FILTRID
    st.sidebar.header(t["sidebar_head"])
    
    # KUJU
    with st.sidebar.expander(t["shape"], expanded=False):
        shapes = [("shape_bilateral", "Bilateraalne", "Bilateral", "bilateral.png"),
                  ("shape_tetra", "Tetraeedriline", "Tetrahedral", "tetra.png"),
                  ("shape_spherical", "Sfääriline", "Spherical", "spherical.png")]
        for col, et, en, img in shapes:
            if col in df.columns:
                c1, c2 = st.columns([2, 1], vertical_alignment="center")
                label = et if st.session_state.lang == "Eesti" else en
                if c1.checkbox(label, key=f"chk_{col}"): df = df[df[col] == 1]
                if os.path.exists(f"pildid/{img}"): c2.image(f"pildid/{img}", use_container_width=True)

    # PERISPOOR
    with st.sidebar.expander(t["perine"], expanded=False):
        if 'perine_absent' in df.columns:
            if st.checkbox(t["p_absent"], key='p_abs'): df = df[df['perine_absent'] == 1]
            if st.checkbox(t["p_present"], key='p_pres'): df = df[df['perine_absent'] == 0]

    # PINNASTRUKTUUR
    with st.sidebar.expander(t["surface"], expanded=False):
        if 'surf_reticulate' in df.columns:
            c1, c2 = st.columns([2, 1], vertical_alignment="center")
            label = "Retikulaarne" if st.session_state.lang == "Eesti" else "Reticulate"
            if c1.checkbox(label, key="chk_retic"): df = df[df['surf_reticulate'] == 1]
            if os.path.exists("pildid/reticulate.png"): c2.image("pildid/reticulate.png", use_container_width=True)
        
        st.divider()
        muud_pinnad = {
            "Ogaline (echinate)": "surf_echinate", "Peeneogaline (microechinate)": "surf_microechinate",
            "Tüükaline (verrucate)": "surf_verrucate", "Lohuline (lophate)": "surf_lophate",
            "Harjaline (cristate)": "surf_cristate", "Kurruline (rugulate)": "surf_rugulate",
            "Konksuline (hamulate)": "surf_hamulate", "Sile (psilate)": "surf_psilate"
        }
        for silt, veerg in muud_pinnad.items():
            if veerg in df.columns and st.checkbox(silt, key=f"chk_{veerg}"): df = df[df[veerg] == 1]

    # SUURUSED (P ja E)
    if 'P_mean' in df.columns:
        p_data = df_full['P_mean'].dropna()
        if not p_data.empty:
            with st.sidebar.expander(t["p_axis"], expanded=False):
                v_p = st.slider("P", float(p_data.min()), float(p_data.max()), (float(p_data.min()), float(p_data.max())), key="s_p")
                df = df[(df['P_mean'].between(v_p[0], v_p[1])) | (df['P_mean'].isna())]

    if 'E_mean' in df.columns:
        e_data = df_full['E_mean'].dropna()
        if not e_data.empty:
            with st.sidebar.expander(t["e_diam"], expanded=False):
                v_e = st.slider("E", float(e_data.min()), float(e_data.max()), (float(e_data.min()), float(e_data.max())), key="s_e")
                df = df[(df['E_mean'].between(v_e[0], v_e[1])) | (df['E_mean'].isna())]

    # === TULEMUSED ===
    if len(df) == 0:
        st.warning(t["no_results"])
    else:
        st.success(f"{t['results']}: {len(df)}")
        for _, row in df.iterrows():
            f_name = format_species_name(row['species'])
            with st.expander(f_name):
                st.markdown(f"### {f_name}")
                col_text, col_img = st.columns([2, 1], gap="large")
                with col_text:
                    st.write(f"**{t['desc']}:**")
                    st.write(row.get('description', t['none']))
                    st.divider()
                    st.write(f"📐 **{t['p_label']}:** {row.get('P_mean', '-')} µm")
                    st.write(f"📐 **{t['e_label']}:** {row.get('E_mean', '-')} µm")
                with col_img:
                    if pd.notna(row.get('image_url')) and str(row['image_url']).strip() != "":
                        try: st.image(row['image_url'], use_container_width=True)
                        except: st.caption("📸 N/A")

except Exception as e:
    st.error(f"Viga / Error: {e}")
