"""
Silksong-specific file processor for XML localization files
"""
import re
from pathlib import Path
from typing import List
from xml.sax.saxutils import escape, unescape

# When core is added as submodule, these imports will work
import sys
from pathlib import Path

from core.src.processors.base_file_processor import BaseFileProcessor
from core.src.core.models import LineTranslationUnit, TranslationUnit, ProjectConfig


class SilksongProcessor(BaseFileProcessor):
    """File processor for Silksong XML localization files"""
    
    def __init__(self, config: ProjectConfig):
        super().__init__(config)
        self.entry_pattern = re.compile(r'<entry name="([^"]+)">([^<]*)</entry>')
    
    def read_file(self, file_path: Path) -> List[TranslationUnit]:
        """Read Silksong XML file and extract translation units"""
        units = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all entry elements
            matches = self.entry_pattern.findall(content)
            
            for name, text in matches:
                # Unescape HTML entities
                clean_text = unescape(text)
                
                unit = LineTranslationUnit(
                    key=name,
                    original_text=clean_text,
                    metadata={
                        'source_file': str(file_path),
                        'entry_name': name
                    }
                )
                units.append(unit)
                
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            raise
        
        return units
    
    def write_file(self, file_path: Path, units: List[TranslationUnit]) -> None:
        """Write translated units to Silksong XML file"""
        
        # Ensure output directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build XML content
        xml_lines = ['<entries>']
        
        for unit in units:
            if unit.translated_text:
                # Escape special XML characters
                escaped_text = escape(unit.translated_text)
                xml_lines.append(f'<entry name="{unit.key}">{escaped_text}</entry>')
            else:
                # Fallback to original text if no translation
                escaped_text = escape(unit.original_text)
                xml_lines.append(f'<entry name="{unit.key}">{escaped_text}</entry>')
        
        xml_lines.append('</entries>')
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(xml_lines))
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            raise
    
    def get_output_filename(self, source_filename: str) -> str:
        """Transform EN_* filename to DE_* filename"""
        if source_filename.startswith(f"{self.config.source_lang}_"):
            return source_filename.replace(
                f"{self.config.source_lang}_", 
                f"{self.config.target_lang_code}_"
            )
        return source_filename
    
    def get_all_source_files(self) -> List[Path]:
        """Get all Silksong localization files"""
        source_dir = Path(self.config.source_dir)
        if not source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {source_dir}")
        
        # Look for files starting with source language prefix
        pattern = f"{self.config.source_lang}_*"
        return list(source_dir.glob(pattern))
    
    def get_output_path(self, source_file: Path) -> Path:
        """Get full output path for a source file"""
        output_filename = self.get_output_filename(source_file.name)
        return Path(self.config.get_output_dir()) / output_filename