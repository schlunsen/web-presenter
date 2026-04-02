// ========================================
// NAVIGATION
// ========================================
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
const counter = document.getElementById('slide-counter');
const prevBtn = document.getElementById('nav-prev');
const nextBtn = document.getElementById('nav-next');
let currentSlide = 0;
const totalSlides = slides.length;
let isTransitioning = false;

function goToSlide(index, direction) {
  direction = direction || 'next';
  if (index < 0 || index >= totalSlides || index === currentSlide || isTransitioning) return;
  isTransitioning = true;
  var current = slides[currentSlide];
  var next = slides[index];
  current.classList.remove('slide-active', 'slide-exit-left');
  next.classList.remove('slide-active', 'slide-exit-left');
  if (direction === 'next') {
    next.style.transform = 'translateX(60px)';
    next.style.opacity = '0';
    current.classList.add('slide-exit-left');
  } else {
    next.style.transform = 'translateX(-60px)';
    next.style.opacity = '0';
    current.style.transform = 'translateX(60px)';
    current.style.opacity = '0';
  }
  current.classList.remove('slide-active');
  void next.offsetWidth;
  next.style.transform = '';
  next.style.opacity = '';
  next.classList.add('slide-active');
  dots[currentSlide].classList.remove('active');
  dots[index].classList.add('active');
  counter.textContent = (index + 1) + ' / ' + totalSlides;
  currentSlide = index;
  triggerSlideAnimations(index);
  if (typeof window.__playSlideAudio === 'function') window.__playSlideAudio(index);
  setTimeout(function() {
    isTransitioning = false;
    current.classList.remove('slide-exit-left');
    current.style.transform = '';
    current.style.opacity = '';
  }, 650);
}

function nextSlide() { if (currentSlide < totalSlides - 1) goToSlide(currentSlide + 1, 'next'); }
function prevSlide() { if (currentSlide > 0) goToSlide(currentSlide - 1, 'prev'); }

document.addEventListener('keydown', function(e) {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') { e.preventDefault(); nextSlide(); }
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); prevSlide(); }
});
nextBtn.addEventListener('click', nextSlide);
prevBtn.addEventListener('click', prevSlide);
dots.forEach(function(dot, i) {
  dot.addEventListener('click', function() { goToSlide(i, i > currentSlide ? 'next' : 'prev'); });
});

var touchStartX = 0, touchStartY = 0;
document.addEventListener('touchstart', function(e) { touchStartX = e.touches[0].clientX; touchStartY = e.touches[0].clientY; }, { passive: true });
document.addEventListener('touchend', function(e) {
  var dx = e.changedTouches[0].clientX - touchStartX, dy = e.changedTouches[0].clientY - touchStartY;
  if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 50) { if (dx < 0) nextSlide(); else prevSlide(); }
}, { passive: true });

// ========================================
// SLIDE ANIMATIONS
// ========================================
function animateCount(el, target, duration) {
  var startTime = performance.now();
  function update(now) {
    var progress = Math.min((now - startTime) / duration, 1);
    el.textContent = Math.round(target * (1 - Math.pow(1 - progress, 3)));
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

function triggerSlideAnimations(index) {
  var slide = slides[index];
  if (index === 1) slide.querySelectorAll('.philosophy-point').forEach(function(p, i) { setTimeout(function() { p.classList.add('visible'); }, 400 + i * 300); });
  if (index === 3) {
    slide.classList.remove('phase-intro', 'phase-settled');
    slide.querySelectorAll('.agent-orbital').forEach(function(n) { n.classList.remove('visible'); });
    slide.classList.add('phase-intro');
    setTimeout(function() {
      slide.classList.remove('phase-intro'); slide.classList.add('phase-settled');
      slide.querySelectorAll('.agent-orbital').forEach(function(n, i) { setTimeout(function() { n.classList.add('visible'); }, 1200 + i * 2000); });
    }, 4000);
  }
  if (index === 4) {
    // Zoom-Through Pipeline: badges zoom from dots, shockwaves fire, cards materialize
    var ztTitle = slide.querySelector('.zt-title');
    var badges = slide.querySelectorAll('.zt-badge');
    var shockwaves = slide.querySelectorAll('.zt-shockwave');
    var bodies = slide.querySelectorAll('.zt-card-body');
    var connectors = slide.querySelectorAll('.zt-connector-line');

    // Reset all state for re-entry
    if (ztTitle) ztTitle.classList.remove('visible');
    badges.forEach(function(b) { b.classList.remove('zoom-in'); });
    shockwaves.forEach(function(s) { s.classList.remove('fire'); });
    bodies.forEach(function(b) { b.classList.remove('materialize'); });
    connectors.forEach(function(c) { c.classList.remove('draw'); });
    void slide.offsetWidth; // force reflow

    // Card 1: dot → badge → shockwave → card materializes
    setTimeout(function() { badges[0].classList.add('zoom-in'); }, 400);
    setTimeout(function() { shockwaves[0].classList.add('fire'); }, 650);
    setTimeout(function() { bodies[0].classList.add('materialize'); }, 900);

    // Connector 1 draws
    setTimeout(function() { connectors[0].classList.add('draw'); }, 1400);

    // Card 2: same sequence
    setTimeout(function() { badges[1].classList.add('zoom-in'); }, 1800);
    setTimeout(function() { shockwaves[1].classList.add('fire'); }, 2050);
    setTimeout(function() { bodies[1].classList.add('materialize'); }, 2300);

    // Connector 2 draws
    setTimeout(function() { connectors[1].classList.add('draw'); }, 2800);

    // Card 3: same sequence
    setTimeout(function() { badges[2].classList.add('zoom-in'); }, 3200);
    setTimeout(function() { shockwaves[2].classList.add('fire'); }, 3450);
    setTimeout(function() { bodies[2].classList.add('materialize'); }, 3700);

    // Title fades in LAST — content first, label last
    setTimeout(function() { if (ztTitle) ztTitle.classList.add('visible'); }, 4500);
  }
  if (index === 5) {
    slide.querySelectorAll('.loop-node').forEach(function(n, i) { setTimeout(function() { n.classList.add('visible'); }, 200 + i * 200); });
    var r = slide.querySelector('.loop-repeat'); if (r) setTimeout(function() { r.classList.add('visible'); }, 1200);
    slide.querySelectorAll('.docker-container').forEach(function(c, i) { setTimeout(function() { c.classList.add('visible'); }, 400 + i * 150); });
  }
  if (index === 6) slide.querySelectorAll('.timeline-event').forEach(function(e, i) { setTimeout(function() { e.classList.add('visible'); }, 300 + i * 200); });
  if (index === 7) slide.querySelectorAll('.dash-row:not(.header)').forEach(function(r, i) { setTimeout(function() { r.classList.add('visible'); }, 300 + i * 200); });
  if (index === 8) slide.querySelectorAll('.severity-item').forEach(function(s, i) { setTimeout(function() { s.classList.add('visible'); }, 200 + i * 150); });
  // Slide 10 (index 9): IMPACT stagger + count + bars
  if (index === 9) {
    slide.querySelectorAll('.stagger-item').forEach(function(el) { el.classList.remove('visible'); });
    slide.querySelectorAll('.impact-bar-fill').forEach(function(el) { el.style.width = '0%'; });
    slide.querySelectorAll('.stagger-item').forEach(function(item) {
      var delay = parseInt(item.dataset.stagger || 0) * 600 + 300;
      setTimeout(function() {
        item.classList.add('visible');
        item.querySelectorAll('[data-count]').forEach(function(n) { animateCount(n, parseInt(n.dataset.count), 1500); });
        item.querySelectorAll('.impact-bar-fill').forEach(function(bar, bi) {
          setTimeout(function() { bar.style.width = bar.dataset.width + '%'; }, 200 + bi * 300);
        });
      }, delay);
    });
  }
}
triggerSlideAnimations(0);

// ========================================
// AUDIO NARRATION (overlap-safe)
// ========================================
var audioToggle = document.getElementById('audio-toggle');
var volumeSlider = document.getElementById('volume-slider');
var audioProgressBar = document.getElementById('audio-progress-bar');
var audioEnabled = true, audioVolume = 0.8, currentAudio = null, audioProgressInterval = null;
var slideAudioCache = {};
var activeFadeIntervals = [];  // track all fade intervals so we can kill them
var pendingTimer = null;
var audioGeneration = 0;  // increments on every playSlideAudio call; stale callbacks check this

function preloadAllAudio() {
  for (var i = 0; i < totalSlides; i++) {
    var audio = new Audio();
    audio.preload = 'auto';
    audio.src = 'presentation-audio/slide-' + String(i + 1).padStart(2, '0') + '.mp3';
    audio.volume = audioVolume;
    (function(idx, a) {
      a.addEventListener('error', function() { delete slideAudioCache[idx]; });
      a.addEventListener('canplaythrough', function() { slideAudioCache[idx] = a; }, { once: true });
      slideAudioCache[idx] = a;
    })(i, audio);
  }
}
preloadAllAudio();

function cancelAllFades() {
  for (var i = 0; i < activeFadeIntervals.length; i++) {
    clearInterval(activeFadeIntervals[i]);
  }
  activeFadeIntervals = [];
}

function fadeAudio(audio, to, dur, cb) {
  var from = audio.volume;
  if (from === to) { if (cb) cb(); return; }
  var steps = 25, stepVal = (to - from) / steps, iv = dur / steps;
  var t = setInterval(function() {
    audio.volume = Math.max(0, Math.min(1, audio.volume + stepVal));
    if ((stepVal > 0 && audio.volume >= to - 0.01) || (stepVal < 0 && audio.volume <= to + 0.01)) {
      audio.volume = Math.max(0, Math.min(1, to));
      clearInterval(t);
      var idx = activeFadeIntervals.indexOf(t);
      if (idx !== -1) activeFadeIntervals.splice(idx, 1);
      if (to === 0) audio.pause();
      if (cb) cb();
    }
  }, iv);
  activeFadeIntervals.push(t);
}

// Hard-stop every audio element immediately — no fade, no delay
function killAllAudio() {
  cancelAllFades();
  if (pendingTimer) { clearTimeout(pendingTimer); pendingTimer = null; }
  if (audioProgressInterval) { clearInterval(audioProgressInterval); audioProgressInterval = null; }
  Object.values(slideAudioCache).forEach(function(a) {
    if (!a.paused) { a.pause(); }
    a.currentTime = 0;
    a.volume = audioVolume;
  });
  currentAudio = null;
  audioProgressBar.style.width = '0%';
}

function stopCurrentAudio() {
  killAllAudio();
}

function playSlideAudio(si) {
  // Immediately kill everything — no overlap possible
  killAllAudio();
  audioGeneration++;
  var gen = audioGeneration;

  if (!audioEnabled) return;
  var nextA = slideAudioCache[si];
  if (!nextA) return;

  // Small delay before starting new audio for a clean transition
  pendingTimer = setTimeout(function() {
    pendingTimer = null;
    if (gen !== audioGeneration) return;  // stale — user already navigated again
    startAudio(nextA, si, gen);
  }, 600);
}

function startAudio(audio, si, gen) {
  if (!audioEnabled || gen !== audioGeneration) return;

  // Safety: make sure nothing else is playing
  Object.values(slideAudioCache).forEach(function(a) {
    if (a !== audio && !a.paused) { a.pause(); a.currentTime = 0; }
  });

  audio.currentTime = 0;
  currentAudio = audio;
  audio.volume = 0;
  audio.play().catch(function() {});
  fadeAudio(audio, audioVolume, 600);

  audioProgressInterval = setInterval(function() {
    if (gen !== audioGeneration) { clearInterval(audioProgressInterval); return; }
    if (audio.duration && !audio.paused) {
      audioProgressBar.style.width = ((audio.currentTime / audio.duration) * 100) + '%';
    }
  }, 200);

  audio.addEventListener('ended', function() {
    if (gen !== audioGeneration) return;
    audioProgressBar.style.width = '100%';
    setTimeout(function() {
      if (gen !== audioGeneration) return;
      audioProgressBar.style.width = '0%';
    }, 500);
    if (audioProgressInterval) { clearInterval(audioProgressInterval); audioProgressInterval = null; }
  }, { once: true });

  audio.addEventListener('ended', function() {
    if (gen !== audioGeneration) return;  // don't auto-advance if user already moved
    if (audioEnabled && si < totalSlides - 1) {
      setTimeout(function() {
        if (gen !== audioGeneration) return;
        goToSlide(si + 1, 'next');
      }, 1200);
    }
  }, { once: true });
}

audioToggle.addEventListener('click', function() {
  audioEnabled = !audioEnabled;
  audioToggle.classList.toggle('muted', !audioEnabled);
  if (!audioEnabled) stopCurrentAudio(); else playSlideAudio(currentSlide);
});
volumeSlider.addEventListener('input', function() {
  audioVolume = parseInt(volumeSlider.value) / 100;
  if (currentAudio && !currentAudio.paused) currentAudio.volume = audioVolume;
  if (audioVolume === 0) { audioToggle.classList.add('muted'); audioEnabled = false; }
  else if (!audioEnabled) { audioEnabled = true; audioToggle.classList.remove('muted'); }
});
document.addEventListener('keydown', function(e) { if (e.key === 'a' || e.key === 'A') audioToggle.click(); });
window.__playSlideAudio = playSlideAudio;

// ========================================
// BACKGROUND MUSIC
// ========================================
var bgMusic = new Audio('presentation-audio/background-music.mp3');
bgMusic.loop = true;
bgMusic.volume = 0;
bgMusic.preload = 'auto';
var bgMusicEnabled = true;
var bgMusicBaseVolume = 0.08;  // quiet background level
var bgMusicDuckedVolume = 0.03;  // duck when narration plays
var musicToggle = document.getElementById('music-toggle');

function fadeBgMusic(to, dur) {
  var from = bgMusic.volume, steps = 20, stepVal = (to - from) / steps, iv = dur / steps;
  var t = setInterval(function() {
    bgMusic.volume = Math.max(0, Math.min(1, bgMusic.volume + stepVal));
    if ((stepVal > 0 && bgMusic.volume >= to - 0.005) || (stepVal < 0 && bgMusic.volume <= to + 0.005) || stepVal === 0) {
      bgMusic.volume = Math.max(0, Math.min(1, to));
      clearInterval(t);
    }
  }, iv);
}

function startBgMusic() {
  if (!bgMusicEnabled) return;
  bgMusic.volume = 0;
  bgMusic.play().catch(function() {});
  fadeBgMusic(bgMusicBaseVolume, 1500);
}

function duckBgMusic() {
  if (!bgMusic.paused) fadeBgMusic(bgMusicDuckedVolume, 400);
}

function unduckBgMusic() {
  if (!bgMusic.paused) fadeBgMusic(bgMusicBaseVolume, 800);
}

// Duck when narration plays, unduck when it ends
var _origStartAudio = startAudio;
startAudio = function(audio, si, gen) {
  duckBgMusic();
  audio.addEventListener('ended', function() { if (gen === audioGeneration) unduckBgMusic(); }, { once: true });
  _origStartAudio(audio, si, gen);
};

musicToggle.addEventListener('click', function() {
  bgMusicEnabled = !bgMusicEnabled;
  musicToggle.classList.toggle('muted', !bgMusicEnabled);
  if (!bgMusicEnabled) {
    fadeBgMusic(0, 400);
    setTimeout(function() { bgMusic.pause(); }, 500);
  } else {
    startBgMusic();
  }
});

document.addEventListener('keydown', function(e) { if (e.key === 'm' || e.key === 'M') musicToggle.click(); });

// ========================================
// PRESENTER AVATAR (audio-reactive)
// ========================================
var presenterBubble = document.getElementById('presenter-bubble');
var presenterA = document.getElementById('presenter-a');
var presenterB = document.getElementById('presenter-b');
var presenterName = document.getElementById('presenter-name');
var audioCtx = null, analyser = null, analyserData = null;
var mouthAnimFrame = null;
var connectedSources = new WeakMap();

// Slide-to-presenter mapping: slides 1-2 = A, slides 3-11 = B
function getPresenter(slideIndex) {
  return slideIndex < 2 ? 'a' : 'b';
}

function showPresenter(slideIndex) {
  var who = getPresenter(slideIndex);
  if (who === 'a') {
    presenterA.style.display = ''; presenterB.style.display = 'none';
    presenterName.textContent = 'Alex';
  } else {
    presenterA.style.display = 'none'; presenterB.style.display = '';
    presenterName.textContent = 'Sam';
  }
  presenterBubble.classList.add('visible');
}

function hidePresenter() {
  presenterBubble.classList.remove('visible', 'speaking');
  stopMouthAnimation();
}

function ensureAudioContext() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioCtx.createAnalyser();
    analyser.fftSize = 256;
    analyser.smoothingTimeConstant = 0.6;
    analyserData = new Uint8Array(analyser.frequencyBinCount);
  }
  if (audioCtx.state === 'suspended') audioCtx.resume();
}

function connectAudioToAnalyser(audio) {
  ensureAudioContext();
  if (!connectedSources.has(audio)) {
    var source = audioCtx.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(audioCtx.destination);
    connectedSources.set(audio, source);
  }
}

function startMouthAnimation(slideIndex) {
  stopMouthAnimation();
  var who = getPresenter(slideIndex);
  var svgEl = who === 'a' ? presenterA : presenterB;
  var mouth = svgEl.querySelector('.presenter-mouth');
  if (!mouth) return;

  presenterBubble.classList.add('speaking');

  function animate() {
    analyser.getByteFrequencyData(analyserData);
    // Focus on voice frequencies (roughly bins 4-20 for speech fundamentals)
    var sum = 0, count = 0;
    for (var i = 3; i < 20; i++) { sum += analyserData[i]; count++; }
    var avg = sum / count;
    var level = Math.min(avg / 140, 1); // 0..1

    // Animate mouth: scale ry (height) based on audio level
    var minRy = 1.5, maxRy = 8;
    var ry = minRy + level * (maxRy - minRy);
    // Also shift cy slightly for open mouth effect
    var cy = 78 + level * 2;
    mouth.setAttribute('ry', ry.toFixed(1));
    mouth.setAttribute('cy', cy.toFixed(1));
    // Also slightly widen mouth when open
    var rx = 8 + level * 3;
    mouth.setAttribute('rx', rx.toFixed(1));

    mouthAnimFrame = requestAnimationFrame(animate);
  }
  mouthAnimFrame = requestAnimationFrame(animate);
}

function stopMouthAnimation() {
  if (mouthAnimFrame) { cancelAnimationFrame(mouthAnimFrame); mouthAnimFrame = null; }
  presenterBubble.classList.remove('speaking');
  // Reset mouths to closed
  var mouths = document.querySelectorAll('.presenter-mouth');
  mouths.forEach(function(m) { m.setAttribute('ry', '1.5'); m.setAttribute('rx', '8'); m.setAttribute('cy', '78'); });
}

// Hook into startAudio to drive the avatar
var _origStartAudioForPresenter = startAudio;
startAudio = function(audio, si, gen) {
  showPresenter(si);
  connectAudioToAnalyser(audio);
  // Start mouth animation once audio is actually playing
  var onPlay = function() {
    if (gen === audioGeneration) startMouthAnimation(si);
  };
  audio.addEventListener('playing', onPlay, { once: true });
  audio.addEventListener('ended', function() {
    if (gen === audioGeneration) {
      stopMouthAnimation();
      // Hide after a delay (unless next slide starts)
      setTimeout(function() {
        if (gen === audioGeneration) hidePresenter();
      }, 2000);
    }
  }, { once: true });
  _origStartAudioForPresenter(audio, si, gen);
};

// Hide presenter when audio is toggled off
var _origStopForPresenter = killAllAudio;
killAllAudio = function() {
  stopMouthAnimation();
  _origStopForPresenter();
};

// ========================================
// PLAY OVERLAY
// ========================================
var playOverlay = document.getElementById('play-overlay');
var playOverlayBtn = document.getElementById('play-overlay-btn');
function beginPresentation() { playOverlay.classList.add('hidden'); startBgMusic(); playSlideAudio(0); }

(function() {
  var t = new Audio('presentation-audio/slide-01.mp3'); t.volume = 0;
  var p = t.play();
  if (p) p.then(function() { t.pause(); t.src = ''; beginPresentation(); }).catch(function() { t.src = ''; playOverlay.classList.remove('hidden'); });
})();

playOverlayBtn.addEventListener('click', beginPresentation);
document.addEventListener('keydown', function sk(e) {
  if (!playOverlay.classList.contains('hidden') && (e.key === 'Enter' || e.key === ' ')) {
    e.preventDefault(); beginPresentation(); document.removeEventListener('keydown', sk);
  }
});
