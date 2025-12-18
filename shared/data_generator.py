"""
Shared Data Generator - Refactored
Minimal version containing only functions used by cart_tracking_router
"""

from faker import Faker
from pathlib import Path
import random
import gzip
import json
import asyncio

# Initialize Faker with Vietnamese locale
fake_vi = Faker('vi_VN')
fake_en = Faker('en_US')

# Shared data storage
SHARED_PRODUCTS = []

# Data directories
DATA_DIR = Path("./shared_data")
SHARE_DATA_DIR = DATA_DIR / "share_data"
PRIVATE_DATA_DIR = DATA_DIR / "private_data"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
SHARE_DATA_DIR.mkdir(exist_ok=True)
PRIVATE_DATA_DIR.mkdir(exist_ok=True)

# Private data directories for each router
PRIVATE_DIRS = {
    "shopify": PRIVATE_DATA_DIR / "shopify",
    "sapo": PRIVATE_DATA_DIR / "sapo",
    "odoo": PRIVATE_DATA_DIR / "odoo",
    "paypal": PRIVATE_DATA_DIR / "paypal",
    "mercury": PRIVATE_DATA_DIR / "mercury",
    "momo": PRIVATE_DATA_DIR / "momo",
    "zalopay": PRIVATE_DATA_DIR / "zalopay",
    "cart_tracking": PRIVATE_DATA_DIR / "cart_tracking",
    "online_orders": PRIVATE_DATA_DIR / "online_orders"
}

# Create all private directories
for dir_path in PRIVATE_DIRS.values():
    dir_path.mkdir(exist_ok=True)

# Async lock for thread-safe operations
_lock = asyncio.Lock()


def load_compressed(filepath):
    """Load compressed JSON data"""
    if not filepath.exists():
        return None
    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        return json.load(f)


def get_share_data_path(filename):
    """Get path for shared data file"""
    return SHARE_DATA_DIR / filename


def get_private_data_path(router_name, filename):
    """Get path for private data file"""
    if router_name in PRIVATE_DIRS:
        return PRIVATE_DIRS[router_name] / filename
    return PRIVATE_DATA_DIR / router_name / filename


async def ensure_products_loaded():
    """Ensure products are loaded into memory from file if available"""
    async with _lock:
        global SHARED_PRODUCTS

        if not SHARED_PRODUCTS or len(SHARED_PRODUCTS) == 0:
            # Try new location first
            products_file = get_share_data_path("products.json.gz")
            # Fallback to old location
            if not products_file.exists():
                products_file = DATA_DIR / "products.json.gz"

            if products_file.exists():
                SHARED_PRODUCTS = load_compressed(products_file)


def get_random_product():
    """Get random product from shared catalog"""
    return random.choice(SHARED_PRODUCTS) if SHARED_PRODUCTS else None


def get_random_customer():
    """Get random customer from shared database"""
    customer_id = random.randint(1, 2_000_000)
    return {"id": customer_id}


async def initialize_shared_data():
    """Initialize shared data on startup (products only for cart tracking)"""
    global SHARED_PRODUCTS

    # Check new location first, then fallback to old location
    products_file = get_share_data_path("products.json.gz")
    if not products_file.exists():
        products_file = DATA_DIR / "products.json.gz"

    if products_file.exists():
        print("Loading existing products...")
        SHARED_PRODUCTS = load_compressed(products_file)
        print(f"Loaded {len(SHARED_PRODUCTS)} products from file")
    else:
        print("No product data found. Generate via /cart/generate/events endpoint")
