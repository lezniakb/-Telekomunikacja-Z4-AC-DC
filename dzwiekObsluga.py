import sounddevice as sd
import soundfile as sf
import time
import numpy as np

def nagrajDzwiek(czasNagrania, czestotliwoscProbkowania, bityKwantyzacji):
    print("Nagrywanie za 1s...")
    time.sleep(1)
    print(f"Nagrywanie dźwięku: {czasNagrania}s, {czestotliwoscProbkowania}Hz, {bityKwantyzacji}bit")

    try:
        nagranie = sd.rec(int(czasNagrania * czestotliwoscProbkowania),
                          samplerate=czestotliwoscProbkowania,
                          channels=1,
                          dtype='float32')
        sd.wait()
    except Exception as e:
        print(f"Błąd nagrywania: {e}")
        return None

    print("Nagrywanie zakończone!")

    if bityKwantyzacji < 32:
        poziomyKwantyzacji = 2 ** bityKwantyzacji
        maxWartosc = np.max(np.abs(nagranie))
        nagranieSkalowane = nagranie / maxWartosc if maxWartosc > 0 else nagranie
        nagranieKwantyzowane = np.round(nagranieSkalowane * (poziomyKwantyzacji / 2 - 1)) / (poziomyKwantyzacji / 2 - 1)
        nagranie = nagranieKwantyzowane

    return nagranie


def zapiszDzwiek(nazwaPliku, nagranie, czestotliwoscProbkowania, bityKwantyzacji):
    try:
        if bityKwantyzacji <= 16:
            sf.write(nazwaPliku, nagranie, czestotliwoscProbkowania)
        elif bityKwantyzacji <= 24:
            sf.write(nazwaPliku, nagranie, czestotliwoscProbkowania, subtype='PCM_24')
        else:
            sf.write(nazwaPliku, nagranie, czestotliwoscProbkowania, subtype='FLOAT')
        print(f"Zapisano dźwięk do pliku: {nazwaPliku}")
    except Exception as e:
        print(f"Błąd zapisu pliku: {e}")


def odtworzDzwiek(nagranie, czestotliwoscProbkowania):
    try:
        print("Odtwarzam nagrany dźwięk...")
        sd.play(nagranie, czestotliwoscProbkowania)
        sd.wait()
        print("Odtwarzanie zakończone!")
    except Exception as e:
        print(f"Błąd odtwarzania: {e}")

