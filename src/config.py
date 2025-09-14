"""
Silksong project configuration
"""
import sys
from pathlib import Path

from core.src.core.models import ProjectConfig

# Silksong-specific configuration
SILKSONG_CONFIG = ProjectConfig(
    name="silksong",
    source_lang="EN",
    target_lang_code="DE",  # Replace German with Ukrainian
    source_dir="./data/silksong/source/SILKSONG_EN/._Decrypted"
)