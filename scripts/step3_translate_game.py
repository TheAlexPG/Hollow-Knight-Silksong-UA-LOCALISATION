#!/usr/bin/env python3
"""
Step 3: Translate game content using approved glossary
"""
import sys
import argparse
from pathlib import Path

# Imports
from src.config import SILKSONG_CONFIG
from core.src.core.config import config_manager
from core.src.pipeline.translator import Translator
from core.src.providers.openai_provider import OpenAIProvider
from core.src.providers.local_provider import LocalProvider
from core.src.providers.deepseek_provider import DeepSeekProvider
from src.processor import SilksongProcessor


def main():
    parser = argparse.ArgumentParser(description="Translate Silksong game content")
    parser.add_argument("--provider", choices=["openai", "local", "deepseek"], default="openai",
                       help="AI provider to use")
    parser.add_argument("--model", default="gpt-4o", help="Model name to use")
    parser.add_argument("--batch-size", type=int, default=5, help="Translation batch size")
    parser.add_argument("--max-files", type=int, help="Maximum number of files to process (for testing)")
    parser.add_argument("--parallel", action="store_true", default=True, help="Enable parallel processing")
    parser.add_argument("--no-parallel", dest="parallel", action="store_false", help="Disable parallel processing")

    args = parser.parse_args()

    print("Translating Silksong game content")
    print(f"Provider: {args.provider}, Model: {args.model}")
    print(f"Batch size: {args.batch_size}, Parallel: {args.parallel}")

    # Setup
    config_manager.register_project(SILKSONG_CONFIG)
    config_manager.ensure_project_dirs(SILKSONG_CONFIG.name)

    print(f"Source: {SILKSONG_CONFIG.source_dir}")
    print(f"Output: {SILKSONG_CONFIG.get_output_dir()}")

    # Create AI provider
    if args.provider == "openai":
        ai_provider = OpenAIProvider(model_name=args.model)
    elif args.provider == "local":
        ai_provider = LocalProvider(model_name=args.model)
    elif args.provider == "deepseek":
        ai_provider = DeepSeekProvider(model_name=args.model)

    # Create processor and translator
    processor = SilksongProcessor(SILKSONG_CONFIG)
    translator = Translator(SILKSONG_CONFIG, processor, ai_provider, batch_size=args.batch_size)

    # Load glossary
    glossary = translator.load_glossary()
    print(f"Loaded glossary with {len(glossary)} terms")

    # Translate files
    print(f"Using {'parallel' if args.parallel else 'sequential'} translation...")
    results = translator.translate_all_files(max_files=args.max_files, parallel=args.parallel)

    print("Translation completed!")
    print(f"Translated files saved to: {SILKSONG_CONFIG.get_output_dir()}")

    return 0


if __name__ == "__main__":
    exit(main())