init python:
    renpy.music.register_channel("tts", mixer="voice", tight=True, loop=False)


init 4096 python:
    import_check("azure.cognitiveservices.speech", "simpleaudio")

    import os, hashlib, tempfile
    import queue, threading

    import azure.cognitiveservices.speech as speechsdk


    # Save original __call__
    _original_say = renpy.say

    _SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
    _SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

    if not _SPEECH_KEY or not _SPEECH_REGION:
        renpy.log("Azure TTS env vars missing")
        raise Exception("Missing AZURE_SPEECH_KEY or AZURE_SPEECH_REGION")

    _TTS_DIRBASENAME = ".tts_cache"
    _TTS_DIR = os.path.join(renpy.config.basedir, "game", _TTS_DIRBASENAME)
    os.makedirs(_TTS_DIR, exist_ok=True)


    _sc =  {
        "audioExtension": ".wav",
        "format": "Riff48Khz16BitMonoPcm",
        "voices": {
            "sayori": {
                "pitch": "+20%",
                "rate": "+10%",
                "voice": "en-US-AmandaMultilingualNeural",
            },
            "natsuki": {
                "pitch": "+20%",
                "rate": "+10%",
                "voice": "en-US-AmandaMultilingualNeural",
            },
            "yuri": {
                "pitch": "+20%",
                "rate": "+10%",
                "voice": "en-US-AmandaMultilingualNeural",
            },
            "monika": {
                "pitch": "+20%",
                "rate": "+10%",
                "voice": "en-US-AmandaMultilingualNeural",
            },
        },
        "volume": 1,
    }

    _speech_config = speechsdk.SpeechConfig(
        subscription=_SPEECH_KEY,
        region=_SPEECH_REGION,
    )
    _speech_config.set_speech_synthesis_output_format(
        getattr(speechsdk.SpeechSynthesisOutputFormat, _sc["format"]),
        # speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm
        # speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm
    )

    # def _process_tts_queue():
    #     """Called from main thread, plays queued TTS."""

    #     while not _tts_queue.empty():
    #         _args = _tts_queue.get()

    #         who = _args.get("who")
    #         what = _args.get("what")
    #         interact = _args.get("interact")
    #         args = _args.get("args")
    #         kwargs = _args.get("kwargs")


    #         _fname = hashlib.md5(f"{who}_{what}".encode()).hexdigest() + ".wav"
    #         _path = os.path.join(_TTS_DIR, _fname)

    #         if os.path.exists(_path):
    #             return

    #         _fhash = hashlib.md5(f"{_sc} § {_args}".encode()).hexdigest()
    #         _fbasename = f"{str(who)}_{_fhash}" + _sc["audioExtension"]
    #         _shallow_path = os.path.join(_TTS_DIRBASENAME, _fbasename)
    #         _path = os.path.join(_TTS_DIR, _fbasename)

    #         if (_ccfg := _sc["voices"].get(str(who).lower())) is None:
    #             return

    #         _subtitle_buffer: list[speechsdk.SpeechSynthesisWordBoundaryEventArgs] = []
    #         _audio_config = speechsdk.audio.AudioOutputConfig(filename=_path)
    #         _synthesizer = speechsdk.SpeechSynthesizer(_speech_config, _audio_config)
    #         _synthesizer.synthesis_word_boundary.connect(
    #             lambda evt: _subtitle_buffer.append(evt)
    #         )

    #         def _strip_lines(text: str) -> str:
    #             return "\n".join(t.strip() for t in text.splitlines())

    #         def _text_to_ssml(text: str):
    #             return _strip_lines(
    #                 f"""<speak version="1.0" xml:lang="en-US">
    #                     <voice name="{_ccfg.get("voice", 'en-US-AmandaMultilingualNeural')}">
    #                         <prosody rate="{_ccfg.get("rate", '0%')}" pitch="{_ccfg.get("pitch", '0%')}">
    #                             {text}
    #                         </prosody>
    #                     </voice>
    #                 </speak>"""
    #             )

    #         def _wait_speak(text: str) -> speechsdk.SpeechSynthesisResult:
    #             _ssml = _text_to_ssml(text)
    #             _speech_task = _synthesizer.speak_ssml_async(_ssml)

    #             return _speech_task.get()

    #         _result = _wait_speak(what)

    #         if _result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
    #             os.remove(_path)
    #             raise Exception(_result.cancellation_details.error_details)

    #         renpy.music.play(_path, channel="tts")


    def _on_say(
        who: "Character | None",
        what: str,
        interact: bool = True,
        *args,
        **kwargs,
    ):
        # if renpy.is_skipping():
        #     return

        def _synthesize_and_play(who, what):
            _hashparams = [
                _sc,
                what,
                interact,
                args,
                kwargs,
            ]
            _fhash = hashlib.md5("§".join(str(x) for x in _hashparams).encode()).hexdigest()
            _fbasename = f"{str(who)}_{_fhash}" + _sc["audioExtension"]
            _shallow_path = os.path.join(_TTS_DIRBASENAME, _fbasename)
            _path = os.path.join(_TTS_DIR, _fbasename)

            if (_ccfg := _sc["voices"].get(str(who).lower())) is None:
                return

            _subtitle_buffer: list[speechsdk.SpeechSynthesisWordBoundaryEventArgs] = []
            _audio_config = speechsdk.audio.AudioOutputConfig(filename=_path)
            _synthesizer = speechsdk.SpeechSynthesizer(_speech_config, _audio_config)
            _synthesizer.synthesis_word_boundary.connect(
                lambda evt: _subtitle_buffer.append(evt)
            )

            def _strip_lines(text: str) -> str:
                return "\n".join(t.strip() for t in text.splitlines())

            def _text_to_ssml(text: str):
                return _strip_lines(
                    f"""<speak version="1.0" xml:lang="en-US">
                        <voice name="{_ccfg.get("voice", 'en-US-AmandaMultilingualNeural')}">
                            <prosody rate="{_ccfg.get("rate", '0%')}" pitch="{_ccfg.get("pitch", '0%')}">
                                {text}
                            </prosody>
                        </voice>
                    </speak>"""
                )

            def _wait_speak(text: str) -> speechsdk.SpeechSynthesisResult:
                _ssml = _text_to_ssml(text)
                _speech_task = _synthesizer.speak_ssml_async(_ssml)

                return _speech_task.get()

            _result = _wait_speak(what)


            if _result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
                os.remove(_path)
                raise Exception(_result.cancellation_details.error_details)

            renpy.music.play(_shallow_path, channel="tts")

        def _worker():
            _synthesize_and_play(who, what)

        threading.Thread(target=_worker, daemon=True).start()


    def _say_wrapper(who: "Character | None", what: str, interact: bool = True, *args, **kwargs):
        _on_say(who, what, interact, *args, **kwargs)
        return _original_say(who, what, interact, *args, **kwargs)

    renpy.say = _say_wrapper
