import streamlit as st
import pandas as pd
import plotly.express as px
import re
import unicodedata

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Dashboard Transport", layout="wide")
st.markdown(
    "<h1 style='text-align:center; color:white;'>🚍 Suivi du transport de personnel</h1>",
    unsafe_allow_html=True
)
st.markdown("""
<style>
/* Carte metric : fond blanc + contour bleu + arrondi + légère ombre */
div[data-testid="stMetric"] {
  background: #1769aa !important;
  border: 2px solid #0a2d49 !important;
  border-radius: 14px !important;
  padding: 12px 14px !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}

/* Libellé (ex: 🚐 Véhicules) */
div[data-testid="stMetric"] span[data-testid="stMetricLabel"] {
  color: #0a2d49 !important;
  font-weight: 600 !important;
}

/* Valeur (ex: 12) */
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
  color: white !important;
}

/* Delta (si tu l’utilises) */
div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
  color: #0a2d49 !important;
}
</style>
""", unsafe_allow_html=True)



BLUE_SCALE = [
    (0.00, "#eaf2fb"),
    (0.10, "#d6e4f6"),
    (0.20, "#c1d6f1"),
    (0.35, "#8fb6e4"),
    (0.50, "#5f97d6"),
    (0.70, "#2f78c9"),
    (0.85, "#155a9d"),
    (1.00, "#0a2d49"),
]


st.divider()


# --- CASA HUB ---
SHEET_ID_CASA = "10pZOIFRyJPsM1ynt2cQQT6kl4iPDCsSBBSQxCeCcyb4"
SHEET_URL_CASA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_CASA}/export?format=csv&gid=0"
SHEET_URL_CASA_SHIFT1 = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_CASA}/export?format=csv&gid=833510072"
SHEET_URL_CASA_SHIFT2 = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_CASA}/export?format=csv&gid=944576156"

# --- LOGIPROD ---
SHEET_ID_LOGIPROD = "15-vYUAshPF1WIec7MYnU7obIu8BF9OGiDSVlj2ugcTA"
SHEET_URL_LOGIPROD = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_LOGIPROD}/export?format=csv&gid=0"
SHEET_URL_LOGIPROD_NORMAL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_LOGIPROD}/export?format=csv&gid=399496494"
SHEET_URL_LOGIPROD_SHIFT1 = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_LOGIPROD}/export?format=csv&gid=859832319"
SHEET_URL_LOGIPROD_SHIFT2 = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_LOGIPROD}/export?format=csv&gid=848354895"

# --- HMI ---
SHEET_ID_HMI = "1MsEzKIjae3pYGFgZVPRft6Zv21k7Jzt8-iXwyiLnoo0"  # 👈 remplace si besoin
SHEET_URL_HMI = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_HMI}/export?format=csv&gid=813428560"
SHEET_URL_HMI_NORMAL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_HMI}/export?format=csv&gid=1643109752"
SHEET_URL_HMI_SHIFT1 = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_HMI}/export?format=csv&gid=407350218"
SHEET_URL_HMI_SHIFT2 = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_HMI}/export?format=csv&gid=1002680487"
SHEET_URL_HMI_SHIFT3 = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_HMI}/export?format=csv&gid=1117573875"
# --- Steripharma ---
SHEET_ID_steri = "1MA9UnXpOYmxs2QbMd2cMRQeuC1wsFQqlJzF8_GvSQ6Q"  # 👈 remplace si besoin
SHEET_URL_steri = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_steri}/export?format=csv&gid=0"
SHEET_URL_steri_NORMAL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_steri}/export?format=csv&gid=1335569597"


# ==============================
# UTILS
# ==============================
@st.cache_data
def load_csv(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        st.warning(f"Erreur de chargement : {e}")
        return pd.DataFrame()

def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text).strip().lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    return re.sub(r"\s+", " ", text)

def convert_duration_to_minutes(duration_str):
    if pd.isna(duration_str) or not isinstance(duration_str, str):
        return 0
    h = re.search(r'(\d+)\s*h', duration_str)
    m = re.search(r'(\d+)\s*min', duration_str)
    total = 0
    if h:
        total += int(h.group(1)) * 60
    if m:
        total += int(m.group(1))
    return total

# ==============================
# LOAD DATA
# ==============================
# --- CASA ---
df_casa = load_csv(SHEET_URL_CASA)
df_casa_shift1 = load_csv(SHEET_URL_CASA_SHIFT1)
df_casa_shift2 = load_csv(SHEET_URL_CASA_SHIFT2)

# --- LOGIPROD ---
df_logi = load_csv(SHEET_URL_LOGIPROD)
df_logi_normal = load_csv(SHEET_URL_LOGIPROD_NORMAL)
df_logi_shift1 = load_csv(SHEET_URL_LOGIPROD_SHIFT1)
df_logi_shift2 = load_csv(SHEET_URL_LOGIPROD_SHIFT2)

# --- HMI ---
df_hmi = load_csv(SHEET_URL_HMI)
df_hmi_normal = load_csv(SHEET_URL_HMI_NORMAL)
df_hmi_shift1 = load_csv(SHEET_URL_HMI_SHIFT1)
df_hmi_shift2 = load_csv(SHEET_URL_HMI_SHIFT2)
df_hmi_shift3 = load_csv(SHEET_URL_HMI_SHIFT3)

# --- Steripharma ---
df_steri = load_csv(SHEET_URL_steri)
df_steri_normal = load_csv(SHEET_URL_steri_NORMAL)


# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("Filtres")
CAPACITE = 20
# st.sidebar.number_input("Capacité par véhicule", min_value=1, max_value=60, value=20)
entreprise = st.sidebar.selectbox("Entreprise", ["Casa hub", "Logiprod", "HMI", "Steripharma"])

# ==============================
# CHOIX DU SITE
# ==============================
if entreprise == "Casa hub":
    df_site = df_casa
    df_shift1_site = df_casa_shift1
    df_shift2_site = df_casa_shift2
elif entreprise == "Logiprod":
    df_site = df_logi
    df_normal_site = df_logi_normal
    df_shift1_site = df_logi_shift1
    df_shift2_site = df_logi_shift2
elif entreprise == "HMI":
    df_site = df_hmi
    df_normal_site = df_hmi_normal
    df_shift1_site = df_hmi_shift1
    df_shift2_site = df_hmi_shift2
    df_shift3_site = df_hmi_shift3

elif entreprise == "Steripharma":
    df_site = df_steri
    df_normal_site = df_steri_normal

else:
    df_site = pd.DataFrame()
    df_normal_site = df_shift1_site = df_shift2_site = pd.DataFrame()

# ==============================
# METRIQUES
# ==============================
mask_personnes = (
    df_site["nom&prenom"].notna()
    & ~df_site["nom&prenom"].str.contains("arret|depart|pt de depart", case=False, na=False)
)

nb_vehicules = df_site["matricule"].dropna().nunique()
nb_chauffeurs = df_site["chauffeur"].dropna().nunique()
nb_shifts = df_site["shift"].dropna().nunique()
nb_personnes = df_site[mask_personnes]["nom&prenom"].count()

c1, c2, c3, c4 = st.columns(4)
c1.metric("🚐 Véhicules", nb_vehicules)
c2.metric("🧑‍✈️ Chauffeurs", nb_chauffeurs)
c3.metric("🕐 Equipes", nb_shifts)
c4.metric("👥 Personnes", nb_personnes)

st.divider()

# ==============================
# GRAPH TAUX DE REMPLISSAGE
# ==============================
st.subheader("📈 Taux de remplissage (%) par Chauffeur et Shift")

df_valid = df_site[mask_personnes].copy()
df_valid["chauffeur_norm"] = df_valid["chauffeur"].apply(normalize)

grouped = (
    df_valid.groupby(["shift", "chauffeur_norm"], dropna=True)
    .agg(nb_personnes=("nom&prenom", "nunique"))
    .reset_index()
)
grouped["taux_pct"] = (grouped["nb_personnes"] / CAPACITE * 100).round(1)

shifts = sorted(grouped["shift"].dropna().unique())
for i in range(0, len(shifts), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j >= len(shifts):
            break
        shift = shifts[i + j]
        df_s = grouped[grouped["shift"] == shift].sort_values("taux_pct", ascending=False)
        fig = px.bar(
            df_s,
            x="chauffeur_norm",
            y="taux_pct",
            text="taux_pct",
            title=f"{shift} — Taux de remplissage (%)",
            color="taux_pct",
            color_continuous_scale=BLUE_SCALE,   # 👈 nuances de bleu
            range_color=(0, 100)                 # pour garder la même échelle sur tous les graphes
        )
        fig.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
        fig.update_yaxes(range=[0, 100], title="Taux (%)")
        fig.update_layout(xaxis_title="Chauffeur", margin=dict(l=20, r=20, t=60, b=20))
        cols[j].plotly_chart(fig, use_container_width=True)

st.divider()

# ==============================
# TABLEAUX PAR SHIFT
# ==============================
st.subheader("📋 Détails par Shift")

def prepare_shift_table(df_shift, shift_name):
    if df_shift.empty:
        return pd.DataFrame(columns=["Chauffeur", "Shift", "Distance", "Durée", "Nb personnes"])

    df_shift = df_shift.rename(columns={
        "chauffeur": "Chauffeur",
        "shift": "Shift",
        "distance": "Distance",
        "durée": "Durée"
    })
    df_shift["chauffeur_norm"] = df_shift["Chauffeur"].apply(normalize)
    df_shift["Durée_min"] = df_shift["Durée"].apply(convert_duration_to_minutes)
    df_shift["Durée"] = df_shift.apply(
        lambda r: f"{r['Durée']} ⚠️" if r["Durée_min"] > 90 else r["Durée"], axis=1
    )

    merged = pd.merge(
        df_shift,
        grouped[["shift", "chauffeur_norm", "nb_personnes"]],
        how="left",
        left_on=["Shift", "chauffeur_norm"],
        right_on=["shift", "chauffeur_norm"]
    )

    merged = merged[["Chauffeur", "Shift", "Distance", "Durée", "nb_personnes"]]
    merged = merged.rename(columns={"nb_personnes": "Nb personnes"})
    return merged

# --- TABLES ---

if entreprise == "Logiprod":
    st.markdown("### 🕐 Normal [🗺️](https://www.google.com/maps/d/edit?hl=fr&mid=1AWwS0Fh7kGqF45LLthDnNUw98p6ZhOA&ll=33.5164216889364%2C-7.668005000000008&z=11)", unsafe_allow_html=True)
    table_normal = prepare_shift_table(df_normal_site, "normal")
    st.dataframe(table_normal, use_container_width=True, hide_index=True)

    st.markdown("### 🕐 Shift 1 [🗺️](https://www.google.com/maps/d/edit?hl=fr&mid=1ORX0VuY0VO8heJBnkg7sm3IkfZqbM9s&ll=33.47766561562251%2C-7.736224999999992&z=12)", unsafe_allow_html=True)
    table1 = prepare_shift_table(df_shift1_site, "shift 1")
    st.dataframe(table1, use_container_width=True, hide_index=True)

    st.markdown("### 🕐 Shift 2 [🗺️](https://www.google.com/maps/d/edit?hl=fr&mid=1CgnWy11ud3Zyuow2S587sD8BQsdowQo&ll=33.454163890190735%2C-7.728035000000006&z=12)", unsafe_allow_html=True)
    table2 = prepare_shift_table(df_shift2_site, "shift 2")
    st.dataframe(table2, use_container_width=True, hide_index=True)

if entreprise == "Casa hub":
    st.markdown("### 🕐 Shift 1 [🗺️](https://www.google.com/maps/d/edit?hl=fr&mid=1o3MrlHn32N8xH_PWpIsxtd163sYAshM&ll=33.515104057542175%2C-7.642830999999996&z=11)", unsafe_allow_html=True)
    table1 = prepare_shift_table(df_shift1_site, "shift 1")
    st.dataframe(table1, use_container_width=True, hide_index=True)

    st.markdown("### 🕐 Shift 2 [🗺️](https://www.google.com/maps/d/edit?hl=fr&mid=1gVo5H_-DJbb5mUe7vgdh-nruCKeiEos&ll=33.56991600416464%2C-7.599525499999997&z=10)", unsafe_allow_html=True)
    table2 = prepare_shift_table(df_shift2_site, "shift 2")
    st.dataframe(table2, use_container_width=True, hide_index=True)

if entreprise == "HMI":
    st.markdown("### 🕐 Normal [🗺️](https://www.google.com/maps/d/edit?hl=fr&mid=19yMtXMhZd1EVtHXctcFAr2ilP3IiNTs&ll=33.48111573873554%2C-7.4896835&z=10)", unsafe_allow_html=True)
    table_normal = prepare_shift_table(df_normal_site, "normal")
    st.dataframe(table_normal, use_container_width=True, hide_index=True)

    st.markdown("### 🕐 Shift 1 [🗺️](https://www.google.com/maps/d/edit?hl=fr&mid=1-VcA0vHT4PFN8RTvyYoDPypTF01zkc4&ll=33.625196155892226%2C-7.468961&z=12)", unsafe_allow_html=True)
    table1 = prepare_shift_table(df_shift1_site, "shift 1")
    st.dataframe(table1, use_container_width=True, hide_index=True)

    st.markdown("### 🕐 Shift 2 [🗺️](https://www.google.com/maps/d/edit?hl=fr&mid=1l7Fq0MjTwsa5JrMuda4SjaYJvl55zrE&ll=33.62434149775241%2C-7.442983499999993&z=12)", unsafe_allow_html=True)
    table2 = prepare_shift_table(df_shift2_site, "shift 2")
    st.dataframe(table2, use_container_width=True, hide_index=True)

    st.markdown("### 🕐 Shift 3 [🗺️](https://www.google.com/maps/d/edit?hl=fr&mid=11ebs_NXb-dgNQyG_51BMMYaMsn6UtWk&ll=33.6677255772706%2C-7.378471999999998&z=15)", unsafe_allow_html=True)
    table3 = prepare_shift_table(df_shift3_site, "shift 3")
    st.dataframe(table3, use_container_width=True, hide_index=True)

if entreprise == "Steripharma":
    st.markdown("### 🕐 Normal [🗺️](https://www.google.com/maps/d/viewer?mid=LIEN_MYMAPS_NORMAL)", unsafe_allow_html=True)
    table1 = prepare_shift_table(df_normal_site, "normal")
    st.dataframe(table1, use_container_width=True, hide_index=True)

  
st.divider()
st.info("⚠️ = durée supérieure à 1h30min")
