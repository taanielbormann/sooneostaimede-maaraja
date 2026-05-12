import streamlit as st
import pandas as pd

# 1. Lehe seadistus
st.set_page_config(page_title="Eesti sooneostaimede eoste määraja", page_icon="🌿", layout="wide")

st.title("🌿 Eesti sooneostaimede eoste määraja")

try:
    # Andmete laadimine ja puhastamine
    df = pd.read_csv('Fixed_Spore_Data.csv', encoding='latin-1')
    df.columns = df.columns.str.strip()
    
    # 2. FILTRITE LOOMINE KÜLJEPEAL
    st.sidebar.header("Määramistunnused")
    aktiivsed_filtrid = []

    # --- KATEGOORIA: KUJU ---
    with st.sidebar.expander("Kuju", expanded=True):
        # Kuvame sinu Illustratori pildid kõrvuti
        col1, col2 = st.columns(2)
        with col1:
            try:
                st.image("pildid/bilateral.png", caption="Bilateraalne")
            except:
                st.caption("🖼️ Bilateraalne pilt")
        with col2:
            try:
                st.image("pildid/tetra.png", caption="Tetraeedriline")
            except:
                st.caption("🖼️ Tetra pilt")

        kuju_valikud = {
            "Bilateraalne": "shape_bilateral",
            "Tetraeedriline": "shape_tetra",
            "Sfääriline": "shape_spherical"
        }
        for silt, veerg in kuju_valikud.items():
            if veerg in df.columns:
                if st.checkbox(silt, key=veerg):
                    df = df[df[veerg] == 1]
                    aktiivsed_filtrid.append(f"Kuju: {silt}")

    # --- KATEGOORIA: PINNASTRUKTUUR ---
    with st.sidebar.expander("Pinnastruktuur", expanded=False):
        # Siia saab tulevikus lisada ka pinnastruktuuride joonise
        pind_valikud = {
            "Ogaline": "surf_echinate", "Tüükaline": "surf_verrucate", 
            "Retikulaarne": "surf_reticulate", "Sile": "surf_psilate"
        }
        for silt, veerg in pind_valikud.items():
            if veerg in df.columns:
                if st.checkbox(silt, key=veerg):
                    df = df[df[veerg] == 1]
                    aktiivsed_filtrid.append(f"Pind: {silt}")

    # --- KATEGOORIA: PERISPOOR ---
    with st.sidebar.expander("Perispoor", expanded=False):
        if 'perine_absent' in df.columns:
            if st.checkbox("Perispoor puudub", key='p_absent'):
                df = df[df['perine_absent'] == 1]
                aktiivsed_filtrid.append("Perispoor: Puudub")
            if st.checkbox("Perispoor olemas", key='p_present'):
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

        # Vormistame nime kaldkirja (Markdown tärnidega st.table jaoks)
        def vormista_kaldkiri(nimi):
            if isinstance(nimi, str) and "(" in nimi and ")" in nimi:
                parts = nimi.split("(", 1)
                eesti = parts[0]
                ladina = parts[1].replace(")", "")
                return f"{eesti} (*{ladina.strip()}*)"
            return nimi

        # Teeme koopia ja vormistame
        df_display = df.copy()
        if 'species' in df_display.columns:
            df_display['Liiginimi (ladina k)'] = df_display['species'].apply(vormista_kaldkiri)
        
        # Valime ainult olemasolevad veerud kuvamiseks
        soovitud = ['Liiginimi (ladina k)', 'genus', 'family']
        olemasolevad = [v for v in soovitud if v in df_display.columns]
        
        # Kuvame tabeli
        st.table(df_display[olemasolevad])

        # --- LIIKIDE FOTOD (tabeli all) ---
        if 'image_url' in df.columns:
            st.subheader("Tuvastatud liikide eoste fotod")
            df_piltidega = df.dropna(subset=['image_url'])
            if not df_piltidega.empty:
                cols = st.columns(3)
                for i, (idx, row) in enumerate(df_piltidega.iterrows()):
                    with cols[i % 3]:
                        st.image(row['image_url'], caption=row['species'], use_container_width=True)

except Exception as e:
    st.error(f"Viga rakenduse töös: {e}")