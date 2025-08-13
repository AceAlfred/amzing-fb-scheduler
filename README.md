# Amzing Facebook Scheduler

Schemalägger Facebook-poster från en CSV-fil via Graph API.

## 📦 Installation
```bash
git clone https://github.com/AceAlfred/amzing-fb-scheduler.git
cd amzing-fb-scheduler
pip install -r requirements.txt
```

## ⚙️ Konfiguration
1. Kopiera `.env.example` till `.env` och fyll i:
```
FB_PAGE_ID=din-page-id
FB_PAGE_ACCESS_TOKEN=din-access-token
```
2. Fyll `amzing_fb_schedule.csv` med poster att schemalägga.

## ▶️ Kör
```bash
python schedule_fb_posts.py
```

## 🔑 Behörigheter
Din Page Access Token måste ha:
- `pages_manage_posts`
- `pages_read_engagement`

## ⏱️ Tidsformat
- ISO8601 med tidszon, t.ex. `2025-08-14T18:30:00+02:00`
- Minst 10 minuter fram i tiden och max 75 dagar framåt.
