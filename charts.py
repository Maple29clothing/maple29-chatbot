"""The 16 user-confirmed size charts, keyed by user-facing product name.

Each chart: {"catalog": catalog item name (for reference),
             "entries": [{"size", "price" (MMK string or None), "measure"}],
             "note": optional extra line}
Prices are the user-confirmed prices from 30 Oct 2026.
"""
# Zero Waste Pants uses the EXACT Burmese wording from the approved draft,
# so it is rendered separately in flows.py (ZW_PANTS_SIZE_GUIDE).

CHARTS = {
    "Vietnamese Blouse": {
        "catalog": "Vietnam Blouse",
        "entries": [
            {"size": "M", "price": "47,000", "measure": "Bust 32–38"},
            {"size": "XL", "price": "47,000", "measure": "Bust 38–42"},
            {"size": "2XL", "price": "47,000", "measure": "Bust 44–50"},
        ],
    },
    "Tulip Garden Blouse": {
        "catalog": "Tulip Garden Blouse",
        "note": "100% cotton, breathable, lightweight",
        "entries": [
            {"size": "XS", "price": "85,000", "measure": "Bust 32"},
            {"size": "S", "price": "85,000", "measure": "Bust 34"},
            {"size": "M", "price": "85,000", "measure": "Bust 36"},
            {"size": "L", "price": "89,000", "measure": "Bust 38"},
            {"size": "XL", "price": "89,000", "measure": "Bust 40"},
            {"size": "2XL", "price": "95,000", "measure": None},
            {"size": "3XL", "price": "95,000", "measure": None},
            {"size": "4XL", "price": "105,000", "measure": None},
        ],
    },
    "Zero Waste Crop Top": {
        "catalog": "Zero Waste Top Short Sleeves",
        "entries": [
            {"size": "M", "price": "28,000", "measure": "Bust 30–38, Length 15.5–16"},
            {"size": "L", "price": "30,000", "measure": "Bust 40–48, Length 20"},
            {"size": "XL", "price": "32,000", "measure": "Bust 50–58, Length 21"},
        ],
    },
    "Bowtie Vietnam Blouse": {
        "catalog": "Bow Tie Vietnam Blouse",
        "entries": [
            {"size": "M", "price": "59,000", "measure": "Bust 32–38"},
            {"size": "XL", "price": "59,000", "measure": "Bust 38–42"},
            {"size": "2XL", "price": "59,000", "measure": "Bust 44–50"},
            {"size": "5XL", "price": "59,000", "measure": "Bust 50–54"},
        ],
    },
    "Strapless Cotton Top": {
        "catalog": "Strapless Cotton Top",
        "note": "100% cotton, breathable, lightweight",
        "entries": [
            {"size": "M", "price": "35,000", "measure": "Bust 36–40"},
            {"size": "XL", "price": "35,000", "measure": "Bust 42–46"},
            {"size": "3XL", "price": "35,000", "measure": "Bust 46–52"},
        ],
    },
    "Boxy Jacket": {
        "catalog": "Boxy Jacket",
        "entries": [
            {"size": "Free (L)", "price": "125,000", "measure": "Bust 32–42"},
            {"size": "Plus (2XL)", "price": "135,000", "measure": "Bust 44–52"},
        ],
    },
    "Summer Escape Mermaid Top": {
        "catalog": "Summer Escape Midmaid Blouse",
        "entries": [
            {"size": "Free size", "price": "45,000", "measure": "Bust 42–52"},
        ],
    },
    "Summer Escape Shirt": {
        "catalog": "Summer Escape Shirt",
        "entries": [
            {"size": "Free size", "price": "46,500–49,500", "measure": "Bust 42–52"},
        ],
    },
    "Plus Size Short Sleeve Shirt": {
        "catalog": "Over Size Short Sleeve Shirt",
        "entries": [
            {"size": "Free size", "price": "46,500", "measure": "Bust 42–56"},
        ],
    },
    "Zero Waste Short Sleeve": {
        "catalog": "Zero Waste Top Short Sleeves",
        "entries": [
            {"size": "M", "price": "28,000", "measure": "Chest 30–38, Length 15.5–16"},
            {"size": "L", "price": "30,000", "measure": "Chest 40–46, Length 16.5–17"},
            {"size": "XL", "price": "32,000", "measure": "Chest 48–54, Length 17.5–18"},
        ],
    },
    "Plus Size Zero Waste Pants": {
        "catalog": "Zero Waste Plus Size Pants Tissue",
        "entries": [
            {"size": "Free Size", "price": "44,000",
             "measure": "Waist 36–44, Hip 46–56, Length 38–39"},
        ],
    },
    "Back Tie Shirt": {
        "catalog": "Back Tie Shirt",
        "entries": [
            {"size": "Free size", "price": "46,500", "measure": "Bust 38–52"},
        ],
    },
    "Plus Size Stripe Pants": {
        "catalog": "Zero Waste Stripe Pant",
        "entries": [
            {"size": "Free Size", "price": "46,500",
             "measure": "Waist 24–38, Hip 34–46, Length 38–39"},
        ],
    },
    "Cheik Skirt": {
        "catalog": "Cheik Skirt",
        "entries": [
            {"size": "XS", "price": "95,000", "measure": "Waist 24, Hip 36, Length 36"},
            {"size": "S", "price": "95,000", "measure": "Waist 25, Hip 37.5, Length 37.5"},
            {"size": "M", "price": "95,000", "measure": "Waist 27, Hip 39, Length 37.75"},
            {"size": "L", "price": "95,000", "measure": "Waist 28, Hip 40.5, Length 37.5"},
            {"size": "XL", "price": "95,000", "measure": "Waist 31, Hip 44, Length 38.5"},
            {"size": "2XL", "price": "95,000", "measure": "Waist 33, Hip 45.5, Length 39"},
            {"size": "3XL", "price": "95,000", "measure": "Waist 35, Hip 47, Length 39"},
            {"size": "4XL", "price": "95,000", "measure": "Waist 36, Hip 48.5, Length 39.5"},
            {"size": "5XL", "price": "95,000", "measure": "Waist 38, Hip 50, Length 39.5"},
            {"size": "6XL", "price": "95,000", "measure": "Waist 39, Hip 51.5, Length 39.5"},
            {"size": "7XL", "price": None, "measure": "Waist 41, Hip 53, Length 40"},
        ],
    },
    "Vest": {
        "catalog": "Cheik Vest",
        "entries": [
            {"size": "8 (M)", "price": "90,000",
             "measure": "Bust 33–36, Shoulder 26–29, Length 24"},
            {"size": "12 (L)", "price": "90,000",
             "measure": "Bust 37–39, Shoulder 30–32, Length 24"},
            {"size": "16 (XL)", "price": "90,000",
             "measure": "Bust 40–43, Shoulder 33–36, Length 24.5"},
            {"size": "20 (2XL)", "price": "90,000",
             "measure": "Bust 44–47, Shoulder 37–40, Length 25"},
            {"size": "24 (3XL)", "price": "90,000",
             "measure": "Bust 48–52, Shoulder 41–44, Length 25"},
        ],
    },
}
