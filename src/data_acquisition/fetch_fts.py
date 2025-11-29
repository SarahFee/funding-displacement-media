"""
FTS Data Acquisition Module
Fetches humanitarian funding data from the FTS API
"""

import requests
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def fetch_funding_data(years: list, save_raw: bool = True) -> pd.DataFrame:
    """
    Fetch funding flows from FTS API
    
    Parameters:
    -----------
    years : list
        List of years to fetch data for
    save_raw : bool
        Whether to save raw responses to disk
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing funding flow data
    """
    all_flows = []
    
    for year in years:
        url = f"https://api.hpc.tools/v1/public/fts/flow?year={year}"
        logger.info(f"Fetching funding data for {year}...")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            flows = data.get("data", {}).get("flows", [])
            all_flows.extend(flows)
            
            logger.info(f"  ✓ Retrieved {len(flows)} flows for {year}")
            
            # Save raw data
            if save_raw:
                raw_dir = Path("data/raw/fts")
                raw_dir.mkdir(parents=True, exist_ok=True)
                pd.DataFrame(flows).to_csv(
                    raw_dir / f"fts_{year}.csv", 
                    index=False
                )
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve data for {year}: {e}")
            continue
    
    funding_df = pd.DataFrame(all_flows)
    logger.info(f"\n✓ Total funding records fetched: {len(funding_df)}")
    
    return funding_df


if __name__ == "__main__":
    # Test the fetcher
    logging.basicConfig(level=logging.INFO)
    df = fetch_funding_data([2022, 2023, 2024])
    print(f"\nShape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nSample:\n{df.head()}")
