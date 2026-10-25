# Pulchowk Notice Tracker

A small Python tool that checks the Student Activity notices on the Pulchowk Campus website and posts each new one to a Discord channel, so you don't have to keep refreshing the site.

> Unofficial student project. Not affiliated with Pulchowk Campus or IOE.

> **Scope:** this tracker only checks the **Student Activity** category (`pcampus.edu.np/category/student-activity/`). Notices posted under other categories, such as scholarships, admissions or exams, are **not** tracked.

<img width="1118" height="670" alt="image" src="https://github.com/user-attachments/assets/4008d4e5-6f8e-4625-9282-e3e1bd648426" />


## The problem

Scholarship lists, hostel results and fee deadlines get posted on the campus website, and nobody checks it until a deadline has already passed. This tracker does the checking and pushes new notices to a place you already look.

## How it works

```
fetcher.py  ->  db.py  ->  notifier.py
 (scrape)     (remember)    (notify)
        \         |          /
            tracker.py   <- run on a schedule by cron
```

1. **Fetch:** `fetcher.py` downloads the notice listing page with `requests` and parses it with `BeautifulSoup`. Each `article.post` on the page becomes a dictionary with a `title`, a `url` and a `date`.
2. **Remember:** `db.py` saves each notice to SQLite with `INSERT OR IGNORE`. The `url` column is `UNIQUE`, so a notice that is already stored is skipped, and the function returns `True` only when a row was actually inserted.
3. **Notify:** `notifier.py` posts a message to a Discord webhook, but only for notices that were new.
4. **Order:** `tracker.py` goes through the list oldest to newest, because the website lists newest first. When several notices arrive at once, they appear in Discord in the order they were posted.

The Discord message contains the notice title in bold and its link.

## Project structure

| File | What it does |
|---|---|
| `fetcher.py` | `fetch_notices()` downloads the page and returns a list of notice dictionaries |
| `db.py` | `init_db()` creates the table, `add_to_db()` saves a notice and reports whether it was new |
| `notifier.py` | `send_notice()` posts a notice to Discord |
| `tracker.py` | `main()` runs fetch, save and notify in order |
| `requirements.txt` | Python dependencies |

## Database

One table, `notices`:

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Primary key, autoincrement |
| `title` | TEXT | Required |
| `url` | TEXT | Required, **unique**, used to detect duplicates |
| `date_posted` | TEXT | ISO 8601 timestamp from the site, e.g. `2026-09-21T11:39:09+05:45` |
| `seen_at` | TEXT | Set automatically when the notice is first saved |

Dates are stored in ISO format so they sort correctly as plain text.

## Setup

**Requirements:** Python 3.12 or newer (the code uses nested double quotes inside an f-string, which older versions don't allow) and a Discord webhook URL.

```bash
git clone https://github.com/akritartha/Pulchowk-Notice-Tracker.git
cd Pulchowk-Notice-Tracker

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set the webhook as an environment variable. The code reads it with `os.environ`, so it is not loaded from a `.env` file:

```bash
export NOTICE_DISCORD_WEBHOOK="https://discord.com/api/webhooks/..."
python3 tracker.py
```

**Use a test channel for the first run.** A new database is empty, so every notice on the page counts as new and all of them are sent at once.

## Running on a schedule

Edit your crontab with `crontab -e`. Cron does not see variables you exported in a terminal, so set the webhook on its own line above the job. This example runs every hour from 9:00 to 18:00:

```
NOTICE_DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
0 9-18 * * * cd /path/to/Pulchowk-Notice-Tracker && venv/bin/python tracker.py >> cron.log 2>&1
```

- The `cd` matters: the database path is relative (`notices.db`), so the script must start inside the project folder. Without it, cron creates a second, empty database and every notice looks new again.
- Calling `venv/bin/python` directly means the virtual environment doesn't need to be activated.
- `>> cron.log 2>&1` saves all output and errors to a log file, which is the first place to look when something fails.

## Which notices it tracks

**Only the Student Activity category.** `fetcher.py` scrapes exactly one page:

```
https://pcampus.edu.np/category/student-activity/
```

Nothing from the home page or any other category is checked, so a notice posted only under scholarships, admissions or exams will never reach Discord. To track a different category instead, change the `URL` constant at the top of `fetcher.py` to that category's page. The CSS selectors (`article.post`, `h2.entry-title a`, `time.entry-date`) match the site's current WordPress theme, so a site redesign would mean updating them.

## Known limitations

- **Student Activity only.** Other notice categories (scholarship, admission, exam and so on) are not tracked yet.
- **Failed sends aren't retried.** A notice is saved to the database before the Discord message is sent. If Discord is unreachable at that moment, the notice is marked as seen and never sent again.
- **No handling for a changed page layout.** If a notice is missing its title link or date, the run stops with an error instead of skipping that notice.
- **First run sends everything.** There is no "seed" mode that fills the database silently.

## Built with

Python, requests, BeautifulSoup, SQLite, Discord webhooks, cron
