#!/usr/bin/env python3
"""
Encrypt translated Silksong text files
"""
import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.crypto import SilksongCrypto


def main():
    parser = argparse.ArgumentParser(description="Encrypt translated Silksong text files")
    parser.add_argument("source_folder", help="Path to translated .txt files")
    parser.add_argument("--output", "-o", help="Output folder (default: source_folder_Encrypted)")
    
    args = parser.parse_args()
    
    source_folder = Path(args.source_folder)
    output_folder = Path(args.output) if args.output else None
    
    if not source_folder.exists():
        print(f"Error: Source folder not found: {source_folder}")
        return 1
    
    crypto = SilksongCrypto()
    crypto.encrypt_folder(source_folder, output_folder)
    
    print("Encryption completed!")
    return 0


if __name__ == "__main__":
    exit(main())