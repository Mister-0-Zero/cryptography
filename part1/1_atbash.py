from baseFunctionForCryptography.baseFunction import ALPHABET, normalize_text, output_text

text = normalize_text()

text_chipper = text[::-1]

output_text(text_chipper, False)