#!/usr/bin/env python3
"""
Step 1: Extract glossary terms from Silksong files
"""
import sys
import json
import argparse
from pathlib import Path

# Imports
from src.config import SILKSONG_CONFIG
from core.src.core.config import config_manager
from core.src.pipeline.extractor import TermExtractor
from src.processor import SilksongProcessor
from core.src.providers.openai_provider import OpenAIProvider
from core.src.providers.local_provider import LocalProvider
from core.src.providers.deepseek_provider import DeepSeekProvider


def main():
    parser = argparse.ArgumentParser(description="Extract glossary terms from Silksong localization files")
    parser.add_argument("--provider", choices=["openai", "local", "deepseek"], default="openai",
                       help="AI provider to use for term extraction")
    parser.add_argument("--model", default="gpt-4o", help="Model name to use")
    parser.add_argument("--max-files", type=int, help="Maximum number of files to process (for testing)")
    parser.add_argument("--output", default="./data/glossaries/extracted_terms.json",
                       help="Output file for extracted terms")

    args = parser.parse_args()

    print("Extracting glossary terms from Silksong files")
    print(f"Provider: {args.provider}, Model: {args.model}")

    # Create AI provider based on args
    if args.provider == "openai":
        ai_provider = OpenAIProvider(model_name=args.model)
    elif args.provider == "local":
        ai_provider = LocalProvider(model_name=args.model)
    elif args.provider == "deepseek":
        ai_provider = DeepSeekProvider(model_name=args.model)

    config_manager.register_project(SILKSONG_CONFIG)
    processor = SilksongProcessor(SILKSONG_CONFIG)
    extractor = TermExtractor(SILKSONG_CONFIG, processor, ai_provider)

    # Extract terms
    terms = extractor.extract_all_terms(max_files=args.max_files)

    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'project': 'silksong',
            'terms': terms,
            'count': len(terms)
        }, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(terms)} unique terms")
    print(f"Saved to: {output_path}")
    return 0


if __name__ == "__main__":
    exit(main())