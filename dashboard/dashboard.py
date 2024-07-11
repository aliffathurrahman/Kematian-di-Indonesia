import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    data = pd.read_csv('Penyebab Kematian di Indonesia yang Dilaporkan - Clean.csv')
    return data

# Memuat data
data = load_data()

# Sidebar untuk navigasi
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Death Data"])

if app_mode == "Home":
    st.title("Home")
    st.write("""
    Selamat datang di web Analisis Data Kematian di Indonesia. 
    Situs ini dirancang untuk menyediakan informasi dan analisis mendalam mengenai data kematian di Indonesia pada tahun 2000-2022, mencakup berbagai faktor penyebab kematian, distribusi demografis, serta tren dan pola yang muncul dari data tersebut. 
    Dengan memanfaatkan teknologi analisis data terkini, kami berusaha memberikan gambaran yang jelas dan akurat tentang situasi kesehatan masyarakat di Indonesia. Melalui platform ini, kami berharap dapat mendukung upaya peningkatan kesehatan dan kebijakan publik yang lebih baik berdasarkan data yang valid dan terpercaya. 
    Terima kasih telah mengunjungi web Analisis Data Kematian di Indonesia. 
    Kami berharap situs ini dapat menjadi sumber informasi yang berharga dan alat yang efektif dalam upaya meningkatkan kualitas hidup masyarakat Indonesia. """)

elif app_mode == "About":
    st.title("About")
    st.write("""
    Aplikasi ini dibuat untuk menganalisis data kematian di Indonesia pada tahun 2000-2022 berdasarkan berbagai penyebab kematian. 
    Dengan menggunakan web ini, pengguna dapat memperoleh wawasan mendalam mengenai penyebab kematian yang paling umum dan distribusinya di berbagai wilayah di Indonesia. 
    Web ini dirancang untuk memudahkan analisis data melalui visualisasi data interaktif dan kemampuan untuk menyaring data berdasarkan kategori berdasarkan tahunnya. 
    Selain itu, web ini juga membuat kebijakan untuk mengidentifikasi tren dan pola dalam data kematian, sehingga dapat mendukung pengambilan keputusan yang lebih baik dalam upaya meningkatkan kesehatan masyarakat. 
    Dengan demikian, aplikasi ini berperan penting dalam membantu memahami dan menangani isu-isu kesehatan yang mempengaruhi penduduk Indonesia.
    """)

elif app_mode == "Death Data":
    st.title("Analisis Data Kematian di Indonesia")

    # Pilihan tahun
    years = sorted(data['Year'].unique())
    selected_year = st.selectbox('Pilih Tahun:', years)

    # Tampilkan data berdasarkan tahun yang dipilih
    st.subheader(f'Data Kematian di Tahun {selected_year}')
    data_by_year = data[data['Year'] == selected_year]
    st.write(data_by_year)

    # Analisis Data
    st.subheader('Jumlah Kematian Berdasarkan Penyebab')
    grouped_cases_df = data_by_year.groupby('Cause')['Total Deaths'].sum()
    st.write(grouped_cases_df)

    st.subheader('Penyebab Kematian Terbanyak')
    cause_sort_data = grouped_cases_df.sort_values(ascending=False)
    st.write(cause_sort_data)

    # Pilihan untuk melihat grafik
    st.subheader('Pilih Grafik untuk Dilihat')
    chart_type = st.radio(
        "Pilih jenis tren kematian yang ingin Anda lihat:",
        (
            'COVID-19', 'Penyakit Sistem Sirkulasi Darah', 'Penyakit Infeksi & Parasit Tertentu', 
            'Kecelakaan Lalu Lintas', 'Gempa Bumi', 'Tsunami', 'AIDS',  
            'Letusan Gunung Api', 'Kekeringan', 'Tanah Longsor'
        )
    )

    def plot_trend(data, cause, title, xticks):
        filtered_data = data[data['Cause'] == cause]
        if filtered_data.empty:
            st.write(f'Tidak ada data untuk {cause}')
            return
        fig, ax = plt.subplots()
        ax.plot(filtered_data['Year'], filtered_data['Total Deaths'], marker='o')
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, rotation=45, ha='right')
        ax.set_title(title)
        ax.set_xlabel('Year')
        ax.set_ylabel('Total Deaths')
        plt.tight_layout()  # Menambahkan ini untuk memastikan label tidak terpotong
        st.pyplot(fig)

    # Plotting logic for each cause
    causes_xticks = {
        'COVID-19': [2020, 2021, 2022],
        'Penyakit Sistem Sirkulasi Darah': [2005, 2006, 2007, 2008],
        'Penyakit Infeksi & Parasit Tertentu': [2005, 2006, 2007, 2008],
        'Kecelakaan Lalu Lintas': [2004, 2005, 2009, 2010],
        'Gempa Bumi': [2004, 2005, 2012, 2020],
        'Tsunami': [2004, 2005, 2012, 2020],
        'AIDS': [2004, 2005, 2012, 2020],
        'Letusan Gunung Api': [2005, 2006, 2010, 2015],
        'Kekeringan': [2018, 2019, 2020, 2021, 2022],
        'Tanah Longsor': [2005, 2006, 2007, 2008, 2010, 2015]
    }

    plot_trend(data, chart_type, f'Tren Kematian {chart_type}', causes_xticks.get(chart_type, []))
