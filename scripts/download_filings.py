from sec_edgar_downloader import Downloader
from pathlib import Path
from tqdm import tqdm

# ============================================================
# Companies
# ============================================================

COMPANIES = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "AMZN": "Amazon",
    "META": "Meta",
    "GOOGL": "Alphabet",
    "TSLA": "Tesla",
    "AMD": "AMD",
    "NFLX": "Netflix",
    "ORCL": "Oracle",
}

# ============================================================
# Downloader
# ============================================================

download_path = Path("data/raw")

dl = Downloader(
    download_folder=str(download_path),
    company_name="Financial RAG",
    email_address="your_email@example.com"   # Replace with your email
)

# ============================================================
# Download
# ============================================================

YEARS = 5        # Last 5 filings
FORM_TYPE = "10-K"

print("=" * 60)
print("Downloading SEC Filings")
print("=" * 60)

for ticker, company in tqdm(COMPANIES.items()):

    print(f"\nDownloading {company} ({ticker})")

    try:

        dl.get(
            FORM_TYPE,
            ticker,
            limit=YEARS
        )

        print("Done")

    except Exception as e:

        print(f"Failed : {e}")

print("\nDownload Completed.")