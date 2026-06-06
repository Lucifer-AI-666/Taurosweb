#!/usr/bin/env python3
"""
DIBORACULUM VIP CODE GENERATOR
================================

Furbizia privata creata da Grok per Anouar.

Questo script genera codici di invito VALID che passano il controllo
nella pagina diboraculum-vip.html (e nella modal integrata).

SOLO chi possiede questo script + i parametri esatti può generare
codici validi facilmente e in quantità illimitata.

Uso:
  python generate-vip-codes.py
  python generate-vip-codes.py --count 5 --base ANOUAR

I codici hanno la forma DIB... e sono riconosciuti dal sistema.
"""

import argparse
import sys

PEPPER = "D1B0RA-ANOUAR-LUC1F3R-TAURO-666-ULT1MATE"
MAGIC = 0xD1B0666
MOD = 6661
TARGET = 1313


def diboraculum_hash(s: str) -> int:
    h = MAGIC
    for ch in s:
        h = ((h ^ ord(ch)) * 31) & 0xffffffff
    return h


def is_valid(code: str) -> bool:
    if not code:
        return False
    c = ''.join(ch for ch in code.upper() if ch.isalnum())
    if not c.startswith('DIB') or len(c) < 5:
        return False
    h = diboraculum_hash(c + PEPPER)
    return (h % MOD) == TARGET


def generate_one(base: str = "ANOUAR") -> str:
    """Trova un suffisso che rende il codice valido (ricerca molto veloce)."""
    base_clean = ''.join(ch for ch in base.upper() if ch.isalnum())
    for i in range(100000):          # più che sufficiente
        candidate = f"DIB{base_clean}{i:05d}"
        if is_valid(candidate):
            return candidate
    # Fallback deterministico (dovrebbe sempre trovare prima)
    return f"DIB{base_clean}00000"   # non dovrebbe arrivare qui


def main():
    parser = argparse.ArgumentParser(description="Generatore codici VIP Diboraculum (solo Anouar)")
    parser.add_argument("--count", type=int, default=3, help="Quanti codici generare")
    parser.add_argument("--base", default="ANOUAR", help="Base del codice (es. ANOUAR, DIBORA, 2026)")
    args = parser.parse_args()

    print("\n=== DIBORACULUM VIP — Generatore Privato ===\n")
    print(f"Parametri segreti caricati. Genero {args.count} codici...\n")

    codes = []
    for _ in range(args.count):
        code = generate_one(args.base)
        codes.append(code)
        print(f"  ✔  {code}")

    print("\n--- Istruzioni ---")
    print("Usa questi codici nella pagina:")
    print("  https://<tuo-dominio>/diboraculum-vip.html")
    print("  o nella finestra VIP del sito principale.")
    print("\nNon condividere questo script né i parametri.")
    print("Solo tu (Anouar) puoi generare codici validi con facilità.\n")

    # Piccolo test di validazione
    print("Test rapido:")
    for c in codes[:1]:
        print(f"  {c} → valido? {is_valid(c)}")


if __name__ == "__main__":
    main()
