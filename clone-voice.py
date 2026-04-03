#!/usr/bin/env python3
"""Clone voices using Chatterbox via HuggingFace API — 3 presenters, 3 voices.

Uses 3 base reference voice samples — one per presenter — and generates
all slide narrations with the matching cloned voice via the fal-ai Chatterbox API.

Setup:
    pip3 install requests
    export HF_TOKEN="hf_your_token_here"

Usage:
    # Place 3 reference audio files (3-10 seconds each, WAV/MP3):
    #   voice-refs/valentina.wav   — e.g. Catherine Tate clip
    #   voice-refs/alex.wav        — e.g. Ali G clip
    #   voice-refs/sam.wav         — e.g. David Attenborough clip
    #
    # Then run:
    python3 clone-voice.py              # generate all slides
    python3 clone-voice.py 1 3 5        # generate specific slides only
    python3 clone-voice.py --list-voices # show presenter → slide mapping
"""

import requests
import base64
import subprocess
import os
import sys

AUDIO_DIR = "presentation-audio"
VOICE_REF_DIR = "voice-refs"
os.makedirs(AUDIO_DIR, exist_ok=True)

HF_TOKEN = os.environ.get("HF_TOKEN", "")
API_URL = "https://router.huggingface.co/fal-ai/fal-ai/chatterbox/text-to-speech"

# ── Presenter voice references ──
PRESENTERS = {
    "valentina": {
        "ref_audio": os.path.join(VOICE_REF_DIR, "valentina.wav"),
        "slides": [1, 12],
        "description": "Sassy female host (Catherine Tate) — opens and closes the show",
    },
    "alex": {
        "ref_audio": os.path.join(VOICE_REF_DIR, "alex.wav"),
        "slides": [2, 11],
        "description": "Ali G energy — why & how-to-build-your-own slides",
    },
    "sam": {
        "ref_audio": os.path.join(VOICE_REF_DIR, "sam.wav"),
        "slides": [3, 4, 5, 6, 7, 8, 9, 10],
        "description": "David Attenborough narrator — core content slides",
    },
}

# ── Slide narration scripts ──
NARRATIONS = {
    1: "Yo yo yo! Check it! Welcome to Web Presenter, the most massive, the most immersive presentation framework ever created by man! Built with pure HTML, CSS, and Three.js! No build tools. No dependencies. Just straight up elegance, innit! Booyakasha!",
    2: "Aight, so picture this yeah? What if presentations was actually not boring? Traditional slide decks is well stale and flat. Web frameworks is too complex. But Web Presenter? This is the answer! One single HTML file with animations, backgrounds, and touch navigation. Respect!",
    3: "Here is the problem with presentations today, right? Building well engaging web presentations requires like dozens of libraries, bare boilerplate code, and fighting with build tools. And the result? Flat, lifeless slides that puts everyone to sleep. That ain't cool!",
    4: "Allow me to introduce you to Web Presenter! A complete framework for well immersive presentations! At its core, we got HTML slides, CSS animations, touch navigation, and Three.js WebGL backgrounds. Everything is connected. Everything is beautiful. Big up yourself!",
    5: "So check this out yeah? This is how it works! Three simple steps innit! Step one, author your slides in plain HTML. Step two, style it with CSS variables for full theme control. Step three, present in any browser with keyboard, touch, or mouse navigation. Easy!",
    6: "Rich slide transitions bring your content to life, you get me? Elements enter, they animate, they advance in a well seamless flow! We got keyboard navigation, touch and swipe support, CSS animations, and WebGL backgrounds! Is it good? It is well good!",
    7: "Built-in layouts give you bare flexibility, right? Choose from title, center, two-column, philosophy cards, dashboard grids, or create your own custom layouts with CSS grid and flexbox. The options is massive!",
    8: "Check this dashboard layout example! It showcases tables, statistics, and animated data! Everything is styled and transitions well smoothly into view! This is proper tech, innit!",
    9: "Under the hood yeah? It is pure HTML5, CSS3, and JavaScript! Three.js provides them WebGL backgrounds! Touch navigation works everywhere! Deploy to GitHub Pages with a single push! Zero dependencies! This is the future!",
    10: "Did you know this yeah? Over eighty percent of audiences loses attention within the first ten minutes of a traditional slideshow! That is well bad! But Web Presenter changes all of that with immersive animations and interactive experiences! Respect!",
    11: "Aight so let me show you how to build your own presentation yeah? It is well simple! Step one, clone the repo and grab a HuggingFace token. Step two, point your favourite AI agent at the project and tell it what you want! The agent writes the slides, generates narration audio with Edge TTS, and creates images with HuggingFace FLUX! Step three, preview it locally and push to GitHub Pages! You can even use the browser-based Studio tools — the Creator and Editor — powered by LLMs! Wicked!",
    12: "So what is you waiting for? Start presenting with proper style! Animated slides! Three.js backgrounds! Zero build tools! Clone the repository and let an AI agent build you something beautiful today! West side! Booyakasha!",
}


def get_presenter_for_slide(slide_num):
    """Return the presenter name for a given slide number."""
    for name, cfg in PRESENTERS.items():
        if slide_num in cfg["slides"]:
            return name
    return "sam"


def list_voices():
    """Print presenter → slide mapping and reference file status."""
    print("\n=== Presenter Voice Mapping ===\n")
    for name, cfg in PRESENTERS.items():
        ref = cfg["ref_audio"]
        exists = "OK" if os.path.exists(ref) else "MISSING"
        slides = ", ".join(str(s) for s in cfg["slides"])
        print(f"  {name:12s}  slides [{slides}]")
        print(f"               {cfg['description']}")
        print(f"               ref: {ref} [{exists}]")
        print()


def load_ref_audio(path):
    """Load reference audio file and return base64 data URI."""
    with open(path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(path)[1].lstrip(".")
    if ext == "mp3":
        mime = "audio/mpeg"
    else:
        mime = f"audio/{ext}"
    return f"data:{mime};base64,{audio_b64}"


def generate_all(slide_nums=None):
    """Generate voice-cloned narration for all (or selected) slides."""
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

    # Validate reference files exist
    for name, cfg in PRESENTERS.items():
        if not os.path.exists(cfg["ref_audio"]):
            print(f"  [ERROR] Missing reference audio: {cfg['ref_audio']}")
            print(f"          Record or place a 3-10 second WAV sample for {name}.")
            sys.exit(1)

    # Pre-load reference audio (cached per presenter)
    print("=== Loading voice references ===")
    ref_data = {}
    for name, cfg in PRESENTERS.items():
        print(f"  Loading {name}: {cfg['ref_audio']}")
        ref_data[name] = load_ref_audio(cfg["ref_audio"])

    # Filter slides
    slides_to_generate = slide_nums or sorted(NARRATIONS.keys())

    print(f"\n=== Generating {len(slides_to_generate)} slides (Chatterbox via fal-ai) ===\n")
    success = 0
    failed = 0

    for slide_num in slides_to_generate:
        if slide_num not in NARRATIONS:
            print(f"  [SKIP] Slide {slide_num:02d}: no narration text defined")
            continue

        presenter = get_presenter_for_slide(slide_num)
        text = NARRATIONS[slide_num]
        print(f"  [CLONE] Slide {slide_num:02d} ({presenter}): generating...")

        try:
            resp = requests.post(API_URL, headers=headers, json={
                "text": text,
                "audio_url": ref_data[presenter],
                "exaggeration": 0.4,
                "temperature": 0.8,
            }, timeout=180)

            if resp.status_code != 200:
                print(f"  [CLONE] Slide {slide_num:02d} ({presenter}): FAILED - HTTP {resp.status_code}: {resp.text[:200]}")
                failed += 1
                continue

            data = resp.json()
            audio_url = data["audio"]["url"]

            # Download wav
            audio_resp = requests.get(audio_url, timeout=60)
            wav_path = os.path.join(AUDIO_DIR, f"slide-{slide_num:02d}.wav")
            mp3_path = os.path.join(AUDIO_DIR, f"slide-{slide_num:02d}.mp3")

            with open(wav_path, "wb") as f:
                f.write(audio_resp.content)

            # Convert to mp3
            result = subprocess.run(
                ["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_path],
                capture_output=True,
            )
            if result.returncode == 0:
                os.remove(wav_path)
                size_kb = os.path.getsize(mp3_path) / 1024
                print(f"  [CLONE] Slide {slide_num:02d} ({presenter}): OK ({size_kb:.0f} KB)")
            else:
                # Keep WAV if ffmpeg fails
                size_kb = os.path.getsize(wav_path) / 1024
                print(f"  [CLONE] Slide {slide_num:02d} ({presenter}): OK as WAV ({size_kb:.0f} KB) — ffmpeg failed")

            success += 1

        except Exception as e:
            print(f"  [CLONE] Slide {slide_num:02d} ({presenter}): FAILED - {e}")
            failed += 1

    print(f"\n=== Done: {success} OK, {failed} failed ===")


if __name__ == "__main__":
    if "--list-voices" in sys.argv:
        list_voices()
        sys.exit(0)

    # Parse optional slide numbers from CLI args
    slide_nums = None
    args = [a for a in sys.argv[1:] if a.isdigit()]
    if args:
        slide_nums = [int(a) for a in args]
        print(f"Generating slides: {slide_nums}")

    generate_all(slide_nums)
