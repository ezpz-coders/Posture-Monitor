from tkinter import *
win = Tk()
gui = Tk(win)
win.geometry("500x500")
b = Button(win, text = "Start")
b.pack()

b2 = Button(win, text = "Stop")
b2.pack()
w1 = Scale(win, from_=0, to=10, orient=HORIZONTAL)
w1.pack()
w2 = Scale(win, from_=0, to=10, orient=HORIZONTAL)
w2.pack()

win.mainloop()
