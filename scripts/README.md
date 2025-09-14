# Скрипти для локалізації Silksong

Цей каталог містить CLI скрипти для автоматизованого перекладу Hollow Knight: Silksong.

## Структура скриптів

```
scripts/
├── step1_extract_glossary.py   # Витяжка ключових термінів з файлів гри
├── step2_translate_glossary.py # Переклад термінів для створення глосарію
├── step3_translate_game.py     # Переклад всіх файлів гри з використанням глосарію
├── decrypt.py                  # Розшифрування файлів гри
├── encrypt.py                  # Зашифрування перекладених файлів
└── check_stats.py              # Перевірка статистики перекладів
```

## Швидкий старт

### 1. Налаштування

```bash
# Клонуйте репозиторій з субмодулями
git clone --recurse-submodules [repo-url]
cd Hollow-Knight-Silksong-UA-LOCALISATION

# Встановіть залежності
pip install -r requirements.txt

# Створіть файл .env (опціонально, для AI провайдерів)
cp .env.example .env
```

### 2. Базові команди

```bash
# Крок 1: Витягнути ключові терміни (3-5 файлів для тесту)
python -m scripts.step1_extract_glossary --provider local --model google/gemma-3-27b --max-files 3

# Крок 2: Перекласти глосарій термінів
python -m scripts.step2_translate_glossary --provider local --model google/gemma-3-27b

# Крок 3: Перекласти файли гри (1 файл для тесту)
python -m scripts.step3_translate_game --provider local --model google/gemma-3-27b --max-files 1
```

## Провайдери AI

### Локальні моделі (безкоштовно)
```bash
# Рекомендована для витяжки термінів
--provider local --model google/gemma-3-12b

# Альтернативи
--provider local --model microsoft/Phi-3.5-mini-instruct
```

### OpenAI (найкраща якість)
```bash
# В .env додайте: OPENAI_API_KEY=your_key_here
--provider openai --model gpt-5-mini     # Рекомендована для глосарію та файлів
--provider openai --model gpt-5          # Максимальна якість
```

### DeepSeek (обмежений бюджет, повільно)
```bash
# В .env додайте: DEEPSEEK_API_KEY=your_key_here
--provider deepseek --model deepseek-chat  # Якщо обмежені ресурси
```

## Детальні параметри

### step1_extract_glossary.py
```bash
python -m scripts.step1_extract_glossary [OPTIONS]

Опції:
  --provider [openai|local|deepseek]  AI провайдер (за замовчуванням: openai)
  --model TEXT                        Назва моделі (за замовчуванням: gpt-4o)
  --max-files INTEGER                 Максимум файлів для обробки (для тестів)

Приклади:
  # Швидке тестування на 3 файлах
  python -m scripts.step1_extract_glossary --provider local --model google/gemma-3-27b --max-files 3

  # Повна витяжка на DeepSeek
  python -m scripts.step1_extract_glossary --provider deepseek --model deepseek-chat
```

### step2_translate_glossary.py
```bash
python -m scripts.step2_translate_glossary [OPTIONS]

Опції:
  --provider [openai|local|deepseek]  AI провайдер (за замовчуванням: openai)
  --model TEXT                        Назва моделі (за замовчуванням: gpt-4o)
  --batch-size INTEGER                Кількість термінів в одному батчі (за замовчуванням: 20)

Приклади:
  # Локальний переклад глосарію
  python -m scripts.step2_translate_glossary --provider local --model google/gemma-3-27b

  # Якісний переклад на DeepSeek
  python -m scripts.step2_translate_glossary --provider deepseek --model deepseek-chat --batch-size 30
```

### step3_translate_game.py
```bash
python -m scripts.step3_translate_game [OPTIONS]

Опції:
  --provider [openai|local|deepseek]  AI провайдер (за замовчуванням: openai)
  --model TEXT                        Назва моделі (за замовчуванням: gpt-4o)
  --batch-size INTEGER                Розмір батчу для перекладу (за замовчуванням: 5)
  --max-files INTEGER                 Максимум файлів для обробки (для тестів)
  --parallel/--no-parallel            Паралельна обробка (за замовчуванням: увімкнено)

Приклади:
  # Тестовий переклад одного файлу
  python -m scripts.step3_translate_game --provider local --model google/gemma-3-27b --max-files 1

  # Повний переклад на OpenAI з великими батчами
  python -m scripts.step3_translate_game --provider openai --model gpt-4o --batch-size 10

  # Послідовний переклад (без паралелізації)
  python -m scripts.step3_translate_game --provider deepseek --model deepseek-chat --no-parallel
```

## Файл .env

Створіть файл `.env` в корені проекту:

```env
# OpenAI API (платно, найкраща якість)
OPENAI_API_KEY=sk-your-openai-key-here

# DeepSeek API (дешево, хороша якість)
DEEPSEEK_API_KEY=your-deepseek-key-here

# Локальний API (LM Studio/Ollama)
LOCAL_API_URL=http://localhost:1234/v1/chat/completions
```

## Стратегії використання

### 🔧 Тестовий пайплайн (безкоштовно)
```bash
python -m scripts.step1_extract_glossary --provider local --model google/gemma-3-12b --max-files 3
python -m scripts.step2_translate_glossary --provider local --model google/gemma-3-12b
python -m scripts.step3_translate_game --provider local --model google/gemma-3-12b --max-files 1
```

### 🎯 Рекомендований (оптимальна якість/швидкість)
```bash
# Витяжка термінів - локально (швидко + безкоштовно)
python -m scripts.step1_extract_glossary --provider local --model google/gemma-3-12b

# Глосарій - OpenAI mini (швидко + якісно)
python -m scripts.step2_translate_glossary --provider openai --model gpt-5-mini

# Контент - OpenAI mini (швидко + якісно)
python -m scripts.step3_translate_game --provider openai --model gpt-5-mini
```

### 💰 Обмежений бюджет (повільно але дешево)
```bash
# Витяжка термінів - локально
python -m scripts.step1_extract_glossary --provider local --model google/gemma-3-12b

# Глосарій та контент - DeepSeek (дешево але повільно)
python -m scripts.step2_translate_glossary --provider deepseek --model deepseek-chat
python -m scripts.step3_translate_game --provider deepseek --model deepseek-chat
```

### 💎 Максимальна якість
```bash
python -m scripts.step1_extract_glossary --provider openai --model gpt-5
python -m scripts.step2_translate_glossary --provider openai --model gpt-5
python -m scripts.step3_translate_game --provider openai --model gpt-5
```

## Структура виводу

```
data/
└── silksong/
    ├── glossaries/
    │   ├── extracted_terms.json      # Витягнуті терміни
    │   ├── final_glossary.json       # Фінальний глосарій для перекладу
    │   └── glossary_for_review.txt   # Людино-читабельний глосарій
    ├── cache/                        # Кеш перекладів
    └── silksong_ua/                  # Перекладені файли
        ├── DE_Achievements-resources.assets-343.txt
        ├── DE_Belltown-resources.assets-286.txt
        └── ...
```

## 🔐 Робота з файлами гри

### Розшифрування файлів (перед перекладом)

**Варіант 1: Python скрипт (рекомендовано)**
```bash
python scripts/decrypt.py path/to/Silksong/Texts
```

**Варіант 2: SilksongDecryptor.exe (фаллбек)**
```bash
# Розшифрувати файли з папки гри
.\SilksongDecryptor.exe -decrypt path/to/Silksong/Texts
```

### Зашифрування перекладених файлів (після перекладу)

**Варіант 1: Python скрипт (рекомендовано)**
```bash
python scripts/encrypt.py data/silksong/silksong_ua --output path/to/output
```

**Варіант 2: SilksongDecryptor.exe (фаллбек)**
```bash
# Зашифрувати перекладені файли
.\SilksongDecryptor.exe -encrypt data/silksong/silksong_ua

# Або з поточної папки
.\SilksongDecryptor.exe -encrypt .
```

### Встановлення в гру
```bash
# Скопіюйте зашифровані файли в папку гри
# Замініть оригінальні файли у:
# "Hollow Knight Silksong_Data/Texts/"
```

### Перевірка статистики перекладів
```bash
python scripts/check_stats.py
```

## Поради по продуктивності

1. **Тестування**: Завжди використовуйте `--max-files` для тестування пайплайну
2. **Локальні моделі**: Ideal для тестів та витяжки термінів
3. **DeepSeek**: Найкращий баланс ціна/якість для глосаріїв
4. **OpenAI**: Найкраща якість для фінального перекладу
5. **Паралелізація**: Використовуйте для швидшої обробки великих файлів

## Усунення проблем

### ModuleNotFoundError
```bash
# Переконайтеся, що запускаете як модуль з коменя проекту
python -m scripts.step1_extract_glossary
# НЕ: python scripts/step1_extract_glossary.py
```

### API ключі не працюють
```bash
# Перевірте файл .env в корені проекту
cat .env
# Переконайтеся, що немає зайвих пробілів навколо =
```

### Локальна модель не відповідає
```bash
# Перевірте, чи працює LM Studio на localhost:1234
curl http://localhost:1234/v1/models
```