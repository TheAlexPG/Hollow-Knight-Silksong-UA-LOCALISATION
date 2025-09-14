# Silksong Translation Scripts

## 📋 Translation Process

The translation process is divided into 3 steps:

### Step 1: Extract Glossary Terms
```bash
python scripts/step1_extract_glossary.py --provider openai --model gpt-4o
```
This extracts important game terms that need consistent translation.

### Step 2: Translate Glossary
```bash
python scripts/step2_translate_glossary.py --provider openai --model gpt-4o
```
Translates the extracted terms. **Review the output before proceeding!**

### Step 3: Translate Game Content
```bash
python scripts/step3_translate_game.py --provider openai --model gpt-4o --batch-size 10
```
Uses the approved glossary to translate all game text files.

## 🔐 Encryption/Decryption

### Decrypt game files (before translation)
```bash
python scripts/decrypt.py path/to/Silksong/Texts
```

### Encrypt translated files (after translation)
```bash
python scripts/encrypt.py data/translations/ua --output path/to/output
```

## 📊 Check Translation Statistics
```bash
python scripts/check_stats.py
```

## 📝 Notes

- Always review glossary translations before step 3
- The glossary ensures consistent terminology across all files
- Use `--max-files` parameter for testing with fewer files
- Encrypted files can be directly placed in the game folder