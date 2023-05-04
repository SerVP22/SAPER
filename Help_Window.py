from customtkinter import CTkToplevel, CTkScrollableFrame, \
                            CTkFrame, CTkLabel, CTkButton, CTkTextbox
import tkinter as tk
import psutil

class HelpWin:
    def change_title(self, win):
        win.title(win.geometry())

    def show_help_window(self):
        W = 460
        H = 400

        help_win = CTkToplevel(self.win)
        help_win.title("Справка")
        help_win.resizable(False, True)
        # help_win.attributes("-alpha", 0.9)
        if psutil.WINDOWS:
            help_win.attributes("-toolwindow", True)
        help_win.attributes("-topmost", True)
        geometry = self.win.geometry()
        help_win.geometry(self.get_toplevel_geometry(W, H, geometry))

        frm_0 = CTkScrollableFrame(help_win)
        frm_0.pack(expand=True, fill="both")



        txt = "Игра SAPER"
        lbl1 = CTkButton(frm_0, text=txt, width=280, height=50, corner_radius=10,
                         text_color="black", font=("Arial", 20, ), fg_color="transparent" )
        if self.bomb_img:
            lbl1.configure(image=self.bomb_img, hover=False, compound="left", border_spacing=5)

        lbl1.pack()
        tb1 = CTkTextbox(frm_0, width=350, height=180, fg_color="grey90", corner_radius=10, )
        tb1.insert("0.0", """
                                          ПРАВИЛА ИГРЫ.
                        
        Для победы в игре необходимо пометить флажками все
мины на игровом поле. 
        Чтобы начать игру, нужно левой клавишей мыши кликнуть
в любую клетку на игровом поле.
        Если в соседних клетках от первоначальной есть мины,
то в клетке отображается их количество.         <соседи>
        """)
        tb1.configure(state="disabled")
        tb1.pack(fill=tk.X, padx=10)
        # frm_1 = CTkFrame(frm_0, fg_color="red", corner_radius=10, width=600, height=50)
        # frm_1.pack()
        # lbl2 = CTkLabel(frm_1, text=txt, width=280, height=50,
        #                 corner_radius=10, bg_color="green")
        # lbl2.pack(fill=tk.BOTH)
        #
        #

        # lbl1.bind("<Button-1>", lambda event: help_win.title(help_win.geometry()))





        # print(type(help_win))
        # help_win.bind_class("customtkinter.windows.ctk_toplevel.CTkToplevel", "<Leave>", lambda event: print("out"))
        help_win.grab_set()
        help_win.focus_set()

        """
                        
        ПРАВИЛА ИГРЫ.
            
            Для победы в игре необходимо пометить флажками все мины на игровом поле. 
        Чтобы начать игру, нужно левой клавишей мыши кликнуть в любую клетку на игровом поле.
        Если в соседних клетках от первоначальной есть мины, то в клетке отображается их количество. 
        <соседи>
        """
        """
            Если в соседних клетках нет мин, то клетка останется пустой.
        Если у клетки в соседях есть другие пустые клетки, а у тех, в свою очередь, свои,
        то все такие клетки откроютсятся автоматически.
        По похожему принципу происходит происходят открытия в остальных клетках на игровом поле.
        Но с одним отличием: в любой из клеток может оказаться мина.
        Если открыть клетку с миной, то произойдет взрыв и игра закончится.
        Для успешного прохождения игры необходимо, ориентируясь на количество мин в открытых клетках,
        пометить флажками все заминированые клетки.
        """
        """
        НАСТРОЙКИ
        """
        """
        УПРАВЛЕНИЕ
        """