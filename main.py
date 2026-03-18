from word_bank import get_word_bank
from scoring import classify_phoneme
from azure_assessment import assess_word
from error_classifier import (
    find_single_phoneme_score,
    find_cluster_scores,
    get_likely_spoken_sound,
    classify_error_label,
)


def process_single_target(item, phonemes, results):
    target_word = item["word"]
    target_phoneme = item["target_phoneme"]

    score, matched_phoneme = find_single_phoneme_score(phonemes, target_phoneme)

    if score is None:
        likely_sound = "omitted/deleted"
        error_label = classify_error_label(item, target_phoneme, likely_sound, None)

        results.append({
            "word": target_word,
            "expected": target_phoneme,
            "status": "Error",
            "likely": likely_sound,
            "error": error_label
        })

        print(f"{target_word} - Error")
        return

    classification = classify_phoneme(score)

    if classification != "Error":
        results.append({
            "word": target_word,
            "expected": target_phoneme,
            "status": "Correct",
            "likely": None,
            "error": None
        })

        print(f"{target_word} - Correct")
        return

    likely_sound = get_likely_spoken_sound(matched_phoneme, target_phoneme, score)
    error_label = classify_error_label(item, target_phoneme, likely_sound, score)

    results.append({
        "word": target_word,
        "expected": target_phoneme,
        "status": "Error",
        "likely": likely_sound,
        "error": error_label
    })

    print(f"{target_word} - Error")


def process_cluster_target(item, phonemes, results):
    target_word = item["word"]
    cluster_results = find_cluster_scores(phonemes, item["target_phoneme"])

    for cluster_item in cluster_results:
        target_phoneme = cluster_item["target"]
        score = cluster_item["score"]
        raw_phoneme = cluster_item["raw_phoneme"]

        if score is None:
            likely_sound = "omitted/deleted"
            error_label = classify_error_label(item, target_phoneme, likely_sound, None)

            results.append({
                "word": target_word,
                "expected": target_phoneme,
                "status": "Error",
                "likely": likely_sound,
                "error": error_label
            })

            print(f"{target_word} - Error")
            continue

        classification = classify_phoneme(score)

        if classification != "Error":
            results.append({
                "word": target_word,
                "expected": target_phoneme,
                "status": "Correct",
                "likely": None,
                "error": None
            })

            print(f"{target_word} - Correct")
            continue

        likely_sound = get_likely_spoken_sound(raw_phoneme, target_phoneme, score)
        error_label = classify_error_label(item, target_phoneme, likely_sound, score)

        results.append({
            "word": target_word,
            "expected": target_phoneme,
            "status": "Error",
            "likely": likely_sound,
            "error": error_label
        })

        print(f"{target_word} - Error")


def select_assessed_word(words, target_word):
    normalized_target = target_word.lower().strip(" .?!,")

    for word in words:
        spoken_word = word.get("Word", "").lower().strip(" .?!,")
        if spoken_word == normalized_target and "Phonemes" in word:
            return word

    for word in words:
        if "Phonemes" in word:
            return word

    return None


def main():
    child_name = input("Enter child name: ")
    child_age = int(input("Enter child age: "))

    word_bank = get_word_bank(child_age)

    if not word_bank:
        print("Invalid age. Supported ages are 4 to 8 only.")
        return

    start = input("Start assessment? (y/n): ").lower()
    if start != "y":
        print("Assessment cancelled.")
        return

    results = []

    print("\nAssessment started...\n")

    for item in word_bank:
        target_word = item["word"]
        target_phoneme = item["target_phoneme"]

        try:
            result = assess_word(target_word)
        except RuntimeError as e:
            print("\nSTOPPED:", e)
            print("Assessment terminated because Azure credentials are invalid.")
            break

        if result is None:
            continue

        data = result["raw_data"]
        nbest = data["NBest"][0]
        assessed_word = select_assessed_word(nbest["Words"], target_word)

        if target_phoneme is None:
            results.append({
                "word": target_word,
                "expected": None,
                "status": "No target phoneme",
                "likely": None,
                "error": None
            })
            print(f"{target_word} - No target phoneme")
            continue

        if assessed_word is None:
            print(f"{target_word} - No phoneme data returned")
            continue

        if isinstance(target_phoneme, str):
            process_single_target(item, assessed_word["Phonemes"], results)

        elif isinstance(target_phoneme, list):
            process_cluster_target(item, assessed_word["Phonemes"], results)

    print("\n" + "=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)

    for entry in results:
        if entry["status"] == "Correct":
            print(
                f"{entry['word']} | Expected: {entry['expected']} | Correct"
            )
        elif entry["status"] == "Error":
            print(
                f"{entry['word']} | Expected: {entry['expected']} | "
                f"Likely: {entry['likely']} | Error: {entry['error']}"
            )
        else:
            print(f"{entry['word']} | No target phoneme")


if __name__ == "__main__":
    main()
