import streamlit as st
import pandas as pd

# 1. Lehe seadistus
st.set_page_config(page_title="Eesti sooneostaimede eoste määraja", page_icon="🌿", layout="wide")

# --- LÕPLIK SLAIDERI VÄLIMUS (CSS) ---
st.markdown("""
    <style>
    /* Üldine pealkiri */
    h1 { color: #2e7d32 !important; }
    
    /* 1. ÜLEMISED NUMBRID: Teeme need roheliseks ja loetavaks */
    div[data-testid="stThumbValue"] { 
        color: #2e7d32 !important; 
        font-weight: bold !important;
        font-size: 14px !important;
    }
    
    /* 2. ALUMISED NUMBRID JA KASTID: Peidame täielikult */
    div[data-testid="stTickBarMin"], 
    div[data-testid="stTickBarMax"],
    .st-emotion-cache-1ghh6m9,
    div[data-baseweb="typo-caption-12"] { 
        display: none !important; 
    }
    
    /* 3. SLAIDERI JOON JA MUMMUD */
    /* Valitud vahemik kahe mummu vahel roheliseks */
    .stSlider [data-baseweb="slider"] > div > div { 
        background-color: #2e7d32 !important; 
    }
    /* Slaideri mummud (nupud) */
    div[role="slider"] { 
        background-color: #2e7d32 !important; 
        border: 2px solid #1b5e20 !important; 
    }
    
    /* Expanderite päised */
    .st-emotion-cache-p4m61c p { color: #1b5e20 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# Pealkiri
st.title("🌿 Eesti sooneostaimede eoste määraja")


# Pealkiri
st.title("🌿 Eesti sooneostaimede eoste määraja")

try:
    # ANDMETE LAADIMINE
    try:
        df = pd.read_csv('Fixed_Spore_Data.csv', encoding='cp1252')
    except:
        df = pd.read_csv('Fixed_Spore_Data.csv', encoding='latin-1')
    
    df.columns = df.columns.str.strip()
    
    # PUHASTAME KIRJELDUSED
    if 'description' in df.columns:
        df['description'] = df['description'].str.replace('\x96', '–', regex=True)
        df['description'] = df['description'].str.replace('\xad', '-', regex=True)

    # 2. FILTRITE LOOMINE KÜLJEPEAL
    st.sidebar.header("Määramistunnused")
    aktiivsed_filtrid = []

    # --- 1. KUJU ---
    with st.sidebar.expander("Kuju", expanded=False):
        if 'shape_bilateral' in df.columns:
            c1, c2 = st.columns([1, 3])
            with c1: st.image("pildid/bilateral.png")
            with c2: 
                if st.checkbox("Bilateraalne", key="chk_bilateral"):
                    df = df[df['shape_bilateral'] == 1]
                    aktiivsed_filtrid.append("Kuju: Bilateraalne")
        
        if 'shape_tetra' in df.columns:
            c1, c2 = st.columns([1, 3])
            with c1: st.image("pildid/tetra.png")
            with c2:
                if st.checkbox("Tetraeedriline", key="chk_tetra"):
                    df = df[df['shape_tetra'] == 1]
                    aktiivsed_filtrid.append("Kuju: Tetraeedriline")

        if 'shape_spherical' in df.columns:
            c1, c2 = st.columns([1, 3])
            with c1: 
                try: st.image("pildid/spherical.png")
                except: st.write("⚪")
            with c2:
                if st.checkbox("Sfääriline", key="chk_spherical"):
                    df = df[df['shape_spherical'] == 1]
                    aktiivsed_filtrid.append("Kuju: Sfääriline")

    # --- 2. PERISPOOR ---
    with st.sidebar.expander("Perispoor", expanded=False):
        if 'perine_absent' in df.columns:
            if st.checkbox("Perispoor puudub", key='chk_p_absent'):
                df = df[df['perine_absent'] == 1]
                aktiivsed_filtrid.append("Perispoor: Puudub")
            if st.checkbox("Perispoor olemas", key='chk_p_present'):
                df = df[df['perine_absent'] == 0]
                aktiivsed_filtrid.append("Perispoor: Olemas")

    # --- 3. PINNASTRUKTUUR ---
    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        if 'surf_reticulate' in df.columns:
            c1, c2 = st.columns([1, 3])
            with c1:
                try: st.image("pildid/reticulate.png")
                except: st.write("🕸️")
            with c2:
                if st.checkbox("Retikulaarne (reticulate)", key="chk_surf_reticulate"):
                    df = df[df['surf_reticulate'] == 1]
                    aktiivsed_filtrid.append("Pind: Retikulaarne")
        
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
                    aktiivsed_filtrid.append(f"Pind: {silt}")

    # --- 4. SUURUS (P ja E) ---
    if 'P_mean' in df.columns:
        with st.sidebar.expander("Polaartelg (µm)", expanded=False):
            p_data = df['P_mean'].dropna()
            if not p_data.empty:
                p_min, p_max = float(p_data.min()), float(p_data.max())
                v_p = st.slider("P-vahemik", p_min, p_max, (p_min, p_max), key="s_p", help=f"Vahemik: {p_min} - {p_max}")
                df = df[(df['P_mean'].between(v_p[0], v_p[1])) | (df['P_mean'].isna())]

    if 'E_mean' in df.columns:
        with st.sidebar.expander("Ekvatoriaaldiameeter (µm)", expanded=False):
            e_data = df['E_mean'].dropna()
            if not e_data.empty:
                e_min, e_max = float(e_data.min()), float(e_data.max())
                v_e = st.slider("E-vahemik", e_min, e_max, (e_min, e_max), key="s_e", help=f"Vahemik: {e_min} - {e_max}")
                df = df[(df['E_mean'].between(v_e[0], v_e[1])) | (df['E_mean'].isna())]

    # 3. TULEMUSTE KUVAMINE
    st.divider()
    vastete_arv = len(df)
    if vastete_arv == 0:
        st.warning("Vasteid ei leitud.")
    else:
        st.success(f"Leitud vasteid: {vastete_arv}")

        for _, row in df.iterrows():
            species_raw = row['species']
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
                    # Siin on muudatus: (P_mean) ja (E_mean) on eemaldatud
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
