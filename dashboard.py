
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="FTM Dashboard", layout="centered")

st.title("📊 FTM Dashboard - Tools Menu")

tool = st.selectbox("Select a Tool:", ["📁 Phone Mapper", "📁 Merge Tool", "📁 Phone Splitter"])

# -----------------------------
# Phone Mapper Tool
# -----------------------------
if tool == "📁 Phone Mapper":
    st.header("📁 Phone Mapper")

    test1_file = st.file_uploader("Upload Test1 - probate.csv", type=["csv"], key="test1")
    test2_file = st.file_uploader("Upload Test2 - probate template.csv", type=["csv"], key="test2")

    if test1_file and test2_file:
        df1 = pd.read_csv(test1_file)
        df2 = pd.read_csv(test2_file)

        def get_phone_columns(prefix, start_idx, phone_col_base):
            mapping = {}
            for i in range(1, 9):
                source = f"{prefix}{i}"
                if source in df1.columns:
                    mapping[phone_col_base + str(start_idx)] = df1[source]
                    mapping["Phone Type " + str(start_idx)] = "Mobile" if "wireless" in source else "Landline"
                    start_idx += 1
            return mapping, start_idx

        out_df = df2.copy()
        out_df.update(df1)

        start = 1
        phone_map, start = get_phone_columns("wirelessa", start, "Phone ")
        temp, start = get_phone_columns("wirelessb", start, "Phone ")
        phone_map.update(temp)
        temp, start = get_phone_columns("wirelessc", start, "Phone ")
        phone_map.update(temp)
        temp, start = get_phone_columns("landline", start, "Phone ")
        phone_map.update(temp)
        temp, start = get_phone_columns("survivor wireless", start, "Phone ")
        phone_map.update(temp)
        temp, start = get_phone_columns("survivor landline", start, "Phone ")
        phone_map.update(temp)

        for col, values in phone_map.items():
            out_df[col] = values

        # Combine name fields
        if "First Name" in df1.columns and "Last Name" in df1.columns:
            out_df["Full Name (deceased)"] = df1["First Name"].fillna("") + " " + df1["Last Name"].fillna("")
        if "Petitioner First Name" in df1.columns and "Petitioner Last Name" in df1.columns:
            out_df["PR Full Name"] = df1["Petitioner First Name"].fillna("") + " " + df1["Petitioner Last Name"].fillna("")
        if "Attorney First Name" in df1.columns and "Attorney Last Name" in df1.columns:
            out_df["Attorney Full Name"] = df1["Attorney First Name"].fillna("") + " " + df1["Attorney Last Name"].fillna("")

        buffer = io.BytesIO()
        out_df.to_excel(buffer, index=False)
        st.download_button("Download Mapped Output", buffer.getvalue(), file_name="Mapped_Output.xlsx")


# -----------------------------
# Merge Tool
# -----------------------------
elif tool == "📁 Merge Tool":
    st.header("📁 Excel Merge Tool")

    uploaded_files = st.file_uploader("Upload multiple Excel/CSV files to merge", type=["xlsx", "csv"], accept_multiple_files=True)

    if uploaded_files:
        merged_df = pd.DataFrame()
        for file in uploaded_files:
            try:
                if file.name.endswith(".csv"):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                merged_df = pd.concat([merged_df, df], ignore_index=True)
            except Exception as e:
                st.error(f"Error reading file '{file.name}': {e}")

        if not merged_df.empty:
            buffer = io.BytesIO()
            merged_df.to_excel(buffer, index=False)
            st.download_button("Download Merged File", buffer.getvalue(), file_name="Merged_Probate_Data.xlsx")


# -----------------------------
# Phone Splitter
# -----------------------------
elif tool == "📁 Phone Splitter":
    st.header("📁 Phone Splitter")

    uploaded = st.file_uploader("Upload Prospect File", type=["csv", "xlsx"])

    if uploaded:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)

        phone_columns = [col for col in df.columns if col.lower().startswith("phone")]

        exploded_rows = []
        for _, row in df.iterrows():
            for phone_col in phone_columns:
                phone_number = row[phone_col]
                if pd.notna(phone_number) and str(phone_number).strip() != "":
                    new_row = row.drop(labels=phone_columns).copy()
                    new_row["Phone"] = phone_number
                    exploded_rows.append(new_row)

        if exploded_rows:
            final_df = pd.DataFrame(exploded_rows)
            buffer = io.BytesIO()
            final_df.to_excel(buffer, index=False)
            st.download_button("Download Split File", buffer.getvalue(), file_name="Split_Prospects.xlsx")
        else:
            st.warning("No valid phone numbers found to split.")
