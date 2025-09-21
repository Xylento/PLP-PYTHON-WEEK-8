import pandas as pd

# Load the dataset
try:
    df = pd.read_csv('metadata.csv')
except FileNotFoundError:
    print("metadata.csv file not found.")
    exit()

print("Dataset dimensions (rows, columns):", df.shape)
print("\nData types and non-null counts:")
print(df.info())

# First few rows
print("\nFirst 5 rows:")
print(df.head())

# Check missing values per column
print("\nMissing values in each column:")
print(df.isnull().sum())

# Statistics for numerical columns
print("\nBasic statistics for numerical columns:")
print(df.describe())

# Inspect columns with many missing values
missing_pct = df.isnull().mean() * 100
print("\nPercentage of missing data in columns:")
print(missing_pct)

# Dropping rows with missing values in critical columns like 'publish_time', 'title'
df_clean = df.dropna(subset=['publish_time', 'title'])

# Convert date column to datetime
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# Extract year for analysis
df_clean['year'] = df_clean['publish_time'].dt.year

# Add new column example: count words in abstract
df_clean['abstract_word_count'] = df_clean['abstract'].fillna('').apply(lambda x: len(x.split()))

print("\nData sample after cleaning:")
print(df_clean[['publish_time', 'year', 'title', 'abstract_word_count']].head())

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Papers by publication year
year_counts = df_clean['year'].value_counts().sort_index()
plt.figure(figsize=(10, 5))
plt.plot(year_counts.index, year_counts.values)
plt.title("Publications Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.show()

# Top journals publishing COVID-19 research
top_journals = df_clean['journal'].value_counts().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_journals.values, y=top_journals.index)
plt.title("Top 10 Publishing Journals")
plt.xlabel("Number of Papers")
plt.ylabel("Journal")
plt.show()

# Frequent words in titles
from collections import Counter
import re

words = ' '.join(df_clean['title'].dropna().tolist()).lower()
words = re.findall(r'\b\w+\b', words)
common_words = Counter(words).most_common(50)

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(common_words))
plt.figure(figsize=(15, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud of Paper Titles")
plt.show()

# Distribution of paper counts by source
source_counts = df_clean['source_x'].value_counts()
plt.figure(figsize=(10, 5))
sns.barplot(x=source_counts.values, y=source_counts.index)
plt.title("Paper Counts by Source")
plt.xlabel("Count")
plt.ylabel("Source")
plt.show()

import streamlit as st

st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research publication metadata")

# Load data once
@st.cache
def load_data():
    return pd.read_csv('metadata.csv')

data = load_data()
data['publish_time'] = pd.to_datetime(data['publish_time'], errors='coerce')
data['year'] = data['publish_time'].dt.year

# Interactive widget
year_range = st.slider("Select Year Range", int(data['year'].min()), int(data['year'].max()), (2020, 2021))

filtered_data = data[(data['year'] >= year_range[0]) & (data['year'] <= year_range[1])]

# Show filtered data
st.write(filtered_data.head())

# Example plot of publications over time within selected range
pub_counts = filtered_data['year'].value_counts().sort_index()
st.bar_chart(pub_counts)
