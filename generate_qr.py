#!/usr/bin/env python3

import qrcode
from PIL import Image
import os

def generate_qr_code():
    url = "https://xx-azazel.github.io/Quiz-Dialetti/"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = "qr_code_quiz_dialetti.png"
    img.save(filename)
    
    print(f"✅ QR Code generato con successo: {filename}")
    print(f"🌐 URL: {url}")
    print(f"📱 Scansiona il QR Code per accedere al quiz sui dialetti!")
    
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
