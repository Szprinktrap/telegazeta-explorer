#!/usr/bin/python
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import requests
import math
import re
import shutil
import sys
import os

obrazki = []
historia = []
kanal = 1

link_do_obrazka = "http://telegazeta.tvp.pl/sync/ncexp/TG1/100/100_0001.png"
mozna_dalej = True
podstrona = 0
pobrana_strona = 0

window = Tk()
window.title("Telegazeta Explorer v1.2")


if getattr(sys, 'frozen', False):
    program_directory = sys._MEIPASS
    icofile = os.path.join(program_directory, "icon.png")
    window.iconphoto(True, PhotoImage(file=icofile))
    print(program_directory)
    print(os.path.join(program_directory, "icon.png"))
else:
    program_directory=os.path.dirname(os.path.abspath(__file__))
    icofile = os.path.join(program_directory, "icon.png")
    window.iconphoto(True, PhotoImage(file=icofile))
    print(program_directory)
    print(os.path.join(program_directory, "icon.png"))


def download():
    filename = filedialog.asksaveasfilename(filetypes=[("Obraz", "*.png")], defaultextension="*.png")
    if not filename:
        print("nie wybrano pliku")
    else:
        try:
            res = requests.get(link_do_obrazka, stream=True)
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(res.raw, out_file)
            del res
            messagebox.showinfo("Informacja", "Pobrano pomyślnie!")
        except:
            err = sys.exc_info()[0]
            messagebox.showerror("Błąd", err)


ch_var = IntVar()
ch_var.set(1)

menu = Menu(window)

plik_submenu = Menu(menu, tearoff=0)
plik_submenu.add_command(label="Zapisz stronę jako...", command=lambda: download(), accelerator="Ctrl+S")
plik_submenu.add_separator()
plik_submenu.add_command(label="Wyjście", command=lambda: exit(), accelerator="Alt+F4")

kanal_submenu = Menu(menu, tearoff=0)
kanal_submenu.add_radiobutton(label="TVP1", variable=ch_var, value=1, command=lambda: change_channel(1))
kanal_submenu.add_radiobutton(label="TVP2", variable=ch_var, value=2, command=lambda: change_channel(2))
kanal_submenu.add_radiobutton(label="TVP Polonia", variable=ch_var, value=3, command=lambda: change_channel(3))
kanal_submenu.add_radiobutton(label="TVP Kultura", variable=ch_var, value=4, command=lambda: change_channel(4))
kanal_submenu.add_radiobutton(label="TVP Sport", variable=ch_var, value=5, command=lambda: change_channel(5))
kanal_submenu.add_radiobutton(label="Polsat", variable=ch_var, value=6, command=lambda: change_channel(6))
kanal_submenu.add_radiobutton(label="TV4", variable=ch_var, value=7, command=lambda: change_channel(7))

nawigacja_submenu = Menu(menu, tearoff=0)
nawigacja_submenu.add_command(label="Poprzednia strona", command=lambda: prev_page(), accelerator="Backspace")
nawigacja_submenu.add_command(label="Strona główna", command=lambda: navigate(100, 1), accelerator="Home")

pomoc_submenu = Menu(menu, tearoff=0)
pomoc_submenu.add_command(label="Skróty klawiszowe", command=lambda: messagebox.showinfo("Skróty klawiszowe", ""
                                                                                                        "Dostępne skróty klawiszowe:\n"
                                                                                                        "A/D - Poprzednia/następna strona\n"
                                                                                                        "W/S - Poprzednia/następna podstrona\n"
                                                                                                        "Home - Strona główna\n"
                                                                                                        "Delete - Poprzednio wyświetlana strona\n"
                                                                                                        "Ctrl+S - Zapisz stronę\n"
                                                                                         ))

menu.add_cascade(label="Plik", menu=plik_submenu)
menu.add_cascade(label="Kanał", menu=kanal_submenu)
menu.add_cascade(label="Nawigacja", menu=nawigacja_submenu)
menu.add_cascade(label="Pomoc", menu=pomoc_submenu)

display = Canvas(window, width=480, height=336)
display.pack()

page_label = Label(window, text="Strona:")
page_stringvar = StringVar()
page_previous = Button(window, text="<<", command=lambda: navigate(pobrana_strona - 1, 1, True))
page_input = Entry(window, textvariable=page_stringvar)
page_next = Button(window, text=">>", command=lambda: navigate(pobrana_strona + 1, 1, True))
page_navigate = Button(window, text="Idź", command=lambda: navigate(int(page_stringvar.get()), 1, True))

subpage_prev = Button(window, text="<", command=lambda: prev_subpage())
subpage_number = Label(window, text=str(podstrona))
subpage_next = Button(window, text=">", command=lambda: next_subpage())


def tvp_fetch(page, subpage, channel, append):
    try:
        global link_do_obrazka
        global mozna_dalej
        global podstrona
        global pobrana_strona
        subpage_digitnum = int(math.log10(subpage)) + 1
        if subpage_digitnum == 1:
            subpage_str = "000" + str(subpage)
        elif subpage_digitnum == 2:
            subpage_str = "00" + str(subpage)
        elif subpage_digitnum == 3:
            subpage_str = "0" + str(subpage)
        elif subpage_digitnum == 4:
            subpage_str = str(subpage)
        r = requests.get(
            "http://www.telegazeta.pl/telegazeta.php?channel=" + channel + "&page=" + str(page) + "_" + subpage_str)
        image = r.text.split('<div id="ekran"><img src="')[1].split('"')[0]
        curr_subpage = r.text.split('podstrona ')[1].split(' z')[0]
        max_subpages = r.text.split('podstrona ' + str(subpage) + " z ")[1].split('"')[0]
        curr_page = r.text.split('strona ')[1].split(",")[0]
        print("status: " + str(r.status_code))
        print("url obrazu: " + image)
        print("ilość podstron: " + max_subpages)
        print("aktualna podstrona: " + curr_subpage)
        print("aktualna strona: " + curr_page)
        link_do_obrazka = image
        pobrana_strona = int(curr_page)
        podstrona = int(curr_subpage)
        if curr_subpage == max_subpages:
            mozna_dalej = False
        else:
            mozna_dalej = True
        print("można na następną podstronę: " + str(mozna_dalej))
        if append:
            historia.append(curr_page + "|" + curr_subpage)

    except:
        err = sys.exc_info()[0]
        messagebox.showerror("Błąd", err)


def polsat_fetch(page, subpage, channel, append):
    try:
        global link_do_obrazka
        global mozna_dalej
        global podstrona
        global pobrana_strona
        subpage_digitnum = int(math.log10(subpage)) + 1
        if subpage_digitnum == 1:
            subpage_str = "000" + str(subpage)
        elif subpage_digitnum == 2:
            subpage_str = "00" + str(subpage)
        elif subpage_digitnum == 3:
            subpage_str = "0" + str(subpage)
        elif subpage_digitnum == 4:
            subpage_str = str(subpage)
        r = requests.get("http://" + channel + ".pl/" + str(page) + "/" + subpage_str)
        image = "http://" + channel + ".pl/" + r.text.split('<center><img width="90%" src="')[1].split('"')[0]
        curr_subpage = re.split("<title>Gazeta .*? strona:", r.text)[1].split('/')[1].split('<')[0]
        curr_page = re.split("<title>Gazeta .*? strona:", r.text)[1].split("/")[0]
        if "png" in image:
            print("status: " + str(r.status_code))
            print("url obrazu: " + image)
            print("ilość podstron: nie sprawdzane w przypadku polsatu")
            print("aktualna podstrona: " + curr_subpage)
            print("aktualna strona: " + curr_page)
            link_do_obrazka = image
            pobrana_strona = int(curr_page)
            podstrona = int(curr_subpage)
            if 'class="btn btn-default"><span class="glyphicon glyphicon-arrow-right"></span></a></div>        </div>' in r.text:
                mozna_dalej = True
            else:
                mozna_dalej = False

                print("można na następną podstronę: " + str(mozna_dalej))
            if append:
                historia.append(curr_page + "|" + curr_subpage)

        else:
            link_do_obrazka = "http://" + channel + ".pl/" + "//teletext/100/100_0001.png"
            pobrana_strona = 100
            podstrona = 1
            mozna_dalej = True
            print("status: " + str(r.status_code))
            print("url obrazu: " + image)
            print("ilość podstron: nie sprawdzane w przypadku polsatu")
            print("aktualna podstrona: " + curr_subpage)
            print("aktualna strona: " + curr_page)
            print("można na następną podstronę: " + str(mozna_dalej))
            if append:
                historia.append("100|1")

    except:
        err = sys.exc_info()[0]
        messagebox.showerror("Błąd", err)


def navigate(page, subpage, append):
    global link_do_obrazka
    page_input["state"] = DISABLED
    page_navigate["state"] = DISABLED
    subpage_prev["state"] = DISABLED
    subpage_next["state"] = DISABLED

    if kanal == 1:
        tvp_fetch(page, subpage, "TG1", append)
    elif kanal == 2:
        tvp_fetch(page, subpage, "TG2", append)
    elif kanal == 3:
        tvp_fetch(page, subpage, "SAT", append)
    elif kanal == 4:
        tvp_fetch(page, subpage, "KUL", append)
    elif kanal == 5:
        tvp_fetch(page, subpage, "SPO", append)
    elif kanal == 6:
        polsat_fetch(page, subpage, "gazetatvpolsat", append)
    elif kanal == 7:
        polsat_fetch(page, subpage, "gazetatv4", append)

    if podstrona == 1:
        subpage_prev["state"] = DISABLED
    else:
        subpage_prev["state"] = NORMAL

    if mozna_dalej:
        subpage_next["state"] = NORMAL
    else:
        subpage_next["state"] = DISABLED

    page_input["state"] = NORMAL
    page_navigate["state"] = NORMAL

    subpage_number["text"] = str(podstrona)
    page_stringvar.set(str(pobrana_strona))

    photo = ImageTk.PhotoImage(Image.open(requests.get(link_do_obrazka, stream=True).raw))
    display.create_image(240, 170, image=photo)
    obrazki.append(photo)


def change_channel(channel):
    global kanal
    kanal = channel
    historia.clear()
    navigate(100, 1, True)


def prev_page():
    print(historia)
    print(len(historia))
    if len(historia) == 1:
        messagebox.showerror("Błąd", "Nie ma gdzie się cofać!")
    else:
        prevpage = historia[len(historia) - 2]
        prevpage_data = prevpage.split("|")
        navigate(int(prevpage_data[0]), int(prevpage_data[1]), False)
        historia.remove(historia[len(historia) - 1])


def next_subpage():
    if mozna_dalej:
        navigate(pobrana_strona, podstrona + 1, True)


def prev_subpage():
    if mozna_dalej:
        navigate(pobrana_strona, podstrona - 1, True)


page_label.pack(side=LEFT)
page_previous.pack(side=LEFT)
page_input.pack(side=LEFT)
page_next.pack(side=LEFT)
page_navigate.pack(side=LEFT)

subpage_next.pack(side=RIGHT)
subpage_number.pack(side=RIGHT)
subpage_prev.pack(side=RIGHT)

window.config(menu=menu)
window.resizable(0, 0)
navigate(100, 1, True)

window.bind("<Control-s>", lambda event: download())
window.bind("<Delete>", lambda event: prev_page())
window.bind("<Home>", lambda event: navigate(100, 1, True))
window.bind("<Return>", lambda event: navigate(int(page_stringvar.get()), 1, True))
window.bind("<A>", lambda event: navigate(pobrana_strona + 1, 1, True))
window.bind("<D>", lambda event: navigate(pobrana_strona - 1, 1, True))
window.bind("<W>", lambda event: next_subpage())
window.bind("<S>", lambda event: prev_subpage())
window.mainloop()
