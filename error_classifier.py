# ASHA-aligned error-classifier logic
# Based primarily on:
# ASHA Practice Portal: "Selected Phonological Patterns"
# https://www.asha.org/practice-portal/clinical-topics/articulation-and-phonology/selected-phonological-patterns/
#
# Notes:
# - This is an ASHA-aligned rule set, not an official ASHA algorithm.
# - ASHA describes the phonological patterns and examples, but does not publish
#   a Python scoring engine or exact Azure-based cutoffs.
# - This classifier uses your Azure phoneme score + NBestPhonemes to infer likely production.

VOICELESS_TO_VOICED = {
    "p": "b",
    "t": "d",
    "k": "g",
    "f": "v",
    "s": "z",
    "ʃ": "ʒ",
    "tʃ": "dʒ",
    "θ": "ð",
}

VOICED_TO_VOICELESS = {
    "b": "p",
    "d": "t",
    "g": "k",
    "v": "f",
    "z": "s",
    "ʒ": "ʃ",
    "dʒ": "tʃ",
    "ð": "θ",
}

VOWELS = {
    "a", "ɑ", "ɒ", "æ", "ʌ", "ə", "ɛ", "ɜ", "ɪ", "i",
    "o", "ɔ", "u", "ʊ", "e", "ɚ", "ɝ"
}


def is_vowel(phoneme):
    return phoneme in VOWELS


def get_likely_spoken_sound(raw_phoneme, target_phoneme, score):
    """
    Use Azure NBestPhonemes to estimate the likely spoken phoneme.
    Returns:
        - actual likely phoneme string
        - 'omitted/deleted'
        - 'unknown'
    """
    if raw_phoneme is None:
        return "omitted/deleted"

    pronunciation_data = raw_phoneme.get("PronunciationAssessment", {})
    nbest = pronunciation_data.get("NBestPhonemes", [])

    if len(nbest) == 0:
        return "unknown"

    # If Azure gives alternatives, choose the first candidate that differs
    # from the expected phoneme.
    for item in nbest:
        candidate = item["Phoneme"]

        if candidate != target_phoneme:
            # Heuristic: very low score + vowel-like alternative may reflect
            # effective omission/poor realization in your pipeline.
            if score is not None and score < 40 and is_vowel(candidate):
                return "omitted/deleted"
            return candidate

    return nbest[0]["Phoneme"]


def find_single_phoneme_score(phonemes, target_phoneme):
    """
    Find one expected phoneme in Azure's returned phoneme list.
    """
    for phoneme in phonemes:
        expected_phoneme = phoneme["Phoneme"]
        phoneme_score = phoneme["PronunciationAssessment"]["AccuracyScore"]

        if expected_phoneme == target_phoneme:
            return phoneme_score, phoneme

    return None, None


def find_cluster_scores(phonemes, target_cluster):
    """
    Find each expected phoneme inside a target cluster.
    Example target_cluster: ["s", "p"] for 'sp'
    """
    found_scores = []
    used_indexes = []

    for target_phoneme in target_cluster:
        found = False

        for i, phoneme in enumerate(phonemes):
            if i in used_indexes:
                continue

            expected_phoneme = phoneme["Phoneme"]
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


def classify_assimilation(expected_phoneme, likely_spoken):
    """
    ASHA explicitly lists two assimilation patterns on the selected patterns page:
    - Velar assimilation: non-velar -> velar because of nearby velar
    - Nasal assimilation: non-nasal -> nasal because of nearby nasal

    Because assimilation depends on neighboring sounds in the word,
    this helper only checks the phoneme-type relationship.
    Full confirmation is done in classify_error_label using word context.
    """
    velars = {"k", "g", "ŋ"}
    nasals = {"m", "n", "ŋ"}

    if expected_phoneme not in velars and likely_spoken in velars:
        return "Velar Assimilation"

    if expected_phoneme not in nasals and likely_spoken in nasals:
        return "Nasal Assimilation"

    return None


def classify_error_label(word_item, expected_phoneme, likely_spoken, score):
    """
    Returns an ASHA-aligned phonological pattern label where possible.

    Expected fields in word_item:
        - position: 'initial', 'medial', 'final', 'cluster initial', etc.
        - word: target word
    Optional fields if you want stronger assimilation logic:
        - word_phonemes: full expected phoneme list for the word
    """
    position = word_item["position"]
    expected = expected_phoneme
    likely = likely_spoken

    # -----------------------------
    # 1. Deletion / syllable structure processes
    # -----------------------------
    if likely == "omitted/deleted":
        if "cluster" in position:
            # ASHA: cluster reduction = simplifying a consonant cluster
            return "Cluster Reduction"

        if "final" in position:
            # ASHA explicitly lists final-consonant deletion
            return "Final Consonant Deletion"

        if "weak syllable" in position or "syllable" in position:
            # ASHA explicitly lists weak-syllable deletion
            return "Weak-Syllable Deletion"

        if "initial" in position:
            # This is clinically useful, but not one of the named patterns
            # on the ASHA selected patterns page.
            return "Initial Consonant Deletion"

        if "medial" in position:
            return "Medial Consonant Deletion"

        return "Deletion"

    # -----------------------------
    # 2. Assimilation / consonant harmony
    # -----------------------------
    # ASHA selected patterns explicitly include:
    # - Velar assimilation
    # - Nasal assimilation
    #
    # Best practice: only use this when the target word actually contains
    # a nearby triggering sound. If word_item contains word_phonemes,
    # use them as supporting context.
    assimilation_label = classify_assimilation(expected, likely)
    if assimilation_label is not None:
        word_phonemes = set(word_item.get("word_phonemes", []))

        if assimilation_label == "Velar Assimilation" and len(word_phonemes & {"k", "g", "ŋ"}) > 0:
            return f"Velar Assimilation ({position})"

        if assimilation_label == "Nasal Assimilation" and len(word_phonemes & {"m", "n", "ŋ"}) > 0:
            return f"Nasal Assimilation ({position})"

    # -----------------------------
    # 3. ASHA substitution patterns
    # -----------------------------

    # ASHA: Fronting = velar replaced by a front/alveolar sound
    if expected in {"k", "g"} and likely in {"t", "d"}:
        return f"Fronting ({position})"

    # ASHA: Stopping = fricative and/or affricate replaced with stop
    if expected in {"f", "v", "s", "z", "ʃ", "θ", "ð", "tʃ", "dʒ"} and likely in {"p", "b", "t", "d", "k", "g"}:
        return f"Stopping ({position})"

    # ASHA: Gliding = liquid replaced by glide
    if expected in {"l", "r", "ɹ"} and likely in {"w", "j"}:
        return f"Gliding ({position})"

    # ASHA: Deaffrication = affricate replaced by fricative
    if expected in {"tʃ", "dʒ"} and likely in {"ʃ", "ʒ", "s", "z", "f", "v", "θ", "ð"}:
        return f"Deaffrication ({position})"

    # -----------------------------
    # 4. Optional custom labels
    # -----------------------------
    # The following are useful in your thesis, but they are not the main named
    # processes on ASHA's "Selected Phonological Patterns" page. Keep them if
    # you want broader classification, but label them as custom/extension logic.

    if expected in {"t", "d"} and likely in {"k", "g"}:
        return f"Backing ({position})"

    if expected in VOICELESS_TO_VOICED and VOICELESS_TO_VOICED[expected] == likely:
        return f"Voicing ({position})"

    if expected in VOICED_TO_VOICELESS and VOICED_TO_VOICELESS[expected] == likely:
        return f"Devoicing ({position})"

    # -----------------------------
    # 5. Fallback
    # -----------------------------
    if score is not None and score < 60:
        return f"Substitution / Other ({position})"

    return "No Specific Error"

