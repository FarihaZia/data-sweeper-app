import streamlit as st
import pandas as pd
import os
from io import BytesIO
  
st.set_page_config(page_title="Data Sweeper", page_icon=":shark:", layout="wide")

#custom css
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Data Sweeper Sterling Integrator")
st.write("This app is designed to help you clean up your Sterling Integrator data. You can upload a CSV file and select the columns you want to keep. The app will then generate a new CSV file with only the selected columns.")

# Upload CSV file
uploaded_files = st.file_uploader("Upload a files(accepts CSV or Excel):", type=["cvs", "xlsx"] , accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"File type not supported: {file_ext}")
            continue

        #file details
        st.write("Preview the head of dataframe")
        st.dataframe(df.head())

        #data cleaning option
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
          col1 , col2 = st.columns(2)

          with col1:
              if st.button(f"Remove Duplicates from the files : {file.name}"):
                  numeric_cols = df.select_dtypes(include=['number']).columns
                  df[numeric_cols] = df[numeric_cols].filna(df[numeric_cols])
                  st.write("✅Missing values have been filled ")

        st.subheader("🎯 Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for, {file.name}", df.columns, default=df.columns)         
        df = df[columns]

        #data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
            
        #Conversion options

        st.subheader(" Conversion Options")
        conversion_type = st.radio(f"Convert{file.name} to", ["CSV", "Excel"], key=file.name)
        if st.button(f"Conver {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Click here to download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉All files processed successfully!")
 