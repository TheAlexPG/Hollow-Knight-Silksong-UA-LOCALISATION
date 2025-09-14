"""
Silksong encryption/decryption utilities
Port of the C# SilksongDecryptor
"""
import json
import base64
from pathlib import Path
from typing import Dict, Any
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class SilksongCrypto:
    """Handles Silksong file encryption/decryption"""
    
    def __init__(self):
        # Same key as C# version
        self.key = b"UKu52ePUBwetZ9wNX88o54dnfKRu0T1l"
        
    def encrypt_bytes(self, data: bytes) -> bytes:
        """Encrypt bytes using AES ECB PKCS7"""
        cipher = Cipher(algorithms.AES(self.key), modes.ECB())
        encryptor = cipher.encryptor()
        
        # Apply PKCS7 padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        
        # Encrypt
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return encrypted
    
    def decrypt_bytes(self, data: bytes) -> bytes:
        """Decrypt bytes using AES ECB PKCS7"""
        cipher = Cipher(algorithms.AES(self.key), modes.ECB())
        decryptor = cipher.decryptor()
        
        # Decrypt
        decrypted_padded = decryptor.update(data) + decryptor.finalize()
        
        # Remove PKCS7 padding
        unpadder = padding.PKCS7(128).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
        return decrypted
    
    def encrypt_string(self, text: str) -> str:
        """Encrypt string and return base64"""
        encrypted_bytes = self.encrypt_bytes(text.encode('utf-8'))
        return base64.b64encode(encrypted_bytes).decode('ascii')
    
    def decrypt_string(self, encrypted_b64: str) -> str:
        """Decrypt base64 string"""
        encrypted_bytes = base64.b64decode(encrypted_b64)
        decrypted_bytes = self.decrypt_bytes(encrypted_bytes)
        return decrypted_bytes.decode('utf-8')
    
    def decrypt_folder(self, source_folder: Path, output_folder: Path = None):
        """Decrypt all .json files in folder"""
        source_folder = Path(source_folder)
        if output_folder is None:
            output_folder = source_folder.parent / f"{source_folder.name}_Decrypted"
        
        output_folder = Path(output_folder)
        output_folder.mkdir(exist_ok=True)
        
        print(f"Decrypting files from {source_folder} to {output_folder}")
        
        for json_file in source_folder.glob("*.json"):
            try:
                # Read JSON file
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract encrypted script
                name = data.get("m_Name", "")
                encrypted_script = data.get("m_Script", "")
                
                if not encrypted_script:
                    print(f"  Skipping {json_file.name}: no m_Script field")
                    continue
                
                # Decrypt
                decrypted_text = self.decrypt_string(encrypted_script)
                
                # Save as .txt with name header
                output_content = f"{name}\n{decrypted_text}"
                output_file = output_folder / f"{json_file.stem}.txt"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(output_content)
                
                print(f"  Decrypted {name}")
                
            except Exception as e:
                print(f"  Error decrypting {json_file.name}: {e}")
    
    def encrypt_folder(self, source_folder: Path, output_folder: Path = None):
        """Encrypt all .txt files in folder"""
        source_folder = Path(source_folder)
        if output_folder is None:
            output_folder = source_folder.parent / f"{source_folder.name}_Encrypted"
        
        output_folder = Path(output_folder)
        output_folder.mkdir(exist_ok=True)
        
        print(f"Encrypting files from {source_folder} to {output_folder}")
        
        for txt_file in source_folder.glob("*.txt"):
            try:
                # Read .txt file
                with open(txt_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                if len(lines) < 2:
                    print(f"  Skipping {txt_file.name}: insufficient lines")
                    continue
                
                # First line is name, rest is script
                name = lines[0].strip()
                script = ''.join(lines[1:])
                
                # Encrypt
                encrypted_script = self.encrypt_string(script)
                
                # Create JSON structure
                json_data = {
                    "m_Name": name,
                    "m_Script": encrypted_script
                }
                
                # Save as .json
                output_file = output_folder / f"{txt_file.stem}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=4)
                
                print(f"  Encrypted {name}")
                
            except Exception as e:
                print(f"  Error encrypting {txt_file.name}: {e}")


def main():
    """CLI interface matching C# version"""
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python silksong_crypto.py -decrypt|-encrypt <folder_path>")
        return
    
    crypto = SilksongCrypto()
    operation = sys.argv[1]
    folder_path = Path(sys.argv[2])
    
    if operation == "-decrypt":
        crypto.decrypt_folder(folder_path)
    elif operation == "-encrypt":
        crypto.encrypt_folder(folder_path)
    else:
        print("Usage: python silksong_crypto.py -decrypt|-encrypt <folder_path>")


if __name__ == "__main__":
    main()