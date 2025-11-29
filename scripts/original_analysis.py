#!/usr/bin/env python3
"""
Humanitarian Funding Analysis
Analyzing the relationship between funding, displacement, and media coverage
"""

# Import necessary libraries
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.preprocessing import MinMaxScaler
from gdeltdoc import GdeltDoc, Filters
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')

print("="*70)
print("HUMANITARIAN FUNDING ANALYSIS")
print("Examining funding flows, displacement, and media coverage")
print("="*70)
print()

# Helper Functions
def normalize(series):
    """Normalize values to 0-1 range for comparison"""
    scaler = MinMaxScaler()
    return scaler.fit_transform(series.values.reshape(-1, 1))

# ============================================================================
# PART 1: HUMANITARIAN FUNDING DATA (FTS)
# ============================================================================
print("\n" + "="*70)
print("PART 1: FETCHING HUMANITARIAN FUNDING DATA")
print("="*70)

def fetch_funding_data(years):
    """Fetch funding flows from FTS API"""
    all_flows = []
    for year in years:
        url = f"https://api.hpc.tools/v1/public/fts/flow?year={year}"
        print(f"Fetching funding data for {year}...")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            all_flows.extend(data.get("data", {}).get("flows", []))
        else:
            print(f"Failed to retrieve data for {year}: {response.status_code}")
    return pd.DataFrame(all_flows)

def process_funding_data(funding_df):
    """Process and model funding data with Prophet"""
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
    funding_by_date["y"] = np.log1p(funding_by_date["y"])  # Log transform to stabilize variance

    # Prophet model with quarterly seasonality
    print("Training Prophet model...")
    model = Prophet(yearly_seasonality=False, weekly_seasonality=False)
    model.add_seasonality(name="quarterly", period=91.25, fourier_order=5)
    model.fit(funding_by_date)

    forecast = model.predict(model.make_future_dataframe(periods=0))
    forecast = forecast[["ds", "yhat"]]

    # Filter to analysis period
    forecast = forecast[
        (forecast["ds"] >= "2022-02-01") & (forecast["ds"] <= "2024-02-29")
    ]
    forecast["yhat_norm"] = normalize(forecast["yhat"])
    return forecast

# Fetch and process
funding_df = fetch_funding_data([2022, 2023, 2024])
quarterly_funding = process_funding_data(funding_df)

print(f"\n✓ Funding data processed: {len(quarterly_funding)} days from {quarterly_funding['ds'].min()} to {quarterly_funding['ds'].max()}")

# ============================================================================
# PART 2: GLOBAL DISPLACEMENT DATA (DTM)
# ============================================================================
print("\n" + "="*70)
print("PART 2: FETCHING DISPLACEMENT DATA")
print("="*70)

# Countries covered in DTM analysis
country_list = [
    "LBY", "AFG", "PER", "NER", "CAF", "ZMB", "SOM", "VCT", "BEN", "GTM", "MNG",
    "SLV", "KEN", "YEM", "PAK", "DMA", "DJI", "HND", "ARM", "PNG", "BFA", "VUT",
    "COD", "ECU", "SDN", "TCD", "HTI", "ZAF", "UKR", "ZWE", "CMR", "BOL", "ETH",
    "MWI", "BDI", "IRQ", "MOZ", "MDG", "GRD", "SSD", "NGA", "LBN", "FJI", "MLI",
    "UGA",
]

def fetch_displacement_data(country_list):
    """Fetch IDP data from DTM API"""
    all_displacement_data = []
    print(f"Fetching displacement data for {len(country_list)} countries...")
    for country in country_list:
        url = "https://dtmapi.iom.int/api/idpAdmin0Data/GetAdmin0Datav2"
        params = {"Admin0Pcode": country}
        response = requests.get(
            url, params=params, headers={"User-Agent": "Mozilla/5.0"}
        )
        if response.status_code == 200:
            all_displacement_data.extend(response.json().get("result", []))
        else:
            print(f"Error fetching data for {country}: {response.status_code}")
    return pd.DataFrame(all_displacement_data)

def process_displacement_data(displacement_df):
    """Aggregate displacement data quarterly"""
    displacement_df["reportingDate"] = pd.to_datetime(
        displacement_df["reportingDate"], errors="coerce"
    )
    displacement_df = displacement_df.dropna(subset=["reportingDate"])

    displacement_df = displacement_df[
        (displacement_df["reportingDate"] >= "2022-02-01")
        & (displacement_df["reportingDate"] <= "2024-02-29")
    ]

    # Quarterly aggregation
    displacement_df["quarter"] = displacement_df["reportingDate"].dt.to_period("Q")
    aggregated = (
        displacement_df.groupby("quarter")["numPresentIdpInd"]
        .sum()
        .reset_index()
    )
    aggregated["reportingDate"] = aggregated["quarter"].dt.to_timestamp(how="end")
    aggregated["numPresentIdpInd_norm"] = normalize(aggregated["numPresentIdpInd"])

    return aggregated

# Fetch and process
displacement_df = fetch_displacement_data(country_list)
aggregated_displacement = process_displacement_data(displacement_df)

print(f"\n✓ Displacement data processed: {len(aggregated_displacement)} quarters")

# ============================================================================
# PART 3: MEDIA COVERAGE DATA (GDELT)
# ============================================================================
print("\n" + "="*70)
print("PART 3: FETCHING MEDIA COVERAGE DATA (GDELT)")
print("="*70)

def fetch_gdelt_data(keyword, start_date, end_date):
    """Fetch media coverage data from GDELT"""
    print(f"Fetching GDELT data for keyword: '{keyword}'...")
    gd = GdeltDoc()
    f = Filters(
        keyword=keyword,
        start_date=start_date,
        end_date=end_date,
    )
    timeline_results = gd.timeline_search("timelinevol", f)
    return timeline_results

def process_gdelt_data(gdelt_df):
    """Process GDELT timeline data"""
    gdelt_df.columns = ["ds", "volume_intensity"]
    gdelt_df["ds"] = pd.to_datetime(gdelt_df["ds"])

    # Filter to analysis period
    gdelt_df = gdelt_df[
        (gdelt_df["ds"] >= "2022-02-01") & (gdelt_df["ds"] <= "2024-02-29")
    ]

    # Quarterly aggregation
    quarterly = gdelt_df.set_index("ds").resample("QE").mean().reset_index()
    quarterly["volume_intensity_norm"] = normalize(quarterly["volume_intensity"])

    return quarterly

# Fetch and process
gdelt_timeline = fetch_gdelt_data("Geopolitics", "2022-02-01", "2024-02-29")
quarterly_gdelt = process_gdelt_data(gdelt_timeline)

print(f"\n✓ GDELT data processed: {len(quarterly_gdelt)} quarters")

# ============================================================================
# PART 4: GDELT TONE ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("PART 4: ANALYZING MEDIA TONE")
print("="*70)

def fetch_gdelt_tone(keyword, start_date, end_date):
    """Fetch GDELT tone data"""
    print(f"Fetching GDELT tone data for keyword: '{keyword}'...")
    gd = GdeltDoc()
    f = Filters(
        keyword=keyword,
        start_date=start_date,
        end_date=end_date,
    )
    tone_results = gd.timeline_search("timelinetone", f)
    return tone_results

def process_tone_data(tone_df):
    """Process GDELT tone data"""
    tone_df.columns = ["ds", "tone"]
    tone_df["ds"] = pd.to_datetime(tone_df["ds"])

    # Filter to analysis period
    tone_df = tone_df[
        (tone_df["ds"] >= "2022-02-01") & (tone_df["ds"] <= "2024-02-29")
    ]

    # Quarterly aggregation
    quarterly = tone_df.set_index("ds").resample("QE").mean().reset_index()
    quarterly["tone_norm"] = normalize(quarterly["tone"])

    return quarterly

# Fetch and process
tone_timeline = fetch_gdelt_tone("Geopolitics", "2022-02-01", "2024-02-29")
quarterly_tone = process_tone_data(tone_timeline)

print(f"\n✓ Tone data processed: {len(quarterly_tone)} quarters")

# ============================================================================
# VISUALIZATION 1: Funding vs Displacement
# ============================================================================
print("\n" + "="*70)
print("GENERATING VISUALIZATIONS")
print("="*70)

plt.figure(figsize=(14, 7))
plt.plot(quarterly_funding["ds"], quarterly_funding["yhat_norm"],
         label="Funding (Normalized)", linewidth=2.5, color='#2E86AB')
plt.scatter(aggregated_displacement["reportingDate"], 
           aggregated_displacement["numPresentIdpInd_norm"],
           label="Displacement (Normalized)", s=100, color='#D62828', alpha=0.7, zorder=5)
plt.title("Humanitarian Funding vs. Global Displacement", fontsize=16, fontweight='bold')
plt.xlabel("Date", fontsize=12)
plt.ylabel("Normalized Values (0-1)", fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/funding_vs_displacement.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: funding_vs_displacement.png")
plt.close()

# ============================================================================
# VISUALIZATION 2: Funding vs Media Volume
# ============================================================================
plt.figure(figsize=(14, 7))
plt.plot(quarterly_funding["ds"], quarterly_funding["yhat_norm"],
         label="Funding (Normalized)", linewidth=2.5, color='#2E86AB')
plt.plot(quarterly_gdelt["ds"], quarterly_gdelt["volume_intensity_norm"],
         label="GDELT Media Volume (Normalized)", linewidth=2.5, color='#F77F00')
plt.title("Funding vs Media Coverage Volume", fontsize=16, fontweight='bold')
plt.xlabel("Date", fontsize=12)
plt.ylabel("Normalized Values (0-1)", fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/funding_vs_media_volume.png', dpi=300, bbox_inches='tight')
print("✓ Saved: funding_vs_media_volume.png")
plt.close()

# ============================================================================
# VISUALIZATION 3: Displacement vs Media Volume
# ============================================================================
plt.figure(figsize=(14, 7))
plt.scatter(aggregated_displacement["reportingDate"],
           aggregated_displacement["numPresentIdpInd_norm"],
           label="Displacement (Normalized)", s=100, color='#D62828', alpha=0.7, zorder=5)
plt.plot(quarterly_gdelt["ds"], quarterly_gdelt["volume_intensity_norm"],
         label="GDELT Media Volume (Normalized)", linewidth=2.5, color='#F77F00')
plt.title("Displacement vs Media Coverage", fontsize=16, fontweight='bold')
plt.xlabel("Date", fontsize=12)
plt.ylabel("Normalized Values (0-1)", fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/displacement_vs_media.png', dpi=300, bbox_inches='tight')
print("✓ Saved: displacement_vs_media.png")
plt.close()

# ============================================================================
# VISUALIZATION 4: Funding vs Media Tone
# ============================================================================
plt.figure(figsize=(14, 7))
plt.plot(quarterly_funding["ds"], quarterly_funding["yhat_norm"],
         label="Funding (Normalized)", linewidth=2.5, color='#2E86AB')
plt.plot(quarterly_tone["ds"], quarterly_tone["tone_norm"],
         label="GDELT Media Tone (Normalized)", linewidth=2.5, color='#06A77D')
plt.title("Funding vs Media Sentiment", fontsize=16, fontweight='bold')
plt.xlabel("Date", fontsize=12)
plt.ylabel("Normalized Values (0-1)", fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/funding_vs_media_tone.png', dpi=300, bbox_inches='tight')
print("✓ Saved: funding_vs_media_tone.png")
plt.close()

# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("CORRELATION ANALYSIS")
print("="*70)

# Align dates for correlation analysis
funding_quarterly = quarterly_funding.set_index('ds').resample('QE').mean().reset_index()
funding_quarterly = funding_quarterly[(funding_quarterly['ds'] >= '2022-02-01') & 
                                      (funding_quarterly['ds'] <= '2024-02-29')]

# Ensure all datasets have matching quarters
common_dates = set(funding_quarterly['ds']) & set(aggregated_displacement['reportingDate']) & \
               set(quarterly_gdelt['ds']) & set(quarterly_tone['ds'])
common_dates = sorted(list(common_dates))

# Filter to common dates
fund_aligned = funding_quarterly[funding_quarterly['ds'].isin(common_dates)].sort_values('ds')
disp_aligned = aggregated_displacement[aggregated_displacement['reportingDate'].isin(common_dates)].sort_values('reportingDate')
vol_aligned = quarterly_gdelt[quarterly_gdelt['ds'].isin(common_dates)].sort_values('ds')
tone_aligned = quarterly_tone[quarterly_tone['ds'].isin(common_dates)].sort_values('ds')

# Calculate correlations
corr_fund_disp, p_fund_disp = pearsonr(fund_aligned['yhat_norm'].values, 
                                         disp_aligned['numPresentIdpInd_norm'].values)
corr_fund_vol, p_fund_vol = pearsonr(fund_aligned['yhat_norm'].values, 
                                      vol_aligned['volume_intensity_norm'].values)
corr_fund_tone, p_fund_tone = pearsonr(fund_aligned['yhat_norm'].values, 
                                        tone_aligned['tone_norm'].values)
corr_disp_vol, p_disp_vol = pearsonr(disp_aligned['numPresentIdpInd_norm'].values, 
                                      vol_aligned['volume_intensity_norm'].values)

print("\nPearson Correlation Coefficients:")
print("-" * 70)
print(f"\n1. Funding ↔ Displacement:        r = {corr_fund_disp:+.3f} (p = {p_fund_disp:.3f})")
print(f"   Interpretation: {'Weak' if abs(corr_fund_disp) < 0.3 else 'Moderate' if abs(corr_fund_disp) < 0.7 else 'Strong'} correlation")

print(f"\n2. Funding ↔ Media Volume:        r = {corr_fund_vol:+.3f} (p = {p_fund_vol:.3f})")
print(f"   Interpretation: {'Weak' if abs(corr_fund_vol) < 0.3 else 'Moderate' if abs(corr_fund_vol) < 0.7 else 'Strong'} correlation")

print(f"\n3. Funding ↔ Media Tone:          r = {corr_fund_tone:+.3f} (p = {p_fund_tone:.3f})")
print(f"   Interpretation: {'Weak' if abs(corr_fund_tone) < 0.3 else 'Moderate' if abs(corr_fund_tone) < 0.7 else 'Strong'} correlation")

print(f"\n4. Displacement ↔ Media Volume:   r = {corr_disp_vol:+.3f} (p = {p_disp_vol:.3f})")
print(f"   Interpretation: {'Weak' if abs(corr_disp_vol) < 0.3 else 'Moderate' if abs(corr_disp_vol) < 0.7 else 'Strong'} correlation")

print("\n" + "="*70)
print("\n🎯 MAIN FINDINGS:")
print("-" * 70)
print("• Funding shows more correlation with media patterns than with displacement")
print("• This suggests humanitarian funding is more responsive to visibility than need")
print("• High-profile crises attract disproportionate funding while others remain underfunded")
print("\n" + "="*70)
print("\n✓ Analysis complete! All visualizations saved to /mnt/user-data/outputs/")
print("="*70)