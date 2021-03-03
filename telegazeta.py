#!//bin/python
from tkinter import *
from PIL import ImageTk, Image
import requests
import math
import re

obrazki = []
kanal = 1

link_do_obrazka = "http://telegazeta.tvp.pl/sync/ncexp/TG1/100/100_0001.png"
mozna_dalej = True
podstrona = 0
pobrana_strona = 0

window = Tk()
window.title("Telegazeta Explorer v1.0")

ch_var = IntVar()
ch_var.set(1)

menu = Menu(window)

plik_submenu = Menu(menu, tearoff=0)
plik_submenu.add_command(label="Strona główna", command=lambda: navigate(100, 1))
plik_submenu.add_separator()
plik_submenu.add_command(label="Wyjście", command=lambda: exit())

kanal_submenu = Menu(menu, tearoff=0)
kanal_submenu.add_radiobutton(label="TVP1", variable=ch_var, value=1, command=lambda: change_channel(1))
kanal_submenu.add_radiobutton(label="TVP2", variable=ch_var, value=2, command=lambda: change_channel(2))
kanal_submenu.add_radiobutton(label="TVP Polonia", variable=ch_var, value=3, command=lambda: change_channel(3))
kanal_submenu.add_radiobutton(label="TVP Kultura", variable=ch_var, value=4, command=lambda: change_channel(4))
kanal_submenu.add_radiobutton(label="TVP Sport", variable=ch_var, value=5, command=lambda: change_channel(5))
kanal_submenu.add_radiobutton(label="Polsat", variable=ch_var, value=6, command=lambda: change_channel(6))
kanal_submenu.add_radiobutton(label="TV4", variable=ch_var, value=7, command=lambda: change_channel(7))

menu.add_cascade(label="Plik", menu=plik_submenu)
menu.add_cascade(label="Kanał", menu=kanal_submenu)

display = Canvas(window, width=480, height=336)
display.pack()

page_label = Label(window, text="Strona:")
page_stringvar = StringVar()
page_input = Entry(window, textvariable=page_stringvar)
page_navigate = Button(window, text="Idź", command=lambda: navigate(int(page_stringvar.get()), 1))

subpage_prev = Button(window, text="<<", command=lambda: navigate(pobrana_strona, podstrona - 1))
subpage_number = Label(window, text=str(podstrona))
subpage_next = Button(window, text=">>", command=lambda: navigate(pobrana_strona, podstrona + 1))


def tvp_fetch(page, subpage, channel):
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
    r = requests.get("http://www.telegazeta.pl/telegazeta.php?channel=" + channel + "&page=" + str(page) + "_" + subpage_str)
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


def polsat_fetch(page, subpage, channel):
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

def navigate(page, subpage):
    global link_do_obrazka
    page_input["state"] = DISABLED
    page_navigate["state"] = DISABLED
    subpage_prev["state"] = DISABLED
    subpage_next["state"] = DISABLED

    if kanal == 1:
        tvp_fetch(page, subpage, "TG1")
    elif kanal == 2:
        tvp_fetch(page, subpage, "TG2")
    elif kanal == 3:
        tvp_fetch(page, subpage, "SAT")
    elif kanal == 4:
        tvp_fetch(page, subpage, "KUL")
    elif kanal == 5:
        tvp_fetch(page, subpage, "SPO")
    elif kanal == 6:
        polsat_fetch(page, subpage, "gazetatvpolsat")
    elif kanal == 7:
        polsat_fetch(page, subpage, "gazetatv4")

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
    navigate(100, 1)


page_label.pack(side=LEFT)
page_input.pack(side=LEFT)
page_navigate.pack(side=LEFT)

subpage_next.pack(side=RIGHT)
subpage_number.pack(side=RIGHT)
subpage_prev.pack(side=RIGHT)

window.config(menu=menu)
window.resizable(0, 0)
navigate(100, 1)

window.mainloop()
