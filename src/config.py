from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "customer_support_tickets.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"

RANDOM_SEED = 42