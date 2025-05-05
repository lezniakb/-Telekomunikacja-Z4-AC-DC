import numpy as np
import matplotlib.pyplot as plots

def narysujWykres(nagranie, czestotliwoscProbkowania, tytul):
    # Obliczenie czasu trwania i osi czasu
    czasTrwania = len(nagranie) / czestotliwoscProbkowania
    czasOsi = np.linspace(0, czasTrwania, len(nagranie))

    # Używamy stylu seaborn dla lepszej estetyki
    plots.style.use("seaborn-v0_8-dark-palette")

    # Konfiguracja wykresu
    plots.figure(figsize=(12, 6))
    plots.plot(czasOsi, nagranie, color="mediumblue", linewidth=1.5)
    plots.title(tytul, fontsize=16, fontweight="bold")
    plots.xlabel("Czas [s]", fontsize=14)
    plots.ylabel("Amplituda", fontsize=14)

    # Dodanie mniejszych podziałek i poprawionej siatki
    plots.minorticks_on()
    plots.grid(which="major", linestyle="--", linewidth=0.75, alpha=0.7)
    plots.grid(which="minor", linestyle=":", linewidth=0.5, alpha=0.5)

    plots.tight_layout()
    nazwaPliku = f"wyniki/{tytul.replace(" ", "_")}.png"
    plots.savefig(nazwaPliku, dpi=300)
    plots.close()
    print(f"Zapisano wykres: {nazwaPliku}")