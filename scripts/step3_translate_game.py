#!/usr/bin/env python3
"""
Step 3: Translate game content using approved glossary
"""
import sys
import json
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
    parser = argparse.ArgumentParser(description="Translate Silksong game content")
    parser.add_argument("--glossary", default="./data/glossaries/final_glossary.json",
                       help="Path to approved glossary file")
    parser.add_argument("--provider", choices=["openai", "local", "deepseek"], default="openai",
                       help="AI provider to use")
    parser.add_argument("--model", default="gpt-4o", help="Model name to use")
    parser.add_argument("--batch-size", type=int, default=10, help="Number of entries to translate at once")
    parser.add_argument("--max-files", type=int, help="Maximum number of files to process (for testing)")
    parser.add_argument("--parallel", action="store_true", help="Use parallel processing")
    parser.add_argument("--output-dir", default="./data/translations/ua",
                       help="Output directory for translated files")

    args = parser.parse_args()

    print("🎮 Translating Silksong game content")
    print(f"Provider: {args.provider}, Model: {args.model}")

    # Check glossary
    glossary_path = Path(args.glossary)
    if not glossary_path.exists():
        print(f"❌ Glossary not found: {glossary_path}")
        print("Please complete steps 1 and 2 first, then create final_glossary.json")
        return 1

    with open(glossary_path, 'r', encoding='utf-8') as f:
        glossary_data = json.load(f)
        glossary = glossary_data.get('translations', {})

    print(f"📚 Loaded glossary with {len(glossary)} terms")

    if core_path.exists():
        # Use core functionality
        from core.src.core.config import config_manager
        from core.src.pipeline.translator import Translator
        from core.src.providers.openai_provider import OpenAIProvider
        from core.src.providers.deepseek_provider import DeepSeekProvider
        from src.processor import SilksongProcessor
        from src.config import SILKSONG_CONFIG

        # Update config with output directory
        SILKSONG_CONFIG.output_dir = args.output_dir

        config_manager.register_project(SILKSONG_CONFIG)

        # Select provider
        if args.provider == "openai":
            provider = OpenAIProvider(model=args.model)
        elif args.provider == "deepseek":
            provider = DeepSeekProvider(model=args.model)
        else:
            print(f"❌ Provider {args.provider} not yet implemented")
            return 1

        # Initialize processor and translator
        processor = SilksongProcessor(SILKSONG_CONFIG)
        translator = Translator(
            config=SILKSONG_CONFIG,
            processor=processor,
            provider=provider,
            glossary=glossary
        )

        # Get all source files
        source_files = processor.get_all_source_files()
        if args.max_files:
            source_files = source_files[:args.max_files]

        print(f"📁 Found {len(source_files)} files to translate")

        # Translate files
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for i, source_file in enumerate(source_files, 1):
            print(f"\n[{i}/{len(source_files)}] Processing {source_file.name}...")

            # Read source file
            units = processor.read_file(source_file)
            print(f"  📖 Loaded {len(units)} entries")

            # Translate in batches
            for j in range(0, len(units), args.batch_size):
                batch = units[j:j + args.batch_size]
                print(f"  🔄 Translating batch {j//args.batch_size + 1}...")

                for unit in batch:
                    # Check if term is in glossary
                    if unit.original_text in glossary:
                        unit.translated_text = glossary[unit.original_text]
                    else:
                        # Translate with context
                        prompt = f"""Translate this game text from English to Ukrainian.
Use this glossary for consistency: {json.dumps(glossary, ensure_ascii=False)}

Text to translate: {unit.original_text}

Return only the translation, nothing else."""

                        unit.translated_text = provider.translate(prompt)

            # Write translated file
            output_file = output_dir / processor.get_output_filename(source_file.name)
            processor.write_file(output_file, units)
            print(f"  ✅ Saved to {output_file.name}")

        print("\n" + "🎉" * 20)
        print("TRANSLATION COMPLETED!")
        print("🎉" * 20)
        print(f"\n📁 All translations saved to: {output_dir}")
        print("📦 Use scripts/encrypt.py to prepare files for the game")

    else:
        print("⚠️  Core not found. Please add core as submodule first.")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())