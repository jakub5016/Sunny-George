# ☀️ Mega-Watt

**Mega-Watt** is a company website for a solar panel retailer. It features an AI chat assistant, a custom genetic algorithm–based PV installation configurator, and a searchable product catalog - all in a clean bilingual (PL/EN) web app.

---

## 🗂 Project overview

```
Mega-Watt/
├── backend/          # Django - REST API, LLM agent, PV designer, admin
│   ├── chat/         # Conversational AI (text + voice)
│   ├── catalog/      # Product listing & filtering API
│   ├── pv_elements/  # PV module & inverter models
│   └── pv_design/    # Genetic algorithm–based installation designer
└── frontend/         # React SPA (Feature-Sliced Design)
    └── src/
        ├── pages/    # chat · pv-designer · catalog
        ├── widgets/  # chat-window, chat-interface, app-header
        ├── features/ # send-message, design-pv, locale, theme …
        ├── entities/ # message, pv-installation
        └── shared/   # API client, i18n, UI primitives
```

---

## 🧬 Genetic Algorithm - PV installation designer

The most interesting part of the codebase. Users provide site conditions and budget; the backend evolves an optimal PV installation configuration using a custom GA.

### 🧩 Chromosome
Each individual in the population is an `InstallationDto` - a tuple of `(inverter, pv_module_type, module_count)`.

### 📐 Fitness function
Electrical validity is checked first (MPPT range, DC voltage at −25 °C, DC power limit, max current). Invalid installations score `0`. Valid ones are scored by:

```
fitness = 1 / (1 + area_deviation + budget_penalty − cost_savings_bonus)
```

- Installations under budget get a cost-savings bonus.
- Going more than 5 % over budget results in a hard zero.

### ⚡ Power model
`P_effective = P_nominal × tilt_factor × shading_factor`

- **Tilt factor** - Gaussian curve peaking at 35 ° (optimal for Poland).
- **Shading factor** - mapped from a 5-point Likert scale.
- Annual yield uses a Poland reference of **1050 kWh/kWp**.

### 🎛️ GA parameters (tunable via env)
| Parameter | Default |
|-----------|---------|
| Population | 100 |
| Generations | 100 |
| Mutation rate | 1 % |
| Crossover rate | 70 % |
| Elitism rate | 10 % |
| Tournament size | 3 |
| Top results kept | 3 |

### 📊 Output
Results are split into **matching** (all client constraints met) and **alternative** (electrically valid but outside requirements) installations, each with a **0–100 % match score** and detailed metrics (area, effective power, total cost).

---

## 🤖 AI chat assistant

- **LLM:** `openai/gpt-oss-20b` via [Groq](https://groq.com) + LangChain
- **Voice:** Groq `whisper-large-v3-turbo` transcribes audio before hitting the same text pipeline
- Fully bilingual - locale is passed per request (`pl` / `en`)
- Conversation history is windowed to the last 6 messages to keep context tight

---

## 🛠 Tech stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python 3.11 · Django 5.1 · Django REST Framework · SQLite |
| **Task queue** | Celery 5 · Redis · django-celery-beat |
| **AI / LLM** | LangChain · langchain-groq · Groq API |
| **Frontend** | React 19 · TypeScript 5.8 · Vite 6 · CSS Modules |
| **i18n** | i18next · react-i18next (PL default, EN) |
| **CI** | GitHub Actions · coverage gate (80 % per app) |

### 🏗️ Architecture highlights
- **Feature-Sliced Design** - strict layer boundaries (`@app` → `@pages` → `@widgets` → `@features` → `@entities` → `@shared`) enforced through Vite/TS path aliases
- **Validator chain pattern** - `InstallationChecker` and `ClientExpectationsChecker` compose small, single-responsibility validators
- **Query builder pattern** - catalog filtering via `PvModuleQueryBuilder` / `InverterQueryBuilder`
- **DTO-first domain layer** - dataclasses separate GA domain logic from serializers
- **In-process GA cache** - module/inverter data cached as a singleton, cleared hourly via Celery Beat

---

## 🚀 Quick start

### 🐍 Backend

```bash
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py load_pv_elements   # seeds modules & inverters from CSV
python manage.py runserver
```

### ⚛️ Frontend

```bash
cd frontend
npm install
npm run dev
```

For a production-like build, run `npm run build` first, then serve via Django.

---

## 🔌 API

### 💬 Chat

| Endpoint | Method | Notes |
|----------|--------|-------|
| `/api/chat/text/` | POST | `{ message, session_id?, locale?, start? }` |
| `/api/chat/voice/` | POST | multipart: `audio`, `session_id?`, `locale?` - WIP |

### 👩🏻‍🎨 PV designer

| Endpoint | Method | Notes |
|----------|--------|-------|
| `/api/pv-design/design/` | POST | client requirements + site conditions → GA results |

### 📦 Catalog

| Endpoint | Method | Filters |
|----------|--------|---------|
| `/api/catalog/modules/` | GET | `search`, `power_min/max`, `efficiency_min/max`, `price_min/max` |
| `/api/catalog/inverters/` | GET | `search`, `phases`, `power_min/max`, `price_min/max` |

---

## ⚙️ Environment variables

```env
# Required
GROQ_API_KEY=...

# Django (production)
DJANGO_SECRET_KEY=...
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Celery (optional - only needed for GA cache clearing)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

> GA hyperparameters (`POPULATION_SIZE`, `MUTATION_RATE`, `CROSSOVER_RATE`, etc.) can also be overridden via env - see `backend/config/const.py`.
