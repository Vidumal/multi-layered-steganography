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