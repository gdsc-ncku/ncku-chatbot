# NCKU Club Crawler

## Usage

```bash
cd MRE_root\club
poetry install
```

---

## Run

#### Crawling club data

```bash
poetry run python club_data.py
```

output will be saved in `club_data/`.

#### Crawling regulations

```bash
poetry run python club_regulations.py
```

output will be saved in `regulations_pdfread/` for pdf files, and `regulations` for txt files.