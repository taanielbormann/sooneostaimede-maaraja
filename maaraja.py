import streamlit as st
import pandas as pd

# 1. Lehe seadistus
st.set_page_config(page_title="Eesti sooneostaimede eoste määraja", page_icon="🌿", layout="wide")

st.title("🌿 Eesti sooneostaimede eoste määraja")

try:
    # Andmete laadimine
    df = pd.read_csv('Fixed_Spore_Data.csv', encoding='latin-1')
    
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
        if 'perine_absent' in df.columns:
            if st.checkbox("Perispoor puudub", key='perine_absent'):
                df = df[df['perine_absent'] == 1]
                aktiivsed_filtrid.append("Perispoor: Puudub")
            if st.checkbox("Perispoor olemas", key='perine_present'):
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

    # --- KATEGOORIA: SUURUS ---
    with st.sidebar.expander("Suurus", expanded=False):
        st.write("Suuruse filtrid lisanduvad siia peagi.")

    # 3. TULEMUSTE KUVAMINE
    st.divider()
    if aktiivsed_filtrid:
        st.write(f"**Valitud filtrid:** {', '.join(aktiivsed_filtrid)}")

    vastete_arv = len(df)
    if vastete_arv == 0:
        st.warning("Selliste tunnustega liike ei leitud. Muuda valikuid.")
    else:
        st.success(f"Leitud vasteid: {vastete_arv}")

        # Vormistame nime kaldkirja ainult sulgude sees
        def vormista_html_nimi(nimi):
            if isinstance(nimi, str) and "(" in nimi and ")" in nimi:
                eesti, ladina = nimi.split("(", 1)
                ladina = ladina.replace(")", "")
                return f"{eesti}(<i>{ladina}</i>)"
            return nimi

        if 'species' in df.columns:
            df['Liiginimi (ladina k)'] = df['species'].apply(vormista_html_nimi)

        # Valime veerud
        naitatavad = ['Liiginimi (ladina k)', 'genus', 'family']
        olemasolevad = [v for v in naitatavad if v in df.columns]
        
        # Teeme tabelist HTML-i
        tabeli_html = df[olemasolevad].to_html(escape=False, index=False)
        
        # Kuvame tabeli koos CSS-iga, et vältida "kõik järjest" probleemi
        st.write(f"""
            <style>
                .custom-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                    font-size: 16px;
                }}
                .custom-table th {{
                    text-align: left;
                    background-color: #262730;
                    padding: 12px;
                    border-bottom: 2px solid #4e4e4e;
                }}
                .custom-table td {{
                    text-align: left;
                    padding: 12px;
                    border-bottom: 1px solid #333333;
                }}
            </style>
            <div class="custom-table">
                {tabeli_html}
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Viga: {e}")