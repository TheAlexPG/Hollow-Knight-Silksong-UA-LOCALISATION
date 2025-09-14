# Інструкція по локалізації Silksong

Цей документ містить повну інструкцію по створенню українського мовного пакету для Hollow Knight: Silksong.

## 📋 Огляд системи

### Архітектура проекту
```
Hollow-Knight-Silksong-UA-LOCALISATION/
├── core/                    # Спільна логіка для перекладів (субмодуль)
│   ├── src/
│   │   ├── processors/      # Обробники файлів для різних ігор
│   │   ├── providers/       # AI провайдери (OpenAI, DeepSeek, Local)
│   │   ├── pipeline/        # Компоненти пайплайну перекладу
│   │   ├── utils/           # Допоміжні утиліти (криптографія, глосарій)
│   │   └── games/           # Конфігурації конкретних ігор
│   └── scripts/             # Референсні скрипти
├── scripts/                 # CLI скрипти для кожного кроку
│   ├── step1_extract_glossary.py   # Витяжка термінів
│   ├── step2_translate_glossary.py # Переклад глосарію
│   ├── step3_translate_game.py     # Переклад гри
│   ├── decrypt.py                  # Розшифрування файлів
│   └── encrypt.py                  # Зашифрування файлів
├── src/                     # Silksong-специфічний код
│   ├── config.py            # Конфігурація проекту
│   ├── processor.py         # Обробник файлів Silksong
│   └── crypto.py            # Криптографічні утиліти
├── data/                    # Дані проектів (глосарії, кеш, результати)
│   └── silksong/
│       ├── source/          # Англійські файли (розшифровані)
│       ├── glossaries/      # Глосарії термінів
│       ├── cache/           # Кеш перекладів
│       └── silksong_ua/     # Перекладені файли
└── releases/                # Готові релізи для гравців
```

## 🚀 Встановлення та налаштування

### 1. Клонування репозиторію
```bash
# Клонуйте з субмодулями
git clone --recurse-submodules https://github.com/your-repo/Hollow-Knight-Silksong-UA-LOCALISATION.git
cd Hollow-Knight-Silksong-UA-LOCALISATION

# Або додайте субмодуль окремо
git submodule update --init --recursive
```

### 2. Встановлення залежностей
```bash
# Створіть віртуальне середовище
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Встановіть залежності
pip install -r requirements.txt
pip install cryptography  # Для Silksong криптографії
```

### 3. Налаштування AI провайдерів

Створіть файл `.env` в корені проекту:

```env
# OpenAI API (платно, найкраща якість)
OPENAI_API_KEY=sk-your-openai-key-here

# DeepSeek API (дешево, хороша якість)
DEEPSEEK_API_KEY=your-deepseek-key-here

# Локальний API (LM Studio/Ollama)
LOCAL_API_URL=http://localhost:1234/v1/chat/completions
```

## 🎯 AI Провайдери та стратегії

### 📊 Порівняння провайдерів

| Провайдер | Модель | Швидкість | Якість | Вартість | Рекомендоване використання |
|-----------|--------|-----------|--------|----------|----------------------------|
| **Local** | gemma-3-12b | Середня | Добра | Безкоштовно | **Витяжка термінів** |
| **OpenAI** | gpt-5-mini | Дуже швидка | Відмінна | Помірно | **Глосарій та переклад файлів** |
| **DeepSeek** | deepseek-chat | Повільна | Відмінна | Дешево | Обмежений бюджет |
| **OpenAI** | gpt-5 | Швидка | Найкраща | Дорого | Максимальна якість |

### 🏆 Рекомендовані стратегії

#### 1. **Тестовий пайплайн** (безкоштовно)
```bash
# Весь пайплайн на локальних моделях
python -m scripts.step1_extract_glossary --provider local --model google/gemma-3-12b --max-files 3
python -m scripts.step2_translate_glossary --provider local --model google/gemma-3-12b
python -m scripts.step3_translate_game --provider local --model google/gemma-3-12b --max-files 1
```

#### 2. **Рекомендований пайплайн** (оптимальна якість/швидкість)
```bash
# Витяжка - локально (швидко + безкоштовно)
python -m scripts.step1_extract_glossary --provider local --model google/gemma-3-12b

# Глосарій - OpenAI mini (швидко + якісно)
python -m scripts.step2_translate_glossary --provider openai --model gpt-5-mini

# Контент - OpenAI mini (швидко + якісно)
python -m scripts.step3_translate_game --provider openai --model gpt-5-mini
```

#### 3. **Обмежений бюджет** (повільно але дешево)
```bash
# Витяжка - локально
python -m scripts.step1_extract_glossary --provider local --model google/gemma-3-12b

# Глосарій та контент - DeepSeek (дешево але повільно)
python -m scripts.step2_translate_glossary --provider deepseek --model deepseek-chat
python -m scripts.step3_translate_game --provider deepseek --model deepseek-chat
```

#### 4. **Максимальна якість**
```bash
python -m scripts.step1_extract_glossary --provider openai --model gpt-5
python -m scripts.step2_translate_glossary --provider openai --model gpt-5
python -m scripts.step3_translate_game --provider openai --model gpt-5
```

## 📝 Повний процес локалізації

### Крок 0: Підготовка вихідних файлів

**Варіант 1: Python скрипт**
```bash
# Розшифрувати файли з гри
python scripts/decrypt.py "path/to/Hollow Knight Silksong/Hollow Knight Silksong_Data/Texts"
```

**Варіант 2: SilksongDecryptor.exe (фаллбек)**
```bash
# Розшифрувати файли з папки гри
.\SilksongDecryptor.exe -decrypt "path/to/Hollow Knight Silksong/Hollow Knight Silksong_Data/Texts"
```

**Варіант 3: Готові файли**
```bash
# Або використовуйте готові розшифровані файли в data/silksong/source/
```

### Крок 1: Витяжка ключових термінів

```bash
# Тестування на 3 файлах
python -m scripts.step1_extract_glossary --provider local --model google/gemma-3-12b --max-files 3

# Повна витяжка (всі файли)
python -m scripts.step1_extract_glossary --provider local --model google/gemma-3-12b
```

**Що відбувається:**
- Аналізуються англійські файли гри
- AI вилучає важливі терміни (імена персонажів, локацій, предметів)
- Створюється файл `data/silksong/glossaries/extracted_terms.json`

### Крок 2: Переклад глосарію

```bash
# Рекомендований варіант
python -m scripts.step2_translate_glossary --provider openai --model gpt-5-mini

# Або для обмеженого бюджету (повільно)
python -m scripts.step2_translate_glossary --provider deepseek --model deepseek-chat

# Або локально (безкоштовно)
python -m scripts.step2_translate_glossary --provider local --model google/gemma-3-12b
```

**Що відбувається:**
- Перекладаються всі витягнуті терміни
- Створюється `final_glossary.json` для використання в кроці 3
- Генерується `glossary_for_review.txt` для ручної перевірки

### Крок 3: Переклад файлів гри

```bash
# Тестування одного файлу
python -m scripts.step3_translate_game --provider openai --model gpt-5-mini --max-files 1

# Повний переклад
python -m scripts.step3_translate_game --provider openai --model gpt-5-mini

# Послідовний переклад (якщо паралельний не працює)
python -m scripts.step3_translate_game --provider openai --model gpt-5-mini --no-parallel
```

**Що відбувається:**
- Використовується створений глосарій для консистентності термінів
- Перекладаються всі файли гри
- Результат зберігається в `data/silksong/silksong_ua/`

### Крок 4: Зашифрування для гри

**Варіант 1: Python скрипт (рекомендовано)**
```bash
# Зашифрувати перекладені файли
python scripts/encrypt.py data/silksong/silksong_ua --output releases/current/
```

**Варіант 2: SilksongDecryptor.exe (фаллбек)**
```bash
# Зашифрувати перекладені файли
.\SilksongDecryptor.exe -encrypt data/silksong/silksong_ua

# Або якщо файли в поточній папці
.\SilksongDecryptor.exe -encrypt .
```

**Створення релізу**
```bash
# Створити ZIP архів для релізу
cd releases/current/
zip -r ../Silksong-UA-v1.0.zip *

# Встановлення в гру:
# Скопіюйте зашифровані файли та замініть оригінальні у:
# "Hollow Knight Silksong_Data/Texts/"
```

## 🔧 Додаткові інструменти

### Перевірка статистики
```bash
python scripts/check_stats.py
```

### Робота з кешем
```bash
# Очистити кеш перед повторним перекладом
python -m scripts.step3_translate_game --clear-cache --provider openai --model gpt-5-mini
```

### Повторна обробка проблемних файлів
```bash
# Повторити тільки файли, що зазнали невдачі
python -m scripts.step1_extract_glossary --retry-failed --max-retries 10
```

## 🎮 Особливості Silksong

### Криптографія
- **Алгоритм**: AES ECB + PKCS7 padding
- **Ключ**: `UKu52ePUBwetZ9wNX88o54dnfKRu0T1l`
- **Формат**: JSON з полями `m_Name` та `m_Script` (base64)
- Python реалізація повністю сумісна з C# версією

### Форматування
- XML теги: `<page=S>`, `<hpage>` зберігаються
- HTML entities: `&#8217;`, `&amp;` не змінюються
- Спеціальні символи зберігаються в оригінальному вигляді
- Перекладається тільки текстовий контент

### Структура файлів
- **Вхідні**: `EN_*.json` (зашифровані)
- **Проміжні**: `EN_*.txt` (розшифровані)
- **Вихідні**: `DE_*.txt` (перекладені)
- **Фінальні**: `DE_*.json` (зашифровані українською)

## 🚨 Типові проблеми та рішення

### ModuleNotFoundError
```bash
# ПРАВИЛЬНО: запускайте як модуль з кореня проекту
python -m scripts.step1_extract_glossary

# НЕПРАВИЛЬНО:
python scripts/step1_extract_glossary.py
```

### API ключі не працюють
1. Перевірте файл `.env` в корені проекту
2. Переконайтеся, що немає пробілів навколо `=`
3. Перезапустіть термінал після зміни `.env`

### Локальна модель не відповідає
```bash
# Перевірте, чи працює LM Studio
curl http://localhost:1234/v1/models

# Переконайтеся, що модель завантажена в LM Studio
```

### Проблеми з кодуванням
- Всі файли мають використовувати UTF-8
- Windows: перевірте налаштування консолі
- Для emoji в виводі використовуйте сучасний термінал

## 📦 Створення релізу

### 1. Підготовка файлів
```bash
# Переконайтеся, що всі файли перекладені
python scripts/check_stats.py

# Зашифруйте файли
python scripts/encrypt.py data/silksong/silksong_ua --output releases/v1.0/
```

### 2. Пакування
```bash
cd releases/v1.0/
zip -r ../Silksong-UA-v1.0.zip *
```

### 3. Тестування
1. Розпакуйте в тестову копію гри
2. Встановіть німецьку мову в налаштуваннях
3. Перевірте ключові елементи (меню, діалоги, досягнення)

## 💡 Поради по оптимізації

### Швидкість
1. Використовуйте `--max-files` для тестування
2. Паралельна обробка прискорює переклад
3. Кеш уникає повторних перекладів

### Якість
1. Використовуйте різні провайдери для різних етапів
2. Переглядайте глосарій перед фінальним перекладом
3. Тестуйте переклад на невеликих вибірках

### Вартість
1. Локальні моделі для тестування та витяжки
2. DeepSeek для глосаріїв (дешевий + якісний)
3. OpenAI mini для масового перекладу

## 🤝 Внесок у проект

1. **Покращення перекладів**: Редагуйте `glossary_for_review.txt`
2. **Звіти про помилки**: Використовуйте GitHub Issues
3. **Нові функції**: Fork → Pull Request
4. **Документація**: Покращуйте цей файл

---

**Автори**: Спільнота українських геймерів
**Ліцензія**: Фанатський проект для навчальних цілей
**Версія документу**: 1.0