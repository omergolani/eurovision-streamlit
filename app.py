import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Eurovision Data Explorer", layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('eurovision.csv')  # Replace with your file path or upload logic

df = load_data()

st.title("🎤 Eurovision Data Explorer")
st.markdown("Explore trends, styles, scores, and more across years of Eurovision entries.")

# Sidebar filters
years = sorted(df['year'].dropna().unique())
styles = df['style'].dropna().unique()

selected_years = st.sidebar.multiselect("Select Years", years, default=years)
selected_styles = st.sidebar.multiselect("Select Styles", styles, default=list(styles))

filtered_df = df[df['year'].isin(selected_years) & df['style'].isin(selected_styles)]

# Display table
st.subheader("Filtered Eurovision Entries")
st.dataframe(filtered_df)

# Plot 1: Final Points by Style
st.subheader("Average Final Points by Style")
fig1, ax1 = plt.subplots()
style_avg = filtered_df.groupby('style')['final_total_points'].mean().sort_values(ascending=False)
sns.barplot(x=style_avg.index, y=style_avg.values, ax=ax1, palette='Purples')
plt.xticks(rotation=45)
st.pyplot(fig1)

# Plot 2: Jury vs. Televote
st.subheader("Jury vs. Televote Points")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=filtered_df, x='final_jury_points', y='final_televote_points', hue='style', ax=ax2, palette='pink')
st.pyplot(fig2)

