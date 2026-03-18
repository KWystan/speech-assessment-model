def get_word_bank(age):
    age_4_words = [
        {"word": "Pig", "target_phoneme": "p", "position": "initial", "category": "Age 4", "process": "Early Acquisition"},
        {"word": "Ball", "target_phoneme": "b", "position": "initial", "category": "Age 4", "process": "Early Acquisition"},
        {"word": "Apple", "target_phoneme": "p", "position": "medial", "category": "Age 4", "process": "Early Acquisition"},
        {"word": "Bunny", "target_phoneme": "n", "position": "medial", "category": "Age 4", "process": "Early Acquisition"},
        {"word": "Cup", "target_phoneme": "p", "position": "final", "category": "Age 4", "process": "Final Consonant Deletion"},
        {"word": "Sun", "target_phoneme": "n", "position": "final", "category": "Age 4", "process": "Final Consonant Deletion"},

        {"word": "Ten", "target_phoneme": "t", "position": "initial", "category": "Age 4", "process": "Early Acquisition"},
        {"word": "Dog", "target_phoneme": "d", "position": "initial", "category": "Age 4", "process": "Early Acquisition"},
        {"word": "Water", "target_phoneme": "t", "position": "medial", "category": "Age 4", "process": "Early Acquisition"},
        {"word": "Ladder", "target_phoneme": "d", "position": "medial", "category": "Age 4", "process": "Early Acquisition"},
        {"word": "Boat", "target_phoneme": "t", "position": "final", "category": "Age 4", "process": "Final Consonant Deletion"},
        {"word": "Bed", "target_phoneme": "d", "position": "final", "category": "Age 4", "process": "Final Consonant Deletion"},

        {"word": "Key", "target_phoneme": "k", "position": "initial", "category": "Age 4", "process": "Fronting"},
        {"word": "Goat", "target_phoneme": "g", "position": "initial", "category": "Age 4", "process": "Fronting"},
        {"word": "Cookie", "target_phoneme": "k", "position": "medial", "category": "Age 4", "process": "Fronting"},
        {"word": "Tiger", "target_phoneme": "g", "position": "medial", "category": "Age 4", "process": "Fronting"},
        {"word": "Bike", "target_phoneme": "k", "position": "final", "category": "Age 4", "process": "Fronting"},
        {"word": "Pig", "target_phoneme": "g", "position": "final", "category": "Age 4", "process": "Fronting"},

        {"word": "Fish", "target_phoneme": "f", "position": "initial", "category": "Age 4", "process": "Early Fricatives"},
        {"word": "Whale", "target_phoneme": "w", "position": "initial", "category": "Age 4", "process": "Glides"},
        {"word": "Elephant", "target_phoneme": "f", "position": "medial", "category": "Age 4", "process": "Early Fricatives"},
        {"word": "Leaf", "target_phoneme": "f", "position": "final", "category": "Age 4", "process": "Early Fricatives"},

        {"word": "Banana", "target_phoneme": None, "position": "syllable_shape", "category": "Age 4", "process": "Weak Syllable / 3-Syllable Check"},
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

        {"word": "Spider", "target_phoneme": "sp", "position": "initial_cluster", "category": "Age 5", "process": "Cluster Reduction"},
        {"word": "Star", "target_phoneme": "st", "position": "initial_cluster", "category": "Age 5", "process": "Cluster Reduction"},
        {"word": "Blue", "target_phoneme": "bl", "position": "initial_cluster", "category": "Age 5", "process": "Cluster Reduction"},
        {"word": "Plane", "target_phoneme": "pl", "position": "initial_cluster", "category": "Age 5", "process": "Cluster Reduction"},
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

        {"word": "Frog", "target_phoneme": "fr", "position": "initial_cluster", "category": "Age 6-7", "process": "Cluster / R-Cluster"},
        {"word": "Truck", "target_phoneme": "tr", "position": "initial_cluster", "category": "Age 6-7", "process": "Cluster / R-Cluster"},
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
        return age_8_words
    elif age == 7 or age == 6:
        return age_6_7_words
    elif age == 5:
        return age_5_words
    elif age == 4:
        return age_4_words
    else:
        return []