#!/usr/bin/env python3
"""Generate TTS narration (Edge TTS) and images (HuggingFace) for the presentation."""

import asyncio
import os
import sys

AUDIO_DIR = "presentation-audio"
IMAGE_DIR = "presentation-images"

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# ── Slide narration scripts (Ali G style — energetic, hype) ──
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

# Per-presenter voices (matches presenter mapping in presentation-script.js)
# Valentina (slides 1 & 12), Alex (slides 2 & 11), Sam (slides 3-10)
VOICES = {
    "valentina": {"voice": "en-US-JennyNeural",  "rate": "+0%",   "pitch": "+0Hz"},   # Warm, friendly female — natural speed
    "alex":      {"voice": "en-US-GuyNeural",     "rate": "-10%",  "pitch": "-8Hz"},   # Energetic male voice
    "sam":       {"voice": "en-US-AndrewNeural",  "rate": "+0%",   "pitch": "+0Hz"},   # Confident male voice
}

def get_voice_for_slide(slide_num):
    """Return the voice config dict for a given slide number (1-based)."""
    if slide_num in (1, 12):
        return VOICES["valentina"]
    if slide_num in (2, 11):
        return VOICES["alex"]
    return VOICES["sam"]


# ── Generate TTS audio via Edge TTS ──
async def generate_tts(slide_num, text):
    """Generate TTS using Microsoft Edge TTS (free, high quality)."""
    import edge_tts

    vcfg = get_voice_for_slide(slide_num)
    voice, rate, pitch = vcfg["voice"], vcfg["rate"], vcfg["pitch"]
    print(f"  [TTS] Slide {slide_num:02d}: generating ({voice}, rate={rate}, pitch={pitch})...")
    outpath = os.path.join(AUDIO_DIR, f"slide-{slide_num:02d}.mp3")
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await communicate.save(outpath)
        size_kb = os.path.getsize(outpath) / 1024
        print(f"  [TTS] Slide {slide_num:02d}: OK ({size_kb:.0f} KB)")
        return True
    except Exception as e:
        print(f"  [TTS] Slide {slide_num:02d}: FAILED - {e}")
        return False


async def generate_all_tts():
    """Generate TTS for all slides sequentially."""
    for slide_num, text in NARRATIONS.items():
        await generate_tts(slide_num, text)


# ── Generate images via HuggingFace ──
IMAGE_PROMPTS = {
    "slide-01-hero": "abstract geometric art, rose gold and lavender crystals floating in deep purple space, soft glowing particles, dreamy ethereal atmosphere, minimalist, 4k",
    "slide-02-why": "watercolor illustration of a lightbulb blooming into flowers, rose pink and lavender palette, soft gradient background, creative inspiration concept, elegant minimal",
    "slide-04-constellation": "abstract network of glowing rose gold nodes connected by lavender threads, organic flowing shapes, dark purple background, feminine tech aesthetic, soft bloom lighting",
    "slide-11-stats": "elegant data visualization with flowing curves and circles in rose gold lavender and sage green, dark background, modern infographic style, abstract and beautiful",
}


def generate_image(name, prompt):
    """Generate image using FLUX.1-schnell via HuggingFace."""
    from huggingface_hub import InferenceClient

    HF_TOKEN = os.environ.get("HF_TOKEN", "")
    client = InferenceClient(token=HF_TOKEN)

    print(f"  [IMG] {name}: generating...")
    try:
        image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-schnell",
            width=1024,
            height=576,
        )
        outpath = os.path.join(IMAGE_DIR, f"{name}.png")
        image.save(outpath)
        size_kb = os.path.getsize(outpath) / 1024
        print(f"  [IMG] {name}: OK ({size_kb:.0f} KB)")
        return True
    except Exception as e:
        print(f"  [IMG] {name}: FAILED - {e}")
        return False


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "tts"):
        print("\n=== Generating TTS narration (Edge TTS) ===")
        asyncio.run(generate_all_tts())

    if mode in ("all", "images"):
        print("\n=== Generating images (HuggingFace FLUX) ===")
        for name, prompt in IMAGE_PROMPTS.items():
            generate_image(name, prompt)

    print("\n=== Done ===")
