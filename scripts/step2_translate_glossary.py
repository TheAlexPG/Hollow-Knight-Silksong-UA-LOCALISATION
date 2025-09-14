#!/usr/bin/env python3
"""
Step 2: Translate extracted glossary terms
"""
import sys
import json
import argparse
from pathlib import Path

# Imports
from src.config import SILKSONG_CONFIG
from core.src.core.config import config_manager
from core.src.utils.glossary import GlossaryManager
from core.src.providers.openai_provider import OpenAIProvider
from core.src.providers.local_provider import LocalProvider
from core.src.providers.deepseek_provider import DeepSeekProvider


def main():
    parser = argparse.ArgumentParser(description="Translate Silksong glossary terms")
    parser.add_argument("--provider", choices=["openai", "local", "deepseek"], default="openai",
                       help="AI provider to use")
    parser.add_argument("--model", default="gpt-4o", help="Model name to use")
    parser.add_argument("--batch-size", type=int, default=20, help="Number of terms to translate at once")

    args = parser.parse_args()

    print("Translating glossary terms")
    print(f"Provider: {args.provider}, Model: {args.model}")

    # Setup
    config_manager.register_project(SILKSONG_CONFIG)
    glossary_manager = GlossaryManager(SILKSONG_CONFIG)

    # Load extracted terms
    terms = glossary_manager.load_extracted_terms()
    if not terms:
        print("No extracted terms found. Please run step1_extract_glossary.py first")
        return 1

    print(f"Loaded {len(terms)} terms to translate")

    # Create AI provider
    if args.provider == "openai":
        ai_provider = OpenAIProvider(model_name=args.model)
    elif args.provider == "local":
        ai_provider = LocalProvider(model_name=args.model)
    elif args.provider == "deepseek":
        ai_provider = DeepSeekProvider(model_name=args.model)

    # Translate terms using provider's glossary method
    print("Translating all terms...")
    translated_terms = ai_provider.translate_glossary(
        terms,
        source_lang=SILKSONG_CONFIG.source_lang,
        target_lang="Ukrainian"
    )

    # Save final glossary directly
    final_file = glossary_manager.create_final_glossary(translated_terms)

    print(f"Translated {len(translated_terms)} terms")
    print(f"Final glossary: {final_file}")
    print("Glossary is ready for use in translation!")

    return 0


if __name__ == "__main__":
    exit(main())