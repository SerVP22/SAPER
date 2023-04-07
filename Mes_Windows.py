from customtkinter import CTkLabel, CTkButton, CTkToplevel, CTkComboBox, CTkScrollableFrame, \
                          CTkSwitch,  CTkImage, CTkEntry, CTkFrame
import json, time
from PIL import Image, ImageSequence
import tkinter as tk


class MesWindows:

    def show_settings_window(self):
        geometry = self.win.geometry()
        win_set = CTkToplevel(self.win)
        W = 255
        H = 215

        win_set.title("Настройки игры")
        win_set.resizable(False, False)
        win_set.attributes("-alpha", 0.9)
        win_set.attributes("-toolwindow", True)
        win_set.attributes("-topmost", True)

        win_set.geometry(self.get_toplevel_geometry(W, H, geometry))

        CTkLabel(win_set, text="Сложность:", anchor="e", fg_color='white', corner_radius=5,
                 width=140, font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)

        val1 = list(self.HARD_LEVELS.keys())
        comb1 = CTkComboBox(win_set, values=val1, width=100)
        comb1.grid(row=0, column=1, pady=5)
        comb1.set(str(self.get_current_hard()))

        CTkLabel(win_set, text="Количество строк:", anchor="e", fg_color='white', corner_radius=5,
                 width=140, font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=5)
        val2 = [str(i) for i in range(4, self.get_max_fields_count()[1] + 1)]
        comb2 = CTkComboBox(win_set, values=val2, width=100)
        comb2.grid(row=1, column=1, pady=5)
        comb2.set(str(self.STROKI))

        CTkLabel(win_set, text="Количество столбцов:", anchor="e", fg_color='white', corner_radius=5,
                 width=140, font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=5)
        val3 = [str(i) for i in range(7, self.get_max_fields_count()[0] + 1)]
        comb3 = CTkComboBox(win_set, values=val3, width=100)
        comb3.grid(row=2, column=1, pady=5)
        comb3.set(str(self.STOLBCI))

        CTkLabel(win_set, text="Звук в игре:", anchor="e", fg_color='white', corner_radius=5,
                 width=140, font=("Arial", 12, "bold")).grid(row=3, column=0, padx=5, pady=5)
        switch1 = CTkSwitch(master=win_set, text="", onvalue="on", offvalue="off")
        switch1.configure(command=lambda: self.switch1_event(switch1))
        if self.SOUND_ON:
            switch1.select()
        else:
            switch1.deselect()
        switch1.grid(row=3, column=1, pady=5)

        btn1 = CTkButton(win_set, text="Применить параметры", command=
        lambda: self.save_settings_button_click(win_set, comb1, comb2, comb3, switch1))
        btn1.grid(row=4, column=0, columnspan=2, pady=15)

        win_set.grab_set()


    def get_toplevel_geometry(self, W, H, geometry):
        parent_size, parent_x, parent_y = geometry.split(sep="+")
        parent_W, parent_H = parent_size.split(sep="x")
        center_x = int(parent_x) + int(parent_W) // 2
        center_y = int(parent_y) + int(parent_H) // 2
        new_x = center_x - W // 2
        new_y = center_y - H // 2
        return f"{W}x{H}+{new_x}+{new_y + 5}"

    def switch1_event(self, sw:CTkSwitch):
        if sw.get() == "on":
            self.switch0.select()
        else:
            self.switch0.deselect()
        self.switch0_event()

    def gif_play(self, file, win, x, y, size_x, size_y):
        try:
            img = Image.open(file)
            lbl = CTkLabel(win, text="")
            lbl.place(x=x, y=y)

            while True:
                try:
                    for frame in ImageSequence.Iterator(img):
                        # frame = frame.resize((size_x, size_y))
                        # frame = ImageTk.PhotoImage(frame)
                        frame = CTkImage(light_image=frame, dark_image=frame, size=(size_x, size_y))
                        if win. winfo_exists():
                            lbl.configure(image=frame)
                        time.sleep(0.02)
                        win.update()
                except Exception as msg:
                    print('gif play error:', msg)
                    break
        except Exception as msg:
            print("gif image load error:", msg)

    def show_game_over_window(self):

        W = 350
        H = 140

        win_g_o = CTkToplevel(self.win)
        win_g_o.title("Ты проиграл!")
        win_g_o.resizable(False, False)
        # win_g_o.attributes("-alpha", 0.9)
        win_g_o.attributes("-toolwindow", True)
        win_g_o.attributes("-topmost", True)
        geometry = self.win.geometry()
        win_g_o.geometry(self.get_toplevel_geometry(W, H, geometry))

        CTkLabel(win_g_o, text="У тебя был шанс...", font=('Arial', 22), pady=10, fg_color="white",
                corner_radius=10).place(x=135, y=10)
        CTkButton(win_g_o, text="Закрыть окно", command=win_g_o.destroy).place(x=170, y=65)
        CTkButton(win_g_o, text="Перезапуск игры", command=
        lambda: self.destroy_message_window_and_reboot(win_g_o)
                  ).place(x=170, y=100)


        win_g_o.grab_set()
        if self.SOUND_ON and self.sound_boom:
            self.sound_boom.play()

        self.gif_play("images/exploding_low.gif", win_g_o, 10, 10, 120, 120)

    def read_winners_from_JSON(self):
        winners = []
        try:
            with open("winners.json", "r") as f:
                winners = json.load(f)
        except FileNotFoundError:
            return []
        return winners

    def list_players_update(self, players: list, score: int):
        new_list = []
        user_inside = False
        for i in players:
            if score<i["score"]:
                new_list.append(i)
            elif score>=i["score"] and not user_inside:
                new_list.append({"name":"",
                                 "score": score,
                                 "level": f"{self.get_current_hard()} {self.STROKI}x{self.STOLBCI}"
                                })
                new_list.append(i)
                user_inside = True
            elif score>=i["score"] and user_inside:
                new_list.append(i)
        return new_list

    def name_enter(self, players_list: list, num_line: int, cell: CTkEntry, win, but):
        name = cell.get()
        if name != "":
            cell.configure(state="disabled", fg_color="white")
            but.configure(text="Перезапуск игры", command=lambda: self.destroy_message_window_and_reboot(win))
            players_list[num_line]["name"] = name
            self.save_user_name_to_JSON(players_list, cell)

    def save_user_name_to_JSON(self, players_list: list, cell: CTkEntry):
        try:
            with open("winners.json", "w") as f:
                json.dump(players_list, f)
        except:
            cell.delete(0, tk.END)
            cell.insert(0, "Ошибка записи в файл")

    def show_win_window(self):

        score = round(self.MINES * (self.CURRENT_LEVEL * 100) ** 2)

        W = 350
        H = 370
        WINNERS_COUNT = 20

        win_win = CTkToplevel(self.win)
        win_win.title("Победа!")
        win_win.resizable(False, False)
        # win_win.attributes("-alpha", 0.9)
        win_win.attributes("-toolwindow", True)
        win_win.attributes("-topmost", True)
        geometry = self.win.geometry()
        win_win.geometry(self.get_toplevel_geometry(W, H, geometry))

        frm_0 = CTkFrame(win_win, width=330, height=65)
        frm_0.place(x=10, y=10)
        CTkLabel(frm_0, text="Вы набрали", font=('Arial', 18), pady=10).place(x=30, y=10)
        CTkLabel(frm_0, text=str(score), font=('Arial', 21), pady=10, width=90, fg_color="white",
                 corner_radius=10).place(x=140, y=10)
        if str(score)[-1] in "1":
            text = "очко"
        elif str(score)[-1] in "234":
            text = "очка"
        else:
            text = "очков"
        CTkLabel(frm_0, text=text, font=('Arial', 18), pady=10).place(x=240, y=10)

        frm_1 = CTkScrollableFrame(win_win, width=308, height=10)
        frm_1.place(x=10, y=85)


        CTkLabel(frm_1, text="№", corner_radius=5, width=30).grid(row=0, column=0, padx=1)
        head_label = CTkLabel(frm_1, text="Имя игрока", corner_radius=5, width=115)
        head_label.grid(row=0, column=1, padx=1)
        CTkLabel(frm_1, text="Очки", corner_radius=5, width=60).grid(row=0, column=2, padx=1)
        CTkLabel(frm_1, text="Сложность", corner_radius=5, width=95).grid(row=0, column=3, padx=1)

        list_players = self.read_winners_from_JSON()
        if len(list_players)>0:
            list_players = self.list_players_update(list_players, score)
        else:
            list_players.append({"name": "",
                                 "score": score,
                                 "level": f"{self.get_current_hard()} {self.STROKI}x{self.STOLBCI}"
                                })

        enabled_cell = None
        line_num = 0
        lbl2 = None

        for i in range(1, WINNERS_COUNT+1):
            lbl1 = CTkEntry(frm_1, width=30, )
            if i<10:
                txt_num = str(i)
            else:
                txt_num = str(i)
            lbl1.insert(0, txt_num)
            lbl1.configure(state=tk.DISABLED, justify="center")
            lbl1.grid(row=i, column=0, padx=1, pady=1)

            lbl2 = CTkEntry(frm_1, width=115, )
            try:
                txt_name = list_players[i-1]["name"]
            except LookupError:
                txt_name = ""
            lbl2.insert(0, txt_name)
            lbl2.configure(state=tk.DISABLED)
            lbl2.grid(row=i, column=1, padx=1, pady=1)

            lbl3 = CTkEntry(frm_1, width=60, )
            try:
                txt_score = list_players[i-1]["score"]
            except LookupError:
                txt_score = ""
            lbl3.insert(0, txt_score)
            lbl3.configure(state=tk.DISABLED, justify="right")
            lbl3.grid(row=i, column=2, padx=1, pady=1)

            lbl4 = CTkEntry(frm_1, width=95, )
            try:
                txt_level = list_players[i-1]["level"]
            except LookupError:
                txt_level = ""
            lbl4.insert(0, txt_level)
            lbl4.configure(state=tk.DISABLED, justify="center")
            lbl4.grid(row=i, column=3, padx=1, pady=1)

            try:
                if list_players[i-1]["name"] == "" and list_players[i-1]["score"] == score:
                    enabled_cell = lbl2
                    line_num = i
            except LookupError:
                pass


        frm_2 = CTkFrame(win_win, width=330, height=50)
        frm_2.place(x=10, y=310)
        CTkButton(frm_2, text="Закрыть окно", command=win_win.destroy).place(x=10, y=10)


        if line_num>5:
            shift = head_label.cget("height") + (lbl2.cget("height") +2) * (line_num - 2) - 4
            frm_1._parent_canvas.yview_scroll(shift, "units")

        if enabled_cell:
            btn1 = CTkButton(frm_2, text="Сохранить имя", command=lambda: \
                self.name_enter(list_players[0:20], line_num - 1, enabled_cell, win_win, btn1))
            btn1.place(x=180, y=10)
            enabled_cell.configure(state="normal", placeholder_text="Введи своё имя", placeholder_text_color="red",
                                   fg_color="yellow")
            enabled_cell.bind("<Return>", lambda event: \
                                        self.name_enter(list_players[0:20], line_num-1, enabled_cell, win_win, btn1))
        else:
            btn1 = CTkButton(frm_2, text="Перезапуск игры", command=lambda: \
                self.destroy_message_window_and_reboot(win_win))
            btn1.place(x=180, y=10)




        # print(type(win_win))
        # win_win.bind_class("customtkinter.windows.ctk_toplevel.CTkToplevel", "<Leave>", lambda event: print("out"))
        win_win.grab_set()
        win_win.focus_set()

        if self.SOUND_ON and self.sound_win:
            self.sound_win.play()

    def destroy_message_window_and_reboot(self, win):
        # win.after_cancel(self.loop_1)
        win.destroy()
        self.reload_game()

    def save_settings_to_JSON(self, settings):
        mono_list = []
        mono_list.append(settings)
        try:
            with open(self.FILE_CFG, "w") as f:
                json.dump(mono_list, f)
        except:
            pass


    def save_settings_button_click(self, win, *args):
        settings = {}
        settings["level"] = args[0].get()
        settings["rows"] = args[1].get()
        settings["columns"] = args[2].get()
        settings["sound"] = args[3].get()
        self.save_settings_to_JSON(settings)
        win.destroy()
        self.reload_game()