"""Natto : Robel mezemir ( robi ) <robelmezemir@gmail.com>"""
# ... and he said " let there be time " python line 3:12
import time

import logging
import os
import threading
# Tkinter and stuff
from tkinter import Tk
from tkinter import Label, LabelFrame
from tkinter import Button, Entry, StringVar
from tkinter import PhotoImage
from tkinter import DISABLED, NORMAL
from pathlib import Path
from PIL import Image  # pylint: disable=E0401
import requests  # pylint: disable=E0401
from hentai import Hentai, Format  # pylint: disable=E0401

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [ %(threadName)s ] [ %(levelname)s ] %(message)s",
    handlers=[
        logging.FileHandler("debug.log", mode='w', encoding=None, delay=False),
        logging.StreamHandler()
    ]
)

logging.info('Imports done ')


class Natto():# pylint: disable=too-many-instance-attributes
    """Natto class"""

    def __init__(self):
        """initialize class"""
        logging.info('[ Sys call ] __init__ ')
        # initializing attributes
        self.root = None
        self.app_width = None
        self.app_height = None
        self.cover = None
        self.sauce_frame = None
        self.sauce_entry = None
        self.sauce_search_button = None
        self.sauce_stat = None
        self.sauce_stat_label = None
        self.download_frame = None
        self.download_button = None
        self.download_status = None
        self.download_status_label = None
        self.sauce_id = None
        self.sauce_label = None
        self.title = None
        self.title_label = None
        self.title_jp = None
        self.title_jp_label = None
        self.title_en = None
        self.title_en_label = None
        self.pages = None
        self.pages_label = None
        self.tags = None
        self.tags_label = None
        self.sauce_data = None
        self.program_status = None
        self.check_cwd()
        self.start_ui()
        self.cleanup_cover()

    def sanitize_foldername(self, folder_dirty):
        """Cleans up folder names from illegal characters."""
        logging.info('[ Sys call ] sanitize_foldername')
        folder_clean = folder_dirty.replace("?", "")
        folder_clean = folder_clean.replace(">", "")
        folder_clean = folder_clean.replace("<", "")
        folder_clean = folder_clean.replace("\\", "")
        folder_clean = folder_clean.replace("/", "")
        folder_clean = folder_clean.replace("*", "")
        folder_clean = folder_clean.replace("|", "")
        folder_clean = folder_clean.replace(":", "")
        folder_clean = folder_clean.replace("\"", "")

        logging.debug('Sanitized : %s', folder_dirty)
        logging.debug('Clean Filename :  %s', folder_dirty)
        self.program_status = 'ok'
        return folder_clean

    def start_ui(self):
        """Starts the ui main loop"""
        logging.info('[ Sys call ] start_ui')
        self.ui_init()
        self.add_ui_elements()
        self.start_mainloop()

    def ui_init(self):
        """initializes the ui"""
        logging.info('[ Sys call ] ui_init')
        self.root = Tk()
        self.app_width = 820
        self.app_height = 740
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = (screen_width / 2) - (self.app_width/2)+900
        height = (screen_height / 2) - (self.app_height/2)
        # window size and positioning
        self.root.geometry(
            f'{self.app_width}x{self.app_height}+{int(width/2)}+{int(height/2)}')
        self.root.title('Natto | Stay Degenerate ')

    def check_cwd(self):
        """check the current working directory"""
        logging.info('[ Sys call ] check_cwd')
        # Check current filesys directory
        working_dir = Path.cwd()
        logging.info('Working dir : %s', working_dir)
        hentai_folder_exists = Path.exists(
            Path.joinpath(working_dir, './hentai'))
        logging.info('Hentai folder : %s', hentai_folder_exists)
        if not hentai_folder_exists:
            print(
                "Can't find the Hentai folder near me \n"
                "  Creating one at the current working directory ...")
            os.mkdir('hentai')
            self.program_status = 'ok'
        else:
            logging.info("Hentai folder exists , All good .")
        return True

    def add_ui_elements(self):
        """adds ui elements to tk"""
        logging.info('[ Sys call ] add_ui_elements')
        # cover_image = PhotoImage(file='def.png')
        self.cover = Label(self.root, text=" --- Cover image --- ")
        cover_pos_x = (self.app_width/4)
        self.cover.place(x=cover_pos_x-50, y=0, relwidth=1, relheight=1)

        self.sauce_frame = LabelFrame(
            self.root, text='Sauce.', padx=10, pady=10)
        self.sauce_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")
        self.sauce_entry = Entry(self.sauce_frame, width=20)
        self.sauce_entry.grid(row=0, column=0, sticky="W")
        self.sauce_entry.bind('<KeyPress-Return>', self.on_enter)
        self.sauce_search_button = Button(
            self.sauce_frame, text="Search !", command=self.sauce_search_callback)
        self.sauce_search_button.grid(
            row=0, column=1, sticky="E", padx=5, pady=5)

        self.sauce_stat = StringVar()
        self.sauce_stat.set('Type Sauce and Search.')
        self.sauce_stat_label = Label(
            self.sauce_frame, textvar=self.sauce_stat, wraplength=250, justify="center")
        self.sauce_stat_label.grid(row=1, column=0, sticky="W")

        self.download_frame = LabelFrame(self.root, text='', padx=10, pady=10)
        self.download_frame.grid(
            row=2, column=0, padx=10, pady=10, sticky="NSEW")
        self.download_button = Button(
            self.download_frame, text="Download", command=self.download_button_callback)
        self.download_button.grid(row=0, column=0, sticky="NSEW")
        self.download_status = StringVar()
        self.download_status.set('-------------------')
        self.download_status_label = Label(
            self.download_frame, textvar=self.download_status, wraplength=210, justify="center")
        self.download_status_label.grid(row=1, column=0, sticky='W')

        # description frame
        details_frame = LabelFrame(
            self.root, text='Doujin Data', padx=10, pady=10)
        details_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NESW")

        #  Sauce
        self.sauce_id = StringVar()
        self.sauce_id.set('#177013')
        self.sauce_label = Label(
            details_frame, textvar=self.sauce_id, wraplength=250, justify="left")
        self.sauce_label.grid(row=0, column=0, sticky="W")
        # Pretty title
        self.title = StringVar()
        self.title.set('Doujin Title : ')
        self.title_label = Label(
            details_frame, textvar=self.title, wraplength=250, justify="left")
        self.title_label.grid(row=1, column=0, sticky="W")
        # Japaneese title
        self.title_jp = StringVar()
        self.title_jp.set('Japaneese Title : ')
        self.title_jp_label = Label(
            details_frame, textvar=self.title_jp, wraplength=250, justify="left")
        self.title_jp_label.grid(row=2, column=0, sticky="W")
        # English title
        self.title_en = StringVar()
        self.title_en.set('English Title : ')
        self.title_en_label = Label(
            details_frame, textvar=self.title_en, wraplength=250, justify="left")
        self.title_en_label.grid(row=3, column=0, sticky="W")
        #  Number of pages
        self.pages = StringVar()
        self.pages.set('Number of Pages : ')
        self.pages_label = Label(
            details_frame, textvar=self.pages, wraplength=250, justify="left")
        self.pages_label.grid(row=4, column=0, sticky="W")
        # Tags
        self.tags = StringVar()
        self.tags.set('Tags : ')
        self.tags_label = Label(
            details_frame, textvar=self.tags, wraplength=250, justify="left")
        self.tags_label.grid(row=5, column=0, sticky="W")

    def download_button_callback(self):
        """Callback for download button"""
        logging.info('[ Sys call ] download_button_callback')
        to_download_pages = []
        downloaded_pages = []
        # populate the todownload if the sauce has been got
        logging.info("Sauce to download : %s", self.sauce_data.image_urls)

        if len(self.sauce_data.image_urls) > 0:
            for page in self.sauce_data.image_urls:
                to_download_pages.append(page.split("/")[-1])

        def downloading_status():
            search_ongoing = True
            while search_ongoing:
                search_ongoing = thread1.is_alive()
                self.download_status.set(
                    f'Downloaded pages : {downloaded_pages}\n\n'
                    'Pages to download : {to_download_pages}')
                # logging.debug('Download Thread Ongoing? %s',search_ongoing)
                # ☑☒
                self.download_button.config(text="▀ Downloading... ▀")
                time.sleep(0.5)
                self.download_button.config(text="█ Downloading... █")
                time.sleep(0.5)
                self.download_button.config(text="▄ Downloading... ▄")
                time.sleep(0.5)
                self.download_button.config(text="  Downloading...  ")
                time.sleep(0.5)
            self.download_button.config(text=" ☑ Downloaded   ")
            self.download_status.set(
                f"Downloaded {len(downloaded_pages)} pages \n\n"
                f" {downloaded_pages}  ")

        def threaded_download():
            if self.sauce_data:
                foldername = self.sanitize_foldername(
                    self.sauce_data.title(Format.Pretty))
                hentai_directory = f'./hentai/{foldername}'
                os.mkdir(hentai_directory)
                self.download_button.config(state=DISABLED)
                self.sauce_search_button.config(state=DISABLED)

            while len(to_download_pages) >= 1:
                # If there are pages to download .
                # create the directory to store them
                for i in self.sauce_data.image_urls:
                    # for each of them
                    try:
                        current_url = i
                        response = requests.get(current_url, stream=True)
                        if response.status_code == 200:
                            with open(f"{hentai_directory}/{i.split('/')[-1]}", 'wb') as file:
                                file.write(response.content)
                                file.close()
                        logging.debug('[ Downloaded ] %s', i)
                        downloaded_pages.append(i.split('/')[-1])
                        to_download_pages.remove(i.split('/')[-1])
                    except Exception as err:  # pylint: disable=broad-except
                        self.download_button.config(
                            text='▒ Downloading... ▒ ')
                        logging.debug('[ Dld Error ]:  %s ', err)

            self.download_button.config(state=NORMAL)
            self.sauce_search_button.config(state=NORMAL)

        thread1 = threading.Thread(target=threaded_download, daemon=True)
        thread2 = threading.Thread(target=downloading_status, daemon=True)
        thread1.start()
        thread2.start()

    def sauce_search_callback(self):
        """callback for sauce search"""
        logging.info('[ Sys call ] sauce_search_callback')
        self.sauce_data = None

        def search_status():
            if self.sauce_entry.get() == '':
                self.sauce_stat.set('Gib sauce pls .')
            else:
                search_ongoing = True
                while search_ongoing:
                    search_ongoing = thread1.is_alive()

                    self.sauce_search_button.config(text="▀ Searching ... ▀")
                    time.sleep(0.4)
                    self.sauce_search_button.config(text="█ Searching... █")
                    time.sleep(0.2)
                    self.sauce_search_button.config(text="▄ Searching... ▄")
                    time.sleep(0.4)
                    self.sauce_search_button.config(text=".  Searching...  .")
                    time.sleep(0.2)

                self.sauce_search_button.config(text="  Done   ")

        def threaded_search():
            if self.sauce_entry.get() == '':
                self.sauce_stat.set('Gib sauce pls .')
            else:
                logging.info('Threaded Search Started')
                while self.sauce_data is None:
                    try:
                        sauce = self.sauce_entry.get()
                        sauce_exists = Hentai.exists(sauce)
                        if sauce_exists:
                            sauce_return = Hentai(sauce)
                        else:
                            self.sauce_stat.set('Sauce does not exist ')
                            sauce_return = '404'
                        self.sauce_data = sauce_return
                        logging.debug('Search returned  %s', sauce_return)
                    except Exception as err:  # pylint: disable=broad-except
                        logging.debug('Error Searching %s', err)
                # Display data to user if it exists
                if self.sauce_data is not None or self.sauce_data != '404':
                    self.update_desc(self.sauce_data)
                    self.update_cover()

        thread1 = threading.Thread(target=threaded_search, daemon=True)
        thread2 = threading.Thread(target=search_status, daemon=True)
        thread1.start()
        thread2.start()

    def update_cover(self):
        """Updates the cover """
        logging.info('[ Sys call ] update_cover ')
        basewidth = 470
        killswitch = True
        print(self.sauce_data, killswitch)
        while killswitch:
            if not self.sauce_data:
                self.sauce_stat.set('No sauce ?')
                logging.info('sauce data unavailable for update cover scope ')
                time.sleep(1)
            else:
                killswitch = False
                logging.info('Updating cover image ')
                # downloading cover image

                def get_cover():
                    kill_switch = True
                    while kill_switch:
                        try:
                            logging.info('Downloading Cover image  ')
                            self.cover.config(
                                text='Downloading cover image ...')
                            img = Image.open(requests.get(
                                self.sauce_data.thumbnail, stream=True).raw)
                            wpercent = (basewidth/float(img.size[0]))
                            hsize = int((float(img.size[1])*float(wpercent)))
                            img = img.resize(
                                (basewidth, hsize), Image.ANTIALIAS)
                            logging.info('Saving Cover image  ')
                            img.save('cover.png')
                            cover_image = PhotoImage(file='cover.png')
                            logging.info('displaying cover image')
                            self.cover.config(image=cover_image)
                            self.cover.image = cover_image
                            logging.info('displayed cover image')
                            kill_switch = False
                        except Exception as err:  # pylint: disable=broad-except
                            logging.debug(
                                'Error Downloading cover image  %s', err)

                thread1 = threading.Thread(target=get_cover, daemon=True)
                thread1.start()

    def update_button(self):
        """updates the button"""
        logging.info('[ Sys call ] update_button')
        self.sauce_frame.config(bg='whitesmoke')
        self.sauce_entry.config(bg='honeydew')
        self.sauce_search_button.config(bg='azure')

    def update_desc(self, dou):
        """updates the description"""
        logging.info('[ Sys call ] update_desc')
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

    def on_enter(self):
        """callback on keyboard return key pressed"""
        logging.info('[ Sys call ] on_enter')
        self.sauce_search_callback()

    def start_mainloop(self):
        """starts the main loop"""
        logging.info('[ Sys call ] start_mainloop')
        logging.info('UI Started .')
        self.root.mainloop()
        logging.info('UI Exit . ')

    def cleanup_cover(self):
        """cleans up cover.png"""
        if os.path.exists("cover.png"):
            os.remove("cover.png")
            self.program_status = 'ok'
        else:
            pass


if __name__ == '__main__':
    nat = Natto()
    logging.info('Execution Finished  ')
