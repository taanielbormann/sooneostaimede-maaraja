import streamlit as st
import pandas as pd

# Lehe seadistus
st.set_page_config(page_title="Eesti sooneostaimede eoste määraja", page_icon="🌿", layout="wide")

st.title("🌿 Eesti sooneostaimede eoste määraja")

# 1. Andmete laadimine
try:
    df = pd.read_csv('Fixed_Spore_Data.csv', encoding='latin-1')
    
    st.sidebar.header("Määramistunnused")
    st.sidebar.write("Vali eose tunnused:")

    # 2. Dünaamiline filtreerimine
    # See osa loob automaatselt filtrid veergudele nagu 'Kuju', 'Pind' jne.
    # Kontrolli, et need nimed ühtiksid sinu CSV päistega!
    tunnused = ['Kuju', 'Pind', 'Värvus'] # Lisa siia nimekirja teisi veerge, mida soovid filtreerida
    
    for tunnus in tunnused:
        if tunnus in df.columns:
            valikud = sorted(df[tunnus].dropna().unique())
            valitud = st.sidebar.multiselect(f"Vali {tunnus.lower()}:", valikud)
            if valitud:
                df = df[df[tunnus].isin(valitud)]

    # 3. Tulemuste kuvamine
    st.divider()
    vastete_arv = len(df)
    
    if vastete_arv == 0:
        st.warning("Selliste tunnustega liike ei leitud. Proovi valikuid muuta.")
    else:
        st.success(f"Leitud vasteid: {vastete_arv}")
        
        # Kui jääb alles ainult üks liik
        if vastete_arv == 1:
            st.balloons()
            liigi_nimi = df.iloc[0]['Liik'] if 'Liik' in df.columns else "Tuvastamata liik"
            st.info(f"Leitud liik: **{liigi_nimi}**")

        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Viga: {e}")