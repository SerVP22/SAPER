from customtkinter import CTkToplevel, CTkScrollableFrame, CTkFrame, CTkLabel

class HelpWin:

    def show_help_window(self):
        W = 800
        H = 600

        help_win = CTkToplevel(self.win)
        help_win.title("Справка")
        # help_win.resizable(False, False)
        # help_win.attributes("-alpha", 0.9)
        help_win.attributes("-toolwindow", True)
        help_win.attributes("-topmost", True)
        geometry = self.win.geometry()
        help_win.geometry(self.get_toplevel_geometry(W, H, geometry))

        frm_0 = CTkScrollableFrame(help_win)
        frm_0.pack(expand=True, fill="both")

        txt = "Игра SAPER"
        frm_1 = CTkFrame(frm_0, fg_color="white", corner_radius=10, width=200, height=50)
        frm_1.pack(padx=200, expand=False, )

        CTkLabel(frm_1, text=txt, width=180, height=30,
                 corner_radius=10, bg_color="blue").pack(expand=True, fill="x")






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