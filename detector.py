
import re
from lingua import Language, LanguageDetectorBuilder


# =====================================================
# SUPPORTED LANGUAGES
# =====================================================

languages = [
    Language.ENGLISH,
    Language.TAMIL,
    Language.FRENCH,
    Language.SPANISH,
    Language.GERMAN,
    Language.HINDI,
    Language.TELUGU,
    Language.BENGALI,
    Language.GUJARATI,
    Language.MARATHI,
    Language.PUNJABI,
    Language.URDU,
    Language.CHINESE,
    Language.JAPANESE,
    Language.KOREAN,
    Language.ARABIC,
    Language.PORTUGUESE,
    Language.ITALIAN,
    Language.RUSSIAN,
    Language.TSWANA
]


# =====================================================
# INITIALIZE LANGUAGE DETECTOR
# =====================================================

detector = (
    LanguageDetectorBuilder
    .from_languages(*languages)
    .build()
)


# =====================================================
# TANGLISH DETECTION
# =====================================================

TANGLISH_WORDS = {
    "vanakkam", "eppadi", "epdi",
    "iruka", "irukeenga", "irukinga",
    "irukiya", "irukkiya",
    "naan", "nalla", "iruken",
    "saptiya", "sapten", "saaptiya",
    "enna", "ennada", "ennanga",
    "ungal", "ungalukku",
    "romba", "seri", "sari",
    "illa", "illai", "aama",
    "machi", "poda", "dei",
    "sollu", "sollunga", "nanri",
    "nandri", "thambi", "akka",
    "anna", "amma", "appa",
    "veetla", "enga", "inga",
    "anga", "pogalama", "varuven",
    "pannunga", "panren", "pannuren",
    "theriyum", "theriyala",
    "konjam", "nalla", "irukku"
}


# =====================================================
# HELPER: RESULT FORMAT
# =====================================================

def create_result(language, code, confidence, script, method):

    return {
        "language": language,
        "code": code,
        "confidence": round(confidence, 2),
        "script": script,
        "method": method
    }


# =====================================================
# MAIN LANGUAGE DETECTION
# =====================================================

def detect_language(text):

    if not isinstance(text, str) or not text.strip():

        return create_result(
            "Unknown",
            "N/A",
            0.0,
            "Unknown",
            "No input"
        )

    text = text.strip()

    # Extract alphabetic words
    words = set(
        re.findall(r"[a-zA-Z]+", text.lower())
    )

    # Identify common Tamil transliterations
    tamil_matches = words.intersection(TANGLISH_WORDS)

    # Require at least one distinctive Tamil word
    # or multiple Tamil vocabulary matches.
    if (
        len(tamil_matches) >= 2
        or "vanakkam" in tamil_matches
    ):

        return create_result(
            "Tamil (Tanglish)",
            "ta-Latn",
            0.0,
            "Latin (Transliterated)",
            "Tamil vocabulary heuristic"
        )

    # =================================================
    # LINGUA DETECTION
    # =================================================

    detected_language = detector.detect_language_of(text)

    if detected_language is None:

        return create_result(
            "Unknown",
            "N/A",
            0.0,
            "Unknown",
            "Lingua NLP"
        )

    confidence_values = (
        detector.compute_language_confidence_values(text)
    )

    confidence = next(
        (
            item.value
            for item in confidence_values
            if item.language == detected_language
        ),
        0.0
    )

    language_name = detected_language.name.title()

    language_code = (
        detected_language.iso_code_639_1.name.lower()
    )

    return create_result(
        language_name,
        language_code,
        confidence * 100,
        "Native / Detected Script",
        "Lingua NLP"
    )
