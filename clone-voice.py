#!/usr/bin/env python3
"""Clone voices using Qwen3-TTS via HuggingFace Spaces API — 3 presenters, 3 voices.

Uses 3 base reference voice samples — one per presenter — and generates
all slide narrations with the matching cloned voice via the Qwen3-TTS Space.

Setup:
    pip3 install requests
    export HF_TOKEN="hf_your_token_here"

Usage:
    # Place 3 reference audio files (3-30 seconds each, WAV):
    #   voice-refs/valentina.wav   — Gillian Anderson voice clone
    #   voice-refs/alex.wav        — Ali G energy voice
    #   voice-refs/sam.wav         — Frank Costanza voice clone
    #
    # Then run:
    python3 clone-voice.py              # generate all slides
    python3 clone-voice.py 1 3 5        # generate specific slides only
    python3 clone-voice.py --list-voices # show presenter -> slide mapping
"""

import requests
import subprocess
import os
import sys
import json
import time

AUDIO_DIR = "presentation-audio"
VOICE_REF_DIR = "voice-refs"
os.makedirs(AUDIO_DIR, exist_ok=True)

HF_TOKEN = os.environ.get("HF_TOKEN", "")
SPACE_URL = "https://qwen-qwen3-tts.hf.space"
API_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# -- Presenter voice references --
PRESENTERS = {
    "valentina": {
        "ref_audio": os.path.join(VOICE_REF_DIR, "valentina.wav"),
        "slides": [1, 12],
        "description": "Gillian Anderson voice — opens and closes the show",
    },
    "alex": {
        "ref_audio": os.path.join(VOICE_REF_DIR, "alex.wav"),
        "slides": [2, 11],
        "description": "Ali G energy — why & how-to-build-your-own slides",
    },
    "sam": {
        "ref_audio": os.path.join(VOICE_REF_DIR, "sam.wav"),
        "slides": [3, 4, 5, 6, 7, 8, 9, 10],
        "description": "Frank Costanza voice — core content slides",
    },
}

# -- Slide narration scripts --
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
    11: "Aight so let me show you how to build your own presentation yeah? It is well simple! Step one, clone the repo and grab a HuggingFace token. Step two, point your favourite AI agent at the project and tell it what you want! The agent writes the slides, generates narration audio with Edge TTS, and creates images with HuggingFace FLUX! Step three, preview it locally and push to GitHub Pages! You can even use the browser-based Studio tools - the Creator and Editor - powered by LLMs! Wicked!",
    12: "So what is you waiting for? Start presenting with proper style! Animated slides! Three.js backgrounds! Zero build tools! Clone the repository and let an AI agent build you something beautiful today! West side! Booyakasha!",
}


def get_presenter_for_slide(slide_num):
    """Return the presenter name for a given slide number."""
    for name, cfg in PRESENTERS.items():
        if slide_num in cfg["slides"]:
            return name
    return "sam"


def list_voices():
    """Print presenter -> slide mapping and reference file status."""
    print("\n=== Presenter Voice Mapping ===\n")
    for name, cfg in PRESENTERS.items():
        ref = cfg["ref_audio"]
        exists = "OK" if os.path.exists(ref) else "MISSING"
        slides = ", ".join(str(s) for s in cfg["slides"])
        print(f"  {name:12s}  slides [{slides}]")
        print(f"               {cfg['description']}")
        print(f"               ref: {ref} [{exists}]")
        print()


def upload_ref(path):
    """Upload a reference audio file to the Qwen3-TTS Space. Returns server path."""
    with open(path, "rb") as f:
        resp = requests.post(
            f"{SPACE_URL}/gradio_api/upload",
            headers=API_HEADERS,
            files={"files": (os.path.basename(path), f, "audio/wav")},
            timeout=60,
        )
    resp.raise_for_status()
    paths = resp.json()
    return paths[0]


def submit_clone(ref_path, text):
    """Submit a voice clone job. Returns event_id."""
    payload = {
        "data": [
            {
                "path": ref_path,
                "meta": {"_type": "gradio.FileData"},
                "orig_name": os.path.basename(ref_path),
                "mime_type": "audio/wav",
            },
            "",  # ref_text (empty = x-vector only)
            text,
            "English",
            True,
            "1.7B",
        ]
    }
    resp = requests.post(
        f"{SPACE_URL}/gradio_api/call/generate_voice_clone",
        headers={**API_HEADERS, "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["event_id"]


def collect_result(event_id, timeout=180):
    """Poll for a clone job result. Returns audio URL or None."""
    resp = requests.get(
        f"{SPACE_URL}/gradio_api/call/generate_voice_clone/{event_id}",
        headers=API_HEADERS,
        stream=True,
        timeout=timeout,
    )
    audio_url = None
    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue
        if line.startswith("event: error"):
            return None
        if line.startswith("data: ") and "audio.wav" in line:
            data = json.loads(line[6:])
            audio_url = data[0]["url"]
    return audio_url


def download_audio(url, dest_path):
    """Download audio from the Space to a local file."""
    resp = requests.get(url, headers=API_HEADERS, timeout=60)
    resp.raise_for_status()
    with open(dest_path, "wb") as f:
        f.write(resp.content)


def generate_all(slide_nums=None):
    """Generate voice-cloned narration for all (or selected) slides via Qwen3-TTS."""
    # Validate reference files exist
    for name, cfg in PRESENTERS.items():
        if not os.path.exists(cfg["ref_audio"]):
            print(f"  [ERROR] Missing reference audio: {cfg['ref_audio']}")
            print(f"          Place a WAV sample for {name} in voice-refs/.")
            sys.exit(1)

    # Upload reference audio files
    print("=== Uploading voice references to Qwen3-TTS ===")
    ref_paths = {}
    for name, cfg in PRESENTERS.items():
        print(f"  Uploading {name}: {cfg['ref_audio']}")
        ref_paths[name] = upload_ref(cfg["ref_audio"])
        print(f"    -> {ref_paths[name]}")

    # Filter slides
    slides_to_generate = slide_nums or sorted(NARRATIONS.keys())

    print(f"\n=== Generating {len(slides_to_generate)} slides (Qwen3-TTS voice clone) ===\n")
    success = 0
    failed = 0

    for slide_num in slides_to_generate:
        if slide_num not in NARRATIONS:
            print(f"  [SKIP] Slide {slide_num:02d}: no narration text defined")
            continue

        presenter = get_presenter_for_slide(slide_num)
        text = NARRATIONS[slide_num]
        wav_path = os.path.join(AUDIO_DIR, f"slide-{slide_num:02d}.wav")
        mp3_path = os.path.join(AUDIO_DIR, f"slide-{slide_num:02d}.mp3")

        print(f"  [CLONE] Slide {slide_num:02d} ({presenter}): submitting...", end=" ", flush=True)

        try:
            # Submit job
            event_id = submit_clone(ref_paths[presenter], text)
            print("waiting...", end=" ", flush=True)

            # Collect result
            audio_url = collect_result(event_id)
            if not audio_url:
                print("FAILED (no audio)")
                failed += 1
                continue

            # Download
            download_audio(audio_url, wav_path)

            # Convert to mp3
            result = subprocess.run(
                ["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_path],
                capture_output=True,
            )
            if result.returncode == 0:
                os.remove(wav_path)
                size_kb = os.path.getsize(mp3_path) / 1024
                print(f"OK ({size_kb:.0f} KB)")
            else:
                size_kb = os.path.getsize(wav_path) / 1024
                print(f"OK as WAV ({size_kb:.0f} KB) - ffmpeg failed")

            success += 1

        except Exception as e:
            print(f"FAILED - {e}")
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
