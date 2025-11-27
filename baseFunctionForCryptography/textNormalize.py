def normalize_text(text: str = "Не все те повара, что с длинными ножами ходят.") -> str:
    norm_text = text.replace(" ", "").lower().replace(",", "зпт").replace(".", "тчк")
    return norm_text