
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="RFM Customer Segmentation", layout="wide")

st.title("📊 RFM Customer Segmentation Dashboard")
st.caption(
    "Dashboard analisis segmentasi customer berbasis Recency, Frequency, dan Monetary "
    "untuk mendukung pengambilan keputusan pemasaran."
)

@st.cache_data
def load_data():
    return pd.read_csv("rfm_segmentasi_final.csv")

df = load_data()

cluster_palette = sns.color_palette("Set2")

st.sidebar.header("🔎 Filter Data")
selected_clusters = st.sidebar.multiselect(
    "Pilih Cluster",
    options=sorted(df['Cluster'].unique()),
    default=sorted(df['Cluster'].unique())
)

filtered_df = df[df['Cluster'].isin(selected_clusters)]

col1, col2, col3 = st.columns(3)
col1.metric("Total Customer", f"{len(filtered_df):,}")
col2.metric("Avg Frequency", round(filtered_df['Frequency'].mean(), 2))
col3.metric("Avg Monetary (£)", round(filtered_df['MonetaryValue'].mean(), 2))

st.divider()

st.subheader("🍩 Proporsi Customer per Cluster")
cluster_counts = filtered_df['Cluster'].value_counts().sort_index()

fig1, ax1 = plt.subplots(figsize=(6, 6))
ax1.pie(
    cluster_counts.values,
    labels=[f"Cluster {c}" for c in cluster_counts.index],
    autopct='%1.1f%%',
    startangle=120,
    colors=cluster_palette,
    wedgeprops={'edgecolor': 'white'}
)

centre_circle = plt.Circle((0, 0), 0.65, fc='white')
ax1.add_artist(centre_circle)
ax1.set_title("Distribusi Customer per Cluster", fontsize=13, fontweight='bold')
st.pyplot(fig1)

st.divider()

st.subheader("🎯 Sebaran Customer (Recency vs Monetary)")
fig2, ax2 = plt.subplots(figsize=(8, 5))

sns.scatterplot(
    data=filtered_df,
    x='Recency',
    y='MonetaryValue',
    hue='Cluster',
    palette=cluster_palette,
    alpha=0.75,
    s=60,
    ax=ax2
)

ax2.set_xlabel("Recency (days)")
ax2.set_ylabel("Monetary Value (£)")
ax2.set_title("Customer Segmentation (Recency vs Monetary)")
ax2.legend(title="Cluster")
st.pyplot(fig2)

st.divider()

st.subheader("🎻 Distribusi RFM per Cluster")
fig3, ax3 = plt.subplots(1, 3, figsize=(16, 4))

sns.violinplot(data=filtered_df, x='Cluster', y='Recency',
               palette=cluster_palette, inner='quartile', ax=ax3[0])
ax3[0].set_title("Recency")

sns.violinplot(data=filtered_df, x='Cluster', y='Frequency',
               palette=cluster_palette, inner='quartile', ax=ax3[1])
ax3[1].set_title("Frequency")

sns.violinplot(data=filtered_df, x='Cluster', y='MonetaryValue',
               palette=cluster_palette, inner='quartile', ax=ax3[2])
ax3[2].set_title("Monetary Value")

st.pyplot(fig3)

st.divider()

st.subheader("🧠 Penjelasan & Insight Cluster RFM")

with st.expander("🔵 Cluster 0 – Lowest Customers"):
    st.markdown("""
**Karakteristik:**  
- Nilai belanja rendah  
- Frekuensi pembelian rendah  
- Sudah lama tidak bertransaksi  

**Aksi:**  
- Kampanye re-engagement  
- Diskon agresif  
- Survei penyebab churn  
""")

with st.expander("🟠 Cluster 1 – Best Customers"):
    st.markdown("""
**Karakteristik:**  
- Nilai belanja tertinggi  
- Frekuensi pembelian tinggi  

**Aksi:**  
- VIP treatment  
- Reward eksklusif  
- Referral program  
""")

with st.expander("🟢 Cluster 2 – Potential Customers"):
    st.markdown("""
**Karakteristik:**  
- Pelanggan baru  
- Potensi berkembang  

**Aksi:**  
- Welcome voucher  
- Edukasi produk  
""")

with st.expander("🟣 Cluster 3 – Active Customers"):
    st.markdown("""
**Karakteristik:**  
- Aktif bertransaksi  
- Nilai menengah  

**Aksi:**  
- Loyalty program  
- Promo eksklusif  
""")

st.subheader("📄 Data Customer (Sample)")
st.dataframe(filtered_df.head(50), use_container_width=True)
