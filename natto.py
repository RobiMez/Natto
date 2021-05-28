# ... and he said " let there be time " python line 2:12
import time

import logging
import os
import requests
import threading
import socket
import sys

from tkinter import *
from tkinter import ttk

from PIL import Image
from pathlib import Path
from hentai import Hentai,Format

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [ %(threadName)s ] [ %(levelname)s ] %(message)s",
    handlers=[
        logging.FileHandler("debug.log",mode='w',encoding=None,delay=False),
        logging.StreamHandler()
    ]
)

print('\n\n\n\n\n\n\n\n\n')
logging.info('Imports done ')
class natto():
    def __init__(self):
        self.start_ui()
        logging.info('UI Shutdown...')
        
    def sanitize_foldername(self, folder_dirty):
        
        folder_clean = folder_dirty.replace("?","")
        folder_clean = folder_clean.replace(">","")
        folder_clean = folder_clean.replace("<","")
        folder_clean = folder_clean.replace("\\","")
        folder_clean = folder_clean.replace("/","")
        folder_clean = folder_clean.replace("*","")
        folder_clean = folder_clean.replace("|","")
        folder_clean = folder_clean.replace(":","")
        folder_clean = folder_clean.replace("\"","")

        print(folder_dirty)
        print(folder_clean)
        return folder_clean
    
    def start_ui(self):
        self.app_init()
        self.add_ui_elements()
        logging.info('UI Started.')
        self.start_mainloop()

    def app_init(self):
        self.root = Tk()
        self.app_width = 820
        self.app_height = 740
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (self.app_width/2)
        y = (screen_height / 2) - (self.app_height/2)
        # window size and positioning
        self.root.geometry(f'{self.app_width}x{self.app_height}+{int(x/2)}+{int(y/2)}')
        self.root.title('Natto | Stay Degenerate ')
        self.check_cwd()

    def check_cwd(self):
        # Check current filesys directory 
        wd = Path.cwd()
        logging.info('Working dir : %s',wd)
        hentai_folder_exists = Path.exists(Path.joinpath(wd,'./hentai'))
        logging.info('Hentai folder : %s',hentai_folder_exists)
        if hentai_folder_exists == False:
            print("Can't find the Hentai folder near me \n  Creating one at the current working directory ...")
            os.mkdir('hentai')
        else : 
            logging.info("Hentai folder exists , All good .")

        return True

    def add_ui_elements(self):
        # cover_image = PhotoImage(file='def.png')
        self.cover = Label(self.root, text=" --- Cover image --- ")
        cover_pos_x = (self.app_width/4)
        self.cover.place(x=cover_pos_x-50, y=0, relwidth=1, relheight=1)
        
        self.sauce_frame = LabelFrame(self.root, text='Sauce.', padx=10, pady=10)
        self.sauce_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
        self.sauce_entry = Entry(self.sauce_frame, width=25)
        self.sauce_entry.grid(row=0, column=0, sticky="W")
        self.sauce_entry.bind('<KeyPress-Return>',self.on_enter)
        self.sauce_search_button = Button(self.sauce_frame, text="Search !", command=self.sauce_poured)
        self.sauce_search_button.grid(row=0, column=1, sticky="E", padx=5, pady=5)
        
        self.sauce_stat =  StringVar()
        self.sauce_stat.set('Type Sauce and Search.')
        self.sauce_stat_label = Label(self.sauce_frame, textvar=self.sauce_stat,wraplength=250, justify="center")
        self.sauce_stat_label.grid(row=1, column=0, sticky="W")
        
        self.download_frame = LabelFrame(self.root, text='', padx=10, pady=10)
        self.download_frame.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")
        self.download_button = Button(self.download_frame, text="Download", command=self.download_button_callback)
        self.download_button.grid(row=0,column=0,sticky="NSEW")
        self.download_status = StringVar()
        self.download_status.set('-------------------')
        self.download_status_label = Label(self.download_frame, textvar=self.download_status)
        self.download_status_label.grid(row=1,column=0,sticky='W')


        # description frame 
        details_frame = LabelFrame(self.root, text='Doujin Data', padx=10, pady=10)
        details_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NESW")

        #  Sauce 
        self.sauce_id = StringVar()
        self.sauce_id.set('#177013')
        self.sauce_label = Label(details_frame, textvar=self.sauce_id,wraplength=250, justify="left")
        self.sauce_label.grid(row=0, column=0, sticky="W")
        # Pretty title
        self.title = StringVar()
        self.title.set('Doujin Title : ')
        self.title_label = Label(details_frame, textvar=self.title,wraplength=250, justify="left")
        self.title_label.grid(row=1, column=0, sticky="W")
        # Japaneese title
        self.title_jp = StringVar()
        self.title_jp.set('Japaneese Title : ')
        self.title_jp_label = Label(details_frame, textvar=self.title_jp,wraplength=250, justify="left")
        self.title_jp_label.grid(row=2, column=0, sticky="W")
        # English title
        self.title_en = StringVar()
        self.title_en.set('English Title : ')
        self.title_en_label = Label(details_frame, textvar=self.title_en,wraplength=250, justify="left")
        self.title_en_label.grid(row=3, column=0, sticky="W")
        #  Number of pages 
        self.pages = StringVar()
        self.pages.set('Number of Pages : ')
        self.pages_label = Label(details_frame, textvar=self.pages,wraplength=250, justify="left")
        self.pages_label.grid(row=4, column=0, sticky="W")
        # Tags
        self.tags = StringVar()
        self.tags.set('Tags : ')
        self.tags_label = Label(details_frame, textvar=self.tags,wraplength=250, justify="left")
        self.tags_label.grid(row=5, column=0, sticky="W")
        

    
    def get_doujin_data(self):
        print('| ---- [Syscall] Get doujin data.')
        self.current_doujin = None
        sauce = self.sauce_entry.get()
        if sauce == '':
            self.sauce_stat.set('Gib sauce.')
        else :
            
            hentai_exists = Hentai.exists(sauce)
            hope = True
            while hope:
                try:
                    if hentai_exists :
                        dou = Hentai(sauce)
                        print(sauce)
                        print(dou)
                        hope = False
                        self.current_doujin = dou
                        return dou
                    else:
                        self.sauce_stat.set('Bad sauce ')
                        return False
                except:
                    self.sauce_stat.set('Temporary error ... Trying again.')
                    return False
        return False

    def download_button_callback(self):
        dou = self.current_doujin
        print('| ---- [ JOB ] Download requested ')
        def download_pages ():
            hope  = True
            while hope:
                print('Retrying ')
                try:
                    dou.download(Path.cwd())
                    hope = False
                except Exception as e : 
                    print('Internal chaos ',e)

        print('| ---- [ JOB ] Download done ')

        t1 = threading.Thread(target=download_pages)
        t1.start()



        self.download_button.config(text="Downloading ... ? ")

        # print('started dat in another thred')
    
    def sauce_poured (self):
        print('🧪 System call : Sauce Click  ')

        for trial in range(10): 
            try:
                dou = self.get_doujin_data()
                if dou != False: 
                    print(dou.image_urls)
                    self.update_cover(dou)
                    self.update_desc(dou)
                    self.update_button(dou)
                    self.sauce_stat.set('Fetched data ')
                    break

            except TypeError as e :
                print(f'Temporary error ... Retrying {trial+1}/10',e)
                self.sauce_stat.set(f'Network error ... ')
                
                # with concurrent.futures.ThreadPoolExecutor() as self.executor:
                #     self.executor.submit(update_sauce_stat)
    
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
        self.cover.config(image=new_cover_image)
        self.cover.image = new_cover_image
        print(' System notice : Cover Changed ')
        self.sauce_stat.set('Sauce poured')

    def update_button(self,dou):
        print('System call : Update button ')
        self.sauce_frame.config(bg='whitesmoke')
        self.sauce_entry.config(bg='honeydew')
        self.sauce_search_button.config(bg='azure')
    
    def update_desc(self,dou):
        print('System call : Update description ')
        self.sauce_id.set(dou.id)
        self.title.set(dou.title(format=Format.Pretty))
        self.title_jp.set(dou.title(format=Format.Japanese))
        self.title_en.set(dou.title(format=Format.English))
        self.pages.set(dou.num_pages)
        tag_names = 'Tags : '

        for tag in dou.tag:
            tag_names = tag_names + tag.name + ' | '
            print(tag.name)
        self.tags.set(tag_names)
        print(dou.json)
        print(dou.title(format=Format.Pretty))

    def on_enter(self,e):
        self.sauce_poured()

    def start_mainloop(self):
        def test_sleep():
            for _ in range(5):
                print('Starting sleep')
                time.sleep(1)
                print('Stopping sleep')
        
        # tmain = threading.Thread(target=test_sleep)
        # print('threaded sleep')
        # tmain.start()
        self.root.mainloop()



if __name__ == '__main__' :
    nat = natto()






