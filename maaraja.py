import streamlit as st
import pandas as pd
import os

# 1. LEHE SEADISTUS
st.set_page_config(
    page_title="Eesti sooneostaimede eoste määraja", 
    page_icon="🌿", 
    layout="wide"
)

# --- JÕULINE CSS: SLAIDERID, LOGO JA VÄRVID ---
st.markdown("""
    <style>
    /* Üldine pealkiri */
    h1 { color: #2e7d32 !important; padding-top: 10px !important; }
    
    /* 1. PEIDAME KÕIK ALUMISED NUMBRID, KASTID JA VAHEMIKUD */
    div[data-testid="stTickBarMin"], 
    div[data-testid="stTickBarMax"],
    div[data-baseweb="typo-caption-12"],
    [data-testid="stMetricValue"],
    .st-emotion-cache-1ghh6m9, 
    .st-emotion-cache-16idsys,
    .st-emotion-cache-p5mre8 { 
        display: none !important; 
    }
    
    /* 2. ÜLEMISED NUMBRID: Muudame punase roheliseks */
    div[data-testid="stThumbValue"] { 
        color: #2e7d32 !important; 
        font-weight: bold !important;
        font-size: 14px !important;
    }

    /* 3. SLAIDERI JOON: Eemaldame punase ja asendame rohelisega */
    /* See sihib joont mummude vahel */
    div[data-baseweb="slider"] > div > div { 
        background-color: #2e7d32 !important; 
    }
    /* See sihib mummusid ehk nuppe */
    div[role="slider"] { 
        background-color: #2e7d32 !important; 
        border: 2px solid #1b5e20 !important; 
    }

    /* 4. LOGO JA PEALKIRJA JOONDUS */
    [data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }

    /* Expanderite päised küljel */
    .st-emotion-cache-p4m61c p { color: #1b5e20 !important; font-weight: bold !important; }
    
    /* Success box */
    .stSuccess { background-color: #e8f5e9; border-color: #2e7d32; color: #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# --- PEALKIRI KOOS LOGOGA ---
# Kui pilt on GitHubis nimega fern.png, siis kontrollime seda
logo_path = "fern.png"
col_logo, col_title = st.columns([1, 6]) 

with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)
    else:
        # Kui pilti pole, siis kuvame suurema sümboli, et koht poleks tühi
        st.markdown("<h1 style='text-align: center;'>🌿</h1>", unsafe_allow_html=True)

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
    
    if 'description' in df.columns:
        df['description'] = df['description'].str.replace('\x96', '–', regex=True)
        df['description'] = df['description'].str.replace('\xad', '-', regex=True)

    # --- 2. FILTRID KÜLJEPEAL ---
    st.sidebar.header("Määramistunnused")
    
    # KUJU
    with st.sidebar.expander("Kuju", expanded=False):
        if 'shape_bilateral' in df.columns:
            c1, c2 = st.columns([1, 3])
            with c1: st.image("pildid/bilateral.png")
            with c2: 
                if st.checkbox("Bilateraalne", key="chk_bilateral"):
                    df = df[df['shape_bilateral'] == 1]
        
        if 'shape_tetra' in df.columns:
            c1, c2 = st.columns([1, 3])
            with c1: st.image("pildid/tetra.png")
            with c2:
                if st.checkbox("Tetraeedriline", key="chk_tetra"):
                    df = df[df['shape_tetra'] == 1]

        if 'shape_spherical' in df.columns:
            c1, c2 = st.columns([1, 3])
            with c1: 
                try: st.image("pildid/spherical.png")
                except: st.write("⚪")
            with c2:
                if st.checkbox("Sfääriline", key="chk_spherical"):
                    df = df[df['shape_spherical'] == 1]

    # PERISPOOR
    with st.sidebar.expander("Perispoor", expanded=False):
        if 'perine_absent' in df.columns:
            if st.checkbox("Perispoor puudub", key='chk_p_absent'):
                df = df[df['perine_absent'] == 1]
            if st.checkbox("Perispoor olemas", key='chk_p_present'):
                df = df[df['perine_absent'] == 0]

    # PINNASTRUKTUUR
    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        if 'surf_reticulate' in df.columns:
            c1, c2 = st.columns([1, 3])
            with c1:
                try: st.image("pildid/reticulate.png")
                except: st.write("🕸️")
            with c2:
                if st.checkbox("Retikulaarne", key="chk_surf_reticulate"):
                    df = df[df['surf_reticulate'] == 1]
        
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

    # SUURUS (Slaiderid, kus peitsime sildid)
    if 'P_mean' in df.columns:
        with st.sidebar.expander("Polaartelg (µm)", expanded=False):
            p_data = df['P_mean'].dropna()
            if not p_data.empty:
                p_min, p_max = float(p_data.min()), float(p_data.max())
                # label_visibility="collapsed" aitab topelttekste vältida
                v_p = st.slider("Polaartelg", p_min, p_max, (p_min, p_max), key="s_p", label_visibility="collapsed")
                df = df[(df['P_mean'].between(v_p[0], v_p[1])) | (df['P_mean'].isna())]

    if 'E_mean' in df.columns:
        with st.sidebar.expander("Ekvatoriaaldiameeter (µm)", expanded=False):
            e_data = df['E_mean'].dropna()
            if not e_data.empty:
                e_min, e_max = float(e_data.min()), float(e_data.max())
                v_e = st.slider("Ekvatoriaaldiameeter", e_min, e_max, (e_min, e_max), key="s_e", label_visibility="collapsed")
                df = df[(df['E_mean'].between(v_e[0], v_e[1])) | (df['E_mean'].isna())]

    # --- 3. TULEMUSTE KUVAMINE ---
    vastete_arv = len(df)
    if vastete_arv == 0:
        st.warning("Vasteid ei leitud.")
    else:
        st.success(f"Leitud vasteid: {vastete_arv}")

        for _, row in df.iterrows():
            species_raw = str(row['species'])
            if "(" in species_raw:
                eesti, ladina = species_raw.split("(", 1)
                ladina = ladina.replace(")", "").strip()
                pealkiri_valjas = eesti.strip()
            else:
                pealkiri_valjas = species_raw
                ladina = None

            with st.expander(pealkiri_valjas):
                if ladina:
                    st.markdown(f"### {pealkiri_valjas} *({ladina})*")
                else:
                    st.markdown(f"### {pealkiri_valjas}")
                
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
                        except: st.caption("📸 Pilti ei saa kuvada")
                    else:
                        st.caption("📸 Foto puudub")

except Exception as e:
    st.error(f"Viga: {e}")
