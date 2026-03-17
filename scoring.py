def classify_phoneme(score):
    if score >= 80:
        return "Correct"
    elif score < 60:
        return "Error"
    else:
        return "Borderline"


def compute_pcc(correct_consonants, total_consonants):
    if total_consonants == 0:
        return 0
    return (correct_consonants / total_consonants) * 100


def get_severity(pcc):
    if pcc >= 85:
        return "Mild"
    elif pcc >= 65:
        return "Mild-to-Moderate"
    elif pcc >= 50:
        return "Moderate-to-Severe"
    else:
        return "Severe"