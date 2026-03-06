# pages/Personal_Storage.py
import streamlit as st
from backend import chat_manager
from utils.theme import apply_theme
apply_theme()


st.title("Personal Chat Storage")

user_id = "default_user"

chats = chat_manager.list_chats(user_id)
if not chats:
    st.info("No chats found yet. Use the chat pages to create conversations.")
else:
    for c in chats[::-1]:
        st.markdown(f"**Subject:** {c.get('subject')} • **Time:** {c.get('ts')}")
        st.write(f"**Q:** {c.get('message')}")
        st.write(f"**A:** {c.get('reply')}")
        if st.button("Delete", key=c.get("id")):
            chat_manager.delete_chat(user_id, c.get("id"))
            st.rerun()
