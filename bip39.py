"""BIP39 mnemonic generate/validate (standard library only)."""
import hashlib
import secrets
from pathlib import Path

WORDS = [w.strip() for w in (Path(__file__).parent / "wordlist" / "english.txt").read_text().split() if w.strip()]
assert len(WORDS) == 2048, "wordlist must have 2048 words"
INDEX = {w: i for i, w in enumerate(WORDS)}


def _checksum_bits(entropy: bytes) -> str:
    cs_len = len(entropy) * 8 // 32
    return f"{hashlib.sha256(entropy).digest()[0]:08b}"[:cs_len]


def generate(n_words: int = 12) -> list[str]:
    if n_words not in (12, 15, 18, 21, 24):
        raise ValueError("n_words must be 12, 15, 18, 21 or 24")
    entropy = secrets.token_bytes(n_words * 11 * 32 // 33 // 8)
    bits = "".join(f"{b:08b}" for b in entropy) + _checksum_bits(entropy)
    return [WORDS[int(bits[i:i + 11], 2)] for i in range(0, len(bits), 11)]


def validate(phrase: str) -> tuple[bool, str]:
    ws = phrase.lower().split()
    if len(ws) not in (12, 15, 18, 21, 24):
        return False, f"{len(ws)} words; need 12, 15, 18, 21 or 24"
    bad = [w for w in ws if w not in INDEX]
    if bad:
        return False, "not in wordlist: " + ", ".join(bad[:3])
    bits = "".join(f"{INDEX[w]:011b}" for w in ws)
    el = len(ws) * 11 * 32 // 33
    entropy = bytes(int(bits[i:i + 8], 2) for i in range(0, el, 8))
    if _checksum_bits(entropy) != bits[el:]:
        return False, "checksum mismatch"
    return True, "valid BIP39 phrase"


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    p = generate(n)
    assert validate(" ".join(p))[0]
    print(" ".join(p))
