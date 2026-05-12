import streamlit as st
import pandas as pd

# 1. Lehe seadistus
st.set_page_config(page_title="Eesti sooneostaimede eoste määraja", page_icon="🌿", layout="wide")

st.title("🌿 Eesti sooneostaimede eoste määraja")

try:
    # Andmete laadimine (veebis kasutame vaid faili nime)
    df = pd.read_csv('Fixed_Spore_Data.csv', encoding='latin-1')
    
    # 2. FILTRITE LOOMINE KATEGOORIATENA (SIDEBAR)
    st.sidebar.header("Määramistunnused")
    st.sidebar.write("Vali eose tunnused kategooriate kaupa:")

    aktiivsed_filtrid = []

    # --- KATEGOORIA: KUJU ---
    with st.sidebar.expander("Kuju", expanded=False):
        kuju_valikud = {
            "Bilateraalne": "shape_bilateral",
            "Sfääriline": "shape_spherical",
            "Tetraeedriline": "shape_tetra"
        }
        for silt, veerg in kuju_valikud.items():
            if veerg in df.columns:
                if st.sidebar.checkbox(silt, key=veerg):
                    df = df[df[veerg] == 1]
                    aktiivsed_filtrid.append(f"Kuju: {silt}")

    # --- KATEGOORIA: PERISPOOR ---
    with st.sidebar.expander("Perispoor", expanded=False):
        if 'perine_absent' in df.columns:
            if st.sidebar.checkbox("Perispoor puudub", key='perine_absent'):
                df = df[df['perine_absent'] == 1]
                aktiivsed_filtrid.append("Perispoor puudub")

    # --- KATEGOORIA: PINNASTRUKTUUR ---
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
                if st.sidebar.checkbox(silt, key=veerg):
                    df = df[df[veerg] == 1]
                    aktiivsed_filtrid.append(f"Pind: {silt}")

    # --- KATEGOORIA: SUURUS ---
    with st.sidebar.expander("Suurus", expanded=False):
        st.sidebar.info("Siia saame lisada suuruse filtrid, kui andmed on tabelis olemas.")

    # 3. TULEMUSTE KUVAMINE
    st.divider()
    
    if aktiivsed_filtrid:
        st.write(f"**Valitud filtrid:** {', '.join(aktiivsed_filtrid)}")

    vastete_arv = len(df)
    
    if vastete_arv == 0:
        st.warning("Selliste tunnustega liike ei leitud. Muuda valikuid.")
    else:
        # Loome kaldkirjas liiginime veeru kuvamiseks
        if 'species' in df.columns:
            df['Liiginimi'] = df['species'].apply(lambda x: f"*{x}*")

        # Kuvame leitud vastete arvu
        st.success(f"Leitud vasteid: {vastete_arv}")

        if vastete_arv == 1:
            st.info(f"Tuvastatud liik: **{df.iloc[0]['species']}**")

        # Kuvame tabeli (peidame tehnilised veerud ja näitame kaldkirjas nime)
        naitatavad_veerud = ['Liiginimi', 'genus', 'family']
        olemasolevad = [v for v in naitatavad_veerud if v in df.columns]
        
        st.dataframe(
            df[olemasolevad], 
            use_container_width=True,
            column_config={
                "Liiginimi": st.column_config.TextColumn("Liiginimi (ladina k)")
            },
            hide_index=True 
        )

except Exception as e:
    st.error(f"Viga: {e}")