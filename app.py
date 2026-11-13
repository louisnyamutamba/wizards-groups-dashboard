# WIZARDS GROUPS - WZD DASHBOARD
# Owner: Louis Nyamutamba
# Email: louisnyamutamba@gmail.com
# Created: Nov 2026

import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Wizards Groups Dashboard", layout="wide")
st.title("WIZARDS GROUPS - DASHBOARD")
st.caption("Laptops + Accessories | Daily Sales + Stock Monitoring | Owner: Louis Nyamutamba | louisnyamutamba@gmail.com")

# Sidebar - 5 Employees
st.sidebar.title("WIZARDS MENU")
st.sidebar.write("Logged in as: Louis Nyamutamba")
menu = st.sidebar.radio("Go to:", ["Home", "Daily Sales", "Stock", "Pendings", "Returns", "Boss Report"])
uploaded = st.sidebar.file_uploader("Upload Daily Sales CSV", type=["csv"])
st.sidebar.caption("CSV: Date,Customer,Phone,Item,Serial,Qty,Price,Paid/Pending,Seller")

if uploaded is None:
    st.info("Upload your Daily Sales CSV to start. Use Wizards Template format.")
    st.markdown("**Demo row:**\n`2026-11-13,HIRWA,078...,HP 840 G8 I5,SN123,1,450000,Paid,Louis`")
    st.stop()

df = pd.read_csv(uploaded)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Amount'] = df['Qty'] * df['Price']

# HOME
if menu == "Home":
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Revenue", f"{df['Amount'].sum():,.0f} RWF")
    c2.metric("Total Sold", f"{df['Qty'].sum():.0f} pcs")
    c3.metric("Paid", f"{df[df['Paid/Pending']=='Paid']['Amount'].sum():,.0f} RWF")
    c4.metric("Pending Money", f"{df[df['Paid/Pending']=='Pending']['Amount'].sum():,.0f} RWF")
    st.subheader("Revenue by Item - Best Sellers")
    st.bar_chart(df.groupby('Item')['Amount'].sum().sort_values(ascending=False))
    st.subheader("Sales by Seller - Employee Performance")
    st.bar_chart(df.groupby('Seller')['Amount'].sum())

# DAILY SALES
elif menu == "Daily Sales":
    st.subheader("Daily Sales - All Records")
    st.dataframe(df)
    st.subheader("Sales by Day")
    st.line_chart(df.groupby('Date')['Amount'].sum())

# STOCK
elif menu == "Stock":
    stock = df.groupby('Item').agg(Sold=('Qty','sum'), Revenue=('Amount','sum')).sort_values('Sold', ascending=False)
    stock['Alert'] = stock['Sold'].apply(lambda x: "🔴 Fast Selling - Reorder" if x>=10 else "🟢 OK")
    st.dataframe(stock)
    st.warning("Check physical count: Opening - Sold + New = Closing. If not match, find it same night.")

# PENDINGS
elif menu == "Pendings":
    p = df[df['Paid/Pending']=='Pending']
    st.subheader(f"Pendings: {len(p)} orders - {p['Amount'].sum():,.0f} RWF to collect")
    st.dataframe(p[['Date','Customer','Phone','Item','Qty','Amount','Seller']])
    if len(p)>0:
        st.error(f"Follow up urgently: {p.iloc[0]['Customer']} - {p.iloc[0]['Item']} - {p.iloc[0]['Phone']}")

# RETURNS
elif menu == "Returns":
    st.subheader("Returns Log")
    st.info("Add returns in your sheet: Date, Customer, Item, Reason, Approved By")
    st.write("Example from Week 28: HIRWA - 5x HP 840 G8 I5 - Return - Needs check")

# BOSS REPORT + WHATSAPP
elif menu == "Boss Report":
    total = df['Amount'].sum()
    best = df.groupby('Item')['Amount'].sum().idxmax()
    worst = df.groupby('Item')['Amount'].sum().idxmin()
    top_seller = df.groupby('Seller')['Amount'].sum().idxmax()
    best_day = df.groupby('Date')['Amount'].sum().idxmax()
    report = f"""WIZARDS GROUPS - BOSS REPORT
Period: {df['Date'].min().date()} to {df['Date'].max().date()}
Total Revenue: {total:,.0f} RWF
Total Sold: {df['Qty'].sum()} pcs
Best Item: {best}
Worst Item: {worst}
Best Employee: {top_seller}
Best Day: {best_day.date()}
Pending to Collect: {df[df['Paid/Pending']=='Pending']['Amount'].sum():,.0f} RWF
- Prepared by Louis Nyamutamba | louisnyamutamba@gmail.com"""
    st.text(report)
    msg = urllib.parse.quote(report)
    st.link_button("📱 Send on WhatsApp", f"https://wa.me/?text={msg}")