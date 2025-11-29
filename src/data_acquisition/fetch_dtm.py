"""
DTM Data Acquisition Module
Fetches displacement data from the DTM API
"""

import requests
import pandas as pd
import logging
from pathlib import Path
from time import sleep

logger = logging.getLogger(__name__)


def fetch_displacement_data(country_list: list, save_raw: bool = True) -> pd.DataFrame:
    """
    Fetch IDP data from DTM API for multiple countries
    
    Parameters:
    -----------
    country_list : list
        List of ISO3 country codes
    save_raw : bool
        Whether to save raw responses to disk
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing displacement data
    """
    all_displacement_data = []
    
    logger.info(f"Fetching displacement data for {len(country_list)} countries...")
    
    for i, country in enumerate(country_list, 1):
        url = "https://dtmapi.iom.int/api/idpAdmin0Data/GetAdmin0Datav2"
        params = {"Admin0Pcode": country}
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json().get("result", [])
            all_displacement_data.extend(result)
            
            if result:
                logger.info(f"  [{i}/{len(country_list)}] {country}: {len(result)} records")
            else:
                logger.warning(f"  [{i}/{len(country_list)}] {country}: No data")
            
            # Rate limiting
            sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"  [{i}/{len(country_list)}] {country}: Error - {e}")
            continue
    
    displacement_df = pd.DataFrame(all_displacement_data)
    logger.info(f"\n✓ Total displacement records fetched: {len(displacement_df)}")
    
    # Save raw data
    if save_raw and not displacement_df.empty:
        raw_dir = Path("data/raw/dtm")
        raw_dir.mkdir(parents=True, exist_ok=True)
        displacement_df.to_csv(raw_dir / "dtm_raw.csv", index=False)
    
    return displacement_df


if __name__ == "__main__":
    # Test the fetcher
    logging.basicConfig(level=logging.INFO)
    
    test_countries = ["UKR", "SYR", "AFG", "SOM", "YEM"]
    df = fetch_displacement_data(test_countries)
    
    print(f"\nShape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nSample:\n{df.head()}")
