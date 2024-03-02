from Tkinter import *

class test(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.make()
        self.grid()

    def make(self):
        self.canvas = Canvas(
            self,width=500,height=500,bg='white'
            )
        self.canvas.grid()


root = Tk()
derp = test(root)
root.mainloop()
