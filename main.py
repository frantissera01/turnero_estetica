import tkinter as tk
from views.main_view import MainView

def main():
    root = tk.Tk()
    root.title("Turnero Estética")
    root.geometry("800x600")
    MainView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
 