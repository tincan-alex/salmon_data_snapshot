import json
import time
import requests

from src.constructs import DataSource, DataSourceType
from src.process.constructs import DEFAULT_DELAYS, EPICOLLECT_DELAYS


class SurveyDataPuller:
    def __init__(self, data_sources: list[DataSource], destination_path: str):
        self.data_sources = data_sources
        self.path = destination_path

    def pull_data(self):
        for source in self.data_sources:
            self._process_source(source)

    def _process_source(self, source: DataSource):
        url = source.url
        data_type = source.data_type
        year = source.year
        label = f"{year}_{data_type}"
        page = 1

        while url:
            print(f"Fetching {label} page {page}...")
            entries, url = self._fetch_page(url=url, label=f"{label}_{page}", is_epicollect=source.source_type == DataSourceType.EPICOLLECT)
            if entries is None:
                print(f"Stopping load for {label} page {page} because the page failed or was malformed.")
                break
            path = self.path / f"{label}_{page}.json"
            with open(path, "w", encoding="utf-8") as file:
                json.dump(entries, file, indent=4, ensure_ascii=False)
            page += 1

    def _fetch_page(self, url: str, label: str, is_epicollect: bool):
        if is_epicollect:
            delays = EPICOLLECT_DELAYS
        else:
            delays = DEFAULT_DELAYS
        for attempt, delay in enumerate(delays, start=1):
            time.sleep(delay)

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as exc:
                print(f"[{label}] fetch error attempt {attempt} for {url}: {exc}")
            except ValueError as exc:
                print(f"[{label}] invalid JSON attempt {attempt} for {url}: {exc}")
            else:
                if is_epicollect:
                    entries = data.get("data", {}).get("entries")
                    next_uri = data.get("links", {}).get("next")
                else:
                    entries = data.get("results")
                    next_uri = data.get("next")
                if isinstance(entries, list):
                    return entries, next_uri

                print(f"[{label}] malformed response attempt {attempt} for {url}: missing entries")

            if attempt == len(delays):
                print(f"[{label}] giving up after {attempt} attempts for {url}")
                return None, None

            next_delay = delays[attempt] if attempt < len(delays) else 0
            print(f"[{label}] retrying in {next_delay} seconds...")
        
        return None, None
