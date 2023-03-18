from customtkinter import CTkLabel, CTkButton, CTkToplevel, CTkComboBox, CTkCanvas, CTk, CTkEntry, CTkFrame

import json
root = CTk()

fr = CTkFrame(root)

btn = CTkEntry(fr)

btn.grid()
# btn.focus()
# btn.update()
# c = CTkCanvas(btn, width=300, height=300)
# c.grid(row=0, column=0)

root.mainloop()


# players = [
#     {"name": "Куликов Сергей", "score": 6000, "level": "Easy"},
#     {"name": "Парохонько Игорь", "score": 35080, "level": "Normal"}
# ]
#
# sets = {"lev": "Easy", "rows": 7, "columns": 12}
#
# rez = []
# rez.append(players)
# rez.append(sets)
#
# with open("data.json", "w") as f:
#     json.dump(rez, f)
# # with open("data.json", "a") as f:
# #     json.dump(sets, f, indent=4)
#
# with open("data.json", "r") as f:
#     data = json.load(f)
#
# print(data[0][0])
# print(data[0][1])
# print(data[1])