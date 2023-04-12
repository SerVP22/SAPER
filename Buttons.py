from customtkinter import CTkButton, CTkFont


class SapButton(CTkButton):

    def __init__(self, master, x, y, num, *args, **kwargs):
        self.x = x
        self.y = y
        self.num = num
        super().__init__(master, *args, font=CTkFont(size=20, weight="bold"), **kwargs)
        self.bomba = False
        self.bombs_around = 0
        self.visit = False

    def __repr__(self):
        if self.bomba:
            # return f"BOMB {self.num:2} ({self.x},{self.y})"
            return f"({self.x},{self.y})[ BOMB ]"
        else:
            #  return f".... {self.num:2} ({self.x},{self.y})"
            return f"({self.x},{self.y})[\033[31mn{self.num:2} \033[32mb{self.bombs_around}\033[0m]"
