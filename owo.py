# 31234
# 32134



from tkinter import Button, Tk, HORIZONTAL

from tkinter.ttk import Progressbar
import time
import threading

class MonApp(Tk):
    def __init__(self):
        super().__init__()


        self.btn = Button(self, text='Traitement', command=self.traitement)
        self.btn.grid(row=0,column=0)
        self.progress = Progressbar(self, orient=HORIZONTAL,length=100,  mode='indeterminate')


    def traitement(self):
        def real_traitement():
            self.progress.grid(row=1,column=0)
            self.progress.start()
            time.sleep(5)
            self.progress.stop()
            self.progress.grid_forget()

            self.btn['state']='normal'

        self.btn['state']='disabled'
        threading.Thread(target=real_traitement).start()

if __name__ == '__main__':

    app = MonApp()
    app.mainloop()