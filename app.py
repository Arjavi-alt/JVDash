import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load data
df = pd.read_excel("Sustainable_Fashion_Raw_800.xlsx", sheet_name="Raw_Data")


st.set_page_config(page_title="Sustainable FashionInsights", layout="wide")

st.title("🌿 Sustainable Fashion HR Dashboard")
st.markdown("This dashboard provides micro and macro-level HR insights for stakeholders using behavioral and transactional data from a sustainable fashion business.")

# Sidebar filters
st.sidebar.header("🔎 Filter Data")
gender_filter = st.sidebar.multiselect("Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
region_filter = st.sidebar.multiselect("Region", options=df["Region"].unique(), default=df["Region"].unique())
product_filter = st.sidebar.multiselect("Product Category", options=df["Product_Category"].unique(), default=df["Product_Category"].unique())
platform_filter = st.sidebar.multiselect("Social Media Platform", options=df["Social_Media_Platform"].unique(), default=df["Social_Media_Platform"].unique())

filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Region"].isin(region_filter)) &
    (df["Product_Category"].isin(product_filter)) &
    (df["Social_Media_Platform"].isin(platform_filter))
]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Macro Insights", "🎯 Conversion Analysis", "📈 Engagement Analysis", "💸 Purchase Behavior"])

# ---------- TAB 1 ----------
with tab1:
    st.subheader("Customer Demographics Overview")
    st.markdown("Get a quick snapshot of who your customers are based on region, gender, and product interests.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🎨 Gender Distribution")
        gender_count = filtered_df["Gender"].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(gender_count, labels=gender_count.index, autopct='%1.1f%%', startangle=90)
        st.pyplot(fig1)

    with col2:
        st.markdown("#### 🌍 Regional Spread")
        region_bar = filtered_df["Region"].value_counts().reset_index()
        fig2 = px.bar(region_bar, x='index', y='Region', labels={'index':'Region', 'Region':'Count'}, color='index')
        st.plotly_chart(fig2)

    st.markdown("#### 🧵 Product Preference by Region")
    fig3 = px.histogram(filtered_df, x="Product_Category", color="Region", barmode="group")
    st.plotly_chart(fig3)

    st.markdown("#### 🥇 Membership Distribution")
    fig4 = px.pie(filtered_df, names="Membership_Status", title="Membership Breakdown")
    st.plotly_chart(fig4)

# ---------- TAB 2 ----------
with tab2:
    st.subheader("Conversion Analysis")
    st.markdown("Understand how likely a user is to buy and what influences conversion behavior.")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 🎯 Likelihood vs Actual Purchase")
        fig5 = px.box(filtered_df, x="Actual_Purchase", y="Purchase_Likelihood", color="Actual_Purchase")
        st.plotly_chart(fig5)

    with col4:
        st.markdown("#### 🧠 Influence of Environmental Score on Purchase")
        fig6 = px.scatter(filtered_df, x="Environmental_Score", y="Purchase_Likelihood", color="Actual_Purchase", trendline="ols")
        st.plotly_chart(fig6)

    st.markdown("#### 📈 Promo Code Impact on Purchase")
    fig7 = px.histogram(filtered_df, x="Promo_Code_Used", color="Actual_Purchase", barmode="group")
    st.plotly_chart(fig7)

    st.markdown("#### 🤝 Referral Influence on Purchase")
    fig8 = px.histogram(filtered_df, x="Referral_Used", color="Actual_Purchase", barmode="group")
    st.plotly_chart(fig8)

# ---------- TAB 3 ----------
with tab3:
    st.subheader("Engagement Insights")
    st.markdown("Track how different users engage based on platform and campaign metrics.")

    st.markdown("#### 📱 Ad Engagement by Platform")
    fig9 = px.box(filtered_df, x="Social_Media_Platform", y="Ad_Engagement", color="Social_Media_Platform")
    st.plotly_chart(fig9)

    st.markdown("#### 📊 Engagement vs Purchase Likelihood")
    fig10 = px.scatter(filtered_df, x="Ad_Engagement", y="Purchase_Likelihood", color="Product_Category", trendline="ols")
    st.plotly_chart(fig10)

    st.markdown("#### 🎥 Platform Preferences by Gender")
    fig11 = px.histogram(filtered_df, x="Social_Media_Platform", color="Gender", barmode="group")
    st.plotly_chart(fig11)

# ---------- TAB 4 ----------
with tab4:
    st.subheader("Purchase Behavior & Revenue Insights")
    st.markdown("Get insights into how customers spend and how fast they convert.")

    st.markdown("#### 💵 Average Order Value by Gender")
    fig12 = px.violin(filtered_df, x="Gender", y="Avg_Order_Value", box=True)
    st.plotly_chart(fig12)

    st.markdown("#### ⏱ Days to Purchase Distribution")
    fig13 = px.histogram(filtered_df, x="Days_to_Purchase", nbins=20)
    st.plotly_chart(fig13)

    st.markdown("#### 💸 Revenue Heatmap by Region & Category")
    pivot_data = filtered_df.pivot_table(values="Avg_Order_Value", index="Region", columns="Product_Category", aggfunc="mean")
    fig14, ax14 = plt.subplots()
    sns.heatmap(pivot_data, annot=True, cmap="YlGnBu", fmt=".0f", ax=ax14)
    st.pyplot(fig14)

    st.markdown("#### 📦 Total Orders by Membership")
    fig15 = px.histogram(filtered_df[filtered_df["Actual_Purchase"]==1], x="Membership_Status", color="Product_Category", barmode="group")
    st.plotly_chart(fig15)

# Footer
st.markdown("---")
st.markdown("👩‍💻 Built by Arjavi | MBA | Powered by Streamlit + Plotly + Pandas")
