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
    voimalikud_veerud = [
        'shape_bilateral', 'shape_spherical', 'shape_tetra', 
        'perine_absent', 'surf_cristate', 'surf_echinate', 
        'surf_reticulate', 'surf_verrucate'
    ]

    aktiivsed_filtrid = []

    # Käime kõik võimalikud veerud läbi
    for veerg in voimalikud_veerud:
        if veerg in df.columns:
            # Teeme ilusa nime (nt shape_bilateral -> Bilateral)
            ilus_nimi = veerg.replace('_', ' ').capitalize()
            
            # Kui kasutaja märgib kasti, siis filtreerime
            if st.sidebar.checkbox(ilus_nimi, key=veerg):
                df = df[df[veerg] == 1]
                aktiivsed_filtrid.append(ilus_nimi)

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
