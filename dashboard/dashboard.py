import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='white')

df = pd.read_csv('https://raw.githubusercontent.com/luigiifan/bikerent-dashboard/main/dashboard/main_data.csv')
df['dteday'] = pd.to_datetime(df['dteday'])
df['year_month'] = df['dteday'].dt.to_period('M')

weather_labels = {1: "Baik", 2: "Sedang", 3: "Buruk"}
df['weathersit'] = df['weathersit'].map(weather_labels)

# Sidebar
st.sidebar.header("Pilih Rentang Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df['dteday'].max())

# Filter Data
filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

st.title("📊 BIKE RENT DASHBOARD 🚴‍♂️")

total_rentals = filtered_df['cnt'].sum()
average_rentals = filtered_df['cnt'].mean()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Penyewaan Sepeda", value=f"{total_rentals:,.0f} 🚲")
with col2:
    st.metric(label="Rata-rata Penyewaan per Hari", value=f"{average_rentals:,.0f} 👥")

st.subheader("📌 Distribusi Jumlah Sewa Sepeda")
workingday_counts = filtered_df.groupby("workingday")['cnt'].sum()
fig, ax = plt.subplots()
ax.bar(["Hari Kerja", "Akhir Pekan"], [workingday_counts[1], workingday_counts[0]], color=["red", "green"])
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Distribusi Penyewaan Sepeda")
st.pyplot(fig)

st.subheader("💰 Rata-rata Jumlah Sewa Sepeda per-Bulan")
st.dataframe(
    filtered_df.groupby("year_month")['cnt'].mean()
    .reset_index()
    .rename(columns={"year_month": "Bulan", "cnt": "Rata-rata Penyewaan"})
    .style.format({"Rata-rata Penyewaan": "{:.0f}"})
    .set_properties(**{'text-align': 'left'})
)

st.subheader("🌎 Pengaruh Cuaca terhadap Penyewaan Sepeda")
weather_counts = filtered_df.groupby("weathersit")["cnt"].sum().reset_index()
st.markdown(
    f"""
    <div style="background-color: #f4f4f4; padding: 20px; border-radius: 10px;">
        <h4 style="color: #333;">Total Penyewaan Berdasarkan Cuaca:</h4>
        <ul style="list-style-type: none; padding-left: 0;">
            <li><b>☀️ Baik (Cerah) --> </b> {weather_counts[weather_counts['weathersit'] == 'Baik']['cnt'].values[0]:,.0f} sepeda</li>
            <li><b>⛅ Sedang (Berawan) --> </b> {weather_counts[weather_counts['weathersit'] == 'Sedang']['cnt'].values[0]:,.0f} sepeda</li>
            <li><b>🌧️ Buruk (Hujan/Salju) --> </b> {weather_counts[weather_counts['weathersit'] == 'Buruk']['cnt'].values[0]:,.0f} sepeda</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("🎯 Korelasi Suhu dengan Penyewaan Sepeda")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_df, x='atemp', y='cnt', hue='workingday', alpha=0.5, ax=ax, palette={0: "red", 1: "green"})
ax.set_xlabel("Suhu yang Dirasakan")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Korelasi Suhu vs Penyewaan")
ax.legend(labels=["Akhir Pekan", "Hari Kerja"])
st.pyplot(fig)

st.subheader("✨ Tren Penyewaan Sepeda dalam Rentang Bulan yang Dipilih")
monthly_trend = filtered_df.groupby('year_month')['cnt'].mean()
fig, ax = plt.subplots(figsize=(10, 4))
monthly_trend.plot(ax=ax, marker='o', linestyle='-', color='tab:red')
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Tren Penyewaan Sepeda")
plt.xticks(rotation=45)
st.pyplot(fig)

st.markdown("---")
st.markdown("Data berasal dari **Capital Bikeshare System, Washington D.C.** tahun 2011-2012. \nDibuat oleh Luigi Ifan")
