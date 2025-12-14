import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(
    page_title="RFM Customer Segmentation",
    layout="wide"
)

st.title("📊 RFM Customer Segmentation Dashboard")
st.caption(
    "Dashboard analisis segmentasi customer berbasis Recency, Frequency, dan Monetary "
    "untuk mendukung pengambilan keputusan pemasaran."
)

# ============================
# LOAD DATA
# ============================
@st.cache_data
def load_data():
    return pd.read_csv("rfm_segmentasi_final.csv")

df = load_data()

# ============================
# WARNA CLUSTER (SESUAI PERMINTAAN)
# ============================
cluster_colors = {
    0: '#1f77b4',  # Biru
    1: '#ff7f0e',  # Oranye
    2: '#2ca02c',  # Hijau
    3: '#d62728'   # Merah
}

# ============================
# SIDEBAR FILTER
# ============================
st.sidebar.header("🔎 Filter Data")

selected_clusters = st.sidebar.multiselect(
    "Pilih Cluster",
    options=sorted(df['Cluster'].unique()),
    default=sorted(df['Cluster'].unique())
)

filtered_df = df[df['Cluster'].isin(selected_clusters)]

# ============================
# METRIC CARDS
# ============================
col1, col2, col3 = st.columns(3)

col1.metric("Total Customer", f"{len(filtered_df):,}")
col2.metric("Avg Frequency", round(filtered_df['Frequency'].mean(), 2))
col3.metric("Avg Monetary (£)", round(filtered_df['MonetaryValue'].mean(), 2))

st.divider()

# ============================
# BAR CHART – JUMLAH CUSTOMER
# ============================
st.subheader("📊 Jumlah Customer per Cluster")

cluster_counts = filtered_df['Cluster'].value_counts().sort_index()

fig_bar, ax_bar = plt.subplots(figsize=(8, 5))

bars = ax_bar.bar(
    cluster_counts.index.astype(str),
    cluster_counts.values,
    color=[cluster_colors[c] for c in cluster_counts.index]
)

ax_bar.set_title("Jumlah Customer per Cluster", fontsize=14, fontweight='bold')
ax_bar.set_xlabel("Cluster")
ax_bar.set_ylabel("Jumlah Customer")

for bar in bars:
    height = bar.get_height()
    ax_bar.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f'{int(height)}',
        ha='center',
        va='bottom',
        fontsize=11
    )

st.pyplot(fig_bar)

st.divider()

# ============================
# DONUT CHART – PROPORSI
# ============================
st.subheader("🍩 Proporsi Customer per Cluster")

fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
ax_pie.pie(
    cluster_counts.values,
    labels=[f"Cluster {c}" for c in cluster_counts.index],
    autopct='%1.1f%%',
    startangle=120,
    colors=[cluster_colors[c] for c in cluster_counts.index],
    wedgeprops={'edgecolor': 'white'}
)

centre_circle = plt.Circle((0, 0), 0.65, fc='white')
ax_pie.add_artist(centre_circle)

ax_pie.set_title("Distribusi Customer per Cluster", fontsize=13, fontweight='bold')
st.pyplot(fig_pie)

st.divider()

# ============================
# SCATTER 2D
# ============================
st.subheader("🎯 Sebaran Customer (Recency vs Monetary)")

fig_scatter, ax_scatter = plt.subplots(figsize=(8, 5))

for c in cluster_counts.index:
    subset = filtered_df[filtered_df['Cluster'] == c]
    ax_scatter.scatter(
        subset['Recency'],
        subset['MonetaryValue'],
        label=f'Cluster {c}',
        color=cluster_colors[c],
        alpha=0.75,
        s=60,
        edgecolor='white'
    )

ax_scatter.set_xlabel("Recency (days)")
ax_scatter.set_ylabel("Monetary Value (£)")
ax_scatter.set_title("Customer Segmentation (Recency vs Monetary)")
ax_scatter.legend(title="Cluster")

st.pyplot(fig_scatter)

st.divider()

# ============================
# VIOLIN PLOTS
# ============================
st.subheader("🎻 Distribusi RFM per Cluster")

fig_violin, ax = plt.subplots(1, 3, figsize=(16, 4))

sns.violinplot(
    data=filtered_df, x='Cluster', y='Recency',
    palette=cluster_colors, inner='quartile', ax=ax[0]
)
ax[0].set_title("Recency")

sns.violinplot(
    data=filtered_df, x='Cluster', y='Frequency',
    palette=cluster_colors, inner='quartile', ax=ax[1]
)
ax[1].set_title("Frequency")

sns.violinplot(
    data=filtered_df, x='Cluster', y='MonetaryValue',
    palette=cluster_colors, inner='quartile', ax=ax[2]
)
ax[2].set_title("Monetary Value")

st.pyplot(fig_violin)

st.divider()

# ============================
# INSIGHT CLUSTER
# ============================
st.subheader("🧠 Penjelasan & Insight Cluster RFM")

with st.expander("🔵 Cluster 0 – Lowest Customers"):
    st.markdown("""
- Nilai belanja dan frekuensi rendah  
- Lama tidak bertransaksi  
**Strategi:** re-engagement, diskon agresif, survei churn
""")

with st.expander("🟠 Cluster 1 – Best Customers"):
    st.markdown("""
- Nilai belanja tertinggi  
- Sangat loyal  
**Strategi:** VIP treatment, reward eksklusif, referral
""")

with st.expander("🟢 Cluster 2 – Potential Customers"):
    st.markdown("""
- Pelanggan baru / nilai kecil  
- Potensi tumbuh  
**Strategi:** welcome voucher, edukasi produk, upselling ringan
""")

with st.expander("🔴 Cluster 3 – Active Customers"):
    st.markdown("""
- Aktif bertransaksi  
- Nilai menengah  
**Strategi:** loyalty tier, promo eksklusif, personalisasi
""")

st.divider()

# ============================
# DATA TABLE
# ============================
st.subheader("📄 Data Customer (Sample)")
st.dataframe(filtered_df.head(50), use_container_width=True)

st.caption(
    "📌 Insight Utama: Segmentasi RFM membantu bisnis memahami perilaku pelanggan "
    "dan menyusun strategi pemasaran yang lebih tepat sasaran."
)

