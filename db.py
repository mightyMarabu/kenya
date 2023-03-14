import sqlite3
from nicegui import ui

from nicegui.element import Element

conn = sqlite3.connect("app.sqlite")
cursor = conn.cursor()

name = ui.input(label="user").classes("w-full")

dataList = ui.column()

getID = ui.label()

# class spatialite(Element):
# add data
def addData():
    try:
        cursor.execute('''INSERT INTO users(name) VALUES (?)''',(name.value,))
        conn.commit()
        ui.notify(f"data saved: {name.value}", color="blue")
        name.value = ""
        dataList.clear()
        getData()
    except Exception as e:
        print ("total desaster!")
        print (e)

ui.button("add new user",
        on_click=addData
        )
def editData():
    pass

def deleteData(x):
    getID.text = x.default_slot.children[0].text
    try:
        cursor.execute('''DELETE FROM users WHERE id = (?)''',(getID.text,))
        conn.commit()
        ui.notify(f"data deleted!", color="red")
        dataList.clear()
        getData()
    except Exception as e:
        print ("total desaster!")
        print (e)


def getData():
    cursor.execute('''SELECT * FROM users''')
    res = cursor.fetchall()
    result = []
    for r in res:
        data = {}
        for i,col in enumerate(cursor.description):
            data[col[0]] = r[i]
        result.append(data)
    print(result)

    for d in result:
        with dataList:
            with ui.card():
                with ui.column():
                    with ui.row().classes("justify-between w-full") as carddata:
                        ui.label(d['id'])
                        ui.label(d['name'])
                    with ui.row():
                         ui.button("edit").on("click", lambda e, carddata=carddata : editData(carddata))
                         ui.button("delete").on("click", lambda e, carddata=carddata : deleteData(carddata)).classes("bg-red")

getData()

ui.run()