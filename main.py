import pandas as pd
from io import BytesIO
import streamlit as st
import os

st.set_page_config( page_title="📁 file Converter And Cleaner",layout='wide') 



st.title("📁 file Converter And Cleaner")
st.write("upload your csv and excel files to clean the data  Convert formats effortlessly  🧹")
files=st.file_uploader(" upload csv and excel file", type=["csv","xlsx"],accept_multiple_files=True)
if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file)if ext == "csv" else pd.read_excel(file)
        st.subheader(f"{file.name} - preview" )
        st.dataframe(df.head())
        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(),inplace=True)
            st.success("Missing values filled successfully! ")
            st.dataframe(df.head())
        select_columns=st.multiselect(f"select Columns - {file.name}", df.columns, default=df.columns)
        df= df[select_columns]
        st.dataframe(df.head( ))      
        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2]) 
        format_choice =  st.radio (f"Convert {file.name}to: ", ['csv','excel'],key=file.name)
  
        if st.button(f" Download {file.name} as {format_choice} " ):
            output= BytesIO()
            if format_choice == "csv":
                df.to_csv(output ,index=False)
                mime ="text/csv"
                new_mime = file.name.replace(ext,"csv")
            else:
                df.to_excel(output,index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_mime = file.name.replace(ext,"xlsx") 
            output.seek(0)
            st.download_button(f" download file",file_name="new_name",data=output,mime=mime)
        st.success("Processing Complete")