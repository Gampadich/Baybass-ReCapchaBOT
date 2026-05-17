# reCAPTCHA Audio Bypass

An automated tool that solves Google reCAPTCHA v2 challenges by leveraging the audio accessibility feature and speech recognition.

## How It Works

1. Opens a Chromium browser with automation detection disabled
2. Navigates to the target page and clicks the reCAPTCHA checkbox
3. Switches to the audio challenge mode
4. Downloads the audio challenge file (`.mp3`)
5. Converts audio to WAV and transcribes it using Google Speech Recognition
6. Fills in the transcribed answer and submits

## Project Structure

```
.
├── main.py            # Main automation script (Playwright)
└── speechToText.py    # Audio transcription module
```

## Requirements

- Python 3.8+
- Google Chrome / Chromium

## Installation

```bash
pip install playwright pydub SpeechRecognition
playwright install chromium
```

> **Note:** `pydub` requires [FFmpeg](https://ffmpeg.org/download.html) to be installed and available in your `PATH` for MP3-to-WAV conversion.

## Usage

```bash
python main.py
```

By default, the script targets the official reCAPTCHA demo page:
`https://www.google.com/recaptcha/api2/demo`

To use it on a different page, update the `page.goto(...)` URL in `main.py`.

## Modules

### `main.py` — Browser Automation

Uses [Playwright](https://playwright.dev/python/) to control a Chromium browser.

Key techniques used to avoid bot detection:

- `--disable-blink-features=AutomationControlled` launch argument
- Overrides `navigator.webdriver` via `add_init_script`
- Custom `User-Agent` header mimicking a real Chrome browser
- Random human-like delays between actions (`human_delay`)

**Flow:**
1. Launch browser → navigate to target page
2. Find and click the reCAPTCHA anchor iframe
3. Detect audio challenge button and click it
4. Download the audio challenge MP3
5. Pass the file to `speechToText.transcribe_audio()`
6. Type the result into the audio response input and verify
7. Submit the form and check for success

### `speechToText.py` — Audio Transcription

Converts the downloaded MP3 challenge into text.

**Flow:**
1. Load `captcha_audio.mp3` with `pydub`
2. Export to a temporary WAV file (`temp_captcha_audio.wav`)
3. Transcribe using `speech_recognition` with Google's Web Speech API (`en-US`)
4. Clean up the temporary WAV file
5. Return the transcribed string (or `None` on failure)

## Limitations

- Depends on Google's free Speech Recognition API — may be rate-limited
- reCAPTCHA may present image challenges or block repeated attempts
- Detection heuristics change frequently; evasion is not guaranteed

## Disclaimer

This project is intended for **educational and research purposes only**. Bypassing CAPTCHAs on services you do not own or have explicit permission to test may violate the terms of service of those services and applicable laws. Use responsibly.