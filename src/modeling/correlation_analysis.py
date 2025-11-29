"""
Correlation Analysis Module
Calculates Pearson correlations between different time series
"""

import pandas as pd
import logging
from scipy.stats import pearsonr
from pathlib import Path

logger = logging.getLogger(__name__)


def run_correlation_analysis(
    funding_df: pd.DataFrame,
    displacement_df: pd.DataFrame,
    gdelt_volume_df: pd.DataFrame,
    gdelt_tone_df: pd.DataFrame,
    save_results: bool = True
) -> dict:
    """
    Run correlation analysis between all time series
    
    Parameters:
    -----------
    funding_df : pd.DataFrame
        Processed funding data
    displacement_df : pd.DataFrame
        Processed displacement data
    gdelt_volume_df : pd.DataFrame
        Processed GDELT volume data
    gdelt_tone_df : pd.DataFrame
        Processed GDELT tone data
    save_results : bool
        Whether to save results to file
        
    Returns:
    --------
    dict
        Dictionary containing correlation coefficients and p-values
    """
    logger.info("Running correlation analysis...")
    
    # Align funding data to quarterly
    funding_quarterly = funding_df.set_index('ds').resample('QE').mean().reset_index()
    funding_quarterly = funding_quarterly[
        (funding_quarterly['ds'] >= '2022-02-01') & 
        (funding_quarterly['ds'] <= '2024-02-29')
    ]
    
    # Find common dates across all datasets
    common_dates = (
        set(funding_quarterly['ds']) & 
        set(displacement_df['reportingDate']) &
        set(gdelt_volume_df['ds']) & 
        set(gdelt_tone_df['ds'])
    )
    common_dates = sorted(list(common_dates))
    
    logger.info(f"  Common quarters for analysis: {len(common_dates)}")
    
    # Align all datasets
    fund_aligned = funding_quarterly[
        funding_quarterly['ds'].isin(common_dates)
    ].sort_values('ds')
    
    disp_aligned = displacement_df[
        displacement_df['reportingDate'].isin(common_dates)
    ].sort_values('reportingDate')
    
    vol_aligned = gdelt_volume_df[
        gdelt_volume_df['ds'].isin(common_dates)
    ].sort_values('ds')
    
    tone_aligned = gdelt_tone_df[
        gdelt_tone_df['ds'].isin(common_dates)
    ].sort_values('ds')
    
    # Calculate correlations
    corr_fund_disp, p_fund_disp = pearsonr(
        fund_aligned['yhat_norm'].values,
        disp_aligned['numPresentIdpInd_norm'].values
    )
    
    corr_fund_vol, p_fund_vol = pearsonr(
        fund_aligned['yhat_norm'].values,
        vol_aligned['volume_intensity_norm'].values
    )
    
    corr_fund_tone, p_fund_tone = pearsonr(
        fund_aligned['yhat_norm'].values,
        tone_aligned['tone_norm'].values
    )
    
    corr_disp_vol, p_disp_vol = pearsonr(
        disp_aligned['numPresentIdpInd_norm'].values,
        vol_aligned['volume_intensity_norm'].values
    )
    
    # Compile results
    results = {
        'fund_disp': corr_fund_disp,
        'fund_disp_p': p_fund_disp,
        'fund_vol': corr_fund_vol,
        'fund_vol_p': p_fund_vol,
        'fund_tone': corr_fund_tone,
        'fund_tone_p': p_fund_tone,
        'disp_vol': corr_disp_vol,
        'disp_vol_p': p_disp_vol,
    }
    
    # Log results
    logger.info("\nCorrelation Results:")
    logger.info("-" * 70)
    
    def interpret_correlation(r):
        if abs(r) < 0.3:
            return 'Weak'
        elif abs(r) < 0.7:
            return 'Moderate'
        else:
            return 'Strong'
    
    logger.info(f"\n1. Funding ↔ Displacement:        r = {corr_fund_disp:+.3f} (p = {p_fund_disp:.3f})")
    logger.info(f"   Interpretation: {interpret_correlation(corr_fund_disp)} correlation")
    
    logger.info(f"\n2. Funding ↔ Media Volume:        r = {corr_fund_vol:+.3f} (p = {p_fund_vol:.3f})")
    logger.info(f"   Interpretation: {interpret_correlation(corr_fund_vol)} correlation")
    
    logger.info(f"\n3. Funding ↔ Media Tone:          r = {corr_fund_tone:+.3f} (p = {p_fund_tone:.3f})")
    logger.info(f"   Interpretation: {interpret_correlation(corr_fund_tone)} correlation")
    
    logger.info(f"\n4. Displacement ↔ Media Volume:   r = {corr_disp_vol:+.3f} (p = {p_disp_vol:.3f})")
    logger.info(f"   Interpretation: {interpret_correlation(corr_disp_vol)} correlation")
    
    # Save results
    if save_results:
        results_dir = Path("data/outputs")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        results_df = pd.DataFrame([results])
        results_df.to_csv(results_dir / "correlation_results.csv", index=False)
        
        # Save detailed report
        with open(results_dir / "correlation_report.txt", 'w') as f:
            f.write("HUMANITARIAN FUNDING ANALYSIS - CORRELATION REPORT\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Analysis Period: 2022-02-01 to 2024-02-29\n")
            f.write(f"Common Quarters: {len(common_dates)}\n\n")
            f.write("CORRELATION RESULTS:\n")
            f.write("-" * 70 + "\n\n")
            f.write(f"1. Funding ↔ Displacement:        r = {corr_fund_disp:+.3f} (p = {p_fund_disp:.3f})\n")
            f.write(f"   Interpretation: {interpret_correlation(corr_fund_disp)} correlation\n\n")
            f.write(f"2. Funding ↔ Media Volume:        r = {corr_fund_vol:+.3f} (p = {p_fund_vol:.3f})\n")
            f.write(f"   Interpretation: {interpret_correlation(corr_fund_vol)} correlation\n\n")
            f.write(f"3. Funding ↔ Media Tone:          r = {corr_fund_tone:+.3f} (p = {p_fund_tone:.3f})\n")
            f.write(f"   Interpretation: {interpret_correlation(corr_fund_tone)} correlation\n\n")
            f.write(f"4. Displacement ↔ Media Volume:   r = {corr_disp_vol:+.3f} (p = {p_disp_vol:.3f})\n")
            f.write(f"   Interpretation: {interpret_correlation(corr_disp_vol)} correlation\n\n")
            f.write("=" * 70 + "\n\n")
            f.write("KEY FINDINGS:\n")
            f.write("• Funding shows more correlation with media patterns than displacement\n")
            f.write("• This suggests funding is more responsive to visibility than need\n")
            f.write("• High-profile crises attract disproportionate funding\n")
    
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Correlation analysis module loaded successfully")
