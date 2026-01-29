import re
import hashlib

# Common password dictionary

COMMON_PASSWORDS = [
    "password", "123456", "123456789", "qwerty",
    "abc123", "letmein", "welcome", "admin"
]

COMMON_HASHES = {
    hashlib.sha256(p.encode()).hexdigest()
    for p in COMMON_PASSWORDS
}

# Helper checks

def has_repeated_chars(password):
    return bool(re.search(r"(.)\1{2,}", password))


def has_sequential_pattern(password):
    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "qwertyuiopasdfghjklzxcvbnm"
    ]
    lower = password.lower()
    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in lower:
                return True
    return False


def is_dictionary_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed in COMMON_HASHES


# Strength evaluation

def check_password_strength(password):
    score = 0
    feedback = []

    # Length

    length = len(password)
    if length >= 16:
        score += 30
    elif length >= 12:
        score += 20
    elif length >= 8:
        score += 10
        feedback.append("Increase password length.")
    else:
        feedback.append("Password is too short.")

    # Character variety

    categories = 0
    if re.search(r"[a-z]", password):
        categories += 1
    if re.search(r"[A-Z]", password):
        categories += 1
    if re.search(r"\d", password):
        categories += 1
    if re.search(r"[^\w\s]", password):
        categories += 1

    score += categories * 7.5
    if categories < 4:
        feedback.append("Use a mix of upper, lower, digits, and symbols.")

    # Pattern checks

    if has_repeated_chars(password):
        feedback.append("Avoid repeated characters.")
    else:
        score += 10

    if has_sequential_pattern(password):
        feedback.append("Avoid sequential or keyboard patterns.")
    else:
        score += 15

    # Dictionary check

    if is_dictionary_password(password):
        feedback.append("Password found in common password list.")
    else:
        score += 15

    # Final rating

    if score >= 80:
        rating = "Strong"
    elif score >= 60:
        rating = "Moderate"
    else:
        rating = "Weak"

    return {
        "score": int(score),
        "rating": rating,
        "feedback": feedback
    }



# usage

if __name__ == "__main__":
    pwd = input("Enter password: ")
    result = check_password_strength(pwd)

    print(f"\nStrength: {result['rating']}")
    print(f"Score: {result['score']}/100")
    if result["feedback"]:
        print("Issues:")
        for item in result["feedback"]:
            print(f"- {item}")
