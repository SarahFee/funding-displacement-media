#!/usr/bin/env python3
"""
Main Pipeline for Humanitarian Funding Analysis
Orchestrates data acquisition, processing, modeling, and visualization
"""

import sys
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from data_acquisition.fetch_fts import fetch_funding_data
from data_acquisition.fetch_dtm import fetch_displacement_data
from data_acquisition.fetch_gdelt import fetch_gdelt_data, fetch_gdelt_tone
from processing.process_funding import process_funding_data
from processing.process_displacement import process_displacement_data
from processing.process_gdelt import process_gdelt_data, process_tone_data
from visualization.plots import generate_all_visualizations
from modeling.correlation_analysis import run_correlation_analysis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run the complete analysis pipeline"""
    
    logger.info("="*70)
    logger.info("HUMANITARIAN FUNDING ANALYSIS PIPELINE")
    logger.info("="*70)
    
    # Configuration
    YEARS = [2022, 2023, 2024]
    START_DATE = "2022-02-01"
    END_DATE = "2024-02-29"
    GDELT_KEYWORD = "Geopolitics"
    
    # Countries for DTM analysis
    COUNTRY_LIST = [
        "LBY", "AFG", "PER", "NER", "CAF", "ZMB", "SOM", "VCT", "BEN", "GTM", "MNG",
        "SLV", "KEN", "YEM", "PAK", "DMA", "DJI", "HND", "ARM", "PNG", "BFA", "VUT",
        "COD", "ECU", "SDN", "TCD", "HTI", "ZAF", "UKR", "ZWE", "CMR", "BOL", "ETH",
        "MWI", "BDI", "IRQ", "MOZ", "MDG", "GRD", "SSD", "NGA", "LBN", "FJI", "MLI",
        "UGA",
    ]
    
    try:
        # Step 1: Data Acquisition
        logger.info("\n" + "="*70)
        logger.info("STEP 1: DATA ACQUISITION")
        logger.info("="*70)
        
        logger.info("Fetching FTS funding data...")
        funding_df = fetch_funding_data(YEARS)
        
        logger.info("Fetching DTM displacement data...")
        displacement_df = fetch_displacement_data(COUNTRY_LIST)
        
        logger.info("Fetching GDELT media volume data...")
        gdelt_timeline = fetch_gdelt_data(GDELT_KEYWORD, START_DATE, END_DATE)
        
        logger.info("Fetching GDELT tone data...")
        tone_timeline = fetch_gdelt_tone(GDELT_KEYWORD, START_DATE, END_DATE)
        
        # Step 2: Data Processing
        logger.info("\n" + "="*70)
        logger.info("STEP 2: DATA PROCESSING")
        logger.info("="*70)
        
        logger.info("Processing funding data with Prophet...")
        quarterly_funding = process_funding_data(funding_df)
        
        logger.info("Processing displacement data...")
        aggregated_displacement = process_displacement_data(displacement_df)
        
        logger.info("Processing GDELT volume data...")
        quarterly_gdelt = process_gdelt_data(gdelt_timeline)
        
        logger.info("Processing GDELT tone data...")
        quarterly_tone = process_tone_data(tone_timeline)
        
        # Step 3: Correlation Analysis
        logger.info("\n" + "="*70)
        logger.info("STEP 3: CORRELATION ANALYSIS")
        logger.info("="*70)
        
        correlations = run_correlation_analysis(
            quarterly_funding,
            aggregated_displacement,
            quarterly_gdelt,
            quarterly_tone
        )
        
        # Step 4: Visualization
        logger.info("\n" + "="*70)
        logger.info("STEP 4: GENERATING VISUALIZATIONS")
        logger.info("="*70)
        
        generate_all_visualizations(
            quarterly_funding,
            aggregated_displacement,
            quarterly_gdelt,
            quarterly_tone
        )
        
        # Summary
        logger.info("\n" + "="*70)
        logger.info("PIPELINE COMPLETE")
        logger.info("="*70)
        logger.info("\nKey Findings:")
        logger.info(f"  - Funding ↔ Displacement correlation: {correlations['fund_disp']:.3f}")
        logger.info(f"  - Funding ↔ Media Volume correlation: {correlations['fund_vol']:.3f}")
        logger.info(f"  - Funding ↔ Media Tone correlation: {correlations['fund_tone']:.3f}")
        logger.info(f"\nOutputs saved to: data/outputs/")
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
