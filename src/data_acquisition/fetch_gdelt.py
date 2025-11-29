"""
GDELT Data Acquisition Module
Fetches media coverage data from GDELT using gdeltdoc
"""

import pandas as pd
import logging
from pathlib import Path
from gdeltdoc import GdeltDoc, Filters

logger = logging.getLogger(__name__)


def fetch_gdelt_data(
    keyword: str,
    start_date: str,
    end_date: str,
    save_raw: bool = True
) -> pd.DataFrame:
    """
    Fetch media coverage volume data from GDELT
    
    Parameters:
    -----------
    keyword : str
        Search keyword (e.g., "Geopolitics", "Humanitarian crisis")
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str
        End date in YYYY-MM-DD format
    save_raw : bool
        Whether to save raw data to disk
        
    Returns:
    --------
    pd.DataFrame
        Timeline of media volume intensity
    """
    logger.info(f"Fetching GDELT volume data for keyword: '{keyword}'")
    logger.info(f"  Period: {start_date} to {end_date}")
    
    try:
        gd = GdeltDoc()
        f = Filters(
            keyword=keyword,
            start_date=start_date,
            end_date=end_date,
        )
        
        timeline_results = gd.timeline_search("timelinevol", f)
        
        logger.info(f"✓ Retrieved {len(timeline_results)} daily data points")
        
        # Save raw data
        if save_raw:
            raw_dir = Path("data/raw/gdelt")
            raw_dir.mkdir(parents=True, exist_ok=True)
            timeline_results.to_csv(
                raw_dir / f"gdelt_volume_{keyword.lower()}.csv",
                index=False
            )
        
        return timeline_results
        
    except Exception as e:
        logger.error(f"Failed to fetch GDELT volume data: {e}")
        raise


def fetch_gdelt_tone(
    keyword: str,
    start_date: str,
    end_date: str,
    save_raw: bool = True
) -> pd.DataFrame:
    """
    Fetch media tone/sentiment data from GDELT
    
    Parameters:
    -----------
    keyword : str
        Search keyword
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str
        End date in YYYY-MM-DD format
    save_raw : bool
        Whether to save raw data to disk
        
    Returns:
    --------
    pd.DataFrame
        Timeline of media tone
    """
    logger.info(f"Fetching GDELT tone data for keyword: '{keyword}'")
    logger.info(f"  Period: {start_date} to {end_date}")
    
    try:
        gd = GdeltDoc()
        f = Filters(
            keyword=keyword,
            start_date=start_date,
            end_date=end_date,
        )
        
        tone_results = gd.timeline_search("timelinetone", f)
        
        logger.info(f"✓ Retrieved {len(tone_results)} daily tone data points")
        
        # Save raw data
        if save_raw:
            raw_dir = Path("data/raw/gdelt")
            raw_dir.mkdir(parents=True, exist_ok=True)
            tone_results.to_csv(
                raw_dir / f"gdelt_tone_{keyword.lower()}.csv",
                index=False
            )
        
        return tone_results
        
    except Exception as e:
        logger.error(f"Failed to fetch GDELT tone data: {e}")
        raise


if __name__ == "__main__":
    # Test the fetchers
    logging.basicConfig(level=logging.INFO)
    
    # Test volume
    volume_df = fetch_gdelt_data(
        keyword="Humanitarian Crisis",
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
    print(f"\nVolume data shape: {volume_df.shape}")
    print(volume_df.head())
    
    # Test tone
    tone_df = fetch_gdelt_tone(
        keyword="Humanitarian Crisis",
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
    print(f"\nTone data shape: {tone_df.shape}")
    print(tone_df.head())
