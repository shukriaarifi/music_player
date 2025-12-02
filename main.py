import pygame
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
from mutagen.mp3 import MP3
import time
from PIL import Image, ImageTk
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def img(path) :
    return os.path.join(BASE_DIR, "assets", path)
#--------------------------------------------------------------------------------------------------
win = Tk()
win.title("Music player")
win.geometry("500x650")
bg_color="#88A5C6"
#--------------------------------------------------------------------------------------------------

lb_main = Label(win, text="My Music Player", bg=bg_color, fg="white",
                height=2, relief="groove", font=("Segoe Print", 30, "bold"))

lb_main.pack(side="top", fill="x", padx=5, pady=5)
#--------------------------------------------------------------------------------------------------
song_paths = []

def def_load_music() :

    folder_path = filedialog.askdirectory(title="Choosse your music folder")

    if not folder_path :
        return

    all_musics_list.delete(0, END)
    global song_paths

    song_paths = []

    for filename in os.listdir(folder_path) :
        if filename.endswith(".mp3") :
            full_path = os.path.join(folder_path, filename)

            song_paths.append(full_path)

            all_musics_list.insert(END, filename)


bt_load_music = Button(win, text="Selecte musics folder", bg=bg_color, fg="white",
                relief="groove", font=("Segoe Print", 10, "bold"), command=def_load_music, width=19)

bt_load_music.place(x=295, y=154)
#--------------------------------------------------------------------------------------------------
def search_def() :
    query = search_en.get().strip().lower()
    if not query :
        return
    for i in range(all_musics_list.size()) :
        song_name = all_musics_list.get(i).lower()
        song_name = song_name.replace(".mp3", "")
        if query in song_name :
            all_musics_list.selection_clear(0, END)
            all_musics_list.selection_set(i)
            all_musics_list.see(i)
            return
    
    messagebox.showinfo("", "No song with this name was found!")

search_en = Entry(win, width=26, fg="#90a3bd", bg="#FFFFFF", font=("Trebuchet MS", 13))
search_en.place(x=5, y=160)

search_icon = PhotoImage(file=img("search.png"))
search_bt = Button(win, image=search_icon, command=search_def)
search_bt.place(x=255, y=158)
#--------------------------------------------------------------------------------------------------
def setting_def() :
    pass

setting_icon = PhotoImage(file=img("bolt.png"))
setting_bt = Button(win, image=setting_icon, command=setting_def)
setting_bt.place(x=463, y=158)
#--------------------------------------------------------------------------------------------------
lb_all_music = Label(win, text="Musics List:", bg=bg_color, anchor="w", fg="white",
                relief="groove", font=("Segoe Print", 15, "bold"), width=18)

lb_all_music.place(x=5, y=195)

all_musics_list = Listbox(win, height=13, width=26, fg="#90a3bd", bg="#FFFFFF", font=("Trebuchet MS", 13))
all_musics_list.place(x=5, y=243)


Scroll_all = Scrollbar(win, orient=VERTICAL)
Scroll_all.place(x=225 , y=246, height=310)

all_musics_list.config(yscrollcommand=Scroll_all.set)
Scroll_all.config(command=all_musics_list.yview)
#--------------------------------------------------------------------------------------------------
lb_fav_music = Label(win, text="Favorite Musics:", bg=bg_color, anchor="w", fg="white",
                relief="groove", font=("Segoe Print", 15, "bold"), width=18)

lb_fav_music.place(x=253, y=195)

fav_paths = []

fav_musics_list = Listbox(win, height=13, width=26, fg="#90a3bd", bg="#FFFFFF", font=("Trebuchet MS", 13))
fav_musics_list.place(x=255, y=243)


Scroll_fav = Scrollbar(win, orient=VERTICAL)
Scroll_fav.place(x=474 , y=246, height=310)

fav_musics_list.config(yscrollcommand=Scroll_fav.set)
Scroll_fav.config(command=fav_musics_list.yview)
#--------------------------------------------------------------------------------------------------
left_icon = PhotoImage(file=img("skip-back.png"))
right_icon = PhotoImage(file=img("skip-forward.png"))
pause_icon = PhotoImage(file=img("circle-pause.png"))
play_icon = PhotoImage(file=img("circle-play.png"))
rep_icon = PhotoImage(file=img("repeat.png"))
fav_icon = PhotoImage(file=img("file-heart.png"))

music_img = Image.open(img("music_icon.png"))
music_img = music_img.resize((220, 220), Image.Resampling.LANCZOS)
music_icon = ImageTk.PhotoImage(music_img)


def def_play() :
    play_win = Toplevel(win, bg="white")
    play_win.title("Playing...")
    play_win.geometry("280x430")

    up = Frame(play_win, width=220, height=220, bg="white", relief="groove")
    up.pack_propagate(False)
    up.pack(pady=20)

    music_lb = Label(up, image=music_icon)
    music_lb.pack()

    def load_new_music(path) :
        nonlocal song_path, audio, total_time

        song_path = path
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

        audio = MP3(song_path)
        total_time = int(audio.info.length)

        lb_music_name.config(text=os.path.basename(song_path))
        progress.set(0)
        current_time_lb1.config(text="00:00")
        total_time_lb1.config(text=time.strftime("%M:%S", time.gmtime(total_time)))


    def left_def() :
        nonlocal current_index, current_list
        if current_list == "all" :
            if current_index > 0 :
                current_index-=1
                all_musics_list.selection_clear(0, END)
                all_musics_list.selection_set(current_index)
                all_musics_list.see(current_index)
                load_new_music(song_paths[current_index])
            else :       
                messagebox.showwarning("Warning!", "There is no previous music!")
                return
        else :
            if current_index > 0 :
                current_index-=1
                fav_musics_list.selection_clear(0, END)
                fav_musics_list.selection_set(current_index)
                fav_musics_list.see(current_index)
                load_new_music(fav_paths[current_index])
            else :        
                messagebox.showwarning("Warning!", "There is no previous music!")
                return
        
        if song_path not in fav_paths :
            fav_bt.config(bg="SystemButtonFace")
        else :    
            fav_bt.config(bg="lightblue")

    left_bt = Button(play_win, image=left_icon, command=left_def)
    left_bt.place(x=75, y=375)


    def right_def() :
        nonlocal current_index, current_list
        if current_list == "all" :
            if current_index < len(song_paths)-1 :
                current_index+=1
                all_musics_list.selection_clear(0, END)
                all_musics_list.selection_set(current_index)
                all_musics_list.see(current_index)
                load_new_music(song_paths[current_index])
            else :       
                messagebox.showwarning("Warning!", "There is no next music!")
                return
        else :
            if current_index < len(fav_paths)-1 :
                current_index+=1
                fav_musics_list.selection_clear(0, END)
                fav_musics_list.selection_set(current_index)
                fav_musics_list.see(current_index)
                load_new_music(fav_paths[current_index])
            else :        
                messagebox.showwarning("Warning!", "There is no next music!")
                return
        
        if song_path not in fav_paths :
            fav_bt.config(bg="SystemButtonFace")
        else :    
            fav_bt.config(bg="lightblue")


    right_bt = Button(play_win, image=right_icon, command=right_def)
    right_bt.place(x=175, y=375)


    is_playing = True
    is_paused = False

    def play_pause() :
        nonlocal is_playing, is_paused
        if is_playing :
            pygame.mixer.music.pause()
            is_playing = False
            is_paused = True
            play_pause_bt.config(image=play_icon)
        else :
            pygame.mixer.music.unpause()
            is_playing = True
            is_paused = False
            play_pause_bt.config(image=pause_icon)

    play_pause_bt = Button(play_win, image=pause_icon, command=play_pause)
    play_pause_bt.place(x=124, y=375)


    is_repeat = False
    def rep_def() :
        nonlocal is_repeat
        is_repeat = not is_repeat
        if is_repeat :
            rep_bt.config(bg="lightblue")
        else :
            rep_bt.config(bg="SystemButtonFace")

    rep_bt = Button(play_win, image=rep_icon, command=rep_def)
    rep_bt.place(x=30, y=375)


    def fav_music() :
        if song_path not in fav_paths :
            fav_bt.config(bg="lightblue")
            fav_paths.append(song_path)
            fav_musics_list.insert(END, os.path.basename(song_path))
        else :
            for i in range(fav_musics_list.size()) :
                if fav_musics_list.get(i) == os.path.basename(song_path) :
                    fav_musics_list.delete(i)
                    break
            fav_paths.remove(song_path)
            fav_bt.config(bg="SystemButtonFace")

    fav_bt = Button(play_win, image=fav_icon, command=fav_music)
    fav_bt.place(x=220, y=375)
    #-----------------------------------------------------------------------------------------
    selected_all = all_musics_list.curselection()
    selected_fav = fav_musics_list.curselection()

    if selected_all :
        current_list = "all"
        current_index = selected_all[0]    
        song_path = song_paths[current_index]
    elif selected_fav :
        current_list = "fav"
        current_index = selected_fav[0]    
        song_path = fav_paths[current_index]
    else :
        messagebox.showwarning("Warning!", "Selecte a song from list!")
        return


    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()


    audio = MP3(song_path)
    total_time = int(audio.info.length)

    current_time = 0

    total_time_lb1 = Label(play_win, text=time.strftime("%M:%S", time.gmtime(total_time)),
                        font=("Segoe Print", 9, "bold"), fg=bg_color)

    total_time_lb1.place(x=205, y=320)


    current_time_lb1 = Label(play_win, text="00:00",
                        font=("Segoe Print", 9, "bold"), fg=bg_color)

    current_time_lb1.place(x=30, y=320)


    progress = Scale(play_win, from_=0, to=total_time, orient="horizontal", length=115, showvalue=0, sliderlength=8,
                     troughcolor="#ddd", fg=bg_color, bg="#f0f0f0")
    
    progress.place(x=80, y=323)


    def update_progress() :
        nonlocal current_time
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms >= 0 :
            current_time = int(pos_ms/1000)
        else:
            current_time = 0
        
        if current_time > total_time :
            current_time = total_time

        progress.set(current_time)
        current_time_lb1.config(text=time.strftime("%M:%S", time.gmtime(current_time)))
        play_win.after(500, update_progress)

    update_progress()

    
    def check_end() :
        if pygame.mixer.music.get_pos() == -1 and is_playing:
            if is_repeat :
                load_new_music(song_path)
            else :
                right_def()
        play_win.after(1000, check_end)

    check_end()
        

    def on_close() :
        pygame.mixer.music.stop()
        play_win.destroy()

    play_win.protocol("WM_DELETE_WINDOW", on_close)


    music_name = os.path.basename(song_path)
    lb_music_name = Label(play_win, fg=bg_color, text= music_name,
                    font=("Segoe Print", 11, "bold"), width=21)

    lb_music_name.place(x=32, y=250)


bt_play = Button(win, text="Play", bg=bg_color, fg="white",
                relief="groove", font=("Segoe Print", 13, "bold"), width=43, command=def_play)

bt_play.place(x=8, y=566)
#--------------------------------------------------------------------------------------------------
mainloop()