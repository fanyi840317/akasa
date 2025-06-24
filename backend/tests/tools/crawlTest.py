import sys
from pathlib import Path
backend_path = str((Path(__file__).parent.parent.parent).resolve())
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from src.tools.crawl import mystery_site_crawler
from src.tools.search import MysterySearch, search_academic_databases
from src.tools.search import AcademicSearch, MysterySearch, LoggedDuckDuckGoSearch
from langchain_community.tools import DuckDuckGoSearchRun

result = mystery_site_crawler("ufo", ["sighting", "abduction"], max_pages=2)
print(result.run())