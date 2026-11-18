
from detector import detect_language

samples = [
    "Hello, how are you?",
    "Vanakkam! Eppadi irukeenga?",

    # Tamil
    "\u0ba8\u0bbe\u0ba9\u0bcd \u0ba8\u0ba9\u0bcd\u0bb1\u0bbe\u0b95 \u0b87\u0bb0\u0bc1\u0b95\u0bcd\u0b95\u0bbf\u0bb1\u0bc7\u0ba9\u0bcd.",

    # Hindi
    "\u0928\u092e\u0938\u094d\u0924\u0947, \u0906\u092a \u0915\u0948\u0938\u0947 \u0939\u0948\u0902?",

    # Telugu
    "\u0c2e\u0c40\u0c30\u0c41 \u0c0e\u0c32\u0c3e \u0c09\u0c28\u0c4d\u0c28\u0c3e\u0c30\u0c41?",

    "Bonjour, comment allez-vous?",
    "Hola, como estas?",
    "Guten Morgen!"
]

print("=" * 50)
print("       POLYGLOT AI - LANGUAGE TEST")
print("=" * 50)

for index, text in enumerate(samples, start=1):
    result = detect_language(text)

    print(f"\nTest {index}")
    print("Input:", text)
    print("Language:", result["language"])
    print("Code:", result["code"])
    print("Confidence:", result["confidence"], "%")
    print("Script:", result["script"])
    print("Method:", result["method"])
    print("-" * 50)
