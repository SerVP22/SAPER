import customtkinter


class LoginWindow(customtkinter.CTkToplevel):
    def __init__(self, login_command, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x200")
        self.title("login window")

        self.button_1 = customtkinter.CTkButton(self, text="login", command=login_command)
        self.button_1.pack(side="top", padx=20, pady=20)


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")
        self.title("main window")

        self.label_1 = customtkinter.CTkLabel(self, text="main app")
        self.label_1.pack(side="top", padx=20, pady=20)

        self.withdraw()  # hide main window
        self.login_window = LoginWindow(self.login)  # create login window and pass self.login() method

    def login(self):
        self.login_window.destroy()
        self.deiconify()  # make window visible


if __name__ == "__main__":
    app = App()
    app.mainloop()