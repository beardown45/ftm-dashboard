
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Tool Dashboard", layout="wide")
st.title("📊 Data Tool Dashboard")

# Tool selection
tool = st.sidebar.selectbox("Select a Tool", [
    "📞 Prospect Phone Splitter",
    "📍 Phone Mapper Tool",
    "🧾 Excel Merge Tool"
])

# Load each tool based on selection
if tool == "📞 Prospect Phone Splitter":
    st.header("Prospect Phone Splitter")
    uploaded_file = st.file_uploader("Upload Prospect CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        phone_cols = [col for col in df.columns if 'phone' in col.lower()]
        if not phone_cols:
            st.error("No phone columns found.")
        else:
            expanded_rows = []
            for _, row in df.iterrows():
                for phone_col in phone_cols:
                    phone = row[phone_col]
                    if pd.notna(phone):
                        new_row = row.copy()
                        new_row["Phone"] = phone
                        expanded_rows.append(new_row.drop(phone_cols))
            if expanded_rows:
                df_expanded = pd.DataFrame(expanded_rows)
                st.success(f"{len(df)} rows expanded to {len(df_expanded)} by phone number.")
                st.download_button("Download", df_expanded.to_csv(index=False), "expanded_prospects.csv", "text/csv")
            else:
                st.warning("No valid phone numbers found.")

elif tool == "📍 Phone Mapper Tool":
    st.header("Phone Mapper Tool")
    test1_file = st.file_uploader("Upload Test1 - probate.csv", type=["csv"], key="test1")
    test2_file = st.file_uploader("Upload Test2 - probate template.csv", type=["csv"], key="test2")

    if test1_file and test2_file:
        df1 = pd.read_csv(test1_file)
        df2 = pd.read_csv(test2_file)

        min_len = min(len(df1), len(df2))
        df1 = df1.iloc[:min_len]
        df2 = df2.iloc[:min_len]

        phone_fields = [
            ('Wireless 1', 'Phone 1', 'Phone Type 1', 'mobile'),
            ('Wireless 2', 'Phone 2', 'Phone Type 2', 'mobile'),
            ('Wireless 3', 'Phone 3', 'Phone Type 3', 'mobile'),
            ('Wireless 4', 'Phone 4', 'Phone Type 4', 'mobile'),
            ('Wireless 5', 'Phone 5', 'Phone Type 5', 'mobile'),
            ('Wireless 6', 'Phone 6', 'Phone Type 6', 'mobile'),
            ('Landline 1', 'Phone 7', 'Phone Type 7', 'landline'),
            ('Landline 2', 'Phone 8', 'Phone Type 8', 'landline'),
            ('Landline 3', 'Phone 9', 'Phone Type 9', 'landline'),
            ('Landline 4', 'Phone 10', 'Phone Type 10', 'landline'),
            ('Survivor Wireless 1', 'Phone 11', 'Phone Type 11', 'mobile'),
            ('Survivor Wireless 2', 'Phone 12', 'Phone Type 12', 'mobile'),
            ('Survivor Landline 1', 'Phone 13', 'Phone Type 13', 'landline'),
            ('Survivor Landline 2', 'Phone 14', 'Phone Type 14', 'landline')
        ]

        for source, phone_col, type_col, ptype in phone_fields:
            if source in df1.columns:
                df2[phone_col] = df1[source]
                df2[type_col] = df1[source].apply(lambda x: ptype if pd.notna(x) else '')

        df2['Full Name (deceased)'] = df1['Dec First Name'].fillna('') + ' ' + df1['Dec Last Name'].fillna('')
        df2['PR Full Name'] = df1['Petitioner First Name'].fillna('') + ' ' + df1['Petitioner Last Name'].fillna('')
        df2['Attorney Full Name'] = df1['Attorney First Name'].fillna('') + ' ' + df1['Attorney Last Name'].fillna('')

        fields_to_copy = [
            ('Parcel ID', 'Parcel ID'), ('Property Value', 'Property Value'),
            ('Property Use', 'Property Use'), ('Date of Death', 'Date of Death'),
            ('Email 1', 'Email 1'), ('Email 2', 'Email 2'), ('Email 3', 'Email 3')
        ]
        for src, tgt in fields_to_copy:
            if src in df1.columns:
                df2[tgt] = df1[src]

        st.success(f"Mapped {min_len} rows successfully.")
        st.download_button("Download Mapped CSV", df2.to_csv(index=False), "mapped_output.csv", "text/csv")

elif tool == "🧾 Excel Merge Tool":
    st.header("Excel Merge Tool")
    uploaded_files = st.file_uploader("Upload multiple Excel or CSV files", type=["csv", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        all_dfs = []
        for file in uploaded_files:
            try:
                if file.name.endswith(".csv"):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                all_dfs.append(df)
            except Exception as e:
                st.error(f"Error reading {file.name}: {e}")

        if all_dfs:
            merged_df = pd.concat(all_dfs, ignore_index=True)
            st.success(f"Merged {len(all_dfs)} files into {len(merged_df)} rows.")
            st.download_button("Download Merged File", merged_df.to_csv(index=False), "merged_output.csv", "text/csv")
