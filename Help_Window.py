from customtkinter import CTkToplevel, CTkScrollableFrame, \
                            CTkImage, CTkLabel, CTkButton, CTkTextbox, CTkFrame
import tkinter as tk
import psutil
from PIL import Image

class HelpWin:
    def show_help_window(self):
        W = 460
        H = 450

        help_win = CTkToplevel(self.win)
        help_win.title("Справка")
        help_win.resizable(False, True)
        # help_win.attributes("-alpha", 0.9)
        if psutil.WINDOWS:
            help_win.attributes("-toolwindow", True)
        help_win.attributes("-topmost", True)
        geometry = self.win.geometry()
        help_win.geometry(self.get_toplevel_geometry(W, H, geometry))

        try:
            h00_img = CTkImage(dark_image=Image.open("images/h00.png"))
            im_size = h00_img._dark_image.size
            h00_img = CTkImage(light_image=Image.open("images/h00.png"),
                                dark_image=Image.open("images/h00.png"), size=im_size)
            h01_img = CTkImage(dark_image=Image.open("images/h01.png"))
            im_size = h01_img._dark_image.size
            h01_img = CTkImage(light_image=Image.open("images/h01.png"),
                               dark_image=Image.open("images/h01.png"), size=im_size)
        except Exception as msg:
            h00_img = h01_img = None
            print(msg)

        # главный фрейм окна

        frm_0 = CTkScrollableFrame(help_win)
        frm_0.pack(expand=True, fill="both")

        # заголовок

        lbl1 = CTkButton(frm_0, text="Игра SAPER", width=280, height=50, corner_radius=10,
                         text_color="black", font=("Arial", 20, ), fg_color="transparent" )
        if self.bomb_img:
            lbl1.configure(image=self.bomb_img, hover=False, compound="left", border_spacing=5)
        lbl1.grid(row=0, column=1, columnspan=8)

        # текстовый блок 1

        tb1 = CTkTextbox(frm_0, width=420, height=145, fg_color="grey90", corner_radius=10, )
        tb1.insert("0.0", """\t\t            ПРАВИЛА ИГРЫ.

        Для  победы  в  игре  необходимо  пометить  флажками  все
мины на игровом поле.
        Чтобы начать игру, нужно левой клавишей мыши кликнуть
в любую клетку на игровом поле.
        Если  в  соседних  клетках  от  первоначальной  есть  мины,
то в клетке отображается их количество.""")
        tb1.configure(state="disabled")
        tb1.grid(row=1, column=0, columnspan=10, padx=10, pady=10)

        # рисунок 1 и рисунок 2

        if h00_img and h01_img:
            CTkLabel(frm_0, image=h00_img,text="" ).grid(row=2, column=0, columnspan=6, padx=10, pady=5)
            CTkLabel(frm_0, image=h01_img, text="").grid(row=2, column=6, columnspan=4, padx=10, pady=5,
                                                         sticky="e")

        # текстовый блок 2

        tb2 = CTkTextbox(frm_0, width=420, height=190, fg_color="grey90", corner_radius=10, )
        tb2.insert("0.0",
        """         Если   в   соседних  клетках  мин  нет,  то   в   таком  случае 
клетка останется пустой.   Если у клетки в соседях есть другие 
пустые клетки, а у тех,  в свою очередь, свои, то все эти клетки 
откроются автоматически. По похожему принципу происходят
открытия в остальных клетках  на  игровом  поле.  Но  с  одним
отличием:  в  любой  из  клеток  может  оказаться  мина.  Если 
открыть   клетку   с   миной,   то   произойдет   "взрыв"    и   игра 
закончится.
         Для   успешного   прохождения  игры  SAPER  необходимо, 
ориентируясь    на    количество    мин    в   открытых    клетках, 
пометить флажками все заминированые клетки.""")
        tb2.configure(state="disabled")
        tb2.grid(row=3, column=0, columnspan=10, padx=10, pady=10)

        # frm_1 = CTkFrame(frm_0, fg_color="red", corner_radius=10, width=600, height=50)
        # frm_1.pack()
        # lbl2 = CTkLabel(frm_1, text=txt, width=280, height=50,
        #                 corner_radius=10, bg_color="green")
        # lbl2.pack(fill=tk.BOTH)
        #
        #

        # lbl1.bind("<Button-1>", lambda event: help_win.title(help_win.geometry()))
        print(frm_0.grid_size())




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