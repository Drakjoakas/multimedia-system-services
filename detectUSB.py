# !/usr/bin/env python3
# ## ###############################################
#
# detectUSB.py
# Performs actions according to the file types found in a USB
# connected. Designed for 'multimedia-system'
#
# Autor: Joaquin Sandoval - Sebastián Arjona - Isaac Nájera
# License: MIT
#
# ## ###############################################

import subprocess
import os
import tkinter as tk
from tkinter import ttk

VIDEO_TYPES = ['.mp4','.avi']
IMAGE_TYPES = ['.jpg','.jpeg','.png','.gif']
MUSIC_TYPES = ['.mp3']


getUserProc = subprocess.Popen(['whoami'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
user, err = getUserProc.communicate()
user = user.decode('ascii')[:-1]



def hasFileType(target: str, types: list) -> bool:
    hasFile = False
    for tp in types:
        hasFile = hasFile or (target.find(tp) != -1)
    return hasFile

def displayImages(name:str):
    cmd = ['sxiv','-f','-b','-S','5','/media/'+user+'/'+name]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o,e = proc.communicate()
#	o = o.decode('ascii')
    if len(e) > 0:
        print(e)
    else:
        print(o)
        
        

        
        
def playAllVideos(videos: list,name:str):
    cmd = ['cvlc','-f']
    for video in videos:
        cmd.append('/media/{0}/{1}/{2}'.format(user,name,video))

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o,e = proc.communicate()

def displayVideos(name:str, closeWindow):    
    videos = filter(lambda y: y.find('.mp4') != -1, os.listdir('/media/{0}/{1}'.format(user,name)))
    
    videos = list(videos)
    
    if len(videos) > 1:
        root = tk.Tk()
        window_width = 500
        window_height = 250
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
    
        root.title("Videos")
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        root.attributes('-topmost',1)
        msg = ttk.Label(root,text="Elige un video o reproduce todos los videos")
        msg.pack(pady=16)
        
        
        opc = tk.StringVar()
        
        videos_cb = ttk.Combobox(root, textvariable=opc)
        videos_cb['values'] = videos
        videos_cb['state']  = 'readonly'
        videos_cb.pack(fill=tk.X,padx=8, pady=8)
        
        def playSingleVideo():
            video = videos_cb.get()
            proc = subprocess.Popen(['cvlc','-f','/media/{0}/{1}/{2}'.format(user,name,video)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            o,e = proc.communicate()
            print(e)

        
        playButton = ttk.Button(
            root,
            text='Reproducir',
            command=playSingleVideo,
            state='disabled'
            )
        playButton.pack(pady=8)
        
        playAllButton = ttk.Button(
            root,
            text='Reproducir Todos',
            command=lambda:  playAllVideos(videos,name)
            )
        playAllButton.pack(pady=8)
        
        def video_changed(event):
            playButton.state(['!disabled'])
        
        videos_cb.bind('<<ComboboxSelected>>', video_changed)
        
        closeWindow()
        root.mainloop()
        
    else:
        playAllVideos(list(videos))
    
        
def playMusic(name:str):
    cmd = ['vlc','-f']
    canciones = filter(lambda y: y.find('.mp3') != -1, os.listdir('/media/{0}/{1}'.format(user,name)))
    for cancion in list(canciones):
        proc = subprocess.Popen(cmd + ['/media/{0}/{1}/{2}'.format(user,name,cancion)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o,e  = proc.communicate()
        o = o.decode('ascii')
        
        if len(e) > 0:
            print(e)


def handleDeviceByAction(prev_action:str,action: str, name: str):
    if action == 'change' and prev_action=='add':
        files = ",".join(os.listdir('/media/{0}/{1}'.format(user,name)))
        
        hasVideos = hasFileType(files, VIDEO_TYPES)
        hasImages = hasFileType(files, IMAGE_TYPES)
        hasMusic  = hasFileType(files, MUSIC_TYPES)
        
        if (hasMusic and hasVideos) or (hasImages and hasVideos) or (hasMusic and hasImages):
            root = tk.Tk()
            
            def closeWindow():
                root.destroy()
            
            window_width = 500
            window_height = 250
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            center_x = int(screen_width/2 - window_width/2)
            center_y = int(screen_height/2 - window_height/2)
            
            
            root.title("Dispositivo " + name)
            root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
            root.attributes('-topmost',-1)
            message = tk.Label(
                root,
                text="Se ha detectado archivos múltimedia de diferentes tipos, seleccione que desea reproducir",
                anchor=tk.W,
                wraplength='500',
            )
            message.pack(pady=(16, 16))
            
            if hasVideos:            
                buttonVideo = ttk.Button(
                    root,
                    text='Videos',
                    command=lambda: displayVideos(name, closeWindow)
                    )
                
                buttonVideo.pack(pady=(8))
                
            if hasImages:            
                buttonImages = ttk.Button(
                    root,
                    text='Imágenes',
                    command=lambda: displayImages(name)
                    )
                
                buttonImages.pack(pady=(8))
                
            if hasMusic:
                buttonMusic = ttk.Button(
                    root,
                    text='Música',
                    command=lambda: playMusic(name)
                    )
                buttonMusic.pack(pady=(8))
            
            root.mainloop()
        else:
            if hasImages:
                displayImages(name)
            elif hasVideos:
                displayVideos(name)
            elif hasMusic:
                playMusic(name)