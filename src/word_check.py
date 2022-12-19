with open("dict/english.txt", mode="r", encoding="utf-8") as f: eng_arr = f.read().splitlines()
with open("dict/farsi.txt", mode="r", encoding="utf-8") as f: far_arr = f.read().splitlines()

keyboard_map_far = {
    "ا": "h",
    "ب": "f",
    "پ": "\\",
    "ت": "j",
    "ث": "e",
    "ج": "[",
    "چ": "]",
    "ح": "p",
    "خ": "o",
    "د": "n",
    "ذ": "b",
    "ر": "v",
    "ز": "c", ###
    "ژ": "C", ###
    "س": "s",
    "ش": "a",
    "ص": "w",
    "ض": "q",
    "ط": "x",
    "ظ": "z",
    "ع": "u",
    "غ": "y",
    "ف": "t",
    "ق": "r",
    "ک": ";",
    "گ": "'",
    "ل": "g",
    "م": "l",
    "ن": "k",
    "و": ",",
    "ه": "i",
    "ی": "d",
}
keyboard_map_eng = {
    "h": "ا",
    "f": "ب",
    "\\": "پ",
    "j": "ت",
    "e": "ث",
    "[": "ج",
    "]": "چ",
    "p": "ح",
    "o": "خ",
    "n": "د",
    "b": "ذ",
    "v": "ر",
    "c": "ز",
    "C": "ژ",
    "s": "س",
    "a": "ش",
    "w": "ص",
    "q": "ض",
    "x": "ط",
    "z": "ظ",
    "u": "ع",
    "y": "غ",
    "t": "ف",
    "r": "ق",
    ";": "ک",
    "'": "گ",
    "g": "ل",
    "l": "م",
    "k": "ن",
    ",": "و",
    "i": "ه",
    "d": "ی",
}

def lookup_word(word_in_memory, lang):

    word_is_en = word_in_memory["word-en"] in eng_arr
    if lang == "en" and word_is_en: return [True, word_in_memory[f"word-{lang}"]]

    word_is_fa = word_in_memory["word-fa"] in far_arr
    if lang == "fa" and word_is_fa: return [True, word_in_memory[f"word-{lang}"]]
    
    if not (word_is_en | word_is_fa): return [True, word_in_memory[f"word-{lang}"]]

    if lang == "en": return [False, word_in_memory["word-fa"]]
    elif lang == "fa": return [False, word_in_memory["word-en"]]

def en_to_fa(original_word):
    changed_word = ""

    for letter in original_word: 
        try: changed_word += keyboard_map_eng[letter]
        except: changed_word += ""
    
    return changed_word