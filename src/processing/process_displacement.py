"""
Displacement Data Processing Module
Processes DTM data with quarterly aggregation
"""

import pandas as pd
import logging
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)


def process_displacement_data(
    displacement_df: pd.DataFrame,
    start_date: str = "2022-02-01",
    end_date: str = "2024-02-29",
    save_processed: bool = True
) -> pd.DataFrame:
    """
    Process displacement data with quarterly aggregation
    
    Parameters:
    -----------
    displacement_df : pd.DataFrame
        Raw displacement data from DTM
    start_date : str
        Analysis start date
    end_date : str
        Analysis end date
    save_processed : bool
        Whether to save processed data
        
    Returns:
    --------
    pd.DataFrame
        Quarterly aggregated and normalized displacement data
    """
    logger.info("Processing displacement data...")
    
    # Parse dates
    displacement_df["reportingDate"] = pd.to_datetime(
        displacement_df["reportingDate"], 
        errors="coerce"
    )
    displacement_df = displacement_df.dropna(subset=["reportingDate"])
    
    # Filter to analysis period
    displacement_df = displacement_df[
        (displacement_df["reportingDate"] >= start_date) &
        (displacement_df["reportingDate"] <= end_date)
    ]
    
    logger.info(f"  Records in period: {len(displacement_df)}")
    
    # Quarterly aggregation
    displacement_df["quarter"] = displacement_df["reportingDate"].dt.to_period("Q")
    
    aggregated = (
        displacement_df.groupby("quarter")["numPresentIdpInd"]
        .sum()
        .reset_index()
    )
    
    # Convert quarter back to timestamp (end of quarter)
    aggregated["reportingDate"] = aggregated["quarter"].dt.to_timestamp(how="end")
    
    # Normalize
    scaler = MinMaxScaler()
    aggregated["numPresentIdpInd_norm"] = scaler.fit_transform(
        aggregated["numPresentIdpInd"].values.reshape(-1, 1)
    )
    
    logger.info(f"  ✓ Processed {len(aggregated)} quarters")
    logger.info(f"  ✓ Total IDPs: {aggregated['numPresentIdpInd'].sum():,.0f}")
    
    # Save processed data
    if save_processed:
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        aggregated.to_csv(processed_dir / "displacement_processed.csv", index=False)
    
    return aggregated


if __name__ == "__main__":
    # Test processing
    logging.basicConfig(level=logging.INFO)
    
    # Create sample data
    dates = pd.date_range(start='2022-01-01', end='2024-02-29', freq='M')
    sample_df = pd.DataFrame({
        'reportingDate': dates,
        'numPresentIdpInd': [100000 + i*10000 for i in range(len(dates))]
    })
    
    result = process_displacement_data(sample_df)
    print(f"\nProcessed data shape: {result.shape}")
    print(result)
