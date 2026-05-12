import streamlit as st
import pandas as pd

# 1. Lehe seadistus
st.set_page_config(page_title="Eesti sooneostaimede eoste määraja", page_icon="🌿", layout="wide")

st.title("🌿 Eesti sooneostaimede eoste määraja")

# Algatame session_state, kui seda veel pole
if 'filter_kuju' not in st.session_state:
    st.session_state.filter_kuju = None

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
        col1, col2 = st.columns(2)
        
        with col1:
            st.image("pildid/bilateral.png", caption="Bilateraalne", use_container_width=True)
            if st.button("Vali see", key="btn_bilateral"):
                st.session_state.filter_kuju = "bilateral"
        
        with col2:
            st.image("pildid/tetra.png", caption="Tetraeedriline", use_container_width=True)
            if st.button("Vali see", key="btn_tetra"):
                st.session_state.filter_kuju = "tetra"
        
        # Nupp valiku tühistamiseks
        if st.session_state.filter_kuju:
            if st.button("Tühista kuju valik"):
                st.session_state.filter_kuju = None
                st.rerun()

        # Rakendame filtrid vastavalt "mälule"
        if st.session_state.filter_kuju == "bilateral":
            df = df[df['shape_bilateral'] == 1]
            aktiivsed_filtrid.append("Kuju: Bilateraalne")
        elif st.session_state.filter_kuju == "tetra":
            df = df[df['shape_tetra'] == 1]
            aktiivsed_filtrid.append("Kuju: Tetraeedriline")

    # --- KATEGOORIA: PINNASTRUKTUUR ---
    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        pind_valikud = {
            "Ogaline": "surf_echinate", "Tüükaline": "surf_verrucate", 
            "Retikulaarne": "surf_reticulate", "Sile": "surf_psilate"
        }
        for silt, veerg in pind_valikud.items():
            if veerg in df.columns:
                if st.checkbox(silt, key=veerg):
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