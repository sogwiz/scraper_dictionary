# Scraper Dictionary

## Purpose

This repository is designed to:
- Scrape data from various sites
- Upload the data to MongoDB / Parse backend

---

## Getting Started

### 1. Setup Environment (skip to Docker usage if using Docker)

```bash
pip install virtualenv
source bin/activate
pip install Scrapy
pip install pymongo
pip install git+https://github.com/milesrichardson/ParsePy.git
```

---

### 2. Download Data from assyrianlanguages.org

To scrape the entire repository and download it to a file called `output.json`:

```bash
scrapy crawl assyrianlanguagesloggedin
```

---

### 3. Update MongoDB / Parse Backend

```bash
cd scraper_assyrian
python updater.py
```

---

## Docker Usage

### Build the Docker Image

```bash
docker build -t sogwiz/assyrian_spider .
```

### Run the Scraper with Docker

- Scrape specific keys:
  ```bash
  docker run -v $(pwd):/usr/src/app -it sogwiz/assyrian_spider scrapy crawl assyrianlanguagesloggedin -a searchkey=1232,12,501 -o out3.json
  ```
- Scrape a range of keys:
  ```bash
  docker run -v $(pwd):/usr/src/app -it sogwiz/assyrian_spider scrapy crawl assyrianlanguagesloggedin -a searchkeys=39000-39050 -o out3.json
  ```
- Open an interactive Bash shell in the container:
  ```bash
  docker run -v $(pwd):/usr/src/app -it sogwiz/assyrian_spider /bin/bash
  ```

---

## Workflow

1. **Run the scraper** to download a JSON file.
2. **Run the Java dictionary generator** to generate the index and dictionary folder.
3. **Run the uploader**:

   ```bash
   python scraper_assyrian/uploader.py \
     --dir_east=<DIR_DICTIONARY_GENERATED_AT> \
     --id_app=<PARSE_APP_ID> \
     --key_rest=<PARSE_REST_KEY> \
     --key_master=<PARSE_MASTER_KEY> \
     -file_scrape=<FILE_GENERATED_BY_SCRAPE_STEP>
   ```

---

### Alternate Upload Steps

Instead of step 3 above, you can:

- Create `DictionaryDefinition` using `updaternewentries.py` by pointing to the dictionary folder.
- Create `DictionaryWordDefinitionList` using `uploader_newentries.py` by pointing to the dictionary folder.

---

## TODO

- Update `uploader.py` to read the `english` and `dictionaryArr` fields from the original scraped file.
- Everything else loads from the indexed dictionary generated files.
- The reason: the format of those fields in the original scrape file is much cleaner and difficult to clean after.
- **Temporary workaround:** Load the scraped file into memory and use the `english` and `dictionaryArr` fields from that structure.

---