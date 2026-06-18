# MusicService

**Author:** Vladislava Kuprienko

Data extraction and analytics pipeline for the Chinook music store database.

Loads relational tables from SQLite, exports them to local storage, and runs pandas-based analytics on tracks, genres, and sales.

---

## What it does

```
chinook.db (SQLite) → load tables → data/*.xlsx → analytics → results/*.xlsx
```

### Pipeline steps

1. **Extract** — load 11 tables from `chinook.db` via SQL
2. **Export** — save each table to `data/` as Excel files
3. **Analyze** — run 4 reports and save results to `results/`

### Analytics outputs

| Output file | Description |
|-------------|-------------|
| `avr_duration.xlsx` | Average track duration by genre |
| `tracks_album_artist.xlsx` | Tracks joined with album and artist names |
| `top_5_genres.xlsx` | Top 5 genres by total sales revenue |
| `top_genre_customers.xlsx` | Customers ranked by Rock genre purchases |

---

## Tech stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)

- **Python** — pipeline orchestration
- **pandas** — data manipulation and aggregations
- **SQLite** — source database (`chinook.db`)
- **openpyxl** — Excel export

---

## Project structure

```
MusicService/
├── main.py          # Pipeline entry point
├── defs.py          # Load, save, and analytics functions
├── chinook.db       # SQLite database (not included — see Setup)
├── data/            # Exported source tables (.xlsx)
├── results/         # Analytics outputs (.xlsx)
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/cewson/MusicService.git
cd MusicService
```

### 2. Install dependencies

```bash
pip install pandas openpyxl
```

### 3. Create output folders

```bash
mkdir data results
```

On Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force -Path data, results
```

---

## Run

```bash
python main.py
```

After a successful run:

- raw tables appear in `data/`
- analysis results appear in `results/`

---

## Source tables

`albums` · `artists` · `customers` · `employees` · `genres` · `invoices` · `invoice_items` · `media_types` · `playlists` · `playlist_track` · `tracks`

---

## Author

**Vladislava Kuprienko** — [GitHub](https://github.com/cewson) · [LinkedIn](https://www.linkedin.com/in/vladislava-kuprienko-778995415/)
