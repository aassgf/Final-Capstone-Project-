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
st.caption("Dashboard segmentasi customer berbasis Recency, Frequency, dan Monetary")

# ============================
# LOAD DATA
# ============================
@st.cache_data
def load_data():
    return pd.read_csv("rfm_segmentasi_final.csv")

df = load_data()

# ============================
# WARNA CLUSTER
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
st.sidebar.header("🔎 Filter Global")

selected_clusters = st.sidebar.multiselect(
    "Pilih Cluster",
    options=sorted(df['Cluster'].unique()),
    default=sorted(df['Cluster'].unique())
)

filtered_df = df[df['Cluster'].isin(selected_clusters)]

# ============================
# METRIC GLOBAL
# ============================
c1, c2, c3 = st.columns(3)
c1.metric("Total Customer", f"{len(filtered_df):,}")
c2.metric("Avg Frequency", round(filtered_df['Frequency'].mean(), 2))
c3.metric("Avg Monetary (£)", round(filtered_df['MonetaryValue'].mean(), 2))

st.divider()

# ============================
# TABS
# ============================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Dataset",
    "📊 Jumlah Cluster",
    "🎯 Sebaran Customer",
    "🎻 Distribusi RFM",
    "🧠 Insight Cluster"
])

# =========================================================
# TAB 1 — DATASET
# =========================================================
with tab1:
    st.subheader("📄 Dataset Customer")
    st.dataframe(filtered_df, use_container_width=True)

    st.download_button(
        "⬇️ Download CSV",
        filtered_df.to_csv(index=False),
        "rfm_filtered.csv",
        "text/csv"
    )

# =========================================================
# TAB 2 — JUMLAH CLUSTER
# =========================================================
with tab2:
    st.subheader("📊 Jumlah Customer per Cluster")

    cluster_counts = filtered_df['Cluster'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(
        cluster_counts.index.astype(str),
        cluster_counts.values,
        color=[cluster_colors[c] for c in cluster_counts.index]
    )

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{int(bar.get_height())}",
            ha='center',
            va='bottom'
        )

    ax.set_xlabel("Cluster")
    ax.set_ylabel("Jumlah Customer")
    ax.set_title("Jumlah Customer per Cluster")

    st.pyplot(fig)

    st.info(
        "Cluster dengan jumlah customer terbesar merupakan segmen dominan "
        "yang memerlukan perhatian khusus dalam strategi pemasaran."
    )

# =========================================================
# TAB 3 — SEBARAN CUSTOMER
# =========================================================
with tab3:
    st.subheader("🎯 Sebaran Customer (Recency vs Monetary)")

    fig, ax = plt.subplots(figsize=(8, 5))
    for c in cluster_colors:
        subset = filtered_df[filtered_df['Cluster'] == c]
        ax.scatter(
            subset['Recency'],
            subset['MonetaryValue'],
            label=f"Cluster {c}",
            color=cluster_colors[c],
            alpha=0.7,
            s=60
        )

    ax.set_xlabel("Recency (days)")
    ax.set_ylabel("Monetary Value (£)")
    ax.set_title("Customer Segmentation Scatter")
    ax.legend()

    st.pyplot(fig)

    st.success(
        "Customer dengan Recency rendah dan Monetary tinggi "
        "merupakan pelanggan bernilai tinggi."
    )

# =========================================================
# TAB 4 — DISTRIBUSI RFM
# =========================================================
with tab4:
    st.subheader("🎻 Distribusi RFM per Cluster")

    fig, ax = plt.subplots(1, 3, figsize=(16, 4))

    sns.violinplot(
        data=filtered_df,
        x='Cluster', y='Recency',
        hue='Cluster',
        palette=cluster_colors,
        legend=False,
        ax=ax[0]
    )
    ax[0].set_title("Recency")

    sns.violinplot(
        data=filtered_df,
        x='Cluster', y='Frequency',
        hue='Cluster',
        palette=cluster_colors,
        legend=False,
        ax=ax[1]
    )
    ax[1].set_title("Frequency")

    sns.violinplot(
        data=filtered_df,
        x='Cluster', y='MonetaryValue',
        hue='Cluster',
        palette=cluster_colors,
        legend=False,
        ax=ax[2]
    )
    ax[2].set_title("Monetary Value")

    st.pyplot(fig)

# =========================================================
# TAB 5 — INSIGHT CLUSTER
# =========================================================
with tab5:
    st.subheader("🧠 Penjelasan & Strategi Cluster RFM")

    st.markdown("""
### 📌 Ringkasan Cluster
- **🔵 Cluster 0 (Biru) – Best Customers**  
  Berikan reward untuk pelanggan paling loyal  

- **🟠 Cluster 1 (Oranye) – Lowest Customers**  
  Aktifkan kembali pelanggan yang kurang aktif  

- **🟢 Cluster 2 (Hijau) – Potential Customers**  
  Kembangkan pelanggan baru atau berpotensi  

- **🔴 Cluster 3 (Merah) – Active Customers**  
  Pertahankan pelanggan aktif dan bernilai tinggi  
    """)

    st.divider()

    # =======================
    # CLUSTER 0 – BEST
    # =======================
    with st.expander("🔵 Cluster 0 – Best Customers"):
        st.markdown("""
**Penjelasan:**  
Cluster ini merupakan pelanggan dengan **nilai belanja tertinggi**, **frekuensi pembelian tinggi**,  
dan **aktivitas transaksi terbaru**. Mereka adalah kontributor terbesar terhadap pendapatan  
dan merupakan aset paling bernilai bagi bisnis.

**Aksi yang Disarankan:**  
1. VIP treatment (akses awal produk baru, customer service prioritas)  
2. Hadiah eksklusif, bonus poin, atau cashback premium  
3. Program referral karena mereka cenderung merekomendasikan brand  
4. Komunikasi yang sangat personal untuk menjaga loyalitas  
        """)

    # =======================
    # CLUSTER 1 – LOWEST
    # =======================
    with st.expander("🟠 Cluster 1 – Lowest Customers"):
        st.markdown("""
**Penjelasan:**  
Cluster ini berisi pelanggan dengan **nilai belanja rendah**, **jarang membeli**,  
dan **sudah lama tidak melakukan transaksi**. Mereka memiliki risiko churn yang tinggi  
dan membutuhkan strategi khusus untuk membangkitkan kembali minat mereka.

**Aksi yang Disarankan:**  
1. Kampanye *re-engagement* (email, WhatsApp, notifikasi)  
2. Promo agresif seperti diskon besar atau gratis ongkir  
3. Rekomendasi produk berdasarkan pembelian terakhir  
4. Survei singkat untuk mengetahui alasan pelanggan tidak kembali  
        """)

    # =======================
    # CLUSTER 2 – POTENTIAL
    # =======================
    with st.expander("🟢 Cluster 2 – Potential Customers"):
        st.markdown("""
**Penjelasan:**  
Cluster ini terdiri dari pelanggan baru atau pelanggan dengan **nilai belanja masih kecil**,  
namun menunjukkan **aktivitas transaksi terbaru**. Mereka memiliki potensi besar  
untuk berkembang menjadi pelanggan loyal jika diarahkan dengan tepat.

**Aksi yang Disarankan:**  
1. Welcome voucher atau diskon pembelian kedua  
2. Edukasi produk dan rekomendasi awal  
3. Upselling ringan untuk meningkatkan nilai belanja  
4. Follow-up pasca pembelian untuk membangun engagement sejak awal  
        """)

    # =======================
    # CLUSTER 3 – ACTIVE
    # =======================
    with st.expander("🔴 Cluster 3 – Active Customers"):
        st.markdown("""
**Penjelasan:**  
Cluster ini berisi pelanggan yang **cukup sering berbelanja**, memiliki **nilai belanja menengah**,  
dan masih **aktif bertransaksi**. Mereka merupakan pelanggan inti yang dapat dipacu  
menjadi pelanggan loyal dengan kontribusi pendapatan yang lebih besar.

**Aksi yang Disarankan:**  
1. Program loyalitas bertingkat (misal: Silver → Gold)  
2. Promo eksklusif atau bundling produk  
3. Personalisasi rekomendasi berdasarkan preferensi pelanggan  
4. Penawaran rutin agar pelanggan tetap aktif dan engaged  
        """)

    st.info(
        "💡 Insight Utama: Segmentasi RFM membantu bisnis memahami perilaku pelanggan "
        "dan menyusun strategi pemasaran yang lebih tepat sasaran untuk setiap segmen."
    )
