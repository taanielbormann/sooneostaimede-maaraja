import streamlit as st
import pandas as pd
import os

# 1. LEHE SEADISTUS
st.set_page_config(
    page_title="Eesti sooneostaimede eoste määraja", 
    page_icon="🌿", 
    layout="wide"
)

# --- CSS: SLAIDERID, LOGO JA DISAIN ---
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] {
        gap: 0rem !important;
        align-items: center !important;
    }
    
    h1 { 
        color: #2e7d32 !important; 
        margin-left: -30px !important; 
        padding-top: 10px !important;
    }

    /* SLAIDERI PUHASTUS: Alumiste numbrite peitmine */
    div[data-testid="stTickBarMin"], 
    div[data-testid="stTickBarMax"],
    div[data-baseweb="typo-caption-12"],
    .st-emotion-cache-1ghh6m9, 
    .st-emotion-cache-16idsys,
    .st-emotion-cache-p5mre8,
    .st-emotion-cache-1kyf5f6 { 
        display: none !important; 
    }
    
    div[data-testid="stThumbValue"] { 
        font-weight: bold !important;
    }

    .st-emotion-cache-p4m61c p { color: #1b5e20 !important; font-weight: bold !important; }
    .stSuccess { background-color: #e8f5e9; border-color: #2e7d32; color: #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# --- PEALKIRI ---
logo_path = "pildid/fern.png"
col_logo, col_title = st.columns([1, 10]) 

with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=110)
    else:
        st.write("🌿")

with col_title:
    st.title("Eesti sooneostaimede eoste määraja")

st.divider()

try:
    # 1. ANDMETE LAADIMINE
    try:
        df = pd.read_csv('Fixed_Spore_Data.csv', encoding='cp1252')
    except:
        df = pd.read_csv('Fixed_Spore_Data.csv', encoding='latin-1')
    
    df.columns = df.columns.str.strip()
    
    if 'description' in df.columns:
        df['description'] = df['description'].str.replace('\x96', '–', regex=True)
        df['description'] = df['description'].str.replace('\xad', '-', regex=True)

    # 2. FILTRID KÜLJEPEAL
    st.sidebar.header("Määramistunnused")
    
    # --- KUJU ---
    with st.sidebar.expander("Kuju", expanded=False):
        if 'shape_bilateral' in df.columns:
            c1, c2 = st.columns([3, 1])
            with c1: 
                if st.checkbox("Bilateraalne", key="chk_bilateral"):
                    df = df[df['shape_bilateral'] == 1]
            with c2: st.image("pildid/bilateral.png")
        
        if 'shape_tetra' in df.columns:
            c1, c2 = st.columns([3, 1])
            with c1:
                if st.checkbox("Tetraeedriline", key="chk_tetra"):
                    df = df[df['shape_tetra'] == 1]
            with c2: st.image("pildid/tetra.png")

        if 'shape_spherical' in df.columns:
            c1, c2 = st.columns([3, 1])
            with c1:
                if st.checkbox("Sfääriline", key="chk_spherical"):
                    df = df[df['shape_spherical'] == 1]
            with c2:
                try: st.image("pildid/spherical.png")
                except: st.write("⚪")

    # --- PERISPOOR ---
    with st.sidebar.expander("Perispoor", expanded=False):
        if 'perine_absent' in df.columns:
            if st.checkbox("Perispoor puudub", key='chk_p_absent'):
                df = df[df['perine_absent'] == 1]
            if st.checkbox("Perispoor olemas", key='chk_p_present'):
                df = df[df['perine_absent'] == 0]

    # --- PINNASTRUKTUUR ---
    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        if 'surf_reticulate' in df.columns:
            c1, c2 = st.columns([3, 1])
            with c1:
                if st.checkbox("Retikulaarne (reticulate)", key="chk_surf_reticulate"):
                    df = df[df['surf_reticulate'] == 1]
            with c2:
                try: st.image("pildid/reticulate.png")
                except: st.write("🕸️")
        
        st.divider()
        muud_pinnad = {
            "Ogaline (echinate)": "surf_echinate", "Peeneogaline (microechinate)": "surf_microechinate",
            "Tüükaline (verrucate)": "surf_verrucate", "Lohuline (lophate)": "surf_lophate",
            "Harjaline (cristate)": "surf_cristate", "Kurruline (rugulate)": "surf_rugulate",
            "Konksuline (hamulate)": "surf_hamulate", "Granulaarne (granulate)": "surf_granulate",
            "Peenkare (scabrate)": "surf_scabrate", "Sile (psilate)": "surf_psilate",
            "Auguline (foveolate)": "surf_foveolate", "Voldiline (folded)": "surf_folded"
        }
        for silt, veerg in muud_pinnad.items():
            if veerg in df.columns:
                if st.checkbox(silt, key=f"chk_{veerg}"):
                    df = df[df[veerg] == 1]

    # --- SUURUS ---
    if 'P_mean' in df.columns:
        with st.sidebar.expander("Polaartelg (µm)", expanded=False):
            p_data = df['P_mean'].dropna()
            if not p_data.empty:
                p_min, p_max = float(p_data.min()), float(p_data.max())
                if p_min == p_max: p_min -= 1.0; p_max += 1.0
                v_p = st.slider("P", p_min, p_max, (p_min, p_max), key="s_p", label_visibility="collapsed")
                df = df[(df['P_mean'].between(v_p[0], v_p[1])) | (df['P_mean'].isna())]

    if 'E_mean' in df.columns:
        with st.sidebar.expander("Ekvatoriaaldiameeter (µm)", expanded=False):
            e_data = df['E_mean'].dropna()
            if not e_data.empty:
                e_min, e_max = float(e_data.min()), float(e_data.max())
                if e_min == e_max: e_min -= 1.0; e_max += 1.0
                v_e = st.slider("E", e_min, e_max, (e_min, e_max), key="s_e", label_visibility="collapsed")
                df = df[(df['E_mean'].between(v_e[0], v_e[1])) | (df['E_mean'].isna())]

    # --- TULEMUSED ---
    vastete_arv = len(df)
    if vastete_arv == 0:
        st.warning("Valitud tunnustega vasteid ei leitud.")
    else:
        st.success(f"Leitud vasteid: {vastete_arv}")

        for _, row in df.iterrows():
            # Parandatud liiginime kuvamine
            full_name = str(row['species'])
            eesti_nimi = full_name.split("(")[0].strip()
            
            with st.expander(full_name): # Kuvab päises kogu nime
                col_text, col_img = st.columns([3, 2])
                with col_text:
                    st.write("**Eose kirjeldus:**")
                    st.write(row.get('description', 'Kirjeldus puudub.'))
                    st.divider()
                    st.write(f"📐 **Polaartelg:** {row.get('P_mean', '-')} µm")
                    st.write(f"📐 **Ekvatoriaaldiameeter:** {row.get('E_mean', '-')} µm")

                with col_img:
                    if 'image_url' in row and pd.notna(row['image_url']) and row['image_url'] != "":
                        try: st.image(row['image_url'], use_container_width=True)
                        except: st.caption("📸 Pilti ei leitud")

except Exception as e:
    st.error(f"Viga rakenduse töös: {e}")
