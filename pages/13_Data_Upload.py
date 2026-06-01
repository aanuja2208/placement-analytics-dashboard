import streamlit as st
import pandas as pd
import os
from src.data_loader import DATA_PATH, validate_data

st.set_page_config(page_title="Data Management", layout="wide")

st.title("Data Management")
st.markdown("Upload new placement data to update the system.")
st.markdown('''
Upload new placement data to extend or replace the current dataset. The system validates required columns
(student_id, graduation_year, branch, cgpa, outcome) before accepting the file.

- **Replace**: Overwrites the existing dataset entirely with the uploaded file
- **Append**: Adds new records to the existing dataset, useful for adding new graduation years

After uploading, all dashboard pages will automatically reflect the updated data.
''')

uploaded_file = st.file_uploader("Upload Placement Data (CSV)", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        valid, missing = validate_data(df)
        
        if valid:
            st.success("File validation passed!")
            st.dataframe(df.head())
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Replace Existing Data"):
                    df.to_csv(DATA_PATH, index=False)
                    st.success("Data replaced successfully! Clear cache to reflect changes.")
                    st.cache_data.clear()
            with col2:
                if st.button("Append to Existing Data"):
                    if os.path.exists(DATA_PATH):
                        existing_df = pd.read_csv(DATA_PATH)
                        combined_df = pd.concat([existing_df, df], ignore_index=True)
                        combined_df.to_csv(DATA_PATH, index=False)
                    else:
                        df.to_csv(DATA_PATH, index=False)
                    st.success("Data appended successfully! Clear cache to reflect changes.")
                    st.cache_data.clear()
        else:
            st.error(f"Validation failed. Missing required columns: {', '.join(missing)}")
            
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
