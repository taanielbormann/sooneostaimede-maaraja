import streamlit as st
import pandas as pd

# 1. Lehe seadistus
st.set_page_config(page_title="Eesti sooneostaimede eoste määraja", page_icon="🌿", layout="wide")

st.title("🌿 Eesti sooneostaimede eoste määraja")

try:
    # Andmete laadimine
    df = pd.read_csv('Fixed_Spore_Data.csv', encoding='latin-1')
    df.columns = df.columns.str.strip()
    
    # 2. FILTRITE LOOMINE KÜLJEPEAL
    st.sidebar.header("Määramistunnused")
    aktiivsed_filtrid = []

    # --- KATEGOORIA: KUJU ---
    with st.sidebar.expander("Kuju", expanded=False):
        if 'shape_bilateral' in df.columns:
            st.image("pildid/bilateral.png", width=150)
            if st.checkbox("Bilateraalne", key="chk_bilateral"):
                df = df[df['shape_bilateral'] == 1]
                aktiivsed_filtrid.append("Kuju: Bilateraalne")
        st.divider()
        if 'shape_tetra' in df.columns:
            st.image("pildid/tetra.png", width=150)
            if st.checkbox("Tetraeedriline", key="chk_tetra"):
                df = df[df['shape_tetra'] == 1]
                aktiivsed_filtrid.append("Kuju: Tetraeedriline")
        st.divider()
        if 'shape_spherical' in df.columns:
            if st.checkbox("Sfääriline", key="chk_spherical"):
                df = df[df['shape_spherical'] == 1]
                aktiivsed_filtrid.append("Kuju: Sfääriline")

    # --- KATEGOORIA: PINNASTRUKTUUR ---
    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        pind_valikud = {
            "Ogaline (echinate)": "surf_echinate", "Peeneogaline (microechinate)": "surf_microechinate",
            "Tüükaline (verrucate)": "surf_verrucate", "Lohuline (lophate)": "surf_lophate",
            "Harjaline (cristate)": "surf_cristate", "Retikulaarne (reticulate)": "surf_reticulate",
            "Kurruline (rugulate)": "surf_rugulate", "Konksuline (hamulate)": "surf_hamulate",
            "Granulaarne (granulate)": "surf_granulate", "Peenkare (scabrate)": "surf_scabrate",
            "Sile (psilate)": "surf_psilate", "Auguline (foveolate)": "surf_foveolate",
            "Voldiline (folded)": "surf_folded"
        }
        for silt, veerg in pind_valikud.items():
            if veerg in df.columns:
                if st.checkbox(silt, key=f"chk_{veerg}"):
                    df = df[df[veerg] == 1]
                    aktiivsed_filtrid.append(f"Pind: {silt}")

    # --- KATEGOORIA: PERISPOOR ---
    with st.sidebar.expander("Perispoor", expanded=False):
        if 'perine_absent' in df.columns:
            if st.checkbox("Perispoor puudub", key='chk_p_absent'):
                df = df[df['perine_absent'] == 1]
                aktiivsed_filtrid.append("Perispoor: Puudub")
            if st.checkbox("Perispoor olemas", key='chk_p_present'):
                df = df[df['perine_absent'] == 0]
                aktiivsed_filtrid.append("Perispoor: Olemas")

    # 3. TULEMUSTE KUVAMINE
    st.divider()
    if aktiivsed_filtrid:
        st.write(f"**Valitud filtrid:** {', '.join(aktiivsed_filtrid)}")

    vastete_arv = len(df)
    if vastete_arv == 0:
        st.warning("Selliste tunnustega liike ei leitud. Muuda valikuid.")
    else:
        st.success(f"Leitud vasteid: {vastete_arv}")

        def vormista_ladina(nimi):
            if isinstance(nimi, str) and "(" in nimi and ")" in nimi:
                eesti, ladina = nimi.split("(", 1)
                return eesti.strip(), ladina.replace(")", "").strip()
            return nimi, ""

        # Kuvame iga liigi detailse vaate
        for _, row in df.iterrows():
            eesti_nimi, ladina_nimi = vormista_ladina(row['species'])
            pealkiri = f"{eesti_nimi} ({ladina_nimi})" if ladina_nimi else eesti_nimi
            
            with st.expander(pealkiri):
                # Tekst ja pilt kõrvuti
                col_text, col_img = st.columns([3, 2])
                
                with col_text:
                    st.write("**Eose kirjeldus:**")
                    # Otsime kirjeldust veerust 'description'. Kui seda pole, näitame teadet.
                    kirjeldus = row.get('description', 'Kirjeldus puudub.')
                    if pd.isna(kirjeldus) or kirjeldus == "":
                        kirjeldus = "Selle liigi kohta pole veel põhjalikku kirjeldust lisatud."
                    
                    st.write(kirjeldus)
                    
                    # Kui on olemas mõõtmed, lisame need kirjelduse alla
                    if 'size_min' in row and pd.notna(row['size_min']):
                        st.write(f"📏 **Suurus:** {row['size_min']}–{row['size_max']} µm")

                with col_img:
                    if 'image_url' in row and pd.notna(row['image_url']) and row['image_url'] != "":
                        try:
                            st.image(row['image_url'], use_container_width=True)
                        except:
                            st.caption("🖼️ Fotofaili ei leitud")
                    else:
                        st.caption("📸 Foto puudub")

except Exception as e:
    st.error(f"Viga: {e}")
