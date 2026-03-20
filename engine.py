import os
import random
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_message(message, password):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return salt + iv + encryptor.tag + ciphertext

def hide_data(img_path, message, password, output_path):
    # 1. Encrypt Message
    encrypted_blob = encrypt_message(message, password)
    binary_data = ''.join(format(b, '08b') for b in encrypted_blob)
    # Add a 32-bit header for length
    data_to_hide = format(len(binary_data), '032b') + binary_data
    
    # 2. Open Image and Get Raw Bytes
    img = Image.open(img_path).convert('RGB')
    width, height = img.size
    # Convert image to a mutable byte list
    pixels = list(img.getdata())
    flat_pixels = []
    for p in pixels:
        flat_pixels.extend([p[0], p[1], p[2]])
    
    # 3. Secure Shuffling
    random.seed(str(password))
    indices = list(range(len(flat_pixels)))
    random.shuffle(indices)
    
    if len(data_to_hide) > len(flat_pixels):
        raise ValueError("Image too small!")

    # 4. Hide Bits
    for i, bit in enumerate(data_to_hide):
        idx = indices[i]
        # Clear the LSB and set it to our bit
        flat_pixels[idx] = (flat_pixels[idx] & ~1) | int(bit)
    
    # 5. Rebuild Image
    new_pixels = []
    for i in range(0, len(flat_pixels), 3):
        new_pixels.append((flat_pixels[i], flat_pixels[i+1], flat_pixels[i+2]))
    
    new_img = Image.new('RGB', (width, height))
    new_img.putdata(new_pixels)
    
    # CRITICAL: Save as PNG with NO optimizations that could shift bits
    new_img.save(output_path, format='PNG', optimize=False)
    return True

def extract_data(img_path, password):
    try:
        img = Image.open(img_path).convert('RGB')
        pixels = list(img.getdata())
        flat_pixels = []
        for p in pixels:
            flat_pixels.extend([p[0], p[1], p[2]])
            
        random.seed(str(password))
        indices = list(range(len(flat_pixels)))
        random.shuffle(indices)
        
        # 1. Read 32-bit length
        len_bits = "".join(str(flat_pixels[indices[i]] & 1) for i in range(32))
        data_len = int(len_bits, 2)
        
        if data_len <= 0 or data_len > len(flat_pixels):
            return "Error: Wrong key or image damaged."

        # 2. Read Encrypted Blob
        extracted_bits = "".join(str(flat_pixels[indices[i]] & 1) for i in range(32, 32 + data_len))
        
        blob_bytes = bytearray()
        for i in range(0, len(extracted_bits), 8):
            blob_bytes.append(int(extracted_bits[i:i+8], 2))
            
        # 3. AES-GCM Decryption
        salt = bytes(blob_bytes[:16])
        iv = bytes(blob_bytes[16:28])
        tag = bytes(blob_bytes[28:44])
        ciphertext = bytes(blob_bytes[44:])
        
        key = derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        
        decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_message.decode('utf-8')
        
    except Exception as e:
        return "Decryption Failed: Check your key or image file."