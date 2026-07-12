# This streamlit app is a simple note-taking application 
# that allows users to create, view, search, and delete notes. 
# It also supports file attachments for each note. 
# The app uses SQLite for data storage and provides 
# a user-friendly interface for managing notes.
# It also have analytics and visualization features to help users 
# understand their note-taking habits.

# Developed by Adeyinka B Olamilekan

import streamlit as st
import pandas as pd
import os
from logic import insert_note, get_notes, update_note, delete_note, UPLOAD_DIR, DEBUG, db_config

st.set_page_config(page_title="Note Taking App", page_icon="📓", layout="centered")
st.title("📓 Note Taking App")

if DEBUG:
    st.info("Running in DEBUG mode")


st.subheader("➕ Create a New Note")
title = st.text_input("Title", key="note_title")
content = st.text_area("Content", key="note_content")
uploaded_file = st.file_uploader("Attach a file (Optional)", key="file_upload")

if st.button("Save Note", type="primary"):
    if title.strip() and content.strip():
        saved_file_path = None
        
        # Process the file upload storage mechanism if a file is present
        if uploaded_file is not None:
            saved_file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            try:
                with open(saved_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            except Exception as e:
                st.error(f"Could not write file to drive: {e}")
                st.stop()
        
        # Save note metadata directly to SQLite database 
        if insert_note(db_config, title, content, saved_file_path):
            st.success("🎉 Note saved successfully!")
            st.rerun()
        else:
            st.error("Database save operation failed.")
    else:
        st.warning("Please fill out both the Title and Content fields.")

# --- ARCHIVE ARCHITECTURE WITH DOWNLOAD CAPABILITIES ---
st.subheader("📋 Saved Notes Archive")
notes = get_notes(db_config)

if notes:
    # 4 columns map cleanly now
    df = pd.DataFrame(notes, columns=["ID", "Title", "Content", "File Path"])
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Render file download links for entries that have a file path row
    st.markdown("### 📥 Attached Files Access")
    for idx, row in df.dropna(subset=["File Path"]).iterrows():
        if os.path.exists(row["File Path"]):
            with open(row["File Path"], "rb") as file_bytes:
                st.download_button(
                    label=f"⬇️ Download file for Note #{row['ID']}: {os.path.basename(row['File Path'])}",
                    data=file_bytes,
                    file_name=os.path.basename(row['File Path']),
                    key=f"dl_{row['ID']}"
                )

    # --- SEARCH ENGINE BLOCK ---
    keyword = st.text_input("🔍 Search keyword in contents")
    if keyword:
        filtered = df[df['Content'].str.contains(keyword, case=False, na=False)]
        st.dataframe(filtered, use_container_width=True)

    # --- DATA VISUALIZATION ---
    st.subheader("📊 Notes Distribution Chart")
    st.bar_chart(df['Title'].value_counts())
else:
    df = pd.DataFrame(columns=["ID", "Title", "Content", "File Path"])
    st.info("No notes found in the database yet.")

# --- DELETE ENGINE ---
if not df.empty:
    st.markdown("---")
    st.subheader("🗑️ Delete an Existing Note")
    valid_ids = df["ID"].tolist()
    note_id_to_delete = st.selectbox("Select Note ID to permanently delete", options=valid_ids)
    
    if st.button("Delete Note", type="secondary"):
        if delete_note(db_config, int(note_id_to_delete)):
            st.warning(f"Note ID {note_id_to_delete} was deleted from storage.")
            st.rerun()
        else:
            st.error("Failed to delete the requested record.")
