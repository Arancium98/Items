import streamlit as st
import sqlite3
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode

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

selected_item_clean = selected_item.split("-")[0].strip()


selected_item_query = """
SELECT
    b.item_image_url, 
	b.item_name,
	b.LEVEL,
	w."Min Damage",
	w."Max Damage",
	w."Attack Speed", 
	w.Critical,
	w."Attack Rating",
	w.Integrity,
	w.Block,
	w."Range",
	w.Defense,
	w."Add HP",
	w."Add MP" 
    
FROM weapons w 
LEFT JOIN bitems b ON w.item_id = b.item_id 
LEFT JOIN items i ON b.items = i.items 
WHERE b.item_name  = ?
ORDER BY b."Level" ASC
"""

cursor.execute(selected_item_query, (selected_item_clean,))
rows = cursor.fetchall()

xd = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

def drop_empty_columns(df):
    empty_columns = df.columns[df.isnull().all()]
    df.drop(empty_columns, axis=1, inplace=True)
    return df


xd = drop_empty_columns(xd)
#xd['item_image_url'] = xd['item_image_url'].apply(lambda x: f'"{x}"' if x != '' else '')

st.data_editor(
    xd.T,
    column_config={
        "item_image_url": st.column_config.ImageColumn(
            "item_image_url"
        )
    },
    hide_index=False,
)


data_df = pd.DataFrame(
    {
        "apps": [
            "https://user.wartale.com/images/items/itWA102.jpg",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/ef9a7627-13f2-47e5-8f65-3f69bb38a5c2/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/31b99099-8eae-4ff8-aa89-042895ed3843/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/6a399b09-241e-4ae7-a31f-7640dc1d181e/Home_Page.png",
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "apps": st.column_config.ImageColumn(
            "Preview Image", help="Streamlit app preview screenshots", width="medium"
        )
    },
    hide_index=True,
)

