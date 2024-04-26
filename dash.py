import streamlit as st
import sqlite3
import pandas as pd


item_type = st.selectbox(
   "Items",
   ("Weapons","Defense","Accesories"),
   index=None,
   placeholder="Select and item type",
)

if item_type == "Weapons":
  item =  st.selectbox(
        "Weapons",
        ("Axes",
        "Bows",
        "Claws",
        "Daggers",
        "Fists",
        "Hammers",
        "Javelins",
        "Phantoms",
        "Scythes",
        "Swords",
        "Wands & Staffs"),
        index=None,
        placeholder="Select weapon",
    )
    
elif item_type == "Defense":
   item = st.selectbox(
        "Defense",
        ("Armors",
        "Robes",
        "Shields",
        "Orbs",
        "Bracelets",
        "Gauntlets",
        "Boots"),
        index=None,
        placeholder="Select defense",
    )
else:
  item =  st.selectbox(
        "Accesories",
        ("Amulets",
        "Belts",
        "Rings",
        "Earrings"),
        index=None,
        placeholder="Select accesories",
    )

conn = sqlite3.connect('ItemsDB.db')
cursor = conn.cursor()


item_query = """
SELECT
    b.item_name,
    b.Level 
FROM items i 
LEFT JOIN bitems b ON i.items = b.items 
WHERE i."type" = ?
ORDER BY b.Level ASC
"""

cursor.execute(item_query, (item,))
rows = cursor.fetchall()


list_selected_item = [f"{row[0]} - {row[1]}" for row in rows]

selected_item =st.selectbox("Select an item", list_selected_item)
