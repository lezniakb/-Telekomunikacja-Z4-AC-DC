import numpy as np
from scipy import signal
import os
from scipy.io import wavfile

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

def zapiszPlik(name, nagranie, fs, bity):
    filepath = os.path.join(f"{name}.txt")
    with open(filepath, "w") as f:
        f.write(f"{name}\n")
        f.write(f"{fs}\n")
        f.write(f"{bity}\n")
        f.write(f"{len(nagranie)}\n")

def odczytajDane():
    recordings = []
    folder = "wyniki"

    for plik in os.listdir(folder):
        if plik.endswith(".txt"):
            sciezka = os.path.join(folder, plik)
            try:
                with open(sciezka, "r") as f:
                    lines = f.readlines()
                    name = lines[0].strip()
                    fs = int(lines[1])
                    bity = int(lines[2])

                wav_path = os.path.join(f"{name}")
                if os.path.exists(wav_path):
                    fs_read, data = wavfile.read(wav_path)
                    recordings.append({
                        "name": name,
                        "data": data,
                        "fs": fs,
                        "bity": bity
                    })
                else:
                    print(f"Brakuje pliku WAV: {wav_path}")
            except Exception as e:
                print(f"Nie udało się wczytać {plik}: {e}")
    return recordings

def main():
    if not os.path.exists("wyniki"):
        os.makedirs("wyniki")

    config = None
    while True:
        recordings = odczytajDane()
        charts = []
        print("----------------------------------\n"
        "Testowanie przetworników A/C i C/A\n"
        "1. Zapisz nową konfigurację\n"
        "2. Nagraj dźwięk\n"
        "3. Odtwórz dźwięk\n"
        "4. Oblicz SNR między najlepszym wynikiem, a każdym pozostałym\n"
        "0. Zakończ działanie")
        wybor = input("Wybór [0-4]: ")
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
                zapiszPlik(filename, nagranie, fs, bity)
                charts.append({"name": chart_name, "data": nagranie, "fs": fs})
                print("Nagranie zapisane i wykres wygenerowany.")

        elif wybor == "3":
            if len(recordings) == 0:
                print("Brak nagrań. Najpierw nagraj dźwięk (opcja 2).")
            else:
                print("Lista nagrań:")
                for i, rec in enumerate(recordings):
                    print(f"{i+1}. {rec['name'][7:]}")
                choice = int(input("Wybierz numer nagrania do odtworzenia: "))
                selected = recordings[choice - 1]
                odtworzDzwiek(selected["data"], selected["fs"])

        elif wybor == "4":
            if len(recordings) < 2:
                print("Potrzeba co najmniej dwóch nagrań do porównania.")
            else:
                najlepszy = max(recordings, key=lambda r: (r['bity'], r['fs']))
                print(f"Najlepszy sygnał: '{najlepszy['name'][7:]}' ({najlepszy['bity']} bit, {najlepszy['fs']} Hz)")

                for rec in recordings:
                    if rec is najlepszy:
                        continue
                    snr = obliczSNR(najlepszy['data'], rec['data'])
                    print(f"SNR między '{najlepszy['name'][7:]}' a '{rec['name'][7:]}': {snr:.2f} dB")

        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

        input("Naciśnij Enter aby kontynuować...")
if __name__ == "__main__":
    main()
