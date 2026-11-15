# POLSOLIDE — 20 prostych gadżetów do produkcji seryjnej

Kolekcja wykonana na bazie istniejących czterech projektów, z zachowaniem barw POLSOLIDE:
`#18181B` czarny, `#B7131C` czerwony, `#F1F0EC` biały.

**Otwórz:** [`index.html`](index.html) lub GitHub Pages (katalog).

## Zawartość
- `3mf/NN_*.3mf` — 20 pojedynczych kolorowych modeli, części czarne/czerwone/białe.
- `3mf/NN_*_plyta.3mf` — 20 płytek seryjnych z kopiami, każda zawiera trzy barwy.
- `stl/NN_*_{base,red,white}.stl` — osobne STL dla każdego koloru, w tym samym układzie współrzędnych.
- `src/NN_*.scad` — edytowalne źródła OpenSCAD z oznaczeniami/numerami.
- `previews/*.svg` — podglądy wektorowe, nie zdjęcia gotowych przedmiotów.
- `PACZKA_20_MODELI.zip` — cała kolekcja do pobrania.
- `OFERTA-POLSOLIDE.md` — propozycje cenowe i warianty zamówień.
- `produkty.json`, `kalkulator_produkcji.csv` — wymiary, masy i szacunki partii.

## Druk w Bambu Studio
1. Zaimportuj pojedynczy plik 3MF albo wersję `_plyta.3mf`.
2. Wybierz drukarkę Bambu P2S, dyszę 0,4 mm i odpowiedni profil filamentu.
3. Przypisz trzy kolory AMS (jeśli slicer nie przeniesie palety materiałów automatycznie).
4. Wykonaj slicing i sprawdź, że wszystkie modele leżą na stole, nic nie koliduje z wieżą czyszczącą i wszystkie warstwy są poprawne.
5. Dla profilu FAST zacznij od warstwy 0,24 mm. Dla drobnych napisów porównaj 0,16–0,20 mm.
6. Wydrukuj pojedynczy model do kontroli wymiarów, dopiero później całą płytę.

## 8 godzin
**Nie gwarantujemy dokładnie 8h.** Bez faktycznego slicingu oraz kalibracji drukarki nie można uczciwie przypisać rzeczywistego czasu. Wstępne szacunki dla pełnych płyt przy szybkim profilu to zazwyczaj 4–6h. To świadomie szybkie projekty: nie dokładamy masy tylko po to, by druk trwał dłużej. Jeżeli zależy Ci na zajęciu pełnej 8-godzinnej zmiany, dopasuj liczbę kopii i profil warstwy do wskazań Bambu Studio.

## Produkcja i bezpieczeństwo
- Modele nie powinny wymagać podpór. Większość wydruków nie wymaga montażu.
- Magnesy mają gniazdo 10,35 mm na magnes 10×2 mm; klejenie i test utrzymania po wydruku.
- Drobne produkty z małymi elementami i magnesami nie są zabawkami dla dzieci.
- Przy wydrukach dla klientów testuj ostre krawędzie, temperaturę, wytrzymałość otworów i odporność użytego materiału.
- Wentylacja i nadzór nad drukiem obowiązują także przy PLA. Nie planuj nocnego druku bez nadzoru w sypialni.
