import re
from collections import Counter
import unicodedata

# --- część A ---

def slugify(text: str) -> str:
    replacements = str.maketrans({
        "ą": "a", "ć": "c", "ę": "e", "ł": "l",
        "ń": "n", "ó": "o", "ś": "s", "ź": "z", "ż": "z",
        "Ą": "A", "Ć": "C", "Ę": "E", "Ł": "L",
        "Ń": "N", "Ó": "O", "Ś": "S", "Ź": "Z", "Ż": "Z",
    }) #po konsultacji z z AI dlaczego znika L przy "Łódź", zmiana sposobu zamiany liter na ręczne zdefiniowanie poszukiwanych i zamienników z uwagi na to że unicodedata.normalize(...).encode('ascii', 'ignore') nie zamienia autmatycznie Ł na l
    
    text = text.translate(replacements)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)

    return text.strip("-")

#Refleksja po zadaniu: copilot w obu promptach dał ten sam kod który źle formatował przypadek "Łódź", po konsultacji z copilotem wyników i przypadków testowych, wdrożono ręczną zamiane liter w celu wyeliminowania błędnych przypadków.

# --- część B ---
# czesc wlasnoreczna, pomoc ai w wytlumaczeniu oraz wymienieniu typow oraz ich metod
# def word_freq(text, n=3):
#     text = re.sub(r"[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s]", "", text)
#     text = text.lower()
#     textArr = text.split(" ")
#     counts = {}
#     for word in textArr:
#         if word == "":
#             continue;
#         counts[word] = counts.get(word, 0) + 1; 
#     result = list(counts.items())
#     result = result[:n]
#     result = sorted(result)
#     return(result)

#kod ostateczny po review z ai, zapytalem "wynik koncowy, co wedlug ciebie jest bledne mozna zrobic lepiej? zrob mi review", 

def word_freq(text, n=3):
    text = text.lower()
    text = re.sub(r"[^a-ząćęłńóśźż\s]", "", text)

    counts = {}

    for word in text.split():
        counts[word] = counts.get(word, 0) + 1

    result = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    return result[:n]

#copilot zwrocil uwage na te bledy ktore uwazam za zasadne:
# 1. Sortowanie - najpierw sortuj po liczbie wystąpień (key=lambda x: (-x[1], x[0])), a dopiero potem bierz [:n], bo obecnie bierzesz pierwsze n elementów słownika zamiast n najczęstszych słów.
# 2. split() zamiast split(" ") - split() automatycznie usuwa wielokrotne spacje, dzięki czemu nie potrzebujesz if word == "": continue.
# 3. Średniki - usuń ;, w Pythonie są zbędne i wyglądają nieidiomatycznie.
# 4. Nazewnictwo - textArr lepiej nazwać words, bo jest krótsze i bardziej zgodne z konwencjami Pythona.
# 5. Regex - najpierw zrób lower(), a potem regex tylko dla małych liter, co uprości wzorzec.
# 6. Czytelność - zamiast result = list(counts.items()) → result = sorted(counts.items(), key=...), bo od razu widać cel kodu.
# 7. Poprawność względem zadania - obecna wersja zwraca pierwsze n słów alfabetycznie, a zadanie wymaga zwrócenia n najczęstszych słów z alfabetycznym rozstrzyganiem remisów.
