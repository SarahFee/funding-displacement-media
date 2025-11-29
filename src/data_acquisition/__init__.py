"""
Data Acquisition Module
Handles fetching data from FTS, DTM, and GDELT APIs
"""

from .fetch_fts import fetch_funding_data
from .fetch_dtm import fetch_displacement_data
from .fetch_gdelt import fetch_gdelt_data, fetch_gdelt_tone

__all__ = [
    'fetch_funding_data',
    'fetch_displacement_data',
    'fetch_gdelt_data',
    'fetch_gdelt_tone'
]
