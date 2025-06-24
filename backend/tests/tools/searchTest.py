import sys
from pathlib import Path
backend_path = str((Path(__file__).parent.parent.parent).resolve())
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from src.tools.search import MysterySearch, search_academic_databases
from src.tools.search import AcademicSearch, MysterySearch, LoggedDuckDuckGoSearch
from langchain_community.tools import DuckDuckGoSearchRun

max_results = 10  # Set this to the desired number of results

# Test Academic Search
print("=== Testing Academic Search ===")
databases = ["arxiv"]  # Use available databases
academic_search = AcademicSearch(max_results=max_results, databases=databases)
try:
    academic_results = academic_search.invoke("UFO")
    print(f"Academic search results: {academic_results}")
except Exception as e:
    print(f"Academic search failed: {e}")

# Test Mystery Search
print("\n=== Testing Mystery Search ===")
mystery_search = MysterySearch(max_results=max_results, event_types=["UFO"])
try:
    mystery_results = mystery_search.invoke("UFO")
    print(f"Mystery search results: {mystery_results}")
except Exception as e:
    print(f"Mystery search failed: {e}")

# Test DuckDuckGo Search
print("\n=== Testing DuckDuckGo Search ===")
try:
    duckduckgo_search = DuckDuckGoSearchRun()
    ddg_results = duckduckgo_search.invoke("UFO")
    print(f"DuckDuckGo search results: {ddg_results}")
except Exception as e:
    print(f"DuckDuckGo search failed: {e}")