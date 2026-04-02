#!/usr/bin/env python3
"""Clone voice using Chatterbox via HuggingFace Inference API (fal-ai)."""

import requests
import base64
import subprocess
import os
import sys

AUDIO_DIR = "presentation-audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

HF_TOKEN = os.environ.get("HF_TOKEN", "")
REF_AUDIO = "/tmp/alig-ref.wav"
API_URL = "https://router.huggingface.co/fal-ai/fal-ai/chatterbox/text-to-speech"

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
    10: "So what is you waiting for? Start presenting with proper style! Animated slides! Three.js backgrounds! Zero dependencies! Clone the repository and start creating beautiful presentations today! West side!",
    11: "Did you know this yeah? Over eighty percent of audiences loses attention within the first ten minutes of a traditional slideshow! That is well bad! But Web Presenter changes all of that with immersive animations and interactive experiences! Respect!",
}


def main():
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

    print(f"Loading reference audio: {REF_AUDIO}")
    with open(REF_AUDIO, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()
    ref_data = f"data:audio/wav;base64,{audio_b64}"

    print("\n=== Generating voice-cloned narration (Chatterbox via fal-ai) ===")
    for slide_num, text in NARRATIONS.items():
        print(f"  [CLONE] Slide {slide_num:02d}: generating...")
        try:
            resp = requests.post(API_URL, headers=headers, json={
                "text": text,
                "audio_reference": ref_data,
            }, timeout=120)

            if resp.status_code != 200:
                print(f"  [CLONE] Slide {slide_num:02d}: FAILED - HTTP {resp.status_code}: {resp.text[:200]}")
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
            subprocess.run(
                ["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_path],
                capture_output=True,
            )
            os.remove(wav_path)

            size_kb = os.path.getsize(mp3_path) / 1024
            print(f"  [CLONE] Slide {slide_num:02d}: OK ({size_kb:.0f} KB)")

        except Exception as e:
            print(f"  [CLONE] Slide {slide_num:02d}: FAILED - {e}")

    print("\n=== Done ===")


if __name__ == "__main__":
    main()
