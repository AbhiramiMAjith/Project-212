import socket

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import ftplib
from ftplib import FTP

import os
import time

import ntpath #This is used to extract filename from path
from pathlib import Path

#from playsound import playsound
import pygame
from pygame import mixer

IP_ADDR = '127.0.0.1'
PORT = 5550
SERVER = None
BUFFER_SIZE = 4096

global infolabel
global listbox

global song_counter
song_counter=0
global song_selected

global filepathLabel

def browse_file():
    global listbox
    global song_counter
    global filepathLabel

    try:
        filename = filedialog.askopenfilename()

        HOSTNAME = '127.0.0.1'
        USERNAME = 'lftpd'
        PASSWORD = 'lftpd'

        ftp_server = FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd('shared_files')
        fname = ntpath.basename(filename)

        with open (filename,'rb') as file:
            ftp_server.storbinary(f"STOR {fname}", file)

        ftp_server.dir()
        ftp_server.quit()

        listbox.insert(song_counter,fname)
        song_counter = song_counter + 1

    except FileNotFoundError:
        print("Cancel button pressed")

def download():
    song_to_download = listbox.get(ANCHOR)
    infolabel.configure(text="Downloading "+song_to_download)

    HOSTNAME = '127.0.0.1'
    USERNAME = 'lftpd'
    PASSWORD = 'lftpd'

    home = str(Path.home())
    download_path = home+'\Downloads'

    ftp_server = ftplib.FTP(HOSTNAME,USERNAME,PASSWORD)
    ftp_server.encoding("utf-8")
    ftp_server.cwd("shared_files")

    local_file_name = os.path.join(download_path,song_to_download)
    
    file = open(local_file_name,'wb')
    ftp_server.retrbinary('RETR'+song_to_download,file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()

    infolabel.configure(text='Download complete')
    time.sleep(1)

    if (song_selected!=""):
        infolabel.configure(text='Now playing : '+song_selected)
    else:
        infolabel.configure(text='')


def add_song():
    if ('shared_files' in os.listdir()):
        for file in os.listdir('shared_files'):
            file_name = os.fsdecode(file)
            listbox.insert(song_counter,file_name)
            song_counter = song_counter+1

def play():
    global song_selected
    global listbox
    global infolabel

    song_selected = listbox.get(ANCHOR)

    add_song()

    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()
    if(song_selected != ''):
        infolabel.configure(text="Now PLaying: "+song_selected)
    else:
        infolabel.configure(text="")

def stop():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load("shared_files/"+song_selected)
    mixer.music.pause
    infolabel.configure(text='')

def resume():
    global song_selected

    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()

def pause():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause() 

def musicWindow():
    global listbox
    global infolabel

    window = Tk()
    window.title("Music Window")
    window.geometry("300x300")
    window.configure(bg='LightSkyBlue')

    selectLabel = Label(window,text="Select song", bg ='LightSkyBlue',font=("Calibri",8))
    selectLabel.place(x=2,y=1)

    listbox = Listbox(window,height=10,width=39,activestyle='dotbox',bg='LightSkyBlue',borderwidth=2,font=("Calibri",10))
    listbox.place(x=10,y=10)

    scroll_bar_1 = Scrollbar(listbox)
    scroll_bar_1.place(relheight=1,relx=1)
    scroll_bar_1.config(command=listbox.yview)

    infolabel = Label(window,text='',fg="blue",font=("Calibri",0))
    infolabel.place(x=4,y=200)

    playbutton = Button(window,text='Play',width=10,bd=1,bg ='SkyBlue',font=("Calibri",10),command=play)
    playbutton.place(x=30,y=200)
    
    stopbutton = Button(window,text='Stop',width=10,bd=1,bg ='SkyBlue',font=("Calibri",10),command=stop)
    stopbutton.place(x=200,y=200)

    upload = Button(window,text='Uplaod',width=10,bd=1,bg ='SkyBlue',font=("Calibri",10))
    upload.place(x=30,y=250)

    download = Button(window,text='Download',width=10,bd=1,bg ='SkyBlue',font=("Calibri",10))
    download.place(x=200,y=250)

    resumebutton = Button(window,text='Resume',width=10,bd=1,bg ='SkyBlue',font=("Calibri",10),command=resume)
    resumebutton.place(x=30,y=250)

    pausebutton = Button(window,text='Pause',width=10,bd=1,bg ='SkyBlue',font=("Calibri",10),command=pause)
    pausebutton.place(x=200,y=250)

    window.mainloop()

def setup():
    global IP_ADDR
    global PORT
    global SERVER

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDR,PORT))

    musicWindow()

setup()