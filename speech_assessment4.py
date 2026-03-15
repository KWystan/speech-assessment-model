import azure.cognitiveservices.speech as speechsdk
import json

speech_key = "7iyT7N6LiE2S99igEjCvt3NHZEy8xCfPsxQLzN60sZcEqGn4F5HKJQQJ99BKAC3pKaRXJ3w3AAAYACOGzpew"
speech_endpoint = "https://eastasia.api.cognitive.microsoft.com/"

speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    endpoint=speech_endpoint
)

language = "en-US"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    language=language,
    audio_config=audio_config
)

target_word = "sun"

# Pronunciation config with nBestPhonemeCount to see top 5 candidates
pronunciation_assessment_config = speechsdk.PronunciationAssessmentConfig(
    json_string=f'{{"referenceText":"{target_word}","gradingSystem":"HundredMark","granularity":"Phoneme","phonemeAlphabet":"IPA","nBestPhonemeCount":5}}'
)

pronunciation_config = speechsdk.PronunciationAssessmentConfig(
    reference_text="",
    grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
    granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
    enable_miscue=False
)
pronunciation_config.enable_prosody_assessment()

# Apply pronunciation assessment
speech_recognizer.session_started.connect(
    lambda evt: print(f"SESSION ID: {evt.session_id}")
)
pronunciation_assessment_config.apply_to(speech_recognizer)

print(f"Please say: {target_word}")
print("Listening...\n")

speech_recognition_result = speech_recognizer.recognize_once()

if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:

    print("Recognized:", speech_recognition_result.text)

    pronunciation_assessment_result = speechsdk.PronunciationAssessmentResult(
        speech_recognition_result
    )

    print("\nSentence Scores")
    print("Accuracy:", pronunciation_assessment_result.accuracy_score)
    print("Fluency:", pronunciation_assessment_result.fluency_score)
    print("Completeness:", pronunciation_assessment_result.completeness_score)
    print("Pronunciation:", pronunciation_assessment_result.pronunciation_score)

    pronunciation_assessment_result_json = speech_recognition_result.properties.get(
        speechsdk.PropertyId.SpeechServiceResponse_JsonResult
    )
    data = json.loads(pronunciation_assessment_result_json)

    nbest = data["NBest"][0]

    # ---- Normal phoneme output ----
    print("\nPhoneme Output:\n")
    for word in nbest["Words"]:
        print("Word:", word["Word"])
        print("Word Score:", word["PronunciationAssessment"]["AccuracyScore"])
        if "Phonemes" in word:
            for phoneme in word["Phonemes"]:
                print(
                    "Phoneme:",
                    phoneme["Phoneme"],
                    "| Score:",
                    phoneme["PronunciationAssessment"]["AccuracyScore"]
                )
        print()

    # ---- Phoneme output with N-best ----
    print("Phoneme Output with N-best:\n")
    for word in nbest["Words"]:
        print("Word:", word["Word"])
        print("Word Score:", word["PronunciationAssessment"]["AccuracyScore"])
        if "Phonemes" in word:
            for phoneme in word["Phonemes"]:
                expected_phoneme = phoneme["Phoneme"]
                phoneme_score = phoneme["PronunciationAssessment"]["AccuracyScore"]
                print(f"Expected Phoneme: {expected_phoneme} | Score: {phoneme_score}")

                # Show top N-best phonemes actually spoken
                if "NBestPhonemes" in phoneme["PronunciationAssessment"]:
                    print("  N-best spoken phonemes:")
                    for nb in phoneme["PronunciationAssessment"]["NBestPhonemes"]:
                        print(f"    {nb['Phoneme']} | Score: {nb['Score']}")
        print()

elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized")

elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_recognition_result.cancellation_details
    print("Speech Recognition canceled:", cancellation_details.reason)
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details:", cancellation_details.error_details)