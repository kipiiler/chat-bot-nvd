from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union

class CPE(BaseModel):
    deprecated: bool = Field(False, description="Is this CPE deprecated?")
    cpeName: str = Field(..., description="CPE Name")
    cpeNameId: str = Field(..., description="CPE Name ID")
    lastModifiedDate: Optional[str] = Field(None, description="Last Modified Date")
    created: str = Field(..., description="Created Date")
    titles: List[str] = Field([], description="Titles")
    deprecatedBy: List[str] = Field([], description="Deprecated By")
    vulnerabilities: Optional[List[str]] = Field([], description="Optional vulnerabilities associated with this CPE.")

class CVE(BaseModel):
    id: str = Field(..., description="CVE ID")
    sourceIdentifier: str = Field(..., description="Contact who reported the vulnerability")
    published: str = Field(..., description="CVE publication date. ISO 8601 date/time format.")
    lastModified: str = Field(..., description="CVE modified date. ISO 8601 date/time format.")
    vulnStatus: str = Field(..., description="Vulnerability Status")
    exploitAdd: Optional[str] = Field(None, description="Optional, only exists if the CVE is listed in the Known Exploited Vulnerabilities (KEV) catalog.")
    actionDue: Optional[str] =  Field(None, description="Optional, only exists if the CVE is listed in the Known Exploited Vulnerabilities (KEV) catalog." )
    requiredAction: Optional[str] =  Field(None, description="Required Action")
    descriptions: List[str] = Field([], description="CVE descriptions. Includes other languages.")
    metrics: Optional[Dict[str, Union[float, str, Dict[str, Union[str, float]]]]] = Field(None, description="Class attribute containing scoring lists (cvssMetricV31 / V30 / V2).")
    weaknesses: List[str] = Field([], description="Contains relevant CWE information")
    configurations: List[str] = Field([], description="List containing usually a single element of CPE information")
    references: List[str] = Field([], description="CVE reference links")
    cwe: List[str]  = Field([], description="Common Weakness Enumeration Specification (CWE)")
    url: str = Field(..., description="Link to additional details on nvd.nist.gov for that CVE.")
    cpe: List[str] =  Field([], description="Common Platform Enumeration (CPE) assigned to the CVE.")
    v31score: Optional[float] = None
    v30score: Optional[float] = None
    v2score: Optional[float] = None
    v31vector: Optional[str] = None
    v30vector: Optional[str] = None
    v2vector: Optional[str] = None
    v31severity: Optional[str] = None
    v30severity: Optional[str] = None
    v2severity: Optional[str] = None
    v31exploitability: Optional[float] = None
    v30exploitability: Optional[float] = None
    v2exploitability: Optional[float] = None
    v31impactScore: Optional[float] = None
    v30impactScore: Optional[float] = None
    v2impactScore: Optional[float] = None
    score: Optional[List[Dict[str, Union[int, str]]]] = None
    v31attackVector: Optional[str] = None
    v30attackVector: Optional[str] = None
    v2accessVector: Optional[str] = None
    v31attackComplexity: Optional[str] = None
    v30attackComplexity: Optional[str] = None
    v2accessComplexity: Optional[str] = None
    v31privilegesRequired: Optional[str] = None
    v30privilegesRequired: Optional[str] = None
    v31userInteraction: Optional[str] = None
    v30userInteraction: Optional[str] = None
    v31scope: Optional[str] = None
    v30scope: Optional[str] = None

class FilterByDateArgs(BaseModel):
    keyword: str = Field(..., description="Keyword to search for")
    start_date: str = Field(..., description="Start date in ISO 8601 format")
    end_date: str = Field(..., description="End date in ISO 8601 format")

class FilterByDateWindowArgs(BaseModel):
    keyword: str = Field(..., description="Keyword to search for")
    window_start: str = Field(..., description="Start date in ISO 8601 format")
    window: int = Field(..., description="Number of days to look around the start date")

class CVEShortType(BaseModel):
    id: str = Field(..., description="CVE ID")
    descriptions: str = Field(..., description="CVE descriptions. Includes other languages.")

class ListCVEArgs(BaseModel):
    cve_list: List[CVEShortType] = Field(..., description="List of CVEs to convert to string representation")