import streamlit as st
import pandas as pd

# 1. Lehe seadistus
st.set_page_config(page_title="Eesti sooneostaimede eoste määraja", page_icon="🌿", layout="wide")

st.title("🌿 Eesti sooneostaimede eoste määraja")

try:
    # Andmete laadimine
    df = pd.read_csv('Fixed_Spore_Data.csv', encoding='latin-1')
    
    # 2. FILTRITE LOOMINE (Automaatne)
    st.sidebar.header("Määramistunnused")
    st.sidebar.write("Vali eose tunnused:")

    # Defineerime, milliseid veerge me tahame filtritena kasutada
    # Kontrolli, et need nimed oleksid täpselt samad, mis su Excelis!
   # 2. FILTRITE LOOMINE (Kasutame sinu eestikeelseid termineid)
    st.sidebar.header("Määramistunnused")
    st.sidebar.write("Vali eose tunnused:")

    # Sõnastik: "Eestikeelne nimi" : "Veeru nimi tabelis"
    tunnused = {
        "Kuju: bilateraalne": "shape_bilateral",
        "Kuju: sfääriline": "shape_spherical",
        "Kuju: tetraeedriline": "shape_tetra",
        "Perispoor puudub": "perine_absent",
        "Pind: ogaline (echinate)": "surf_echinate",
        "Pind: peeneogaline (microechinate)": "surf_microechinate",
        "Pind: tüükaline (verrucate)": "surf_verrucate",
        "Pind: lohuline (lophate)": "surf_lophate",
        "Pind: harjaline (cristate)": "surf_cristate",
        "Pind: retikulaarne (reticulate)": "surf_reticulate",
        "Pind: kurruline (rugulate)": "surf_rugulate",
        "Pind: konksuline (hamulate)": "surf_hamulate",
        "Pind: granulaarne (granulate)": "surf_granulate",
        "Pind: peenkare (scabrate)": "surf_scabrate",
        "Pind: sile (psilate)": "surf_psilate",
        "Pind: auguline (foveolate)": "surf_foveolate",
        "Pind: voldiline (folded)": "surf_folded"
    }

    aktiivsed_filtrid = []

    for silt, veerg in tunnused.items():
        if veerg in df.columns:
            if st.sidebar.checkbox(silt, key=veerg):
                df = df[df[veerg] == 1]
                aktiivsed_filtrid.append(silt)

    # 3. TULEMUSTE KUVAMINE
    st.divider()
    
    if aktiivsed_filtrid:
        st.write(f"**Valitud filtrid:** {', '.join(aktiivsed_filtrid)}")

    vastete_arv = len(df)
    
    if vastete_arv == 0:
        st.warning("Selliste tunnustega liike ei leitud. Proovi teisi valikuid.")
    else:
        st.success(f"Leitud vasteid: {vastete_arv}")
        
        if vastete_arv == 1:
            st.balloons()
            st.info(f"Tuvastatud liik: **{df.iloc[0]['species']}**")

        # Näitame tulemusi (ainult olulised veerud, et Exceli tunnet vähendada)
        naidatavad_veerud = ['species', 'genus', 'family']
        # Lisame nimekirja ka need veerud, mis on hetkel tabelis olemas
        olemasolevad = [v for v in naidatavad_veerud if v in df.columns]
        
        st.dataframe(df[olemasolevad] if olemasolevad else df, use_container_width=True)

except Exception as e:
    st.error(f"Viga: {e}")