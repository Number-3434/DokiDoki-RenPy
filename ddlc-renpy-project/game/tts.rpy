init python:
    import_check("azure.cognitiveservices.speech", "dotenv")


    def say_azure(text, filename="line.wav"):
        import azure.cognitiveservices.speech as speechsdk
        import dotenv

        # # Configure TTS
        # speech_config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION)
        # speech_config.speech_synthesis_output_format = speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        # audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

        # # Create synthesizer
        # synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # # Synthesize
        # result = synthesizer.speak_text_async(text).get()

        # if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #     return filename
        # else:
        #     renpy.log("TTS error: " + str(result.reason))
        #     return None
