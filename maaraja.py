import streamlit as st
import pandas as pd

# 1. Lehe seadistus
st.set_page_config(page_title="Eesti sooneostaimede eoste määraja", page_icon="🌿", layout="wide")

st.title("🌿 Eesti sooneostaimede eoste määraja")

try:
    # Andmete laadimine - kontrollime, et fail oleks loetav
    df = pd.read_csv('Fixed_Spore_Data.csv', encoding='latin-1')
    
    # Eemaldame veergude nimedest igaks juhuks tühikud
    df.columns = df.columns.str.strip()
    
    # 2. FILTRITE LOOMINE KÜLJEPEAL
    st.sidebar.header("Määramistunnused")
    aktiivsed_filtrid = []

    # --- KATEGOORIA: KUJU ---
    with st.sidebar.expander("Kuju", expanded=False):
        kuju_valikud = {"Bilateraalne": "shape_bilateral", "Sfääriline": "shape_spherical", "Tetraeedriline": "shape_tetra"}
        for silt, veerg in kuju_valikud.items():
            if veerg in df.columns:
                if st.checkbox(silt, key=veerg):
                    df = df[df[veerg] == 1]
                    aktiivsed_filtrid.append(f"Kuju: {silt}")

    # --- KATEGOORIA: PERISPOOR ---
    with st.sidebar.expander("Perispoor", expanded=False):
        # Kasutame märkeruute, et vältida raadionuppude "Valimata" muret
        if 'perine_absent' in df.columns:
            if st.checkbox("Perispoor puudub", key='perine_absent_check'):
                df = df[df['perine_absent'] == 1]
                aktiivsed_filtrid.append("Perispoor: Puudub")
            if st.checkbox("Perispoor olemas", key='perine_present_check'):
                df = df[df['perine_absent'] == 0]
                aktiivsed_filtrid.append("Perispoor: Olemas")

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

        # Teeme kaldkirja botaanilise nime jaoks
        def vormista_kaldkiri(nimi):
            if isinstance(nimi, str) and "(" in nimi and ")" in nimi:
                eesti, ladina = nimi.split("(", 1)
                return f"{eesti} (*{ladina.replace(')', '')}*)"
            return nimi

        # Loome uue veeru kuvamiseks
        if 'species' in df.columns:
            df['Liiginimi'] = df['species'].apply(vormista_kaldkiri)
        
        # KONTROLL: millised veerud on failis päriselt olemas?
        soovitud_veerud = ['Liiginimi', 'genus', 'family']
        olemasolevad_veerud = [v for v in soovitud_veerud if v in df.columns]

        # Kui veerge 'genus' või 'family' pole, näitame vähemalt liiginime
        if not olemasolevad_veerud and 'species' in df.columns:
            olemasolevad_veerud = ['Liiginimi']

        # KUVAMINE: Kasutame st.table, et vältida HTML-joru ja Markdowni probleeme
        st.table(df[olemasolevad_veerud])

except Exception as e:
    st.error(f"Viga: {e}")