import re
from typing import List, Dict, Any

class HinglishConverter:
    """
    Intelligent Hindi / Devanagari & Urdu to Natural Conversational Hinglish (Roman Script) Converter.
    Includes slang, vocabulary expansion, and automated phonetic spell-correction
    specifically solving issues like 'plwn' -> 'Pehlwan', 'bdmi' -> 'Badmashi', 'rod' -> 'Rude'.
    """

    # Direct phonetic dictionary for common Hindi/Urdu conversational words & slang
    COMMON_WORDS = {
        # Indian Slang & Terms
        "पहलवान": "Pehlwan", "पहलवानों": "Pehlwano", "कुश्ती": "Kushti", "दंगल": "Dangal",
        "बदमाशी": "Badmashi", "बदमाश": "Badmash", "गुंडागर्दी": "Gundagardi", "लफड़ा": "Lafda",
        "कलेश": "Kalesh", "सिस्टम": "System", "रूड": "Rude", "एटीट्यूड": "Attitude",
        "दोस्त": "Dost", "दोस्तों": "Dosto", "यार": "Yaar", "भाई": "Bhai", "ब्रो": "Bro",
        "सीन": "Scene", "बावा": "Bawa", "छपरी": "Chhapri", "स्वैग": "Swag", "देसी": "Desi",
        "डायलॉग": "Dialogue", "पुलिस": "Police", "गाड़ी": "Gaadi", "लड़ाई": "Ladai",
        "झगड़ा": "Jhagda", "खतरनाक": "Khatarnak", "मशहूर": "Mashhoor", "दुश्मनी": "Dushmani",
        "बिग": "Bigg", "बॉस": "Boss", "घर": "Ghar", "कैमरा": "Camera", "कैमरे": "Camere",
        "करोड़": "Crore", "बजट": "Budget", "कंटेस्टेंट": "Contestant", "कंटेस्टेंट्स": "Contestants",
        "सीक्रेट": "Secret", "सच": "Sach", "झूठ": "Jhooth", "शो": "Show", "सीजन": "Season",
        "टीवी": "TV", "फाइट": "Fight", "वीडियो": "Video", "लोग": "Log", "बात": "Baat",

        # Urdu script words (Whisper Urdu tokens with exact phonetic Hinglish mapping)
        "پہلوان": "Pehlwan", "پہلوانوں": "Pehlwano", "پہلوانی": "Pehlwani", "کشتی": "Kushti",
        "بدمعاشی": "Badmashi", "بدمعاش": "Badmash", "غنڈہ": "Gunda", "روڈ": "Rude",
        "ایٹیٹیوڈ": "Attitude", "دوست": "Dost", "دوستوں": "Dosto", "یار": "Yaar",
        "بھائی": "Bhai", "سین": "Scene", "پولیس": "Police", "گاڑی": "Gaadi",
        "لڑائی": "Ladai", "جھگڑا": "Jhagda", "خطرناک": "Khatarnak", "مشہور": "Mashhoor",
        "دوریمون": "Doraemon", "دوریمونوں": "Doraemon", "نوبیتا": "Nobita",
        "فانیلی": "Finally", "فائنلی": "Finally", "انڈیا": "India", "آچوکی": "Aa chuki",
        "آچکے": "Aa chuke", "آیا": "Aaya", "گئے": "Gaye", "ہے": "hai", "ہیں": "hain",
        "اور": "aur", "اسبار": "is baar", "صرف": "sirf", "نام": "naam", "بل": "balki",
        "کی": "ki", "کا": "ka", "کے": "ke", "پورا": "poora", "اپسوڑ": "episode",
        "دیلی": "Delhi", "ٹرافک": "traffic", "گلگپے": "golgappe", "چاہی": "chaat",
        "لستی": "lassi", "انڈیاں": "Indian", "سکول": "school", "لائی": "life",
        "اس": "is", "میں": "mein", "ہم": "hum", "بہس": "bahut", "بہت": "bahut",
        "سالی": "saari", "ساری": "saari", "چھوٹی": "chhoti", "بڑی": "badi",
        "دیٹیل": "details", "لیکن": "lekin", "سب": "sab", "سے": "se",
        "انٹرسٹنگ": "interesting", "بات": "baat", "تو": "toh", "یہ": "yeh",
        "کہ": "ki", "نہیں": "nahi", "کیا": "kya", "کیوں": "kyun", "کیسے": "kaise"
    }

    # Spelling corrections for common mistranscribed or abjad-shortened tokens
    SPELL_CORRECTIONS = {
        "plwn": "Pehlwan",
        "plwno": "Pehlwano",
        "plwnon": "Pehlwano",
        "bdmi": "Badmashi",
        "bdmasi": "Badmashi",
        "bdmashi": "Badmashi",
        "rod": "Rude",
        "rood": "Rude",
        "rud": "Rude",
        "atitud": "Attitude",
        "atitood": "Attitude",
        "doremona": "Doraemon",
        "doramon": "Doraemon",
        "nobitaa": "Nobita",
        "imdiya": "India",
        "indya": "India",
        "imdiyA": "India",
        "gunda": "Gunda",
        "gundagardi": "Gundagardi",
        "kalesh": "Kalesh",
        "lafda": "Lafda",
        "bawa": "Bawa",
        "bhaiya": "Bhaiya",
        "dostan": "Dosto",
        "doston": "Dosto",
        "dostom": "Dosto"
    }

    VOWELS = {
        'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo',
        'ऋ': 'ri', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au', 'अं': 'an', 'अः': 'ah'
    }

    MATRAS = {
        'ा': 'aa', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo', 'ृ': 'ri',
        'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', 'ं': 'n', 'ँ': 'n', 'ः': 'h',
        'ॉ': 'o', 'ॅ': 'e', '्': ''
    }

    CONSONANTS = {
        'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
        'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'ny',
        'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
        'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
        'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
        'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh', 'ष': 'sh', 'स': 's', 'ह': 'h',
        'क्ष': 'ksh', 'त्र': 'tra', 'ज्ञ': 'gya', 'क़': 'q', 'ख़': 'kh', 'ग़': 'gh', 'ज़': 'z', 'फ़': 'f'
    }

    URDU_MAP = {
        'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ٹ': 't', 'ث': 's',
        'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ڈ': 'd', 'ذ': 'z',
        'ر': 'r', 'ڑ': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'z',
        'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'q', 'ک': 'k', 'گ': 'g',
        'ل': 'l', 'م': 'm', 'ن': 'n', 'ں': 'n', 'و': 'o', 'ہ': 'h', 'ھ': 'h', 'ء': '',
        'ی': 'i', 'ے': 'e'
    }

    @classmethod
    def clean_spelling(cls, word: str) -> str:
        """Applies contextual spell correction for common Hindi/English short-form mistakes"""
        lower = word.lower().strip()
        clean = re.sub(r'[^\w]', '', lower)
        if clean in cls.SPELL_CORRECTIONS:
            corrected = cls.SPELL_CORRECTIONS[clean]
            # preserve casing if uppercase
            if word.isupper():
                return corrected.upper()
            return corrected
        return word

    @classmethod
    def transliterate_devanagari_word(cls, word: str) -> str:
        """Converts a single Devanagari Hindi word to clean Roman Hinglish"""
        if word in cls.COMMON_WORDS:
            return cls.COMMON_WORDS[word]

        clean = re.sub(r'[^\u0900-\u097F]', '', word)
        if not clean:
            return cls.clean_spelling(word)

        res = []
        i = 0
        n = len(clean)
        while i < n:
            ch = clean[i]
            if i + 1 < n and clean[i:i+2] in cls.CONSONANTS:
                res.append(cls.CONSONANTS[clean[i:i+2]])
                i += 2
                continue

            if ch in cls.VOWELS:
                res.append(cls.VOWELS[ch])
                i += 1
            elif ch in cls.CONSONANTS:
                base = cls.CONSONANTS[ch]
                if i + 1 < n:
                    nxt = clean[i+1]
                    if nxt in cls.MATRAS:
                        res.append(base + cls.MATRAS[nxt])
                        i += 2
                    elif nxt == '्':
                        res.append(base)
                        i += 2
                    elif nxt in cls.CONSONANTS:
                        res.append(base + 'a')
                        i += 1
                    else:
                        res.append(base)
                        i += 1
                else:
                    res.append(base)
                    i += 1
            elif ch in cls.MATRAS:
                res.append(cls.MATRAS[ch])
                i += 1
            else:
                res.append(ch)
                i += 1

        out = "".join(res)
        out = re.sub(r'a+', 'a', out)
        if out.endswith('aa'):
            out = out[:-1]
        
        return cls.clean_spelling(out)

    @classmethod
    def transliterate_urdu_word(cls, word: str) -> str:
        """Converts Urdu script word to Roman Hinglish with phonetic correction"""
        if word in cls.COMMON_WORDS:
            return cls.COMMON_WORDS[word]

        clean = re.sub(r'[^\u0600-\u06FF]', '', word)
        if not clean:
            return cls.clean_spelling(word)

        res = []
        for ch in clean:
            res.append(cls.URDU_MAP.get(ch, ch))
        out = "".join(res)
        out = out.replace("oo", "u").replace("ee", "i")
        return cls.clean_spelling(out)

    @classmethod
    def to_hinglish(cls, text: str) -> str:
        """
        Converts any text containing Hindi or Urdu characters into clean Roman Hinglish.
        Also corrects mistranscribed words like 'plwn' -> 'Pehlwan', 'bdmi' -> 'Badmashi', 'rod' -> 'Rude'.
        """
        if not text:
            return ""

        words = text.split()
        converted = []
        for w in words:
            p_prefix = re.match(r'^[^\w\u0900-\u097F\u0600-\u06FF]+', w)
            p_suffix = re.search(r'[^\w\u0900-\u097F\u0600-\u06FF]+$', w)
            prefix = p_prefix.group(0) if p_prefix else ""
            suffix = p_suffix.group(0) if p_suffix else ""
            
            clean_word = w
            if prefix:
                clean_word = clean_word[len(prefix):]
            if suffix:
                clean_word = clean_word[:-len(suffix)]

            # Check if Devanagari
            if re.search(r'[\u0900-\u097F]', clean_word):
                trans = cls.transliterate_devanagari_word(clean_word)
            # Check if Urdu/Arabic
            elif re.search(r'[\u0600-\u06FF]', clean_word):
                trans = cls.transliterate_urdu_word(clean_word)
            else:
                # English or Roman: apply spell correction
                trans = cls.clean_spelling(clean_word)

            converted.append(f"{prefix}{trans}{suffix}")

        return " ".join(converted)

    @classmethod
    def convert_clip_words(cls, words_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Converts an entire clip's word tokens to Hinglish while keeping original timestamps intact"""
        new_words = []
        for w in words_list:
            cw = dict(w)
            cw["original_word"] = w.get("word", "")
            cw["word"] = cls.to_hinglish(w.get("word", ""))
            new_words.append(cw)
        return new_words
