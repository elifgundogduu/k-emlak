import urllib.parse

def clean_slug(text: str) -> str:
    tr_map = str.maketrans("çğışöüÇĞİŞÖÜ", "cgisouCGISOU")
    clean = text.lower().translate(tr_map).strip()
    for ch in ["(", ")", "/", ".", ","]:
        clean = clean.replace(ch, "")
    return clean.replace(" ", "-")

def generate_portal_url(portal: str, district: str, neighborhood: str, listing_type: str) -> str:
    dist_slug = clean_slug(district)
    neigh_slug = clean_slug(neighborhood)
    action_jet = "satilik" if listing_type == "Satılık" else "kiralik"
    action_hepsi = "satilik" if listing_type == "Satılık" else "kiralik"

    if portal.lower() == "hepsiemlak":
        # Hepsiemlak %100 Çalışan Mahalle/İlçe Formatı
        return f"https://www.hepsiemlak.com/{dist_slug}-{neigh_slug}-{action_hepsi}"
    else:
        # Emlakjet %100 Çalışan Mahalle/İlçe Formatı
        return f"https://www.emlakjet.com/{action_jet}-daire/istanbul-{dist_slug}-{neigh_slug}-mahallesi/"
