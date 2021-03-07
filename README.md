# telegazeta-explorer
Przeglądarka teletekstu (Telegazety) dla kanałów TVP i Polsatu napisana w Pythonie

## Czemu? ##
Czemu nie?

## Twój kod ssie. ##
Wiem.

## Windows powiedział mi że to wirus! To niedopuszczalne, już leci pozew za rozpowszechnianie malware!
Spokojnie.
Windows po prostu jest paranoikiem, wykrywającym wszystko skompilowane [pyinstallerem](https://www.pyinstaller.org/) jako wirusy.
Możesz bezpiecznie plik odblokować (nie mogę powiedzieć jak, bo na codzień używam Linuxa), nic ci nie grozi.

Jeśli nadal się obawiasz, możesz uruchomić program z źródła.

## Jak to uruchomić z źródła? ##
**Potrzebujesz Pythona 3.** Wg. moich super naukowych badań wynika że program odpala się od min. Pythona 3.6. Niżej może też, ale nie chciało mi się sprawdzać.
Pythona (i pip) pobierzesz z:
* W przypadku Windowsa: [oficjalnej strony.](https://www.python.org/downloads/) **Pamiętaj aby przy instalacji zaznaczyć Add Python to PATH!**
* W przypadku Linuxa: sprawdź repozytoria swojej dystrybucji. **Pamiętaj o doinstalowaniu pip i, jeśli jest rozbite na oddzielny pakiet - tkinter!**
* W przypadku Mac OS: Nie wiem. Nie mam Maca, [ale szukając w internetach wyczytałem że można zainstalować z homebrew.](https://docs.python-guide.org/starting/install3/osx/)

Jeśli masz Pythona i pip, to:
1. Pobierz kod źródłowy, za pomocą git clone lub prosto z GitHuba.
2. W folderze z kodem otwórz terminal, wiersz polecenia, cokolwiek.
3. Wpisz `pip install -r requirements.txt` (lub `pip3 install -r requirements.txt`, jeśli w twoim wypadku tak to działa. Czasami może być konieczne zastąpienie komendy `pip` komendą `python -m pip` lub `python3 -m pip`) 
4. Uruchom plik. Na Windowsie możesz to zrobić bezpośrednio z eksploratora, ale jeśli wolisz to możesz wpisać `py telegazeta.py`, `python telegazeta.py`, `python3 telegazeta.py`, zależy jak to u ciebie jest.

## Czego to używa? ##
* Wbudowanego [tkintera](https://docs.python.org/3/library/tkinter.html) do GUI
* Wbudowanego [re](https://docs.python.org/3/library/re.html) do interpretacji REGEX
* Wbudowanego [shutil](https://docs.python.org/3/library/shutil.html) do zapisywania plików
* Wbudowanego [sys](https://docs.python.org/3/library/sys.html) do error handlingu
* [Requests](https://requests.readthedocs.io/en/master/) do scrapowania stron Telegazety i pobierania obrazków
* [Pillow](https://pillow.readthedocs.io/en/stable/) aby konwertować obrazki na format rozumiany przez tkinter

## Obsługiwane kanały ##
* TVP1
* TVP2
* TVP Polonia
* TVP Kultura
* TVP Sport
* Polsat
* TV4

## Screenshoty ##
![Screenshot 1](https://i.imgur.com/Ii4PO66.png)
![Screenshot 2](https://i.imgur.com/vmyvXEY.png)
![Screenshot 3](https://i.imgur.com/4SF3AOQ.png)
![Screenshot 4](https://i.imgur.com/6dwg1bM.png)
