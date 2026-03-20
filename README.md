# CyberSteg Pro: Multi-Layered Image Steganography

**CyberSteg Pro** is a high-security steganography tool built in Python. Developed as a specialized security project, it combines military-grade encryption with a randomized data-hiding algorithm to ensure that hidden messages are invisible to the eye and mathematically protected against extraction without the correct secret key.

## 🛡️ Security Architecture

The application employs a defense-in-depth strategy, using four distinct layers to protect data:

1. **Layer 1: AES-256-GCM Encryption** – Uses Authenticated Encryption (GCM mode) to ensure the message remains private and has not been tampered with.
2. **Layer 2: PBKDF2 Key Stretching** – Protects against brute-force attacks by hashing the user's password with a random salt and 100,000 iterations.
3. **Layer 3: Seeded PRNG Shuffling** – Instead of hiding data in a predictable linear pattern, the secret key acts as a "seed" to shuffle pixel coordinates, scattering data across the image.
4. **Layer 4: Lossless LSB Embedding** – Uses a "Zero-Optimization" PNG saving method to ensure that the Least Significant Bits (LSB) are never altered by image compression.

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher
* `pip` (Python package installer)

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/CyberSteg-Pro.git](https://github.com/yourusername/CyberSteg-Pro.git)
   cd CyberSteg-Pro

2. Install the required dependencies:
   ```bash
   pip install customtkinter Pillow cryptography


### Usage
1. Launch the App:
   ```bash
   python main.py

2. To Encrypt & Hide:
   * Select the "Encrypt & Hide" tab.
   * Browse for a base image (PNG recommended).
   * Enter a strong Secret Key and your message.
   * Click "Hide & Save" and save the output as a .png file.

3. To Decrypt & Extract:
   * Select the "Decrypt & Extract" tab.
   * Browse for the encrypted .png image.
   * Enter the exact Secret Key used during encryption.
   * Click "Decrypt Message" to view the recovered content.

## 🛠️ Built With

* **CustomTkinter** – For a modern, dark-mode professional desktop interface.
* **Pillow (PIL)** – For precise pixel-level image manipulation and channel control.
* **Cryptography (hazmat)** – For professional-grade AES-GCM and PBKDF2 implementation.
* **Python** – Core logic, randomized pathing, and backend processing.

## 📝 Technical Implementation Notes

This project was developed at SLIIT as part of a Cybersecurity specialization.

**Overcoming Bit-Drifting**
A major technical challenge addressed was Bit-Drifting. Standard image saving often applies optimizations that "correct" pixel values, destroying steganographic data.

* Channel Locking: The tool forces a 3-channel RGB color space to bypass Alpha/Transparency issues.
* Lossless Preservation: By disabling PNG optimization (optimize=False) and using direct byte-list mapping, the tool maintains 100% data integrity.
* Integrity Verification: Unlike basic LSB scripts, the use of AES-GCM allows the tool to verify an internal authentication tag. If the image is altered or the key is wrong, the tool identifies the integrity failure rather than displaying garbled data.


## ⚖️ License
This project is licensed under the MIT License. It is intended for **educational and research purposes only.**