# Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sidebar Information
st.sidebar.title("Proyek Analisis Data: E-Commerce Public Dataset")
st.sidebar.write('''
    **Nama:** Nurul Fadillah  
    **Email:** nurulfadillah1521@gmail.com  
    **ID Dicoding:** nrifdiih
''')
st.sidebar.caption("Copyright © Nurul Fadillah 2024")

# Judul dan Deskripsi Dashboard
st.title('Dashboard Analisis Data E-Commerce')
st.write('''Dashboard ini memberikan insight tentang produk paling laku, produk dengan penjualan terendah, serta analisis demografi pelanggan.''')

# Load data
customers_df = pd.read_csv("data/customers_dataset.csv")
products_df = pd.read_csv("data/products_dataset.csv")
order_items_df = pd.read_csv("data/order_items_dataset.csv")
product_category_name_translation_df = pd.read_csv("data/product_category_name_translation.csv")

# Gabungkan data yang diperlukan
productes_orderitems_df = pd.merge(
    left=order_items_df,
    right=products_df,
    how="left",
    left_on="product_id",
    right_on="product_id"
)

# Gabungkan dengan data kategori produk
productes_orderitems_translated_df = pd.merge(
    left=productes_orderitems_df,
    right=product_category_name_translation_df,
    how="left",
    left_on="product_category_name",
    right_on="product_category_name"
)

# 1. Visualisasi Produk Terlaris dan Paling Tidak Laris
st.subheader('Analisis Produk')
st.write("Visualisasi berikut menunjukkan kategori produk yang paling banyak dan paling sedikit terjual.")

top_5_products = productes_orderitems_translated_df['product_category_name_english'].value_counts().nlargest(5)
least_5_products = productes_orderitems_translated_df['product_category_name_english'].value_counts().nsmallest(5)

col1, col2 = st.columns(2)

with col1:
    st.write("**Top 5 Produk Terlaris**")
    fig, ax = plt.subplots()
    top_5_products.plot(kind='bar', color='skyblue', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.write("**Top 5 Produk Paling Tidak Laris**")
    fig, ax = plt.subplots()
    least_5_products.plot(kind='bar', color='lightcoral', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 2. Analisis Demografi Pelanggan
st.subheader('Analisis Demografi Pelanggan')
st.write("Di sini kita bisa melihat distribusi pelanggan berdasarkan kota dan negara bagian.")

top_5_cities = customers_df['customer_city'].value_counts().head(5)
top_5_states = customers_df['customer_state'].value_counts().head(5)

col3, col4 = st.columns(2)

with col3:
    st.write("**Top 5 Kota Pelanggan Terbanyak**")
    fig, ax = plt.subplots()
    top_5_cities.plot(kind='bar', color='lightgreen', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col4:
    st.write("**Top 5 Negara Bagian Pelanggan Terbanyak**")
    fig, ax = plt.subplots()
    top_5_states.plot(kind='bar', color='lightblue', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Penutup
st.write('''Dengan dashboard ini, kita dapat memahami produk mana yang memiliki performa penjualan terbaik, dan demografi pelanggan yang paling dominan, 
sehingga strategi pemasaran bisa lebih terarah.''')
