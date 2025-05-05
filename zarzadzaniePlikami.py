import os
from scipy.io import wavfile

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
