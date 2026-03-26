# Web Presenter

An interactive, narrated presentation framework built with HTML, CSS, and Three.js. No build step required.

## Features

- **Animated Slides** — Smooth CSS transitions with phased element animations
- **Audio Narration** — Per-slide MP3 narration with Web Audio API reverb
- **Background Music** — Looping background track with automatic ducking
- **Three.js Background** — Animated network topology with hex grid, ripples, and data streams
- **Touch & Keyboard** — Arrow keys, space, swipe gestures, and click navigation
- **Auto-advance** — Slides advance automatically when narration ends
- **Progress Indicators** — Dot navigation, slide counter, and audio progress bar
- **Multiple Layouts** — Title, center, two-column, dashboard, and more
- **Dark Theme** — Terminal-inspired design with CSS custom properties
- **Zero Dependencies** — No npm, no build step. Just HTML files.

## Quick Start

```bash
git clone https://github.com/user/web-presenter.git
cd web-presenter
python3 -m http.server 8000
# Open http://localhost:8000
```

## Customization

### Adding Slides

Each slide is a `<section class="slide">` element. Available layout classes:

- `slide-title-layout` — Centered title with icon
- `slide-center-layout` — Centered content
- `slide-two-col` — Two-column grid
- `slide-two-col-reverse` — Reversed two-column

### Audio Narration

Place MP3 files in `presentation-audio/`:
- `slide-01.mp3` through `slide-NN.mp3` for per-slide narration
- `bg-music.mp3` for background music

### Theming

Edit CSS custom properties in `presentation-styles.css`:

```css
:root {
  --bg: #0a0a0f;
  --cyan: #67e8f9;
  --purple: #a78bfa;
  --text: #e8e8e8;
  /* ... */
}
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Arrow Right / Space | Next slide |
| Arrow Left | Previous slide |
| A | Toggle narration |
| M | Toggle music |

## Deploy to GitHub Pages

1. Push to a GitHub repository
2. Go to Settings > Pages
3. Set source to "main" branch, root directory
4. Your presentation is live!

## License

MIT
