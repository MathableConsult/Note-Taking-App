import streamlit as st
import pandas as pd
import os
from logic import insert_note, get_notes, update_note, delete_note, UPLOAD_DIR, DEBUG, db_config
# from cRUD_oPERATIONS import insert_note,  get_notes, update_note, delete_note, UPLOAD_DIR, DEBUG
# from db_config import  db_config
# reuse your insert_note, get_notes, update_note, delete_note functions

st.title("📓 Note Taking App")
if DEBUG:
    st.info("Running in DEBUG mode")

# Add new note
title = st.text_input("Title")
content = st.text_area("Content")
if st.button("Save Note"):
    insert_note(db_config, title, content)
    st.success("Note saved!")

# View notes
notes = get_notes(db_config)
df = pd.DataFrame(notes, columns=["ID", "Title", "Content"])
st.dataframe(df)

# Delete notes
st.subheader("🗑️ Delete a Note")
note_id_to_delete = st.number_input("Enter Note ID to delete", min_value=1, step=1)
if st.button("Delete Note"):
    delete_note(db_config, note_id_to_delete)
    st.warning(f"Note {note_id_to_delete} deleted!")


uploaded_file = st.file_uploader("Upload a file")
if uploaded_file:
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    insert_note(db_config, title, content)  # extend to include file_path

keyword = st.text_input("Search keyword")
if keyword:
    filtered = df[df['Content'].str.contains(keyword, case=False)]
    st.dataframe(filtered)

st.bar_chart(df['Title'].value_counts())    

