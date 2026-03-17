import azure.cognitiveservices.speech as speechsdk
import json

speech_key = "7iyT7N6LiE2S99igEjCvt3NHZEy8xCfPsxQLzN60sZcEqGn4F5HKJQQJ99BKAC3pKaRXJ3w3AAAYACOGzpew"
speech_endpoint = "https://eastasia.api.cognitive.microsoft.com/"


def assess_word(target_word, max_retries=3):
    retry_count = 0

    while retry_count < max_retries:
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

        pronunciation_assessment_config = speechsdk.PronunciationAssessmentConfig(
            json_string=(
                f'{{"referenceText":"{target_word}",'
                f'"gradingSystem":"HundredMark",'
                f'"granularity":"Phoneme",'
                f'"phonemeAlphabet":"IPA",'
                f'"nBestPhonemeCount":5}}'
            )
        )

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

            return {
                "recognized_text": speech_recognition_result.text,
                "accuracy": pronunciation_assessment_result.accuracy_score,
                "fluency": pronunciation_assessment_result.fluency_score,
                "completeness": pronunciation_assessment_result.completeness_score,
                "pronunciation": pronunciation_assessment_result.pronunciation_score,
                "raw_data": data
            }

        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            retry_count += 1
            print(f"No speech could be recognized. Retrying word '{target_word}' ({retry_count}/{max_retries})...\n")

        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled:", cancellation_details.reason)

            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details:", cancellation_details.error_details)

                if "401" in str(cancellation_details.error_details) or "Authentication" in str(cancellation_details.error_details):
                    raise RuntimeError("Azure authentication failed. Check key and endpoint.")

            return None

    print(f"Skipped word '{target_word}' after {max_retries} failed attempts.")
    return None