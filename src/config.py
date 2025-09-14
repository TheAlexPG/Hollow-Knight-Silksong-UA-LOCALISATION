"""
Silksong project configuration
"""
import sys
from pathlib import Path

# Add core to path when it's available as submodule
core_path = Path(__file__).parent.parent.parent / "core"
if core_path.exists():
    sys.path.insert(0, str(core_path))
    from core.src.core.models import ProjectConfig
else:
    # Fallback for standalone mode
    from dataclasses import dataclass
    from typing import Dict, Optional

    @dataclass
    class ProjectConfig:
        name: str
        source_lang: str
        target_lang_code: str
        source_dir: str
        glossary_terms: Optional[Dict[str, str]] = None
        preserve_terms: Optional[list] = None

# Silksong-specific configuration
SILKSONG_CONFIG = ProjectConfig(
    name="silksong",
    source_lang="EN",
    target_lang_code="DE",  # Replace German with Ukrainian
    source_dir="./data/source/SILKSONG_EN/._Decrypted"
)