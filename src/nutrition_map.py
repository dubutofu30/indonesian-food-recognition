# src/nutrition_map.py
import re
from typing import Dict, Any

def _normalize(s: str) -> str:
    """
    Normalisasi label/folder:
    "01. Ayam Betutu" -> "ayam betutu"
    "37. Cumi - Cumi Goreng" -> "cumi cumi goreng"
    """
    s = s.strip().lower()
    s = re.sub(r"^\d+\.\s*", "", s)  # hapus "01. "
    s = s.replace("-", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s

# Database full dari data kamu (51 kelas)
# Key = nama makanan yang sudah dinormalisasi (tanpa nomor)
NUTRITION_DB: Dict[str, Dict[str, Any]] = {
    "ayam betutu": {
        "display_name": "Ayam Betutu",
        "nutrition": {"calories": 102.0, "protein": 3.2, "fat": 6.0, "carbohydrate": 8.7},
        "match_source": "fuzzy:cammetutu",
    },
    "beberuk Terong": {
       "display_name": "Beberuk Terong",
       "nutrition": { "calories": 65.0, "protein": 1.10, "fat": 5.20, "carbohydrate": 3.50 },
       "match_source": "nilaigizi:beberuk_per_100g",
   },
    "coto makassar": {
        "display_name": "Coto Makassar",
        "nutrition": { "calories": 84.0, "protein": 6.0, "fat": 6.0, "carbohydrate": 1.40 },
        "match_source": "nilaigizi:coto_mangkasara_sapi_per_100g",
    },
    "gudeg": {
        "display_name": "Gudeg",
        "nutrition": {"calories": 53.0, "protein": 1.6, "fat": 1.6, "carbohydrate": 8.8},
        "match_source": "exact",
    },
    "kerak telor": {
        "display_name": "Kerak Telor",
        "nutrition": { "calories": 244.3, "protein": 10.87, "fat": 8.55, "carbohydrate": 30.04 },
        "match_source": "fatsecret:kerak_telor_converted_to_100g",
    },
    "mie aceh": {
        "display_name": "Mie Aceh",
        "nutrition": {"calories": 113.0, "protein": 3.0, "fat": 3.2, "carbohydrate": 18.1},
        "match_source": "fuzzy:mie aceh rebus",
    },
    "nasi kuning": {
        "display_name": "Nasi Kuning",
        "nutrition": {"calories": 357.0, "protein": 8.8, "fat": 0.5, "carbohydrate": 79.5},
        "match_source": "fuzzy:nasi jagung",
    },
    "nasi pecel": {
        "display_name": "Nasi Pecel",
        "nutrition": { "calories": 230.0, "protein": 6.58, "fat": 9.33, "carbohydrate": 31.74 },
        "match_source": "fatsecret:nasi_pecel_per_100g",
    },
    "papeda": {
        "display_name": "Papeda",
        "nutrition": {"calories": 61.0, "protein": 0.2, "fat": 0.1, "carbohydrate": 14.9},
        "match_source": "exact",
    },
    "pempek": {
        "display_name": "Pempek",
        "nutrition": {"calories": 116.0, "protein": 3.0, "fat": 0.4, "carbohydrate": 28.6},
        "match_source": "fuzzy:cempedak",
    },
    "peuyeum": {
        "display_name": "Peuyeum",
        "nutrition": { "calories": 175.0, "protein": 2.27, "fat": 0.50, "carbohydrate": 39.90 },
        "match_source": "fatsecret:tape_singkong_per_100g",
    },
    "rawon": {
        "display_name": "Rawon",
        "nutrition": { "calories": 60.0, "protein": 5.40, "fat": 2.50, "carbohydrate": 4.00 },
        "match_source": "nilaigizi:rawon_masakan_per_100g",
    },
    "rendang": {
        "display_name": "Rendang",
        "nutrition": {"calories": 381.7, "protein": 9.5, "fat": 9.5, "carbohydrate": 65.8},
        "match_source": "fuzzy:jenang",
    },
    "sate madura": {
        "display_name": "Sate Madura",
        "nutrition": { "calories": 225.0, "protein": 19.54, "fat": 14.82, "carbohydrate": 4.87 },
        "match_source": "nilaigizi:sate_ayam_per_100g_proxy",
    },
    "serabi": {
        "display_name": "Serabi",
        "nutrition": {"calories": 70.0, "protein": 0.6, "fat": 0.0, "carbohydrate": 18.9},
        "match_source": "fuzzy:erbis",
    },
    "soto banjar": {
        "display_name": "Soto Banjar",
        "nutrition": {"calories": 110.0, "protein": 2.9, "fat": 9.5, "carbohydrate": 3.2},
        "match_source": "fuzzy:soto banjar masakan",
    },
    "soto lamongan": {
         "display_name": "Soto Lamongan",
        "nutrition": { "calories": 129.5, "protein": 9.96, "fat": 6.19, "carbohydrate": 8.11 },
        "match_source": "fatsecret:soto_ayam_converted_to_100g_proxy",
    },
    "tahu sumedang": {
        "display_name": "Tahu Sumedang",
        "nutrition": { "calories": 271.0, "protein": 17.19, "fat": 20.18, "carbohydrate": 10.49 },
        "match_source": "fatsecret:tahu_goreng_per_100g_proxy",
    },
    "madu": {
        "display_name": "Madu",
        "nutrition": {"calories": 294.0, "protein": 0.3, "fat": 0.0, "carbohydrate": 79.5},
        "match_source": "exact",
    },
    "capcay": {
        "display_name": "Capcay",
        "nutrition": {"calories": 23.0, "protein": 1.8, "fat": 0.3, "carbohydrate": 4.5},
        "match_source": "fuzzy:pecay",
    },
    "combro": {
        "display_name": "Combro",
        "nutrition": {"calories": 210.0, "protein": 1.6, "fat": 6.6, "carbohydrate": 35.8},
        "match_source": "exact",
    },
    "gaplek": {
        "display_name": "Gaplek",
        "nutrition": {"calories": 338.0, "protein": 1.5, "fat": 0.7, "carbohydrate": 81.3},
        "match_source": "exact",
    },
    "ikan bawal": {
        "display_name": "Ikan Bawal",
        "nutrition": {"calories": 96.0, "protein": 19.0, "fat": 1.7, "carbohydrate": 0.0},
        "match_source": "exact",
    },
    "jagung rebus": {
        "display_name": "Jagung Rebus",
        "nutrition": {"calories": 175.0, "protein": 1.8, "fat": 1.8, "carbohydrate": 35.0},
        "match_source": "exact",
    },
    "kacang tanah": {
        "display_name": "Kacang Tanah",
        "nutrition": {"calories": 600.0, "protein": 14.0, "fat": 41.7, "carbohydrate": 42.0},
        "match_source": "fuzzy:noga kacang tanah",
    },
    "mie goreng": {
        "display_name": "Mie Goreng",
        "nutrition": {"calories": 468.0, "protein": 7.6, "fat": 20.4, "carbohydrate": 62.4},
        "match_source": "exact",
    },
    "lawar babi": {
        "display_name": "Lawar Babi",
        "nutrition": {"calories": 174.0, "protein": 17.0, "fat": 10.0, "carbohydrate": 3.0},
        "match_source": "fuzzy:lawar babi masakan",
    },
    "empal goreng": {
        "display_name": "Empal Goreng",
        "nutrition": {"calories": 590.0, "protein": 18.5, "fat": 57.0, "carbohydrate": 0.0},
        "match_source": "exact",
    },
    "kangkung tumis": {
        "display_name": "Kangkung Tumis",
        "nutrition": {"calories": 52.0, "protein": 1.8, "fat": 3.6, "carbohydrate": 3.0},
        "match_source": "exact",
    },
    "karedok sayur": {
        "display_name": "Karedok Sayur",
        "nutrition": {"calories": 92.0, "protein": 2.2, "fat": 3.3, "carbohydrate": 14.1},
        "match_source": "exact",
    },
    "bubur sagu": {
        "display_name": "Bubur Sagu",
        "nutrition": {"calories": 167.0, "protein": 0.2, "fat": 4.0, "carbohydrate": 33.0},
        "match_source": "exact",
    },
    "abon": {
        "display_name": "Abon",
        "nutrition": {"calories": 280.0, "protein": 9.2, "fat": 28.4, "carbohydrate": 0.0},
        "match_source": "exact",
    },
    "bacang": {
        "display_name": "Bacang",
        "nutrition": {"calories": 102.9, "protein": 3.3, "fat": 2.7, "carbohydrate": 16.3},
        "match_source": "exact",
    },
    "bakso": {
        "display_name": "Bakso",
        "nutrition": {"calories": 76.0, "protein": 4.1, "fat": 2.5, "carbohydrate": 9.2},
        "match_source": "exact",
    },
    "bayam": {
        "display_name": "Bayam",
        "nutrition": {"calories": 302.0, "protein": 18.2, "fat": 25.0, "carbohydrate": 0.0},
        "match_source": "fuzzy:ayam",
    },
    "brem": {
        "display_name": "Brem",
        "nutrition": {"calories": 249.0, "protein": 3.4, "fat": 0.4, "carbohydrate": 58.0},
        "match_source": "exact",
    },
    "cumi cumi goreng": {
        "display_name": "Cumi - Cumi Goreng",
        "nutrition": {"calories": 265.0, "protein": 40.6, "fat": 10.1, "carbohydrate": 0.0},
        "match_source": "fuzzy:cumicumi goreng",
    },
    "es mambo": {
        "display_name": "Es Mambo",
        "nutrition": {"calories": 152.0, "protein": 0.0, "fat": 0.0, "carbohydrate": 37.6},
        "match_source": "exact",
    },
    "keju": {
        "display_name": "Keju",
        "nutrition": {"calories": 326.0, "protein": 22.8, "fat": 20.3, "carbohydrate": 13.1},
        "match_source": "exact",
    },
    "kue putu": {
        "display_name": "Kue Putu",
        "nutrition": {"calories": 393.3, "protein": 2.7, "fat": 2.7, "carbohydrate": 79.3},
        "match_source": "fuzzy:kue satu",
    },
    "martabak manis": {
        "display_name": "Martabak Manis",
        "nutrition": {"calories": 265.3, "protein": 4.7, "fat": 5.5, "carbohydrate": 49.3},
        "match_source": "exact",
    },
    "nasi goreng": {
        "display_name": "Nasi Goreng",
        "nutrition": {"calories": 276.0, "protein": 3.2, "fat": 3.2, "carbohydrate": 30.2},
        "match_source": "exact",
    },
    "oncom": {
        "display_name": "Oncom",
        "nutrition": {"calories": 187.0, "protein": 13.0, "fat": 6.0, "carbohydrate": 22.6},
        "match_source": "exact",
    },
    "rebung": {
        "display_name": "Rebung",
        "nutrition": {"calories": 27.0, "protein": 0.6, "fat": 0.3, "carbohydrate": 5.2},
        "match_source": "exact",
    },
    "risoles": {
        "display_name": "Risoles",
        "nutrition": {"calories": 335.0, "protein": 5.3, "fat": 3.5, "carbohydrate": 70.5},
        "match_source": "exact",
    },
    "sayur asem": {
        "display_name": "Sayur Asem",
        "nutrition": {"calories": 29.0, "protein": 0.7, "fat": 0.6, "carbohydrate": 5.0},
        "match_source": "exact",
    },
    "tapai ketan": {
        "display_name": "Tapai Ketan",
        "nutrition": {"calories": 172.0, "protein": 3.0, "fat": 0.5, "carbohydrate": 37.5},
        "match_source": "fuzzy:tapai ketan putih",
    },
    "tekwan": {
        "display_name": "Tekwan",
        "nutrition": {"calories": 53.0, "protein": 1.9, "fat": 0.9, "carbohydrate": 9.4},
        "match_source": "exact",
    },
    "tempe goreng": {
        "display_name": "Tempe Goreng",
        "nutrition": {"calories": 328.0, "protein": 18.4, "fat": 23.2, "carbohydrate": 12.8},
        "match_source": "exact",
    },
    "ubi cilembu": {
        "display_name": "Ubi Cilembu",
        "nutrition": {"calories": 186.0, "protein": 1.9, "fat": 0.2, "carbohydrate": 44.3},
        "match_source": "exact",
    },
    "wingko babat": {
        "display_name": "Wingko Babat",
        "nutrition": {"calories": 355.0, "protein": 3.2, "fat": 15.1, "carbohydrate": 51.4},
        "match_source": "exact",
    },
}

def get_nutrition(label: str) -> Dict[str, Any]:
    """
    Dipakai oleh Streamlit.
    Input label biasanya dari model, contoh: "10. Pempek" / "01. Ayam Betutu"
    Output format cocok buat app_streamlit.py
    """
    key = _normalize(label)
    # display_name tanpa nomor
    display = re.sub(r"^\d+\.\s*", "", label).strip()

    if key in NUTRITION_DB:
        item = NUTRITION_DB[key]
        return {
            "label": label,
            "display_name": item.get("display_name", display),
            "nutrition": item["nutrition"],
            "status": "ok",
            "match_source": item.get("match_source"),
        }

    # kalau tidak ketemu, fallback kosong
    return {
        "label": label,
        "display_name": display,
        "nutrition": {"calories": 0, "protein": 0, "fat": 0, "carbohydrate": 0},
        "status": "not_found",
        "match_source": None,
    }
