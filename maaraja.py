import streamlit as st
import pandas as pd

# 1. Lehe seadistus
st.set_page_config(page_title="Eesti sooneostaimede eoste määraja", page_icon="🌿", layout="wide")

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
    # Parandus: hoiame alles liigid, kellel andmed puuduvad (nt võtmeheinad)
    if 'P_mean' in df.columns:
        with st.sidebar.expander("Polaartelg (P_mean µm)", expanded=False):
            p_data = df['P_mean'].dropna()
            if not p_data.empty:
                p_min, p_max = float(p_data.min()), float(p_data.max())
                v_p = st.slider("P-vahemik", p_min, p_max, (p_min, p_max), key="s_p")
                df = df[(df['P_mean'].between(v_p[0], v_p[1])) | (df['P_mean'].isna())]

    if 'E_mean' in df.columns:
        with st.sidebar.expander("Ekvatoriaaldiameeter (E_mean µm)", expanded=False):
            e_data = df['E_mean'].dropna()
            if not e_data.empty:
                e_min, e_max = float(e_data.min()), float(e_data.max())
                v_e = st.slider("E-vahemik", e_min, e_max, (e_min, e_max), key="s_e")
                df = df[(df['E_mean'].between(v_e[0], v_e[1])) | (df['E_mean'].isna())]

    # 3. TULEMUSTE KUVAMINE
    st.divider()
    vastete_arv = len(df)
    if vastete_arv == 0:
        st.warning("Vasteid ei leitud.")
    else:
        st.success(f"Leitud vasteid: {vastete_arv}")

        # DETAILNE VAADE
        for _, row in df.iterrows():
            # NIMEVORMISTUS
            species_raw = row['species']
            if "(" in species_raw:
                eesti, ladina = species_raw.split("(", 1)
                ladina = ladina.replace(")", "").strip()
                pealkiri_valjas = eesti.strip() # Ainult eestikeelne nimi paneeli peal
            else:
                pealkiri_valjas = species_raw
                ladina = None

            with st.expander(pealkiri_valjas):
                # Paneeli SEES kuvame täisnime koos kaldkirjas ladinakeelse nimega
                if ladina:
                    st.markdown(f"### {pealkiri_valjas} *({ladina})*")
                else:
                    st.markdown(f"### {pealkiri_valjas}")
                
                col_text, col_img = st.columns([3, 2])
                with col_text:
                    st.write("**Eose kirjeldus:**")
                    st.write(row.get('description', 'Kirjeldus puudub.'))
                    st.divider()
                    st.write(f"📐 **P_mean:** {row.get('P_mean', '-')} µm")
                    st.write(f"📐 **E_mean:** {row.get('E_mean', '-')} µm")

                with col_img:
                    if 'image_url' in row and pd.notna(row['image_url']) and row['image_url'] != "":
                        try: st.image(row['image_url'], use_container_width=True)
                        except: st.caption("🖼️ Foto puudub")
                    else:
                        st.caption("📸 Foto puudub")

except Exception as e:
    st.error(f"Viga: {e}")
