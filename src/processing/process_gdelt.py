"""
GDELT Data Processing Module
Processes GDELT media coverage data with quarterly aggregation
"""

import pandas as pd
import logging
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)


def process_gdelt_data(
    gdelt_df: pd.DataFrame,
    start_date: str = "2022-02-01",
    end_date: str = "2024-02-29",
    save_processed: bool = True
) -> pd.DataFrame:
    """
    Process GDELT volume timeline data
    
    Parameters:
    -----------
    gdelt_df : pd.DataFrame
        Raw GDELT timeline data
    start_date : str
        Analysis start date
    end_date : str
        Analysis end date
    save_processed : bool
        Whether to save processed data
        
    Returns:
    --------
    pd.DataFrame
        Quarterly aggregated and normalized media volume data
    """
    logger.info("Processing GDELT volume data...")
    
    # Rename columns
    gdelt_df.columns = ["ds", "volume_intensity"]
    gdelt_df["ds"] = pd.to_datetime(gdelt_df["ds"])
    
    # Filter to analysis period
    gdelt_df = gdelt_df[
        (gdelt_df["ds"] >= start_date) & 
        (gdelt_df["ds"] <= end_date)
    ]
    
    logger.info(f"  Daily data points: {len(gdelt_df)}")
    
    # Quarterly aggregation
    quarterly = gdelt_df.set_index("ds").resample("QE").mean().reset_index()
    
    # Normalize
    scaler = MinMaxScaler()
    quarterly["volume_intensity_norm"] = scaler.fit_transform(
        quarterly["volume_intensity"].values.reshape(-1, 1)
    )
    
    logger.info(f"  ✓ Processed {len(quarterly)} quarters")
    
    # Save processed data
    if save_processed:
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        quarterly.to_csv(processed_dir / "gdelt_volume_processed.csv", index=False)
    
    return quarterly


def process_tone_data(
    tone_df: pd.DataFrame,
    start_date: str = "2022-02-01",
    end_date: str = "2024-02-29",
    save_processed: bool = True
) -> pd.DataFrame:
    """
    Process GDELT tone timeline data
    
    Parameters:
    -----------
    tone_df : pd.DataFrame
        Raw GDELT tone data
    start_date : str
        Analysis start date
    end_date : str
        Analysis end date
    save_processed : bool
        Whether to save processed data
        
    Returns:
    --------
    pd.DataFrame
        Quarterly aggregated and normalized tone data
    """
    logger.info("Processing GDELT tone data...")
    
    # Rename columns
    tone_df.columns = ["ds", "tone"]
    tone_df["ds"] = pd.to_datetime(tone_df["ds"])
    
    # Filter to analysis period
    tone_df = tone_df[
        (tone_df["ds"] >= start_date) & 
        (tone_df["ds"] <= end_date)
    ]
    
    logger.info(f"  Daily data points: {len(tone_df)}")
    
    # Quarterly aggregation
    quarterly = tone_df.set_index("ds").resample("QE").mean().reset_index()
    
    # Normalize
    scaler = MinMaxScaler()
    quarterly["tone_norm"] = scaler.fit_transform(
        quarterly["tone"].values.reshape(-1, 1)
    )
    
    logger.info(f"  ✓ Processed {len(quarterly)} quarters")
    
    # Save processed data
    if save_processed:
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        quarterly.to_csv(processed_dir / "gdelt_tone_processed.csv", index=False)
    
    return quarterly


if __name__ == "__main__":
    # Test processing
    logging.basicConfig(level=logging.INFO)
    
    # Create sample volume data
    dates = pd.date_range(start='2022-01-01', end='2024-02-29', freq='D')
    sample_volume = pd.DataFrame({
        0: dates,
        1: [100 + i for i in range(len(dates))]
    })
    
    # Create sample tone data
    sample_tone = pd.DataFrame({
        0: dates,
        1: [-5 + (i % 20) for i in range(len(dates))]
    })
    
    vol_result = process_gdelt_data(sample_volume)
    print(f"\nVolume processed shape: {vol_result.shape}")
    print(vol_result.head())
    
    tone_result = process_tone_data(sample_tone)
    print(f"\nTone processed shape: {tone_result.shape}")
    print(tone_result.head())
