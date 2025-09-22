#!/usr/bin/env python3
"""
Script per generare un QR Code che punta al Quiz sui Dialetti
URL: https://xx-azazel.github.io/Quiz-Dialetti/
"""

import qrcode
from PIL import Image
import os

def generate_qr_code():
    # URL del tuo sito GitHub Pages
    url = "https://xx-azazel.github.io/Quiz-Dialetti/"
    
    # Creazione del QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Creazione dell'immagine
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Salvataggio del file
    filename = "qr_code_quiz_dialetti.png"
    img.save(filename)
    
    print(f"✅ QR Code generato con successo: {filename}")
    print(f"🌐 URL: {url}")
    print(f"📱 Scansiona il QR Code per accedere al quiz sui dialetti!")
    
    # Creazione anche di una versione più grande
    qr_big = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=6,
    )
    
    qr_big.add_data(url)
    qr_big.make(fit=True)
    
    img_big = qr_big.make_image(fill_color="black", back_color="white")
    filename_big = "qr_code_quiz_dialetti_large.png"
    img_big.save(filename_big)
    
    print(f"✅ QR Code grande generato: {filename_big}")

if __name__ == "__main__":
    generate_qr_code()
