import json
import time
import tkinter as tk
from random import sample
from Buttons import Sap_button
from customtkinter import CTk, CTkOptionMenu, CTkLabel, CTkButton, \
                          CTkToplevel, CTkImage, CTkComboBox, \
                          CTkSwitch, CTkFrame, CTkScrollableFrame, CTkEntry
# from Mes_Box import settings_win, change_hard_level_button_text
# import PIL.features
from PIL import Image, ImageSequence
import winsound, sys



class Saper:
    win = CTk()

    color_dic = {
        1: "#00CD00",
        2: "#C71585",
        3: "#5CACEE",
        4: "#CD9B1D",
        5: "#8FBC8F",
        6: "#68838B",
        7: "#9AC0CD",
        8: "#4B0082"
    }

    title_list = ["[•SAPER•    ]", "[ •SAPER•   ]", "[  •SAPER•  ]",
                  "[   •SAPER• ]", "[    •SAPER•]", "[    •SAPER•]", "[   •SAPER• ]",
                  "[  •SAPER•  ]", "[ •SAPER•   ]", "[•SAPER•    ]",
                  " •SAPEr•     ", " ••SAPer•    ", " •••SAper•   ",
                  " ••••Saper•  ", " •••••saper• ", " •••••sapeR• ", " ••••sapER•  ",
                  " •••saPER•   ", " ••sAPER•   ", " •SAPER•     ",
    ]
    tit_num = 0
    win.title(title_list[tit_num])
    win.resizable(False, False)

    try:
        win.iconbitmap(tk.PhotoImage('bomb4.ico'))
    except:
        ...

    BW = 40  # Ширина кнопки
    BH = 40  # Высота кнопки

    try:
        flag_img = CTkImage(light_image=Image.open("flag2.png"), dark_image=Image.open("flag2.png"), size=(16, 16))
        bomb_img = CTkImage(light_image=Image.open("bomb.png"), dark_image=Image.open("bomb.png"), size=(25, 25))
    except:
        print("Ошибка загрузки изображений")
        win.destroy()
        sys.exit()

    HORIZONTAL_ANIM = False
    HARD_LEVELS = {'Kid': 0.05, 'Easy': 0.125, 'Normal': 0.17, 'Hard': 0.25}
    SW = win.winfo_screenwidth()  # ширина экрана
    SH = win.winfo_screenheight()  # высота экрана

    FILE_CFG = "config.json"



    def __init__(self):

        self.CURRENT_LEVEL, self.STROKI, self.STOLBCI, self.SOUND_ON = self.read_settings_from_file(self.FILE_CFG)
        # self.STROKI = self.STOLBCI = 7
        # self.CURRENT_LEVEL =

        # количество столбцов #(макс 31)
        if self.STOLBCI < 7:
            self.STOLBCI = 7  # минимальное количество столбцов 7
        if self.STOLBCI> self.get_max_fields_count()[0]:
            self.STOLBCI = self.get_max_fields_count()[0]
         # количество строк #(макс.23)
        if self.STROKI < 4:
            self.STROKI = 4  # минимальное количество строк 4
        if self.STROKI> self.get_max_fields_count()[1]:
            self.STROKI = self.get_max_fields_count()[1]

        dX = int((self.SW - self.BW * self.STOLBCI) / 2) - 8  # координата по X
        dY = int((self.SH - self.BH * self.STROKI) / 2) - 30  # координата по Y
        if dX < 0:
            dX = 0
        if dY < 0:
            dY = 0

        """
        Если окно меняет свои размеры, тогда центруем его 
        [[NNN]x[NNN]]+NNN+NNN
        """
        if self.win.geometry().split(sep="+")[0].split(sep="x")[0] != str(self.STOLBCI * self.BW) or \
           self.win.geometry().split(sep="+")[0].split(sep="x")[1] != str(self.STROKI * self.BH + 52):
            self.win.geometry(f'+{dX}+{dY}')  # размещаем игровое поле по центру экрана


        self.MINES = int(self.STROKI * self.STOLBCI * self.CURRENT_LEVEL)  # количество мин на поле

        self.game_win_over_flag = False
        self.flag_list = []
        self.first_shoot = True

        self.buttons_list = []
        count = 1
        for i in range(0, self.STROKI + 2):
            temp_list = []
            for j in range(0, self.STOLBCI + 2):
                if 0 < i < self.STROKI + 1 and 0 < j < self.STOLBCI + 1:
                    num_but = count
                    count += 1
                else:
                    num_but = 0
                but = Sap_button(self.win, x=i, y=j, num=num_but, text='', width=self.BW, height=self.BH,
                                 corner_radius=10, border_width=2, fg_color='grey')
                but.configure(command=lambda b=but: self.click_mouse(b))
                but.bind("<Button-3>", lambda event, b=but: self.r_b_click(b, event))
                temp_list.append(but)

            self.buttons_list.append(temp_list)

    def get_max_fields_count(self):
        """
        Возвращает максимальное допустимое количество полей по горизонтали и вертикали.
        Вычислется на основе текущего разрешения экрана и размеров одного поля (клетки)
        """
        return self.SW//self.BW -1, self.SH//self.BH - 2

    def read_settings_from_file(self, file_name):
        temp_list = []
        try:
            with open(file_name, 'r') as f:
                settings = json.load(f)[0]
            temp_list.append(self.HARD_LEVELS[settings["level"]])
            temp_list.append(int(settings["rows"]))
            temp_list.append(int(settings["columns"]))
            if settings["sound"]=="off":
                temp_list.append(False)
            else:
                temp_list.append(True)
            return temp_list
        except:
            return (0.125, 10, 10, True) #конфигурация игры по умолчанию

    def get_message_window_geometry(self, W, H, geometry):
        parent_size, parent_x, parent_y = geometry.split(sep="+")
        parent_W, parent_H = parent_size.split(sep="x")
        center_x = int(parent_x) + int(parent_W) // 2
        center_y = int(parent_y) + int(parent_H) // 2
        new_x = center_x - W // 2
        new_y = center_y - H // 2
        return f"{W}x{H}+{new_x}+{new_y + 5}"

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

        win_set.geometry(self.get_message_window_geometry(W, H, geometry))



        CTkLabel(win_set, text="Сложность:", anchor="e", fg_color='white', corner_radius=5,
                 width=140, font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)

        val1 = list(self.HARD_LEVELS.keys())
        comb1 = CTkComboBox(win_set, values=val1, width=100)
        comb1.grid(row=0, column=1, pady=5)
        comb1.set(str(self.get_current_hard()))

        CTkLabel(win_set, text="Количество строк:", anchor="e", fg_color='white', corner_radius=5,
                 width=140, font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=5)
        val2 = [str(i) for i in range(4, self.get_max_fields_count()[1]+1)]
        comb2 = CTkComboBox(win_set, values=val2, width=100)
        comb2.grid(row=1, column=1, pady=5)
        comb2.set(str(self.STROKI))

        CTkLabel(win_set, text="Количество столбцов:", anchor="e", fg_color='white', corner_radius=5,
                 width=140, font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=5)
        val3 = [str(i) for i in range(7, self.get_max_fields_count()[0]+1)]
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
        switch1.grid(row=3, column=1, pady=5 )

        btn1 = CTkButton(win_set, text="Применить параметры", command=
            lambda: self.save_settings_to_file_and_reboot(win_set, comb1, comb2, comb3, switch1))
        btn1.grid(row=4, column=0, columnspan=2, pady=15)

        win_set.grab_set()

    def switch0_event(self):
        try:
            with open(self.FILE_CFG, 'r') as f:
                data = json.load(f)
            if self.switch0.get() == "on":
                self.SOUND_ON = True
            else:
                self.SOUND_ON = False
            data[0]["sound"] = self.switch0.get()
            with open(self.FILE_CFG, 'w') as f:
                json.dump(data, f)
        except:
            print("Жопа!!!")

    def switch1_event(self, sw:CTkSwitch):
        if sw.get() == "on":
            self.switch0.select()
        else:
            self.switch0.deselect()
        self.switch0_event()

    def gif_play(self, file, win, x, y, size_x, size_y):
        img = Image.open(file)
        lbl = CTkLabel(win, text="")
        lbl.place(x=x, y=y)

        while True:
            try:
                for frame in ImageSequence.Iterator(img):
                    # frame = frame.resize((size_x, size_y))
                    # frame = ImageTk.PhotoImage(frame)
                    frame = CTkImage(light_image=frame, dark_image=frame, size=(size_x, size_y))
                    lbl.configure(image=frame)
                    time.sleep(0.05)
                    win.update()
            except:
                break

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
        win_g_o.geometry(self.get_message_window_geometry(W, H, geometry))

        CTkLabel(win_g_o, text="У тебя был шанс...", font=('Arial', 22), pady=10, fg_color="white",
                corner_radius=10).place(x=135, y=10)
        CTkButton(win_g_o, text="Закрыть окно", command=win_g_o.destroy).place(x=170, y=65)
        CTkButton(win_g_o, text="Перезапуск игры", command=
        lambda: self.destroy_message_window_and_reboot(win_g_o)
                  ).place(x=170, y=100)


        win_g_o.grab_set()
        if self.SOUND_ON:
            winsound.PlaySound('boom.wav', winsound.SND_FILENAME)

        self.gif_play("exploding_low.gif", win_g_o, 10, 10, 120, 120)

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
                                 # для теста "level": "Normal 23x34"
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
        win_win.geometry(self.get_message_window_geometry(W, H, geometry))

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
        line_num = None
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
        btn1 = CTkButton(frm_2, text="Сохранить имя", command=lambda: \
                                        self.name_enter(list_players[0:19], line_num-1, enabled_cell, win_win, btn1))
        btn1.place(x=180, y=10)

        if line_num>5:
            shift = head_label.cget("height") + (lbl2.cget("height") +2) * (line_num - 2) - 4
            frm_1._parent_canvas.yview_scroll(shift, "units")

        if enabled_cell:
            enabled_cell.configure(state="normal", placeholder_text="Введи своё имя", placeholder_text_color="red",
                                   fg_color="yellow")
            enabled_cell.bind("<Return>", lambda event: \
                                        self.name_enter(list_players[0:19], line_num-1, enabled_cell, win_win, btn1))




        # print(type(win_win))
        # win_win.bind_class("customtkinter.windows.ctk_toplevel.CTkToplevel", "<Leave>", lambda event: print("out"))
        win_win.grab_set()
        win_win.focus_set()
        if self.SOUND_ON:
            winsound.PlaySound('winsound_quite.wav', winsound.SND_FILENAME)

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


    def save_settings_to_file_and_reboot(self, win, *args):
        settings = {}
        settings["level"] = args[0].get()
        settings["rows"] = args[1].get()
        settings["columns"] = args[2].get()
        settings["sound"] = args[3].get()
        self.save_settings_to_JSON(settings)
        win.destroy()
        self.reload_game()

    def reborn_button(self, but):
        copy_but = Sap_button(self.win, but.x, but.y, but.num, text='', width=self.BW, height=self.BH,
                              corner_radius=10, border_width=2, fg_color='grey')
        copy_but.configure(command=lambda b=copy_but: self.click_mouse(b))
        copy_but.bind("<Button-3>", lambda event, b=copy_but: self.r_b_click(b, event))
        self.buttons_list[but.x][but.y] = copy_but
        copy_but.bomba = but.bomba
        copy_but.bombs_around = but.bombs_around
        copy_but.visit = but.visit
        but.destroy()
        copy_but.grid(column=copy_but.y, row=copy_but.x)
        return copy_but

    def check_flags(self):
        """
        Функция проверяет, все ли мины помечены,
        через сравнение списка мин и списка флажков
        Если да, то игра успешно завершается.
        При этом выводится окно верхнего уровня.
        """

        if len(self.list_of_mines) == len(self.flag_list):
            self.list_of_mines.sort()
            self.flag_list.sort()
            count_match = 0
            len_list = len(self.list_of_mines)
            for i in range(len_list):
                if self.list_of_mines[i] == self.flag_list[i]:
                    count_match += 1
            if count_match == len_list:
                self.open_all_buttons(win=True)
                self.game_win_flag = True
                self.show_win_window()

    def r_b_click(self, but: Sap_button, event):
        if not self.first_shoot and not but.visit and not self.game_win_over_flag:
        # если не начало игры, поле не открыто, и игра не окончена
            if self.SOUND_ON:
                winsound.PlaySound('flag.wav', winsound.SND_FILENAME)
            if but.num not in self.flag_list:
                but.configure(image=self.flag_img, state="disabled")


                # canvas = CTkCanvas(self.win, width=25, height=25)
                # canvas.grid(row=but.x, column=but.y)
                # img = ImageTk.PhotoImage(Image.open("flag2.png"))
                # canvas.create_image(25, 25, image=img)
                # # canvas.create_oval(2,2,24,24)
                # canvas.bind("<Button-3>", lambda event: canvas.destroy())

                self.flag_list.append(but.num)

            else:
                self.flag_list.remove(but.num)
                self.reborn_button(but)

            self.label3_update()
            self.check_flags()

    def label3_update(self):
        l = len(self.flag_list)
        if l > self.MINES:
            col = "red"
            fg = "grey10"
        else:
            col = "white"
            fg = "grey65"
        self.label3.configure(fg_color=fg, text_color_disabled=col,
                              text=f"Мины: [ {self.MINES} ] / Флажки: [ {l} ]")

    # def button_animate(self):
    #     if self.HORIZONTAL_ANIM:
    #         for i in range(0, self.STROKI):
    #             for j in range(0, self.STOLBCI):
    #                 but = self.buttons_list[i + 1][j + 1]
    #                 if not but.visit:
    #                     # temp = but.
    #                     but.configure(corner_radius=0)
    #                     but.update()
    #                     time.sleep(0.05)
    #                     but.configure(corner_radius=10)
    #                     but.update()
    #         self.win.after(3000, self.button_animate)
    #     else:
    #         for j in range(0, self.STOLBCI):
    #             for i in range(0, self.STROKI):
    #                 but = self.buttons_list[i + 1][j + 1]
    #                 if not but.visit:
    #                     # temp = but.
    #                     but.configure(corner_radius=0)
    #                     but.update()
    #                     time.sleep(0.05)
    #                     but.configure(corner_radius=10)
    #                     but.update()
    #         self.win.after(3000, self.button_animate)
    #     self.HORIZONTAL_ANIM = not self.HORIZONTAL_ANIM

    def choice_menu(self, option):
        if option == self.menu_command_list[2]:
            self.win.destroy()
        elif option == self.menu_command_list[1]: # Настройки
            self.menu1.set("Меню")
            self.set_win = self.show_settings_window()
        elif option == self.menu_command_list[0]:
            self.menu1.set("Меню")
            self.reload_game()

    def get_current_hard(self):
        for key, value in self.HARD_LEVELS.items():
            if value == self.CURRENT_LEVEL:
                return key

    def create_stage_line(self):

        self.switch0 = CTkSwitch(master=self.win, font=("Arial", 24), text="🔊", onvalue="on", offvalue="off")
        self.switch0.configure(command=self.switch0_event, width=70)
        if self.SOUND_ON:
            self.switch0.select()
        else:
            self.switch0.deselect()
        self.switch0.grid(row=self.STROKI+1, column=1, columnspan=2)

        self.label3 = CTkButton(self.win, text="Выберите первое поле", height=25, width=self.BW * 5,
                                fg_color="gray65", state="disabled", text_color_disabled="white", )
        self.label3.grid(row=self.STROKI+1, column=self.STOLBCI - 4, columnspan=5)


    def create_menu_line(self):

        self.menu_command_list = ["Новая игра", "Настройки", "Выход"]

        self.menu1 = CTkOptionMenu(self.win, width=80, height=25,
                                   values=self.menu_command_list, command=self.choice_menu)
        self.menu1.grid(row=0, column=1, columnspan=2)
        self.menu1.set("Меню")

        self.label1 = CTkButton(self.win, text=f"Сложность:", height=25, width=self.BW * 3,
                                fg_color="gray65", state="disabled", text_color_disabled="white")
        self.label1.grid(row=0, column=self.STOLBCI - 4, columnspan=3)
        self.label2 = CTkButton(self.win, text=f"{self.get_current_hard()}",
                                height=25, width=self.BW * 2, state="normal", text_color_disabled="white",
                                font=("SF Display", 16, "bold"), command=self.show_settings_window)
        self.label2.grid(row=0, column=self.STOLBCI - 1, columnspan=2)

    def draw_buttons(self):
        for i in range(1, self.STROKI + 1):
            for j in range(1, self.STOLBCI + 1):
                but = self.buttons_list[i][j]
                but.grid(column=j, row=i)

    def mines_around(self):
        for i in range(1, self.STROKI + 1):
            for j in range(1, self.STOLBCI + 1):
                but = self.buttons_list[i][j]
                if not but.bomba:
                    count_mines = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if self.buttons_list[i + dy][j + dx].bomba:
                                count_mines += 1

                else:
                    count_mines = -1
                but.bombs_around = count_mines

    def open_all_buttons(self, win=False):
        for i in range(1, self.STROKI + 1):
            for j in range(1, self.STOLBCI + 1):
                but = self.buttons_list[i][j]
                if but.bomba:
                    if not win:
                        but.configure(text='@', fg_color='red', border_width=1, corner_radius=5)
                    else:
                        but.configure(fg_color='white')
                else:
                    if but.bombs_around:
                        txt = but.bombs_around
                        but.configure(text=txt, border_width=1, corner_radius=5, fg_color='white',
                                      text_color_disabled=self.color_dic[txt], state='disabled')
                    else:
                        txt = ""
                        but.configure(text=txt, border_width=1, corner_radius=5, fg_color='white',
                                      state='disabled')

    def click_mouse(self, but: Sap_button):

        if self.SOUND_ON:
            winsound.PlaySound('click.wav', winsound.SND_FILENAME)

        if self.first_shoot:
            self.set_mines(but.num)
            self.mines_around()
            # self.open_all_buttons()
            # self.print_buttons_to_console()
            # self.button_animate()
            self.label3.configure(text="ЛКМ: открыть, ПКМ: флажок")
            self.first_shoot = False

        if but.bomba:  # открыто поле с миной
            but.configure(image=self.bomb_img, text='', fg_color='red', border_width=1,
                          corner_radius=5, state='disabled')
            self.game_over(but)

        else: # в открытом поле нет мины
            if but.bombs_around != 0:   # текст кнопки = количество мин вокруг
                but.visit = True
                txt = but.bombs_around
                but.configure(text=txt, border_width=1, corner_radius=5, fg_color='white',
                              text_color_disabled=self.color_dic[txt], state='disabled')
            else: # открываем всех соседей (алгоритм "поиск в ширину")
                self.search_neighbours(but)

    def game_over(self, but: Sap_button):  # КОНЕЦ ИГРЫ
        for i in range(1, self.STROKI + 1):
            for j in range(1, self.STOLBCI + 1):
                temp_but = self.buttons_list[i][j]
                if temp_but.num in self.flag_list:
                    # temp_but = self.reborn_button(temp_but)
                    if temp_but.num in self.flag_list:
                        temp_but.configure(border_color="blue", border_width=2,)
                if temp_but != but and temp_but.bomba:
                    if temp_but.num in self.flag_list:
                        temp_but.configure(fg_color="green")
                    temp_but.configure(image=self.bomb_img, text='', border_width=2,
                                       corner_radius=5)
                temp_but.configure(state='disabled')
        if len(self.flag_list)>0:
            self.label3.configure(text_color_disabled="blue")
        self.game_win_over_flag = True
        self.show_game_over_window()
        # self.reload_game()

    def search_neighbours(self, but: Sap_button):
        queue = [but]
        while queue:  # цикл отвечает за движение по кнопкам из очереди
            q_but = queue.pop(0)
            but_name = ""
            q_but.visit = True

            if q_but.num in self.flag_list:
                q_but = self.reborn_button(q_but)
                self.flag_list.remove(q_but.num)
                self.label3_update()
                self.check_flags()

            if q_but.bombs_around != 0:
                but_name = q_but.bombs_around
                q_but.configure(text_color_disabled=self.color_dic[but_name])

            else:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        # if abs(i) + abs(j) == 1: # перебор по вертикали и горизонтали
                        new_x = q_but.x + i
                        new_y = q_but.y + j
                        neighbour = self.buttons_list[new_x][new_y]
                        if not neighbour.visit and neighbour not in queue and neighbour.num != 0:
                            queue.append(neighbour)

            q_but.configure(text=but_name, border_width=1, corner_radius=5, fg_color='white', state='disabled')

    def reload_game(self):
        for child in self.win.winfo_children():
            child.destroy()
        self.__init__()
        self.start_game()

    def title_animate(self):
        self.tit_num += 1
        if self.tit_num > 18:
            self.tit_num = 0
        self.win.title(self.title_list[self.tit_num])
        self.win.after(150, self.title_animate)

    def set_mines(self, except_but):
        temp = [i for i in range(1, self.STROKI * self.STOLBCI + 1) if i != except_but]
        self.list_of_mines = sample(temp, k=self.MINES)
        print(self.list_of_mines)
        for i in range(0, self.STROKI + 2):
            for j in range(0, self.STOLBCI + 2):
                but = self.buttons_list[i][j]
                if but.num in self.list_of_mines:
                    but.bomba = True

    # def print_buttons_to_console(self):
    #     for i in self.buttons_list:
    #         print(i)

    def start_game(self):
        self.create_menu_line()
        self.draw_buttons()
        self.create_stage_line()


if __name__ == "__main__":
    game = Saper()
    game.title_animate()
    game.start_game()
    game.win.mainloop()