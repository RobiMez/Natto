import os
import requests
import threading
import socket

import concurrent.futures

from tkinter import *
from tkinter import ttk

from PIL import Image
from pathlib import Path
from hentai import Hentai,Format

print('\n\n\n\n\n\n\n\n\n')
print('\n| ---- [ OK ] Imports \n')

class natto():
    def __init__(self):
        print('\n| ---- [ OK ] Class inititation \n')
        self.initialize_TPE()
        self.add_new_thread(self.check_netbeat)
        self.start_ui()

    def start_ui(self):
        self.app_init()
        print('\n| ---- [ OK ] Ui Started \n')
        self.start_mainloop()



    def app_init(self):
        self.root = Tk()
        app_width = 820
        app_height = 740
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (app_width/2)
        y = (screen_height / 2) - (app_height/2)
        # window size and positioning
        self.root.geometry(f'{app_width}x{app_height}+{int(x/2)}+{int(y/2)}')
        self.root.title('Natto | Stay Degenerate ')

    def check_cwd(self):
        # Check current filesys directory 
        wd = Path.cwd()
        print("Working directory : ",Path.cwd())
        hentai_folder_exists = Path.exists(Path.joinpath(wd,'./hentai'))
        if hentai_folder_exists == False:
            print("Can't find the Hentai folder near me \n  Creating one at the current working directory ...")
            os.mkdir('hentai')
        else : 
            print("Hentai folder exists , All good .")
        print('\n| ---- [ OK ] Filesystem \n')
    def add_ui_elements(self):
        # cover_image = PhotoImage(file='def.png')
        cover = Label(self.root, text="Cover image here")
        cover_pos_x = (app_width/4)
        cover.place(x=cover_pos_x-50, y=0, relwidth=1, relheight=1)
        
        sauce_frame = LabelFrame(self.root, text='Sauwuce', padx=10, pady=10)
        sauce_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
        sauce_entry = Entry(sauce_frame, width=25)
        sauceify = Button(sauce_frame, text="Natto !", command=sauce_poured)
        sauce_entry.bind('<KeyPress-Return>',on_enter)
        
        sauce_stat =  StringVar()
        sauce_stat.set('Type a 5 or 6 digit sauce and Natto')
        sauce_stat_label = Label(sauce_frame, textvar=sauce_stat,wraplength=250, justify="center")
        sauce_stat_label.grid(row=1, column=0, sticky="W")
        
        sauce_entry.grid(row=0, column=0, sticky="W")
        sauceify.grid(row=0, column=1, sticky="E", padx=5, pady=5)
        
        download_frame = LabelFrame(self.root, text='Dload', padx=10, pady=10)
        download_frame.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")
        download_dou = Button(download_frame, text="Swallow !", command=download_dou_callback)
        download_dou.grid(row=0,column=0)

        # description frame 
        details_frame = LabelFrame(self.root, text='Doujin Data', padx=10, pady=10)
        details_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NESW")

        #  Sauce 
        sauce_id = StringVar()
        sauce_id.set('000000')
        sauce_label = Label(details_frame, textvar=sauce_id,wraplength=250, justify="left")
        sauce_label.grid(row=0, column=0, sticky="W")
        # Pretty title
        title = StringVar()
        title.set('Title')
        title_label = Label(details_frame, textvar=title,wraplength=250, justify="left")
        title_label.grid(row=1, column=0, sticky="W")
        # Japaneese title
        title_jp = StringVar()
        title_jp.set('Title')
        title_jp_label = Label(details_frame, textvar=title_jp,wraplength=250, justify="left")
        title_jp_label.grid(row=2, column=0, sticky="W")
        # English title
        title_en = StringVar()
        title_en.set('Title')
        title_en_label = Label(details_frame, textvar=title_en,wraplength=250, justify="left")
        title_en_label.grid(row=3, column=0, sticky="W")
        #  Number of pages 
        pages = StringVar()
        pages.set('Pages')
        pages_label = Label(details_frame, textvar=pages,wraplength=250, justify="left")
        pages_label.grid(row=4, column=0, sticky="W")
        # Tags
        tags = StringVar()
        tags.set('Tags')
        tags_label = Label(details_frame, textvar=tags,wraplength=250, justify="left")
        tags_label.grid(row=5, column=0, sticky="W")
        
        print("Ui Started ...")

    def api_call(self):
        print('System call : API')
        sauce = sauce_entry.get()
        hentai_exists = Hentai.exists(sauce)
        try:
            if hentai_exists :
                dou = Hentai(sauce)
                print(sauce)
                print(dou)
                return dou
            else:
                sauce_stat.set('Bad sauce ')
        except TypeError as e : 
            print(e)
            sauce_stat.set('Temporary error ... Try again.')

    def download_dou_callback(self):
        def download_pages (): 
            print('🧪 System call : Swallow initiated   ')
            dou = api_call()
            download_dir = './hentai'
            os.mkdir(download_dir + f'/{dou.title(Format.Pretty)}')
            images = dou.image_urls
            counter = 0
            for image in images : 
                im = Image.open(requests.get(image, stream=True).raw) 
                im.save(f"{download_dir}/{dou.title(Format.Pretty)}/{counter}.png")
                print('drip')
                counter = counter + 1
        # threading.Thread(target=download_pages).start()
        # download_dou.config(text="Downloading ... i hope ")
        # print('started dat in another thred')
    
    def sauce_poured (self):
        print('🧪 System call : Sauce Poured  ')
        hope = True
        while hope : 
            try:
                dou = api_call()
                print(dou.image_urls)
                update_cover(dou)
                update_desc(dou)
                update_button(dou)
                sauce_stat.set('Saucing ')
                hope = False
            except TypeError as e :
                print('mini stroke ',e)

    def update_cover(self,dou):
        print('🧪 System call : Update cover ')
        basewidth = 470
        im = Image.open(requests.get(dou.thumbnail, stream=True).raw)
        wpercent = (basewidth/float(im.size[0]))
        hsize = int((float(im.size[1])*float(wpercent)))
        im = im.resize((basewidth,hsize), Image.ANTIALIAS)
        im.save('cover.png')
        print(' System notice : Cover downloaded ')
        new_cover_image = PhotoImage(file='cover.png')
        cover.config(image=new_cover_image)
        cover.image = new_cover_image
        print(' System notice : Cover Changed ')
        sauce_stat.set('Sauce poured')

    def update_button(self,dou):
        print('System call : Update button ')
        sauce_frame.config(bg='whitesmoke')
        sauce_entry.config(bg='honeydew')
        sauceify.config(bg='azure')
        
    def update_desc(self,dou):
        print('System call : Update description ')
        sauce_id.set(dou.id)
        title.set(dou.title(format=Format.Pretty))
        title_jp.set(dou.title(format=Format.Japanese))
        title_en.set(dou.title(format=Format.English))
        pages.set(dou.num_pages)
        tag_names = 'Tags : '

        for tag in dou.tag:
            tag_names = tag_names + tag.name + ' | '
            print(tag.name)
        tags.set(tag_names)
        print(dou.json)
        print(dou.title(format=Format.Pretty))

    def on_enter(self,e):
        sauce_poured()

    def start_mainloop(self):
        self.root.mainloop()
    
    def check_netbeat(self):
        hb = True   
        while hb:
            try:
                hentai_sane = Hentai.exists(177013)
                print(f'Hentai Heartbeat : {hentai_sane}')
                return True
            except TypeError as e:
                print('Flat line : ',e)
                return False
            except requests.exceptions.ConnectionError:
                return False
        
    def initialize_TPE(self):
        with concurrent.futures.ThreadPoolExecutor() as self.executor:
            print('starting a new thread to check for a netbeat')
            f1  = self.executor.submit(self.check_netbeat())
            print('done')
    def add_new_thread(self,func):
        print(f"Adding {func} to the Executor")
        f = self.executor.submit(func)
        return f


nat = natto()






