# Web Presenter — Task Runner
# https://github.com/casey/just

# Default: list available recipes
default:
    @just --list

# Serve locally on port 8000 (or specify PORT=XXXX)
serve port="8000":
    @echo "Serving at http://localhost:{{port}}"
    python3 -m http.server {{port}}

# Open in default browser and serve
open port="8000":
    @open "http://localhost:{{port}}" 2>/dev/null || xdg-open "http://localhost:{{port}}" 2>/dev/null || echo "Open http://localhost:{{port}} in your browser"
    python3 -m http.server {{port}}

# Install dependencies (just python3 check + optional live-reload)
setup:
    @echo "Checking dependencies..."
    @which python3 > /dev/null 2>&1 && echo "  python3 ✓" || echo "  python3 ✗ — install Python 3"
    @which git > /dev/null 2>&1 && echo "  git ✓" || echo "  git ✗ — install git"
    @echo ""
    @echo "Optional: install live-reload server"
    @echo "  npm install -g live-server"
    @echo ""
    @echo "Ready! Run 'just serve' to start."

# Serve with live-reload (requires: npm i -g live-server)
live port="8000":
    @which live-server > /dev/null 2>&1 || (echo "Install first: npm install -g live-server" && exit 1)
    live-server --port={{port}} --no-browser

# Deploy to GitHub Pages (push main branch)
deploy:
    git push origin main
    @echo "Deployed! Check GitHub Pages settings if not yet enabled."

# Create a new slide (appended before closing </div> of presentation)
new-slide name="new":
    @echo 'Add this to index.html before the closing </div><!-- presentation -->:'
    @echo ''
    @echo '    <!-- ============ SLIDE: {{name}} ============ -->'
    @echo '    <section class="slide" data-index="N">'
    @echo '      <div class="slide-content slide-center-layout">'
    @echo '        <h2 class="slide-heading">{{name}}</h2>'
    @echo '        <p class="slide-body">Your content here.</p>'
    @echo '      </div>'
    @echo '    </section>'
    @echo ''
    @echo 'Remember to: update slide count, add a progress dot, and add audio file.'

# Validate all referenced assets exist
check:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Checking assets..."
    errors=0
    for f in presentation-styles.css presentation-script.js presentation-bg.js three.min.js; do
        if [ -f "$f" ]; then echo "  $f ✓"; else echo "  $f ✗ MISSING"; errors=$((errors+1)); fi
    done
    echo ""
    echo "Checking audio files..."
    for f in presentation-audio/bg-music.mp3 $(ls presentation-audio/slide-*.mp3 2>/dev/null); do
        if [ -f "$f" ]; then echo "  $f ✓"; else echo "  $f ✗ MISSING"; errors=$((errors+1)); fi
    done
    echo ""
    echo "Checking images..."
    for f in $(ls presentation-images/* 2>/dev/null); do
        echo "  $f ✓"
    done
    echo ""
    if [ $errors -gt 0 ]; then echo "$errors missing file(s)!"; exit 1; else echo "All assets present."; fi

# Show file sizes for deployment planning
size:
    @echo "File sizes:"
    @echo ""
    @du -sh . | awk '{print "  Total: " $1}'
    @echo ""
    @du -sh *.html *.css *.js 2>/dev/null | awk '{print "  " $2 ": " $1}'
    @echo ""
    @du -sh presentation-audio/ 2>/dev/null | awk '{print "  audio/: " $1}'
    @du -sh presentation-images/ 2>/dev/null | awk '{print "  images/: " $1}'

# Clean generated / temp files
clean:
    rm -f .DS_Store **/.DS_Store
    @echo "Cleaned."
