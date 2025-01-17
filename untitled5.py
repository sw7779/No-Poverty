# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13zubvO--nhb9vuxmyMG-JGhTIxDgHAOG
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#  Data
data = pd.read_excel("latest data PDS.xlsx")

# Data Preprocessing
data['is_urban'] = data['is_urban'].astype(int)
data['female'] = data['female'].astype(int)
data['married'] = data['married'].astype(int)
data['employed_last_year'] = data['employed_last_year'].astype(int)

# Sidebar Filters
st.sidebar.title("Filters")
selected_relationship = st.sidebar.multiselect(
    "Select Relationship to Household Head",
    options=data["relationship_to_hh_head"].unique(),
    default=data["relationship_to_hh_head"].unique()
)

selected_employment_category = st.sidebar.multiselect(
    "Select Employment Category",
    options=data["employment_category_last_year"].unique(),
    default=data["employment_category_last_year"].unique()
)

# Filter Data
filtered_data = data[
    (data["relationship_to_hh_head"].isin(selected_relationship)) &
    (data["employment_category_last_year"].isin(selected_employment_category))
]

# Display Key Metrics
st.title("Poverty Insights Dashboard")
st.metric("Average Poverty Probability", f"{filtered_data['poverty_probability'].mean():.2f}")
st.metric("Percentage of Employed Individuals", f"{filtered_data['employed_last_year'].mean() * 100:.2f}%")

# Visualization 1: Bar Chart - Average Poverty Probability by Employment Category
st.subheader("Average Poverty Probability by Employment Category")
employment_avg_poverty = filtered_data.groupby('employment_category_last_year')['poverty_probability'].mean()
fig, ax = plt.subplots(figsize=(8, 6))
employment_avg_poverty.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title("Average Poverty Probability by Employment Category")
ax.set_ylabel("Average Poverty Probability")
ax.set_xlabel("Employment Category")
st.pyplot(fig)

# Visualization 2: Pie Chart - Distribution of Relationship to Household Head
st.subheader("Distribution of Relationship to Household Head")
relationship_distribution = filtered_data['relationship_to_hh_head'].value_counts()
fig, ax = plt.subplots(figsize=(8, 6))
relationship_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"), ax=ax)
ax.set_title("Distribution of Relationship to Household Head")
ax.set_ylabel("")  # Hide y-label for clarity
st.pyplot(fig)

# Visualization 3: Scatter Plot - Age vs Poverty Probability (Urban vs Rural)
st.subheader("Age vs Poverty Probability (Urban vs Rural)")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=filtered_data, x='age', y='poverty_probability', hue='is_urban', palette=['red', 'blue'], alpha=0.7, ax=ax)
ax.set_title("Age vs Poverty Probability (Urban vs Rural)")
ax.set_xlabel("Age")
ax.set_ylabel("Poverty Probability")
ax.legend(title="Is Urban", labels=["Rural", "Urban"])
st.pyplot(fig)
