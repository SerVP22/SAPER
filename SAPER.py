import json
import customtkinter
import pygame

import tkinter as tk
from random import sample
from Buttons import Sap_button
from customtkinter import CTk, CTkOptionMenu, CTkButton, CTkImage, CTkSwitch

from Mes_Windows import MesWindows
from PIL import Image
import sys



class Saper(MesWindows):
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
    customtkinter.set_appearance_mode("light")

    try:
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        sound_boom = pygame.mixer.Sound("sounds/boom.wav")
        sound_win = pygame.mixer.Sound("sounds/win.wav")
        sound_click = pygame.mixer.Sound("sounds/click.wav")
        sound_flag = pygame.mixer.Sound("sounds/flag.wav")
    except Exception as ex:
        sound_click = sound_boom = sound_win = sound_flag = False
        print(ex)

    try:
        win.iconbitmap(tk.PhotoImage('images/bomb4.ico'))
    except Exception as ex:
        print(ex)

    BW = 40  # Ширина кнопки
    BH = 40  # Высота кнопки

    try:
        flag_img = CTkImage(light_image=Image.open("images/flag2.png"),
                            dark_image=Image.open("images/flag2.png"), size=(16, 16))
        bomb_img = CTkImage(light_image=Image.open("images/bomb.png"),
                            dark_image=Image.open("images/bomb.png"), size=(25, 25))
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
        self.gif_loop = False

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
                self.set_bindings_for_btn(but)
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
        except Exception as ex:
            print(ex)

    def btn_anim(self, lst: list):
        def normal(lst): #восстанавливает стандартные значения
            for i in lst:
                i.configure(corner_radius=10, fg_color='grey')

        for i in lst:
            i.configure(corner_radius=5, fg_color='grey80')

        self.win.after(250, lambda: normal(lst))



    def middle_btn_click(self, btn):
        lst = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_x = btn.x + i
                new_y = btn.y + j
                neighbour = self.buttons_list[new_x][new_y]
                if not neighbour.visit:
                    lst.append(neighbour)
        self.btn_anim(lst)


    def set_bindings_for_btn(self, btn:Sap_button):
        if btn.visit:
            if btn.bombs_around>0:
                btn.bind("<Button-2>", lambda event, b=btn: self.middle_btn_click(b))
                btn.bind("<ButtonPress>", lambda event, b=btn: self.visit_button_press(event, b))
        else:
            btn.configure(command=lambda b=btn: self.click_mouse(b))
            btn.bind("<Button-3>", lambda event, b=btn: self.right_btn_click(b))

    def open_neighbours(self, btn):
        success_flag = True
        bombs_list = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                new_x = btn.x + i
                new_y = btn.y + j
                neighbour = self.buttons_list[new_x][new_y]
                if (not neighbour.visit) and (neighbour.num !=0 ) and (neighbour.num not in self.flag_list):

                    if neighbour.bomba:  # открыто поле с миной
                        neighbour.configure(image=self.bomb_img, text='', fg_color='red', border_width=1,
                                      corner_radius=5, state='disabled')
                        neighbour.visit = True
                        success_flag = False
                        bombs_list.append(neighbour)

                    else:  # в открытом поле нет мины
                        if neighbour.bombs_around != 0:  # текст кнопки = количество мин вокруг
                            neighbour.visit = True
                            txt = neighbour.bombs_around
                            neighbour.configure(text=txt, border_width=1, corner_radius=5, fg_color='white',
                                          text_color_disabled=self.color_dic[txt], state='disabled')
                            self.set_bindings_for_btn(neighbour)
                        else:  # открываем всех соседей (алгоритм "поиск в ширину")
                            self.search_neighbours(neighbour)

        if not success_flag:
            self.game_over(bombs_list)


    def visit_button_press(self, event, but):
        if "Mod1|Button1 num=3" in str(event): # проверка на одновременное нажатие правой и левой кнопки мыши
            self.open_neighbours(but)

    def reborn_button(self, but):
        copy_but = Sap_button(self.win, but.x, but.y, but.num, text='', width=self.BW, height=self.BH,
                              corner_radius=10, border_width=2, fg_color='grey')
        self.set_bindings_for_btn(copy_but)
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
        При этом выводится окно успешного конца игры.
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
                self.game_win_over_flag = True
                self.show_win_window()

    def right_btn_click(self, but: Sap_button):
        if not self.first_shoot and not but.visit and not self.game_win_over_flag:
        # если не начало игры, поле не открыто, и игра не окончена
            if self.SOUND_ON and self.sound_flag:
                self.sound_flag.play()
            if but.num not in self.flag_list:
                self.flag_list.append(but.num)
                but.configure(image=self.flag_img, state="disabled")
                but._image_label.bind("<Button-3>", lambda event, b=but: self.right_btn_click(b))

            else:
                self.flag_list.remove(but.num)
                self.reborn_button(but)

            self.status_bar_update()
            self.check_flags()

    def status_bar_update(self):
        l = len(self.flag_list)
        if l > self.MINES:
            col = "red"
            fg = "grey10"
        else:
            col = "white"
            fg = "grey65"
        self.label3.configure(fg_color=fg, text_color_disabled=col,
                              text=f"Мины: [ {self.MINES} ] / Флажки: [ {l} ]")



    def choice_menu(self, option):
        if option == self.menu_command_list[4]: # Выход
            self.win.destroy()
        elif option == self.menu_command_list[1]: # Помощь
            self.menu1.set("Меню")
            pass
        elif option == self.menu_command_list[2]: # Топ-20 игроков
            self.menu1.set("Меню")
            self.show_top_players()
        elif option == self.menu_command_list[3]: # Настройки
            self.menu1.set("Меню")
            self.set_win = self.show_settings_window()
        elif option == self.menu_command_list[0]: # Новая игра
            self.menu1.set("Меню")
            self.reload_game()

    def get_current_hard(self):
        for key, value in self.HARD_LEVELS.items():
            if value == self.CURRENT_LEVEL:
                return key

    def create_status_bar(self):

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

        self.menu_command_list = ["•  Новая игра", "?  Помощь" , "↑  Топ-20 игроков", "↕  Настройки", "↓  Выход"]

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

    def draw_all_buttons(self):
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
        """
        Функция срабатывает при нажатии на кнопку-поле левой кнопкой мыши.
        При открытии стартового поля расставляются мины по всему игровому полю.
        При попадании в заминированое поле вызывает конец игры.
        Иначе: "открывает" поле и устанавливает название для поля равное количеству мин вокруг.
        Если мин вокруг равно 0, то запускается алгоритм поиска в ширину,
        который открывает "пустые" соседние поля

        :param but: принимает объект кнопки Sap_button
        :return: None
        """

        if self.SOUND_ON and self.sound_click:
            self.sound_click.play()

        if self.first_shoot:

            self.set_mines(but.num)
            self.mines_around()
            # self.open_all_buttons()
            # self.print_buttons_to_console()

            self.label3.configure(text="ЛКМ: открыть, ПКМ: флажок")
            self.first_shoot = False

        if but.bomba:  # открыто поле с миной
            but.configure(image=self.bomb_img, text='', fg_color='red', border_width=1,
                          corner_radius=5, state='disabled')
            list_but = [but]
            self.game_over(list_but)

        else: # в открытом поле нет мины
            if but.bombs_around != 0:   # текст кнопки = количество мин вокруг
                but.visit = True
                txt = but.bombs_around
                but.configure(text=txt, border_width=1, corner_radius=5, fg_color='white',
                              text_color_disabled=self.color_dic[txt], state='disabled')
                self.set_bindings_for_btn(but)
            else: # открываем всех соседей (алгоритм "поиск в ширину")
                self.search_neighbours(but)

    def game_over(self, but_list: list):  # КОНЕЦ ИГРЫ
        for i in range(1, self.STROKI + 1):
            for j in range(1, self.STOLBCI + 1):
                temp_but = self.buttons_list[i][j]
                if temp_but.num in self.flag_list:
                    # temp_but = self.reborn_button(temp_but)
                    if temp_but.num in self.flag_list:
                        temp_but.configure(border_color="blue", border_width=2,)
                if temp_but not in but_list and temp_but.bomba:
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
        while queue:  # цикл отвечает за перебор полей из очереди
            q_but = queue.pop(0)
            but_name = ""
            q_but.visit = True

            if q_but.num in self.flag_list: # флаг отмечен неправильно
                q_but = self.reborn_button(q_but)
                self.flag_list.remove(q_but.num)
                self.status_bar_update()
                self.check_flags()

            if q_but.bombs_around != 0:
                but_name = q_but.bombs_around
                q_but.configure(text_color_disabled=self.color_dic[but_name])

            else:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        new_x = q_but.x + i
                        new_y = q_but.y + j
                        neighbour = self.buttons_list[new_x][new_y]
                        if (not neighbour.visit) and (neighbour not in queue) and (neighbour.num != 0):
                            queue.append(neighbour)

            q_but.configure(text=but_name, border_width=1, corner_radius=5, fg_color='white', state='disabled')
            self.set_bindings_for_btn(q_but)
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
        # print(self.list_of_mines)
        for i in range(0, self.STROKI + 2):
            for j in range(0, self.STOLBCI + 2):
                but = self.buttons_list[i][j]
                if but.num in self.list_of_mines:
                    but.bomba = True

    def print_buttons_to_console(self):
        for i in self.buttons_list:
            print(i)

    def start_game(self):
        self.create_menu_line()
        self.draw_all_buttons()
        self.create_status_bar()


if __name__ == "__main__":
    game = Saper()
    game.title_animate()
    game.start_game()
    game.win.mainloop()