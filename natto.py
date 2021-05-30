# ... and he said " let there be time " python line 2:12
import time

import logging
import os
import requests
import threading
import socket
import sys
from random import randint



from tkinter import *
from tkinter import ttk

from PIL import Image
from pathlib import Path
from hentai import Hentai,Format

logging.basicConfig(
    level=logging.DEBUG,
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
        # logging.info('UI Shutdown...')
        # self.current_doujin = ''
        pass

    
    def simulate_io(self,secs):
        logging.info('Simulating IO operation , sleeping for %s second(s)',secs)
        time.sleep(secs)
        logging.info('Simulating IO operation Done sleeping for %s second(s)',secs)
    
    def simulate_io_realist(self):
        def good_run():
            # logging.info('Simulating Realistic IO operation Successful run ')
            pass
        def bad_run():
            # logging.info('Simulating Realistic IO operation Exception')
            raise ZeroDivisionError
            
        if randint(1,100) > 50 : 
            good_run()
            time.sleep(1)
        else : 
            bad_run()
            time.sleep(1)
        
    
    
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
        x = (screen_width / 2) - (self.app_width/2)+900
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
        self.download_status_label = Label(self.download_frame, textvar=self.download_status,wraplength=210,)
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
        logging.info('Get doujin data.')
        
        sauce = self.sauce_entry.get()
        if sauce == '':
            self.sauce_stat.set('Gib sauce.')
        else :
            def get_hentai_data (): 
                logging.info('Fetching hentai data ')
                try:
                    hentai_exists = Hentai.exists(sauce)
                    logging.info('Hentai Exists : %s ',hentai_exists)
                except TypeError as e :
                    logging.error('Error : %s',e)
                
                hope = True
                while hope:
                    try:
                        if hentai_exists :
                            dou = Hentai(sauce)
                            logging.debug(sauce)
                            logging.debug(dou)
                            hope = False
                            self.current_doujin = dou
                            logging.debug(self.current_doujin)
                            logging.debug(dou)
                            return dou
                        else:
                            self.sauce_stat.set('Bad sauce ')
                            return 'Bad_sauce'
                    except:
                        self.sauce_stat.set('Temporary error ... Trying again.')
                        return "Error"
            
            self.t3 = threading.Thread(target=get_hentai_data,daemon=True)
            logging.info('Starting a thread to fetch data ')
            self.sauce_stat.set('On it ...  ')
            self.t3.start()
        
        return False

    def download_button_callback(self):
        to_download_pages = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
        downloaded_pages = []
        
        def downloading_status() : 
            download_ongoing = True
            while download_ongoing:
                download_ongoing = t1.is_alive()
                self.download_status.set(f'Downloaded pages : {downloaded_pages}\nPages to download : {to_download_pages}')
                logging.debug('Download Thread Ongoing? %s',download_ongoing)
                self.download_button.config(text="Downloading .  ")
                time.sleep(0.5)
                self.download_button.config(text="Downloading ..  ")
                time.sleep(0.5)
                self.download_button.config(text="Downloading ...  ")
                time.sleep(0.5)
            self.download_button.config(text="Downloaded !  ")
        def threaded_download():
            # TODO: Change simulation to actual io operation 
            while len(to_download_pages) >= 1 : 
                for i in to_download_pages:
                    try: 
                        self.simulate_io_realist()
                        logging.info('Downloaded %s',i)
                        downloaded_pages.append(i)
                        to_download_pages.remove(i)
                    except ZeroDivisionError:
                        # self.download_status.set(f'Error ...')
                        logging.info('Error downloading %s',i)

        # dou = self.current_doujin
        # def download_pages ():
        #     hope  = True
        #     while hope:
        #         print('Retrying ')
        #         try:
        #             dou.download(Path.cwd())
        #             logging.info('Downloading ... ')
        #             hope = False
        #         except Exception as e : 
        #             logging.warning('Internal chaos %s',e)


        t1 = threading.Thread(target=threaded_download,daemon=True)
        t2 = threading.Thread(target=downloading_status,daemon=True)
        t1.start()
        t2.start()

    
    def sauce_poured (self):
        logging.info(' System call : Sauce Click  ')
        dou = self.get_doujin_data()
        hope = True 
        while hope :
            logging.info('Child is alive %s',self.t3.is_alive())
            time.sleep(2)
            if self.t3.is_alive() == False : 
                logging.info('Child is no longer alive ')
                hope = False
                self.sauce_stat.set('Done ... ')
                logging.info('Data : %s',self.current_doujin)
                
                
                self.update_cover(self.current_doujin)
                self.update_desc(self.current_doujin)
                self.update_button(self.current_doujin)




    
    def update_cover(self,dou):
        logging.info('System call : Update cover ')
        basewidth = 470
        def get_cover():
            logging.info('Downloading Cover image  ')
            im = Image.open(requests.get(dou.thumbnail, stream=True).raw)
            wpercent = (basewidth/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            im = im.resize((basewidth,hsize), Image.ANTIALIAS)
            logging.info('Saving Cover image  ')
            im.save('cover.png')
        t2 = threading.Thread(target=get_cover,daemon=True)
        t2.start()
        logging.info('Started cover download thread ')
        t2.join()
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

        
        logging.info('Tk MainLoop Started ')
        self.root.mainloop()


def test_sleep():
    for _ in range(5):
        print('Starting sleep')
        time.sleep(1)
        print('Stopping sleep')



if __name__ == '__main__' :
    nat = natto()
    # t1 = threading.Thread(target=nat.start_ui)
    # t1.start()
    # t1.join()





