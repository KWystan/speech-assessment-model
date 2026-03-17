def get_word_bank(age):
    age_4_words = [
        {"word": "Cup", "target_phoneme": "p", "position": "final", "category": "Age 4", "process": "Final Consonant Deletion"},
        {"word": "Sun", "target_phoneme": "n", "position": "final", "category": "Age 4", "process": "Final Consonant Deletion"},
    ]

    age_5_words = [
        {"word": "Sun", "target_phoneme": "s", "position": "initial", "category": "Age 5", "process": "Stopping"},
        {"word": "Zebra", "target_phoneme": "z", "position": "initial", "category": "Age 5", "process": "Stopping"},
        {"word": "Pencil", "target_phoneme": "s", "position": "medial", "category": "Age 5", "process": "Stopping"},
        {"word": "Lizard", "target_phoneme": "z", "position": "medial", "category": "Age 5", "process": "Stopping"},
        {"word": "Bus", "target_phoneme": "s", "position": "final", "category": "Age 5", "process": "Stopping"},
        {"word": "Cheese", "target_phoneme": "z", "position": "final", "category": "Age 5", "process": "Stopping"},

        {"word": "Yarn", "target_phoneme": "j", "position": "initial", "category": "Age 5", "process": "Glides"},
        {"word": "Hat", "target_phoneme": "h", "position": "initial", "category": "Age 5", "process": "Early Acquisition"},
        {"word": "Yoyo", "target_phoneme": "j", "position": "medial", "category": "Age 5", "process": "Glides"},

        {"word": "Shoe", "target_phoneme": "ʃ", "position": "initial", "category": "Age 5", "process": "Stopping"},
        {"word": "Flashlight", "target_phoneme": "ʃ", "position": "medial", "category": "Age 5", "process": "Stopping"},
        {"word": "Fish", "target_phoneme": "ʃ", "position": "final", "category": "Age 5", "process": "Stopping"},

        {"word": "Spider", "target_phoneme": ["s", "p"], "position": "initial_cluster", "category": "Age 5", "process": "Cluster Reduction"},
        {"word": "Star", "target_phoneme": ["s", "t"], "position": "initial_cluster", "category": "Age 5", "process": "Cluster Reduction"},
        {"word": "Blue", "target_phoneme": ["b", "l"], "position": "initial_cluster", "category": "Age 5", "process": "Cluster Reduction"},
        {"word": "Plane", "target_phoneme": ["p", "l"], "position": "initial_cluster", "category": "Age 5", "process": "Cluster Reduction"},
    ]

    age_6_7_words = [
        {"word": "Lion", "target_phoneme": "l", "position": "initial", "category": "Age 6-7", "process": "Gliding"},
        {"word": "Balloon", "target_phoneme": "l", "position": "medial", "category": "Age 6-7", "process": "Gliding"},
        {"word": "Bell", "target_phoneme": "l", "position": "final", "category": "Age 6-7", "process": "Gliding"},

        {"word": "Rock", "target_phoneme": "r", "position": "initial", "category": "Age 6-7", "process": "Gliding"},
        {"word": "Mirror", "target_phoneme": "r", "position": "medial", "category": "Age 6-7", "process": "Gliding"},
        {"word": "Star", "target_phoneme": "r", "position": "final", "category": "Age 6-7", "process": "Gliding"},

        {"word": "Volcano", "target_phoneme": "v", "position": "initial", "category": "Age 6-7", "process": "Late Fricatives"},
        {"word": "Seven", "target_phoneme": "v", "position": "medial", "category": "Age 6-7", "process": "Late Fricatives"},
        {"word": "Glove", "target_phoneme": "v", "position": "final", "category": "Age 6-7", "process": "Late Fricatives"},

        {"word": "Chair", "target_phoneme": "tʃ", "position": "initial", "category": "Age 6-7", "process": "Affricates"},
        {"word": "Jeep", "target_phoneme": "dʒ", "position": "initial", "category": "Age 6-7", "process": "Affricates"},
        {"word": "Kitchen", "target_phoneme": "tʃ", "position": "medial", "category": "Age 6-7", "process": "Affricates"},
        {"word": "Orange", "target_phoneme": "dʒ", "position": "medial", "category": "Age 6-7", "process": "Affricates"},
        {"word": "Watch", "target_phoneme": "tʃ", "position": "final", "category": "Age 6-7", "process": "Affricates"},
        {"word": "Bridge", "target_phoneme": "dʒ", "position": "final", "category": "Age 6-7", "process": "Affricates"},

        {"word": "Frog", "target_phoneme": ["f", "r"], "position": "initial_cluster", "category": "Age 6-7", "process": "R-Cluster"},
        {"word": "Truck", "target_phoneme": ["t", "r"], "position": "initial_cluster", "category": "Age 6-7", "process": "R-Cluster"},
    ]

    age_8_words = [
        {"word": "Thumb", "target_phoneme": "θ", "position": "initial", "category": "Age 8", "process": "Voiceless TH"},
        {"word": "Toothbrush", "target_phoneme": "θ", "position": "medial", "category": "Age 8", "process": "Voiceless TH"},
        {"word": "Mouth", "target_phoneme": "θ", "position": "final", "category": "Age 8", "process": "Voiceless TH"},

        {"word": "They", "target_phoneme": "ð", "position": "initial", "category": "Age 8", "process": "Voiced TH"},
        {"word": "This", "target_phoneme": "ð", "position": "initial", "category": "Age 8", "process": "Voiced TH"},
        {"word": "Feather", "target_phoneme": "ð", "position": "medial", "category": "Age 8", "process": "Voiced TH"},
        {"word": "Smooth", "target_phoneme": "ð", "position": "final", "category": "Age 8", "process": "Voiced TH"},

        {"word": "Treasure", "target_phoneme": "ʒ", "position": "medial", "category": "Age 8", "process": "ZH"},

        {"word": "Helicopter", "target_phoneme": None, "position": "initial_complexity", "category": "Age 8", "process": "Multisyllabic Complexity"},
        {"word": "Vegetable", "target_phoneme": None, "position": "medial_complexity", "category": "Age 8", "process": "Multisyllabic Complexity"},
        {"word": "Spaghetti", "target_phoneme": None, "position": "final_complexity", "category": "Age 8", "process": "Multisyllabic Complexity"},
    ]

    if age == 8:
        return age_4_words + age_5_words + age_6_7_words + age_8_words
    elif age == 7 or age == 6:
        return age_4_words + age_5_words + age_6_7_words
    elif age == 5:
        return age_4_words + age_5_words
    elif age == 4:
        return age_4_words
    else:
        return []