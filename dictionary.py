import streamlit as st
import mysql.connector

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dict_db"
)
cursor = connection.cursor()

st.title("Dictionary App")

# Sidebar to choose the operation
operation = st.sidebar.radio("Select an Operation:", ("Search", "Add", "Update", "Delete"))

if operation == "Search":
    st.header("Search a Word")
    search_word = st.text_input("Enter a word to search:")
    
    if st.button("Search"):
        cursor.execute(f"SELECT word, definition FROM dictionary WHERE word LIKE '%{search_word}%'")
        result = cursor.fetchall()
        if result:
            for i in result:
                st.write(f"**{i[0]}**: {i[1]}")
        else:
            st.warning(f"No definition found for '{search_word}'.")

elif operation == "Add":
    st.header("Add a Word")
    new_word = st.text_input("Enter a new word:")
    new_definition = st.text_area("Definition:")
    
    if st.button("Add Word"):
        cursor.execute("INSERT INTO dictionary (word, definition) VALUES (%s, %s)", (new_word, new_definition))
        connection.commit()
        st.success(f"Added '{new_word}' to the dictionary.")

elif operation == "Update":
    st.header("Update a Word")
    update_word = st.text_input("Enter a word to update:")
    updated_definition = st.text_area("Updated Definition:")
    
    if st.button("Update Word"):
        cursor.execute("UPDATE dictionary SET definition=%s WHERE word=%s", (updated_definition, update_word))
        connection.commit()
        st.success(f"Updated definition for '{update_word}'.")

elif operation == "Delete":
    st.header("Delete a Word")
    delete_word = st.text_input("Enter a word to delete:")
    
    if st.button("Delete Word"):
        cursor.execute("DELETE FROM dictionary WHERE word=%s", (delete_word,))
        connection.commit()
        st.success(f"Deleted '{delete_word}' from the dictionary.")

# Close the database connection
cursor.close()
connection.close()