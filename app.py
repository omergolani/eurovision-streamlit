import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Eurovision Explorer Pro", layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("song_data.csv", encoding="latin1")

df = load_data()

st.title("🎤 Eurovision Data Explorer Pro")
st.markdown("A deeper, interactive analysis of Eurovision entries — trends, styles, scores, and more.")

# Sidebar filters
years = sorted(df["year"].dropna().unique())
styles = df["style"].dropna().unique()
countries = df["country"].dropna().unique()

selected_years = st.sidebar.multiselect("Select Years", years, default=years)
selected_styles = st.sidebar.multiselect("Select Styles", styles, default=list(styles))
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=list(countries))

filtered_df = df[
    df["year"].isin(selected_years) &
    df["style"].isin(selected_styles) &
    df["country"].isin(selected_countries)
]

# Show filtered data
st.subheader("🎼 Filtered Eurovision Entries")
st.dataframe(filtered_df)

# Distribution: Final Points
st.subheader("🎯 Distribution of Final Total Points")
sns.set_palette("pastel")
fig1 = sns.displot(data=filtered_df, x="final_total_points", kind="hist", bins=20, kde=True, color="#F9A8D4", height=5, aspect=2)
st.pyplot(fig1.figure)

# Count of Songs by Style
st.subheader("🎵 Count of Songs by Style")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.countplot(data=filtered_df, x="style", order=filtered_df["style"].value_counts().index, palette="Purples", ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)

# Top 10 Countries by Entries
st.subheader("🌍 Top 10 Countries by Number of Entries")
fig3, ax3 = plt.subplots(figsize=(10, 5))
top_countries = filtered_df["country"].value_counts().head(10)
sns.barplot(x=top_countries.index, y=top_countries.values, palette="pink", ax=ax3)
plt.xticks(rotation=45)
st.pyplot(fig3)

# Boxplot: Final Points by Style
st.subheader("🎭 Final Total Points by Musical Style")
fig4, ax4 = plt.subplots(figsize=(12, 5))
sns.boxplot(data=filtered_df, x="style", y="final_total_points", palette="Purples", ax=ax4)
plt.xticks(rotation=45)
st.pyplot(fig4)

# Relplot: Jury vs Televote
st.subheader("🎙️ Jury vs. Televote Points by Style")
fig5 = sns.relplot(data=filtered_df, x="final_jury_points", y="final_televote_points", hue="style", kind="scatter", palette="pastel", height=5, aspect=2)
st.pyplot(fig5.figure)

# Pointplot: Avg Final Points by Language
st.subheader("🗣️ Avg Final Points by Language (Top 5)")
top_languages = df["language"].value_counts().head(5).index
lang_df = df[df["language"].isin(top_languages)]
fig6, ax6 = plt.subplots(figsize=(10, 5))
sns.pointplot(data=lang_df, x="language", y="final_total_points", palette="Purples", ax=ax6)
st.pyplot(fig6)

# Bar: Compare Jury vs. Televote Avg
st.subheader("🆚 Average Jury vs. Televote Points")
fig7, ax7 = plt.subplots()
comparison_df = df[["final_jury_points", "final_televote_points"]].dropna()
comparison_df.mean().plot(kind="bar", color=["#D8B4F8", "#F9A8D4"], ax=ax7)
plt.ylabel("Average Points")
st.pyplot(fig7)

# Trend: Avg Final Points by Year
st.subheader("📈 Average Final Points by Year")
fig8, ax8 = plt.subplots()
yearly_avg = df.groupby("year")["final_total_points"].mean()
sns.lineplot(x=yearly_avg.index, y=yearly_avg.values, marker="o", color="#C084FC", ax=ax8)
plt.ylabel("Average Final Points")
st.pyplot(fig8)

# Style Trends Over Years
st.subheader("📊 Style Trends Over the Years (Top 4 Styles)")
top_styles = df["style"].value_counts().head(4).index
filtered = df[df["style"].isin(top_styles)]
fig9, ax9 = plt.subplots(figsize=(12, 5))
sns.countplot(data=filtered, x="year", hue="style", palette="pastel", ax=ax9)
plt.xticks(rotation=45)
st.pyplot(fig9)

st.markdown("---")
st.markdown("Created by **Ghila Coen** & **Omer Golani** 💜")
