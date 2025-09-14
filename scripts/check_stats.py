#!/usr/bin/env python3
"""
Check translation statistics - what was skipped and why
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.config import config_manager
from src.games.silksong_config import SILKSONG_CONFIG
from src.processors.silksong_processor import SilksongProcessor

def main():
    config_manager.register_project(SILKSONG_CONFIG)
    config = config_manager.get_project("silksong")
    processor = SilksongProcessor(config)
    
    # Get all files
    files = processor.get_all_source_files()
    
    total_units = 0
    empty_units = 0
    short_units = 0
    technical_units = 0
    
    print("Analyzing translation units...")
    print("=" * 50)
    
    for i, file_path in enumerate(files, 1):
        print(f"Processing {i}/{len(files)}: {file_path.name}")
        
        try:
            units = processor.read_file(file_path)
            
            for unit in units:
                total_units += 1
                text = unit.original_text.strip()
                
                # Check for empty/whitespace
                if not text:
                    empty_units += 1
                    continue
                
                # Check for very short content
                if len(text) <= 2:
                    short_units += 1
                    print(f"  Short: '{text}' (key: {unit.key})")
                    continue
                
                # Check for technical content
                if (text.startswith(("debug", "config", "path", "data")) or 
                    text.endswith((".json", ".txt", ".dat")) or
                    text.isdigit()):
                    technical_units += 1
                    print(f"  Technical: '{text}' (key: {unit.key})")
                    continue
                    
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 50)
    print("📊 STATISTICS:")
    print(f"Total units found: {total_units}")
    print(f"Empty units: {empty_units}")
    print(f"Short units (≤2 chars): {short_units}")
    print(f"Technical units: {technical_units}")
    print(f"Expected translatable: {total_units - empty_units - short_units - technical_units}")
    print(f"Actually translated: 5553")
    print(f"Difference: {(total_units - empty_units - short_units - technical_units) - 5553}")

if __name__ == "__main__":
    main()