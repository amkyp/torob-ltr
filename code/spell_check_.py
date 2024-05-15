import csv
import re
import json
import logging
from tqdm import tqdm
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

options = webdriver.ChromeOptions()
# options.binary_location = "/usr/bin/google-chrome-stable"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

service = Service("chromedriver.exe")
# service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(options=options, service=service)

class JsonFileIterator:
    def __init__(self, path):
        self.path = path
        self.f = open(path, "r")
        self.i = 0
        self.length = self.counter_lines()

    def __iter__(self):
        return self

    def __next__(self):
        line = self.f.readline()
        if not line:
            # End of file
            self.f.close()
            raise StopIteration
        self.i += 1
        return json.loads(line)

    def counter_lines(self):
        with open(self.path, "r") as f1:
            return sum(1 for _ in f1)

    def __len__(self):
        return self.length

def read_json_lines(path, n_lines=None):
    with open(path, 'r') as f:
        for i, line in enumerate(f):
            if n_lines is not None and n_lines == i:
                break
            yield json.loads(line)

def process_query(query):
    # logging.info(f"Processing query: {query}")
    driver.get(f"https://torob.com/search/?query={query}")

    check_spell = driver.find_elements("xpath", "//p[contains(@class, 'black_p')]")
    torob_spell_check = False
    corrected_form = None
    for text in check_spell:
        extracted_text = text.get_attribute("innerText")
        if extracted_text.startswith("جستجو غلط‌گیری شد:"):
            torob_spell_check = True
            corrected_query = re.search(r"جستجو غلط‌گیری شد: (.*)", extracted_text).group(1)
            corrected_form = corrected_query
        else:
            corrected_form = None

    names = driver.find_elements("xpath", "//h2[contains(@class,'jsx-fa8eb4b3b47a1d18')]")
    name_list = [name.get_attribute("innerText") for name in names]
    title_text = "\n".join(name_list)

    processed_data = (query, corrected_form, title_text)

    return processed_data

logging.info("Starting data processing...")

search_query = pd.DataFrame(read_json_lines('./torob/torob-search-data_v1.jsonl', n_lines=1000))
queries = search_query['raw_query'].value_counts().to_dict()

logging.info(f"Total queries: {len(queries)}")
logging.info("Sorting queries...")

sorted_queries = sorted(queries.items(), key=lambda x: x[1], reverse=False)
df = pd.DataFrame.from_dict(queries, orient='index', columns=['count'])
df.sort_values(by=['count'], inplace=True, ascending=True)

chunk_size = 50000
chunks = np.array_split(df, len(df) // chunk_size + 1)

field_names = ["query", "spell_checked", "title_text"]

with open("output.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(field_names)

    logging.info("Processing chunks...")
    with ThreadPoolExecutor() as executor:
        futures = []
        for i, chunk in enumerate(chunks):
            logging.info(f"Processing chunk {i+1}/{len(chunks)}")
            for query in chunk.index.tolist():
                futures.append(executor.submit(process_query, query))
        
        for future in tqdm(futures, desc="Processing queries", unit="query"):
            processed_data = future.result()
            writer.writerow(processed_data)

logging.info("Data processing completed.")

# Load the output DataFrame from CSV
output_df = pd.read_csv("output.csv")