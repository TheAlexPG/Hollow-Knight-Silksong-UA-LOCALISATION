#!/usr/bin/env python3
"""
Step 2: Translate extracted glossary terms
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
    parser = argparse.ArgumentParser(description="Translate Silksong glossary terms")
    parser.add_argument("--input", default="./data/glossaries/extracted_terms.json",
                       help="Input file with extracted terms")
    parser.add_argument("--output", default="./data/glossaries/translated_glossary.json",
                       help="Output file for translated glossary")
    parser.add_argument("--provider", choices=["openai", "local", "deepseek"], default="openai",
                       help="AI provider to use")
    parser.add_argument("--model", default="gpt-4o", help="Model name to use")
    parser.add_argument("--batch-size", type=int, default=20, help="Number of terms to translate at once")

    args = parser.parse_args()

    print("🌐 Translating glossary terms")
    print(f"Provider: {args.provider}, Model: {args.model}")

    # Load extracted terms
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        print("Please run step1_extract_glossary.py first")
        return 1

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        terms = data.get('terms', [])

    print(f"📚 Loaded {len(terms)} terms to translate")

    if core_path.exists():
        # Use core functionality
        from src.core.config import config_manager
        from src.providers.openai_provider import OpenAIProvider
        from src.providers.deepseek_provider import DeepSeekProvider
        from src.config import SILKSONG_CONFIG

        config_manager.register_project(SILKSONG_CONFIG)

        # Select provider
        if args.provider == "openai":
            provider = OpenAIProvider(model=args.model)
        elif args.provider == "deepseek":
            provider = DeepSeekProvider(model=args.model)
        else:
            print(f"❌ Provider {args.provider} not yet implemented")
            return 1

        # Translate terms in batches
        translated_terms = {}
        for i in range(0, len(terms), args.batch_size):
            batch = terms[i:i + args.batch_size]
            print(f"Translating batch {i//args.batch_size + 1}/{(len(terms)-1)//args.batch_size + 1}...")

            # Create translation prompt
            prompt = f"""Translate these game terms from English to Ukrainian.
Keep proper names (character names, location names) in English.
Terms to translate:
{json.dumps(batch, ensure_ascii=False, indent=2)}

Return as JSON: {{"term1": "translation1", "term2": "translation2"}}"""

            response = provider.translate(prompt)
            try:
                batch_translations = json.loads(response)
                translated_terms.update(batch_translations)
            except json.JSONDecodeError:
                print(f"⚠️  Failed to parse batch {i//args.batch_size + 1}")

        # Save translated glossary
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'project': 'silksong',
                'source_lang': 'EN',
                'target_lang': 'UA',
                'translations': translated_terms,
                'count': len(translated_terms)
            }, f, indent=2, ensure_ascii=False)

        print(f"✅ Translated {len(translated_terms)} terms")
        print(f"📄 Saved to: {output_path}")

        # Create review file
        review_path = output_path.parent / "glossary_for_review.txt"
        with open(review_path, 'w', encoding='utf-8') as f:
            f.write("SILKSONG GLOSSARY FOR REVIEW\n")
            f.write("=" * 50 + "\n\n")
            for term, translation in sorted(translated_terms.items()):
                f.write(f"{term:30} → {translation}\n")

        print(f"📝 Review file created: {review_path}")
        print("\n⚠️  Please review and edit the translations before proceeding to step 3!")

    else:
        print("⚠️  Core not found. Please add core as submodule first.")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())