#!/usr/bin/env python3
"""
Step 1: Extract glossary terms from Silksong files
"""
import sys
import argparse
from pathlib import Path

# Add paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Future: Add core when available as submodule
core_path = project_root.parent / "core"
if core_path.exists():
    sys.path.insert(0, str(core_path))

def main():
    parser = argparse.ArgumentParser(description="Extract glossary terms from Silksong localization files")
    parser.add_argument("--provider", choices=["openai", "local", "deepseek"], default="openai",
                       help="AI provider to use for term extraction")
    parser.add_argument("--model", default="gpt-4o", help="Model name to use")
    parser.add_argument("--max-files", type=int, help="Maximum number of files to process (for testing)")
    parser.add_argument("--output", default="./data/glossaries/extracted_terms.json",
                       help="Output file for extracted terms")

    args = parser.parse_args()

    print("📚 Extracting glossary terms from Silksong files")
    print(f"Provider: {args.provider}, Model: {args.model}")

    # Import configs
    from src.config import SILKSONG_CONFIG

    if core_path.exists():
        # Use core functionality
        from src.core.config import config_manager
        from src.pipeline.extractor import TermExtractor
        from src.processor import SilksongProcessor

        config_manager.register_project(SILKSONG_CONFIG)
        processor = SilksongProcessor(SILKSONG_CONFIG)
        extractor = TermExtractor(SILKSONG_CONFIG, processor)

        # Extract terms
        terms = extractor.extract_all_terms(max_files=args.max_files)

        # Save to file
        import json
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'project': 'silksong',
                'terms': terms,
                'count': len(terms)
            }, f, indent=2, ensure_ascii=False)

        print(f"✅ Extracted {len(terms)} unique terms")
        print(f"📄 Saved to: {output_path}")
    else:
        print("⚠️  Core not found. Please add core as submodule first.")
        print("Run: git submodule add <core-repo-url> ../core")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())