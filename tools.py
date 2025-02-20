import datetime
import os
import time
from typing import List
from pydantic import BaseModel, Field
import nvdlib
from functools import lru_cache
from langchain_core.tools import tool
from custom_type import CVE, CVEShortType, FilterByDateArgs, FilterByDateWindowArgs, ListCVEArgs 

API_KEY = os.environ["NVD_API_KEY"]
LIMIT_ITEMS = 10

@tool
@lru_cache(maxsize=128)
def search_cpe_by_keyword(keyword):
    """ Search CPE by keyword """

    res = nvdlib.searchCPE(keywordSearch=keyword, key=API_KEY, delay=0.6, limit=LIMIT_ITEMS)
    return res

@tool
@lru_cache(maxsize=128)
def search_cpe_by_cpeid(cpeId):
    """ Search CPE by CPE ID """
    res = nvdlib.searchCPE(cpeNameId=cpeId, key=API_KEY, delay=0.6, limit=LIMIT_ITEMS)
    return res

@tool
@lru_cache(maxsize=128)
def search_cve_by_keyword_brief(keyword: str) -> str:
    """ Search CVE for brief description by keyword, get the first result"""
    try:
        res = nvdlib.searchCVE(keywordSearch=keyword, key=API_KEY, delay=0.6, limit=LIMIT_ITEMS)
    except Exception as e:
        return "Could not found CVE by keyword"
    if len(res) == 0 or res[0].descriptions == None or len(res[0].descriptions) == 0:
        return "Could not found CVE by keyword"
    return res[0].descriptions[0].value

@tool
@lru_cache(maxsize=128)
def search_cve_by_cpe(name: str) -> CVE:
    """ Search CVE-detail by CPE """
    res = nvdlib.searchCVE(cpeName=name, key=API_KEY, delay=0.6, limit=LIMIT_ITEMS)
    return res

@tool("Search detailed CVE by CVE ID")
@lru_cache(maxsize=128)
def search_cve_by_cveid(id: str) -> CVE:
    """ Search CVE by CVE ID """
    # try:
    res = nvdlib.searchCVE(cveId=id, key=API_KEY, delay=0.6, limit=LIMIT_ITEMS)
    # except Exception as e:
        # return None
    return res

@tool("Find CVE ID by keyword and get the first result")
@lru_cache(maxsize=128)
def search_cveID_by_keyword(keyword: str) -> str:
    """ Search CVE ID by keyword and get the first result """
    try:
        res = nvdlib.searchCVE(keywordSearch=keyword, key=API_KEY, delay=0.6, limit=LIMIT_ITEMS)
    except Exception as e:
        return "Could not found CVE by keyword"
    if len(res) == 0 or res[0].descriptions == None or len(res[0].descriptions) == 0:
        return "Could not found CVE by keyword"
    return res[0].id

@tool("Find list of CVEs by keyword")
@lru_cache(maxsize=128)
def search_cve_by_keyword(keyword: str) -> list[CVE]:
    """ Search CVE by keyword """
    try:
        res = nvdlib.searchCVE(keywordSearch=keyword, key=API_KEY, delay=0.6, limit=LIMIT_ITEMS)
    except Exception as e:
        return []
    return res

@tool("Find list of CVEs with a keyword and a start and end date and the keyword can't be empty", args_schema=FilterByDateArgs)
@lru_cache(maxsize=128)
def search_cve_by_keyword_and_date(keyword: str, start_date: str, end_date: str) -> list[CVE]:
    """ Search CVE by keyword and date range """
    try:
        res = nvdlib.searchCVE(keywordSearch=keyword, key=API_KEY, delay=0.6, pubStartDate=start_date, pubEndDate=end_date, limit=LIMIT_ITEMS)
    except Exception as e:
        return []
    return res

@tool("Find list of CVEs with a keyword and a date window and the keyword can't be empty", args_schema=FilterByDateWindowArgs)
@lru_cache(maxsize=128)
def search_cve_by_keyword_and_window(keyword: str, window_start: str, window: int) -> List[CVE]:
    """ Search CVE by keyword and date window """
    try:
        end_date = datetime.datetime.strptime(window_start, "%Y-%m-%d") + datetime.timedelta(days=window)
        end_date = end_date.strftime("%Y-%m-%d")
        res = nvdlib.searchCVE(keywordSearch=keyword, key=API_KEY, delay=0.6, pubStartDate=window_start, pubEndDate=end_date, limit=LIMIT_ITEMS)
    except Exception as e:
        return []
    return [cve.id for cve in res]

@tool("Convert list of CVEs objects to string representation", args_schema=ListCVEArgs)
def convert_cve_list_to_str(cve_list: List[CVEShortType]) -> str:
    """ Convert list of CVEs to string """
    if len(cve_list) == 0:
        return "No CVEs found"
    return "\n".join([cve.id for cve in cve_list])