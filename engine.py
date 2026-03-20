import os
import random
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def derive_key(password, salt):
    """Derives a 32-byte key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_message(message, password):
    """Encrypts a message using AES-GCM (v3 security)."""
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    # Combine salt, iv, tag, and ciphertext into one blob
    return salt + iv + encryptor.tag + ciphertext

def hide_data(img_path, message, password, output_path):
    # 1. Encrypt the data
    encrypted_blob = encrypt_message(message, password)
    binary_data = ''.join(format(b, '08b') for b in encrypted_blob)
    # Add a 32-bit length header so we know when to stop reading
    data_to_hide = format(len(binary_data), '032b') + binary_data
    
    img = Image.open(img_path).convert('RGB')
    pixels = list(img.getdata())
    width, height = img.size
    
    # 2. Secret Shuffling Logic (The "Unique" Part)
    # Use the password as a seed so the random order is ALWAYS the same for this key
    random.seed(password)
    coords = list(range(len(pixels) * 3)) # All available R, G, B slots
    random.shuffle(coords)
    
    if len(data_to_hide) > len(coords):
        raise ValueError("Image too small for this much data!")

    # 3. Bit Manipulation
    pixel_list = list(img.getdata())
    # Flatten pixels into a single R,G,B list for easier bit-swapping
    flat_pixels = [val for pixel in pixel_list for val in pixel]
    
    for i, bit in enumerate(data_to_hide):
        target_index = coords[i]
        # Set the LSB to the data bit
        flat_pixels[target_index] = (flat_pixels[target_index] & ~1) | int(bit)
    
    # Reconstruct the image
    new_pixels = []
    for i in range(0, len(flat_pixels), 3):
        new_pixels.append(tuple(flat_pixels[i:i+3]))
        
    new_img = Image.new('RGB', img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path, "PNG") # Must be PNG to avoid compression loss
    return True