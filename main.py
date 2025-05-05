import numpy as np
from scipy import signal
import os

from dzwiekObsluga import nagrajDzwiek, zapiszDzwiek, odtworzDzwiek
from wykresyGenerator import narysujWykres

def obliczSNR(sygnalOryginalny, sygnalTestowy):
    if len(sygnalOryginalny) != len(sygnalTestowy):
        sygnalTestowy = signal.resample(sygnalTestowy, len(sygnalOryginalny))
    szum = sygnalOryginalny - sygnalTestowy
    mocSygnalu = np.sum(sygnalOryginalny ** 2)
    mocSzumu = np.sum(szum ** 2)
    return float('inf') if mocSzumu == 0 else 10 * np.log10(mocSygnalu / mocSzumu)

def pokazInformacje(nagranie, czestotliwoscProbkowania, bityKwantyzacji):
    print("\nInformacje o nagraniu:")
    print(f"- Długość: {len(nagranie) / czestotliwoscProbkowania:.2f}s")
    print(f"- Próbki: {len(nagranie)}")
    print(f"- Częstotliwość: {czestotliwoscProbkowania} Hz")
    print(f"- Kwantyzacja: {bityKwantyzacji} bit")
    print(f"- Zakres: {np.min(nagranie)} do {np.max(nagranie)}")

def zapiszKonfig():
    # Zakładamy poprawne wprowadzenie wartości przez użytkownika
    czasNagrania = float(input("Podaj czas nagrania (s): "))
    czestotliwosc = int(input("Podaj częstotliwość próbkowania (np. 8000, 16000, 44100): "))
    bity = int(input("Podaj liczbę bitów kwantyzacji (np. 8, 16, 24): "))
    return czasNagrania, czestotliwosc, bity

def main():
    if not os.path.exists("wyniki"):
        os.makedirs("wyniki")

    config = None
    recordings = []
    charts = []

    while True:
        print("----------------------------------\n"
        "Testowanie przetworników A/C i C/A\n"
        "1. Zapisz nową konfigurację\n"
        "2. Nagraj dźwięk\n"
        "3. Odtwórz dźwięk\n"
        "0. Zakończ działanie")
        wybor = input("Wybór [0-3]: ")
        print("----------------------------------")
        if wybor == "0":
            print("Koniec działania programu")
            break

        elif wybor == "1":
            config = zapiszKonfig()
            print("Konfiguracja zapisana.")

        elif wybor == "2":
            if config is None:
                print("Najpierw zapisz konfigurację (opcja 1).")
            else:
                czas, fs, bity = config
                nagranie = nagrajDzwiek(czas, fs, bity)
                name = input("Podaj nazwę nagrania: ")

                filename = f"wyniki/{name}.wav"
                zapiszDzwiek(filename, nagranie, fs, bity)
                pokazInformacje(nagranie, fs, bity)
                chart_name = f"{name}"

                narysujWykres(nagranie, fs, chart_name)
                recordings.append({"name": name, "data": nagranie, "fs": fs, "bity": bity})
                charts.append({"name": chart_name, "data": nagranie, "fs": fs})
                print("Nagranie zapisane i wykres wygenerowany.")

        elif wybor == "3":
            if len(recordings) == 0:
                print("Brak nagrań. Najpierw nagraj dźwięk (opcja 2).")
            else:
                print("Lista nagrań:")
                for i, rec in enumerate(recordings):
                    print(f"{i+1}. {rec['name']}")
                choice = int(input("Wybierz numer nagrania do odtworzenia: "))
                selected = recordings[choice - 1]
                odtworzDzwiek(selected["data"], selected["fs"])

        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main()
