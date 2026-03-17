from word_bank import get_word_bank
from scoring import classify_phoneme
from azure_assessment import assess_word
from error_classifier import (
    find_single_phoneme_score,
    find_cluster_scores,
    get_likely_spoken_sound,
    classify_error_label,
)


def print_word_list(word_bank):
    print("\nWords to assess:")
    for item in word_bank:
        print(
            f"- {item['word']} | "
            f"Target: {item['target_phoneme']} | "
            f"Position: {item['position']} | "
            f"Process: {item['process']}"
        )


def add_error_entry(phoneme_errors, item, target_word, target_phoneme, likely_sound, score):
    error_label = classify_error_label(
        item,
        target_phoneme,
        likely_sound,
        None if score == "Not Found" else score
    )

    phoneme_errors.append({
        "word": target_word,
        "target_phoneme": target_phoneme,
        "likely_spoken": likely_sound,
        "position": item["position"],
        "category": item["category"],
        "process": item["process"],
        "score": score,
        "error_label": error_label
    })

    return error_label


def process_single_target(item, phonemes, phoneme_errors):
    target_word = item["word"]
    target_phoneme = item["target_phoneme"]

    score, matched_phoneme = find_single_phoneme_score(phonemes, target_phoneme)

    if score is None:
        likely_sound = "omitted/deleted"
        error_label = add_error_entry(
            phoneme_errors,
            item,
            target_word,
            target_phoneme,
            likely_sound,
            "Not Found"
        )

        print(
            "Matched Target:", target_phoneme,
            "| Class: Error",
            "| Likely Produced:", likely_sound,
            "| Error:", error_label,
            "| Score: Not Found"
        )
        return

    classification = classify_phoneme(score)
    likely_sound = get_likely_spoken_sound(matched_phoneme, target_phoneme, score)
    error_label = classify_error_label(item, target_phoneme, likely_sound, score)

    print(
        "Matched Target:", target_phoneme,
        "| Class:", classification,
        "| Likely Produced:", likely_sound,
        "| Error:", error_label,
        "| Score:", score
    )

    if classification == "Error":
        add_error_entry(
            phoneme_errors,
            item,
            target_word,
            target_phoneme,
            likely_sound,
            score
        )


def process_cluster_target(item, phonemes, phoneme_errors):
    target_word = item["word"]
    cluster_results = find_cluster_scores(phonemes, item["target_phoneme"])

    for cluster_item in cluster_results:
        if cluster_item["score"] is None:
            likely_sound = "omitted/deleted"
            error_label = add_error_entry(
                phoneme_errors,
                item,
                target_word,
                cluster_item["target"],
                likely_sound,
                "Not Found"
            )

            print(
                "Matched Cluster Target:", cluster_item["target"],
                "| Class: Error",
                "| Likely Produced:", likely_sound,
                "| Error:", error_label,
                "| Score: Not Found"
            )
            continue

        classification = classify_phoneme(cluster_item["score"])
        likely_sound = get_likely_spoken_sound(
            cluster_item["raw_phoneme"],
            cluster_item["target"],
            cluster_item["score"]
        )
        error_label = classify_error_label(
            item,
            cluster_item["target"],
            likely_sound,
            cluster_item["score"]
        )

        print(
            "Matched Cluster Target:", cluster_item["target"],
            "| Class:", classification,
            "| Likely Produced:", likely_sound,
            "| Error:", error_label,
            "| Score:", cluster_item["score"]
        )

        if classification == "Error":
            add_error_entry(
                phoneme_errors,
                item,
                target_word,
                cluster_item["target"],
                likely_sound,
                cluster_item["score"]
            )


def main():
    child_name = input("Enter child name: ")
    child_age = int(input("Enter child age: "))

    word_bank = get_word_bank(child_age)

    if not word_bank:
        print("Invalid age. Supported ages are 4 to 8 only.")
        return

    print_word_list(word_bank)

    start = input("\nStart assessment? (y/n): ").lower()
    if start != "y":
        print("Assessment cancelled.")
        return

    phoneme_errors = []

    for item in word_bank:
        target_word = item["word"]
        target_phoneme = item["target_phoneme"]

        print("\n" + "=" * 50)

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

        print("\nPhoneme Output:\n")

        for word in nbest["Words"]:
            print("Word:", word["Word"])
            print("Word Score:", word["PronunciationAssessment"]["AccuracyScore"])

            if "Phonemes" not in word:
                continue

            for phoneme in word["Phonemes"]:
                print(
                    "Phoneme:",
                    phoneme["Phoneme"],
                    "| Score:",
                    phoneme["PronunciationAssessment"]["AccuracyScore"]
                )

            print()

            if target_phoneme is None:
                print("This word is for syllable/complexity observation only.")
                continue

            if isinstance(target_phoneme, str):
                process_single_target(item, word["Phonemes"], phoneme_errors)

            elif isinstance(target_phoneme, list):
                process_cluster_target(item, word["Phonemes"], phoneme_errors)

    print("\n" + "=" * 60)
    print("WORD LIST")
    print("=" * 60)
    for item in word_bank:
        print(
            f"Word: {item['word']} | "
            f"Target: {item['target_phoneme']} | "
            f"Position: {item['position']} | "
            f"Category: {item['category']} | "
            f"Process: {item['process']}"
        )

    print("\n" + "=" * 60)
    print("POSSIBLE PHONEME ERRORS")
    print("=" * 60)

    if len(phoneme_errors) == 0:
        print("No phoneme errors found.")
    else:
        for error in phoneme_errors:
            print(
                f"Word: {error['word']} | "
                f"Expected: {error['target_phoneme']} | "
                f"Likely Produced: {error['likely_spoken']} | "
                f"Position: {error['position']} | "
                f"Error: {error['error_label']} | "
                f"Score: {error['score']}"
            )


if __name__ == "__main__":
    main()