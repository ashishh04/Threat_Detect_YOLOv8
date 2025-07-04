import streamlit as st
import pandas as pd
import mysql.connector
from PIL import Image
import os

# ------------------ DB CONNECTION ------------------

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="object_detection"
)
cursor = db.cursor()

# ------------------ LOAD DATA ------------------

query = """
SELECT timestamp, object_type, confidence, image_path
FROM threat_log
ORDER BY timestamp DESC
"""
cursor.execute(query)
data = cursor.fetchall()

df = pd.DataFrame(data, columns=["Timestamp", "Class", "Confidence", "Image Path"])

# ------------------ CLASS FILTER ------------------

st.title("🚨 Real-Time Threat Detection Dashboard")
object_filter = st.multiselect(
    "🔍 Filter by Detected Object:",
    options=df["Class"].unique(),
    default=df["Class"].unique()
)

filtered_df = df[df["Class"].isin(object_filter)]

# ------------------ SORTING ------------------

sort_by = st.radio("Sort by:", options=["Newest", "Highest Confidence"])

if sort_by == "Highest Confidence":
    filtered_df = filtered_df.sort_values(by="Confidence", ascending=False)
else:
    filtered_df = filtered_df.sort_values(by="Timestamp", ascending=False)

# ------------------ SUMMARY STATS ------------------

st.subheader("📊 Detection Summary")
st.markdown(f"**Total Detections:** {len(filtered_df)}")

# Bar chart of class counts
st.bar_chart(filtered_df["Class"].value_counts())

# Average confidence per class
st.markdown("**Average Confidence per Class:**")
avg_conf = filtered_df.groupby("Class")["Confidence"].mean().round(2).reset_index()
st.dataframe(avg_conf, use_container_width=True)

# ------------------ DETECTION IMAGES ------------------

st.subheader("🖼️ Detection Snapshots")
for _, row in filtered_df.iterrows():
    if os.path.exists(row["Image Path"]):
        st.image(row["Image Path"], caption=f"{row['Class']} | Confidence: {row['Confidence']:.2f}", use_column_width=True)
    else:
        st.warning(f"Image not found: {row['Image Path']}")
