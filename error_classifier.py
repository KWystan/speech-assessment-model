VOICELESS_TO_VOICED = {
    "p": "b",
    "t": "d",
    "k": "g",
    "f": "v",
    "s": "z",
    "ʃ": "ʒ",
    "tʃ": "dʒ",
    "θ": "ð"
}

VOICED_TO_VOICELESS = {
    "b": "p",
    "d": "t",
    "g": "k",
    "v": "f",
    "z": "s",
    "ʒ": "ʃ",
    "dʒ": "tʃ",
    "ð": "θ"
}

VOWELS = {
    "a", "ɑ", "ɒ", "æ", "ʌ", "ə", "ɛ", "ɜ", "ɪ", "i", "o", "ɔ", "u", "ʊ", "e", "ɚ", "ɝ"
}


def normalize_phoneme(phoneme):
    phoneme_map = {
        "ɡ": "g",
        "ɹ": "r",
        "r": "r",
        "ʃ": "ʃ",
        "ʒ": "ʒ",
        "tʃ": "tʃ",
        "dʒ": "dʒ",
        "θ": "θ",
        "ð": "ð",
        "j": "j",
        "w": "w",
        "ŋ": "ŋ",
        "k": "k",
        "g": "g",
        "p": "p",
        "b": "b",
        "t": "t",
        "d": "d",
        "m": "m",
        "n": "n",
        "f": "f",
        "v": "v",
        "s": "s",
        "z": "z",
        "h": "h",
        "l": "l"
    }
    return phoneme_map.get(phoneme, phoneme)


def is_vowel(phoneme):
    return normalize_phoneme(phoneme) in VOWELS


def get_likely_spoken_sound(raw_phoneme, target_phoneme, score):
    target_phoneme = normalize_phoneme(target_phoneme)

    if raw_phoneme is None:
        return "omitted/deleted"

    pronunciation_data = raw_phoneme.get("PronunciationAssessment", {})
    nbest = pronunciation_data.get("NBestPhonemes", [])

    if len(nbest) == 0:
        return "unknown"

    for item in nbest:
        candidate = normalize_phoneme(item["Phoneme"])

        if candidate != target_phoneme:
            if score is not None and score < 40 and is_vowel(candidate):
                return "omitted/deleted"
            return candidate

    return normalize_phoneme(nbest[0]["Phoneme"])


def find_single_phoneme_score(phonemes, target_phoneme):
    target_phoneme = normalize_phoneme(target_phoneme)

    for phoneme in phonemes:
        expected_phoneme = normalize_phoneme(phoneme["Phoneme"])
        phoneme_score = phoneme["PronunciationAssessment"]["AccuracyScore"]

        if expected_phoneme == target_phoneme:
            return phoneme_score, phoneme

    return None, None


def find_cluster_scores(phonemes, target_cluster):
    found_scores = []
    used_indexes = []

    normalized_targets = []
    for item in target_cluster:
        normalized_targets.append(normalize_phoneme(item))

    for target_phoneme in normalized_targets:
        found = False

        for i, phoneme in enumerate(phonemes):
            if i in used_indexes:
                continue

            expected_phoneme = normalize_phoneme(phoneme["Phoneme"])
            phoneme_score = phoneme["PronunciationAssessment"]["AccuracyScore"]

            if expected_phoneme == target_phoneme:
                found_scores.append({
                    "target": target_phoneme,
                    "score": phoneme_score,
                    "raw_phoneme": phoneme
                })
                used_indexes.append(i)
                found = True
                break

        if not found:
            found_scores.append({
                "target": target_phoneme,
                "score": None,
                "raw_phoneme": None
            })

    return found_scores


def classify_error_label(word_item, expected_phoneme, likely_spoken, score):
    position = word_item["position"]
    expected = normalize_phoneme(expected_phoneme)

    if likely_spoken == "omitted/deleted":
        likely = "omitted/deleted"
    else:
        likely = normalize_phoneme(likely_spoken)

    if likely == "omitted/deleted":
        if "cluster" in position:
            return "Cluster Reduction"
        if "initial" in position:
            return "Initial Consonant Deletion"
        if "final" in position:
            return "Final Consonant Deletion"
        if "medial" in position:
            return "Medial Consonant Deletion"
        return "Deletion"

    if expected in ["k", "g"] and likely in ["t", "d"]:
        return f"Fronting ({position})"

    if expected in ["t", "d"] and likely in ["k", "g"]:
        return f"Backing ({position})"

    if expected in ["f", "s", "z", "ʃ", "v", "θ", "ð", "ʒ"] and likely in ["p", "b", "t", "d", "k", "g"]:
        return f"Stopping ({position})"

    if expected in ["l", "r"] and likely in ["w", "j"]:
        return f"Gliding ({position})"

    if expected in ["tʃ", "dʒ"] and likely in ["ʃ", "s", "ʒ", "z"]:
        return f"Deaffrication ({position})"

    if expected == "ʃ" and likely == "s":
        return f"Palatal Fronting ({position})"

    if expected in ["p", "b", "m", "n"] and likely in ["f", "v"]:
        return f"Frication ({position})"

    if expected in ["w", "j"] and likely in ["l", "r"]:
        return f"Liquidization ({position})"

    if expected in VOICELESS_TO_VOICED and VOICELESS_TO_VOICED[expected] == likely:
        return f"Voicing ({position})"

    if expected in VOICED_TO_VOICELESS and VOICED_TO_VOICELESS[expected] == likely:
        return f"Devoicing ({position})"

    if score is not None and score < 60:
        return f"Substitution / Other ({position})"

    return "No Specific Error"