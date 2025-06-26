
import streamlit as st
import pandas as pd

st.set_page_config(page_title="FTM Dashboard", layout="centered")

st.title("📊 FTM Data Tools Dashboard")
tool = st.selectbox("Choose a tool to launch:", ["📞 Phone Mapper", "🧩 Merge Tool", "🔀 Phone Splitter"])

# ========== PHONE MAPPER ==========
if tool == "📞 Phone Mapper":
    st.header("📞 Phone Mapper")
    st.write("Map phone numbers from multiple fields into ordered phone + type columns.")

    test1_file = st.file_uploader("Upload Test1 - probate.csv", type=["csv", "xlsx"])
    test2_file = st.file_uploader("Upload Test2 - probate template.csv", type=["csv", "xlsx"])

    if test1_file and test2_file:
        df1 = pd.read_csv(test1_file) if test1_file.name.endswith("csv") else pd.read_excel(test1_file)
        df2 = pd.read_csv(test2_file) if test2_file.name.endswith("csv") else pd.read_excel(test2_file)

        phone_cols = ['wireless1', 'wireless2', 'wireless3', 'wireless4', 'wireless5', 'wireless6', 'wireless7', 'wireless8',
                      'landline1', 'landline2', 'landline3', 'landline4', 'landline5',
                      'survivor wireless1', 'survivor wireless2', 'survivor wireless3', 'survivor wireless4',
                      'survivor wireless5', 'survivor wireless6', 'survivor wireless7', 'survivor wireless8',
                      'survivor landline1', 'survivor landline2', 'survivor landline3', 'survivor landline4', 'survivor landline5']

        for i in range(1, 12):
            df2[f'Phone {i}'] = ""
            df2[f'Phone Type {i}'] = ""

        for idx, row in df1.iterrows():
            for i, col in enumerate(phone_cols):
                phone = row.get(col, "")
                if pd.notna(phone) and phone != "":
                    phone_num = phone.strip()
                    phone_index = i + 1
                    phone_type = "mobile" if "wireless" in col else "landline"
                    if phone_index > 10:
                        phone_index += 1  # skip phone 11 if needed
                    df2.at[idx, f'Phone {phone_index}'] = phone_num
                    df2.at[idx, f'Phone Type {phone_index}'] = phone_type

            df2.at[idx, "Full Name (deceased)"] = f"{row.get('first name', '')} {row.get('last name', '')}".strip()
            df2.at[idx, "PR Full Name"] = f"{row.get('petitioner first name', '')} {row.get('petitioner last name', '')}".strip()
            df2.at[idx, "Attorney Full Name"] = f"{row.get('attorney first name', '')} {row.get('attorney last name', '')}".strip()

        st.success("Mapping complete.")
        st.download_button("Download Mapped File", df2.to_csv(index=False).encode(), "Mapped_Output.csv", "text/csv")

# ========== MERGE TOOL ==========
elif tool == "🧩 Merge Tool":
    st.header("🧩 Excel Merge Tool")
    st.write("Merge multiple Excel or CSV files into one master file.")

    uploaded_files = st.file_uploader("Upload files to merge", type=["csv", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        merged_df = pd.DataFrame()
        for file in uploaded_files:
            df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_excel(file)
            merged_df = pd.concat([merged_df, df], ignore_index=True)

        st.success(f"Merged {len(uploaded_files)} files successfully!")
        st.download_button("Download Merged File", merged_df.to_csv(index=False).encode(), "Merged_Probate_Data.csv", "text/csv")

# ========== PHONE SPLITTER ==========
elif tool == "🔀 Phone Splitter":
    st.header("🔀 Phone Splitter")
    st.write("Split each row with multiple phone numbers into separate rows (1 phone number per row).")

    input_file = st.file_uploader("Upload CSV file with up to 8 phone number columns", type=["csv"])

    if input_file:
        df = pd.read_csv(input_file)
        phone_cols = [col for col in df.columns if "phone" in col.lower()]
        exploded_rows = []

        for _, row in df.iterrows():
            for phone_col in phone_cols:
                phone = row.get(phone_col)
                if pd.notna(phone) and phone != "":
                    new_row = row.drop(phone_cols).to_dict()
                    new_row["Phone"] = phone
                    exploded_rows.append(new_row)

        out_df = pd.DataFrame(exploded_rows)
        st.success(f"Created {len(out_df)} phone-specific rows.")
        st.download_button("Download Split File", out_df.to_csv(index=False).encode(), "Split_Phones.csv", "text/csv")
