"""
Visualization Module
Generates plots and charts for the analysis
"""

import matplotlib.pyplot as plt
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')


def plot_funding_vs_displacement(
    funding_df: pd.DataFrame,
    displacement_df: pd.DataFrame,
    output_dir: Path
):
    """Plot funding vs displacement trends"""
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.plot(funding_df["ds"], funding_df["yhat_norm"],
           label="Funding (Normalized)", linewidth=2.5, color='#2E86AB')
    
    ax.scatter(displacement_df["reportingDate"], 
              displacement_df["numPresentIdpInd_norm"],
              label="Displacement (Normalized)", s=100, color='#D62828', 
              alpha=0.7, zorder=5)
    
    ax.set_title("Humanitarian Funding vs. Global Displacement", 
                fontsize=16, fontweight='bold')
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Normalized Values (0-1)", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'funding_vs_displacement.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info("  ✓ Saved: funding_vs_displacement.png")


def plot_funding_vs_media_volume(
    funding_df: pd.DataFrame,
    gdelt_df: pd.DataFrame,
    output_dir: Path
):
    """Plot funding vs media coverage volume"""
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.plot(funding_df["ds"], funding_df["yhat_norm"],
           label="Funding (Normalized)", linewidth=2.5, color='#2E86AB')
    
    ax.plot(gdelt_df["ds"], gdelt_df["volume_intensity_norm"],
           label="GDELT Media Volume (Normalized)", linewidth=2.5, color='#F77F00')
    
    ax.set_title("Funding vs Media Coverage Volume", 
                fontsize=16, fontweight='bold')
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Normalized Values (0-1)", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'funding_vs_media_volume.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info("  ✓ Saved: funding_vs_media_volume.png")


def plot_displacement_vs_media(
    displacement_df: pd.DataFrame,
    gdelt_df: pd.DataFrame,
    output_dir: Path
):
    """Plot displacement vs media coverage"""
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.scatter(displacement_df["reportingDate"],
              displacement_df["numPresentIdpInd_norm"],
              label="Displacement (Normalized)", s=100, color='#D62828', 
              alpha=0.7, zorder=5)
    
    ax.plot(gdelt_df["ds"], gdelt_df["volume_intensity_norm"],
           label="GDELT Media Volume (Normalized)", linewidth=2.5, color='#F77F00')
    
    ax.set_title("Displacement vs Media Coverage", 
                fontsize=16, fontweight='bold')
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Normalized Values (0-1)", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'displacement_vs_media.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info("  ✓ Saved: displacement_vs_media.png")


def plot_funding_vs_media_tone(
    funding_df: pd.DataFrame,
    tone_df: pd.DataFrame,
    output_dir: Path
):
    """Plot funding vs media sentiment/tone"""
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.plot(funding_df["ds"], funding_df["yhat_norm"],
           label="Funding (Normalized)", linewidth=2.5, color='#2E86AB')
    
    ax.plot(tone_df["ds"], tone_df["tone_norm"],
           label="GDELT Media Tone (Normalized)", linewidth=2.5, color='#06A77D')
    
    ax.set_title("Funding vs Media Sentiment", 
                fontsize=16, fontweight='bold')
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Normalized Values (0-1)", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'funding_vs_media_tone.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info("  ✓ Saved: funding_vs_media_tone.png")


def generate_all_visualizations(
    funding_df: pd.DataFrame,
    displacement_df: pd.DataFrame,
    gdelt_volume_df: pd.DataFrame,
    gdelt_tone_df: pd.DataFrame
):
    """Generate all visualization plots"""
    
    logger.info("Generating visualizations...")
    
    # Create output directory
    output_dir = Path("data/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate plots
    plot_funding_vs_displacement(funding_df, displacement_df, output_dir)
    plot_funding_vs_media_volume(funding_df, gdelt_volume_df, output_dir)
    plot_displacement_vs_media(displacement_df, gdelt_volume_df, output_dir)
    plot_funding_vs_media_tone(funding_df, gdelt_tone_df, output_dir)
    
    logger.info(f"\n✓ All visualizations saved to: {output_dir}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Visualization module loaded successfully")
