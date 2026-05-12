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
    with st.sidebar.expander("Kuju", expanded=True):
        st.write("Vali eose kuju:")
        
        # 1. BILATERAALNE
        if 'shape_bilateral' in df.columns:
            st.image("pildid/bilateral.png", width=150)
            if st.checkbox("Bilateraalne", key="chk_bilateral"):
                df = df[df['shape_bilateral'] == 1]
                aktiivsed_filtrid.append("Kuju: Bilateraalne")
        
        st.divider() # Teeb väikse vahejoone valikute vahele

        # 2. TETRAEEDRILINE
        if 'shape_tetra' in df.columns:
            st.image("pildid/tetra.png", width=150)
            if st.checkbox("Tetraeedriline", key="chk_tetra"):
                df = df[df['shape_tetra'] == 1]
                aktiivsed_filtrid.append("Kuju: Tetraeedriline")

        st.divider()

        # 3. SFÄÄRILINE (kui sul selle jaoks pilti pole, jääb ainult tekst)
        if 'shape_spherical' in df.columns:
            # Kui sul tekib sfäärilise pilt, lisa siia: st.image("pildid/spherical.png", width=150)
            if st.checkbox("Sfääriline", key="chk_spherical"):
                df = df[df['shape_spherical'] == 1]
                aktiivsed_filtrid.append("Kuju: Sfääriline")

    # --- KATEGOORIA: PINNASTRUKTUUR ---
    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        pind_valikud = {
            "Ogaline": "surf_echinate", "Tüükaline": "surf_verrucate", 
            "Retikulaarne": "surf_reticulate", "Sile": "surf_psilate"
        }
        for silt, veerg in pind_valikud.items():
            if veerg in df.columns:
                if st.checkbox(silt, key=f"surf_{veerg}"):
                    df = df[df[veerg] == 1]
                    aktiivsed_filtrid.append(f"Pind: {silt}")

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
        
        soovitud = ['Liiginimi (ladina k)', 'genus', 'family']
        olemasolevad = [v for v in soovitud if v in df_display.columns]
        
        st.table(df_display[olemasolevad])

except Exception as e:
    st.error(f"Viga: {e}")