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

    # --- KATEGOORIA: KUJU (expanded=False, et oleks alguses kinni) ---
    with st.sidebar.expander("Kuju", expanded=False):
        st.write("Vali eose kuju:")
        
        # Bilateraalne
        if 'shape_bilateral' in df.columns:
            st.image("pildid/bilateral.png", width=150)
            if st.checkbox("Bilateraalne", key="chk_bilateral"):
                df = df[df['shape_bilateral'] == 1]
                aktiivsed_filtrid.append("Kuju: Bilateraalne")
        
        st.divider()

        # Tetraeedriline
        if 'shape_tetra' in df.columns:
            st.image("pildid/tetra.png", width=150)
            if st.checkbox("Tetraeedriline", key="chk_tetra"):
                df = df[df['shape_tetra'] == 1]
                aktiivsed_filtrid.append("Kuju: Tetraeedriline")

        st.divider()

        # Sfääriline
        if 'shape_spherical' in df.columns:
            if st.checkbox("Sfääriline", key="chk_spherical"):
                df = df[df['shape_spherical'] == 1]
                aktiivsed_filtrid.append("Kuju: Sfääriline")

    # --- KATEGOORIA: PINNASTRUKTUUR (Kõik valikud taastatud) ---
    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        pind_valikud = {
            "Ogaline (echinate)": "surf_echinate",
            "Peeneogaline (microechinate)": "surf_microechinate",
            "Tüükaline (verrucate)": "surf_verrucate",
            "Lohuline (lophate)": "surf_lophate",
            "Harjaline (cristate)": "surf_cristate",
            "Retikulaarne (reticulate)": "surf_reticulate",
            "Kurruline (rugulate)": "surf_rugulate",
            "Konksuline (hamulate)": "surf_hamulate",
            "Granulaarne (granulate)": "surf_granulate",
            "Peenkare (scabrate)": "surf_scabrate",
            "Sile (psilate)": "surf_psilate",
            "Auguline (foveolate)": "surf_foveolate",
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

        # Vormistame nime kaldkirja
        def vormista_kaldkiri(nimi):
            if isinstance(nimi, str) and "(" in nimi and ")" in nimi:
                parts = nimi.split("(", 1)
                return f"{parts[0]} (*{parts[1].replace(')', '').strip()}*)"
            return nimi

        df_display = df.copy()
        if 'species' in df_display.columns:
            df_display['Liiginimi (ladina k)'] = df_display['species'].apply(vormista_kaldkiri)
        
        # Valime veerud kuvamiseks
        soovitud = ['Liiginimi (ladina k)', 'genus', 'family']
        olemasolevad = [v for v in soovitud if v in df_display.columns]
        
        st.table(df_display[olemasolevad])

except Exception as e:
    st.error(f"Viga: {e}")