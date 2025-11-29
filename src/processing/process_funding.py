"""
Funding Data Processing Module
Processes FTS data and applies Prophet forecasting with quarterly seasonality
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from prophet import Prophet
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)


def process_funding_data(
    funding_df: pd.DataFrame,
    start_date: str = "2022-02-01",
    end_date: str = "2024-02-29",
    save_processed: bool = True
) -> pd.DataFrame:
    """
    Process funding data with Prophet modeling
    
    Parameters:
    -----------
    funding_df : pd.DataFrame
        Raw funding data from FTS
    start_date : str
        Analysis start date
    end_date : str
        Analysis end date
    save_processed : bool
        Whether to save processed data
        
    Returns:
    --------
    pd.DataFrame
        Processed and normalized funding forecast
    """
    logger.info("Processing funding data...")
    
    # Parse dates
    funding_df["createdAt"] = pd.to_datetime(funding_df["createdAt"], errors="coerce")
    funding_df = funding_df.dropna(subset=["createdAt"])
    
    # Daily aggregation
    funding_by_date = (
        funding_df.groupby(funding_df["createdAt"].dt.date)["amountUSD"]
        .sum()
        .reset_index()
    )
    funding_by_date.columns = ["ds", "y"]
    funding_by_date["ds"] = pd.to_datetime(funding_by_date["ds"])
    
    # Log transform to stabilize variance
    funding_by_date["y"] = np.log1p(funding_by_date["y"])
    
    logger.info(f"  Daily data points: {len(funding_by_date)}")
    logger.info(f"  Date range: {funding_by_date['ds'].min()} to {funding_by_date['ds'].max()}")
    
    # Prophet model with quarterly seasonality
    logger.info("  Training Prophet model...")
    model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False
    )
    model.add_seasonality(name="quarterly", period=91.25, fourier_order=5)
    
    # Suppress Prophet output
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.fit(funding_by_date)
    
    # Generate forecast
    forecast = model.predict(model.make_future_dataframe(periods=0))
    forecast = forecast[["ds", "yhat"]]
    
    # Filter to analysis period
    forecast = forecast[
        (forecast["ds"] >= start_date) & (forecast["ds"] <= end_date)
    ]
    
    # Normalize
    scaler = MinMaxScaler()
    forecast["yhat_norm"] = scaler.fit_transform(forecast["yhat"].values.reshape(-1, 1))
    
    logger.info(f"  ✓ Processed {len(forecast)} days")
    logger.info(f"  ✓ Period: {forecast['ds'].min()} to {forecast['ds'].max()}")
    
    # Save processed data
    if save_processed:
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        forecast.to_csv(processed_dir / "funding_processed.csv", index=False)
    
    return forecast


if __name__ == "__main__":
    # Test processing
    logging.basicConfig(level=logging.INFO)
    
    # Create sample data
    dates = pd.date_range(start='2022-01-01', end='2024-02-29', freq='D')
    sample_df = pd.DataFrame({
        'createdAt': dates,
        'amountUSD': np.random.exponential(scale=1000000, size=len(dates))
    })
    
    result = process_funding_data(sample_df)
    print(f"\nProcessed data shape: {result.shape}")
    print(result.head())
