import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sidebar Information
st.sidebar.title("Proyek Analisis Data: E-Commerce Public Dataset")
st.sidebar.write('''
    **Nama:** Nurul Fadillah  
    **Email:** nurulfadillah1521@gmail.com  
    **ID Dicoding:** nrifdiih
''')
st.sidebar.caption("Copyright © Nurul Fadillah 2024")

# Load datasets
q1_df = pd.read_csv('q1_df.csv')
q2_df = pd.read_csv('q2_df.csv')


# Set up Streamlit layout
st.title('Dashboard: Penjualan dan Analisis Produk')

# Visualisasi 1: Histogram penjualan dan line chart harga rata-rata
st.subheader('Jumlah Penjualan dan Fluktuasi Harga - Health & Beauty (Okt 2016 - Okt 2018)')

# Filter data for health_beauty category
health_beauty_df = q1_df[q1_df['product_category_name_english'] == 'health_beauty']

# Convert date column to datetime
health_beauty_df['order_delivered_customer_date'] = pd.to_datetime(health_beauty_df['order_delivered_customer_date'])

# Filter for date range Oct 2016 - Oct 2018
mask = (health_beauty_df['order_delivered_customer_date'] >= '2016-10-01') & (health_beauty_df['order_delivered_customer_date'] <= '2018-10-31')
filtered_df = health_beauty_df[mask]

# Create month-year column
filtered_df['month_year'] = filtered_df['order_delivered_customer_date'].dt.to_period('M')

# Calculate monthly sales and average price
monthly_sales = filtered_df.groupby('month_year').size()
monthly_avg_price = filtered_df.groupby('month_year')['price'].mean()

# Plotting the histogram (sales) and line chart (average price)
fig, ax1 = plt.subplots(figsize=(12, 6))

# Histogram for sales
ax1.bar(monthly_sales.index.astype(str), monthly_sales, color='lightblue', label='Sales')
ax1.set_xlabel('Bulan')
ax1.set_ylabel('Jumlah Penjualan', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Atur label sumbu X agar lebih kecil dan tidak overlap
plt.xticks(rotation=90, fontsize=8)

# Line chart for price
ax2 = ax1.twinx()
ax2.plot(monthly_avg_price.index.astype(str), monthly_avg_price, color='red', label='Average Price', linewidth=2)
ax2.set_ylabel('Rata-rata Harga', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Add title and adjust layout
plt.title('Jumlah Penjualan dan Fluktuasi Harga pada Kategori Health & Beauty (Okt 2016 - Okt 2018)')
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()

# Show plot in Streamlit
st.pyplot(fig)

# Visualisasi 2: Double bar chart untuk kota teratas di tahun 2017
st.subheader('Top 2 Kota dengan Jumlah Order dan Produk Paling Banyak Dibeli di Tahun 2017')

# Filter for year 2017
orders_2017 = q2_df[q2_df['year'] == 2017]

# Group by month and city, count orders
grouped_2017 = orders_2017.groupby(['month', 'customer_city']).size().reset_index(name='order_count')

# Find top 2 cities for each month
top_cities_per_month_2017 = (
    grouped_2017.sort_values('order_count', ascending=False)
    .groupby('month')
    .head(2)
)

# Sort by month order
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
top_cities_per_month_2017['month'] = pd.Categorical(top_cities_per_month_2017['month'], categories=month_order, ordered=True)

# Sort by month and order_count
top_cities_per_month_2017 = top_cities_per_month_2017.sort_values(by=['month', 'order_count'], ascending=[True, False])

# Find top products for top cities
top_products_per_city_month = (
    orders_2017.groupby(['month', 'customer_city', 'product_id', 'product_category_name_english'])
    .size()
    .reset_index(name='product_count')
)

# Get top product for each top city
top_products_per_city_month = (
    top_products_per_city_month.sort_values('product_count', ascending=False)
    .groupby(['month', 'customer_city'])
    .head(1)
)

# Merge with top cities
result = top_cities_per_month_2017.merge(top_products_per_city_month, on=['month', 'customer_city'])

# Plotting the double bar chart
plt.figure(figsize=(14, 8))
sns.barplot(data=result, x='month', y='order_count', hue='customer_city', dodge=True)
plt.title('Top 2 Kota dengan Jumlah Order dan Produk Terlaris di Tahun 2017')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Order')
plt.xticks(rotation=45)

# Adding labels for product category
for p in plt.gca().patches:
    order_count = p.get_height()
    if order_count > 0:
        # Get product category name
        category_name = result.loc[result['order_count'] == order_count, 'product_category_name_english'].values[0]
        month_name = result.loc[result['order_count'] == order_count, 'month'].values[0]
        
        # Add vertical label for January
        if month_name == 'January':
            plt.annotate(f'{int(order_count)}\n{category_name}', 
                         (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='bottom', fontsize=8, rotation=90)
        else:
            plt.annotate(f'{int(order_count)}\n{category_name}', 
                         (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='bottom', fontsize=8)

# Adjust layout and legend
plt.legend(title='Kota', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Show plot in Streamlit
st.pyplot(plt)
