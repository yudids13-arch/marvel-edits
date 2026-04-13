/* ===========================
   REELFORGE — APP.JS
   AI-Powered Edit Blueprint Generator
   =========================== */

// ===== SHARED STATE =====
const STATE = {
  clips: [],
  selectedTemplate: 'emotional',
  currentView: 'grid',
  currentFilter: 'all',
  currentCollection: 'all',
  editingClipId: null,
  collections: ['battle', 'emotional', 'highlight']
};

const TEMPLATES = {
  emotional: {
    name: 'Emotional Edit',
    description: 'Slow build, emotional peak at 70%, quiet close',
    pacing: 'Slow → Crescendo → Still',
    cutSpeed: '3–8s early, 1–2s at peak',
    effects: '0.5× slow-mo, soft zoom-in, light contrast lift',
    intensity: 'low'
  },
  comeback: {
    name: 'Comeback Edit',
    description: 'Low point intro, rising action, triumphant close',
    pacing: 'Heavy → Rising → Explosive',
    cutSpeed: '4s intro, 1–2s mid, rapid 0.5s at end',
    effects: 'Speed ramp up, light grain, strong color contrast',
    intensity: 'high'
  },
  sacrifice: {
    name: 'Sacrifice Edit',
    description: 'Weight and consequence framing, slow reveals',
    pacing: 'Deliberate → Heavy → Still',
    cutSpeed: '5–10s held shots, slow-mo on key moments',
    effects: 'Deep desaturation, slow-mo at 40%, single color accent',
    intensity: 'medium'
  },
  rage: {
    name: 'Rage Edit',
    description: 'Rapid escalation, controlled chaos, release',
    pacing: 'Fast → Faster → Peak → Release',
    cutSpeed: '0.5–2s cuts throughout, flash transitions',
    effects: 'Slight overexposure on peak, fast zoom, minimal SFX',
    intensity: 'high'
  },
  hero: {
    name: 'Hero Arc',
    description: 'Origin to power, classic three-act structure',
    pacing: 'Humble → Rising → Mythic',
    cutSpeed: 'Mixed — slow on character, fast on action',
    effects: 'Light vignette, warm grade shift, cinematic bars',
    intensity: 'medium'
  },
  training: {
    name: 'Training Montage',
    description: 'Effort and progress, rhythmic and motivational',
    pacing: 'Steady rhythm, synced to music',
    cutSpeed: 'Beat-synced, 1–3s average',
    effects: 'Slight desaturation, sweat/effort emphasis, speed ramp',
    intensity: 'medium'
  },
  rivalry: {
    name: 'Rivalry',
    description: 'Two forces, contrast and convergence',
    pacing: 'Alternating sides, building collision',
    cutSpeed: 'Cross-cut 2–3s, tighter as tension builds',
    effects: 'Color-coded two characters, opposing angles',
    intensity: 'high'
  },
  custom: {
    name: 'Custom Edit',
    description: 'No preset structure — AI adapts entirely to your description',
    pacing: 'Determined by description',
    cutSpeed: 'Determined by description',
    effects: 'Determined by description',
    intensity: 'variable'
  }
};

// ===== UTILS =====
function generateId() {
  return Math.random().toString(36).substr(2, 9);
}

function formatSize(bytes) {
  if (!bytes) return '';
  const mb = bytes / (1024 * 1024);
  return mb.toFixed(1) + ' MB';
}

function formatDuration(seconds) {
  if (!seconds || isNaN(seconds)) return '--';
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function saveToStorage() {
  const toSave = STATE.clips.map(c => ({
    id: c.id, name: c.name, tags: c.tags,
    collection: c.collection, notes: c.notes,
    size: c.size, duration: c.duration
  }));
  try { localStorage.setItem('reelforge_clips', JSON.stringify(toSave)); } catch(e) {}
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
  initPage();
});

function initPage() {
  const path = window.location.pathname;

  if (path.includes('editor')) {
    initEditor();
  } else if (path.includes('library')) {
    initLibrary();
  } else {
    initHome();
  }
}

// ===== HOME =====
function initHome() {
  const pills = document.querySelectorAll('.template-pill');
  pills.forEach(p => {
    p.addEventListener('click', () => {
      pills.forEach(x => x.classList.remove('active'));
      p.classList.add('active');
    });
  });
}

// ===== EDITOR =====
function initEditor() {
  // Template buttons
  const tmplBtns = document.querySelectorAll('.tmpl-btn');
  tmplBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tmplBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      STATE.selectedTemplate = btn.dataset.template;
    });
  });

  // Char counter
  const desc = document.getElementById('editDesc');
  if (desc) {
    desc.addEventListener('input', () => {
      document.getElementById('charCount').textContent = desc.value.length;
    });
  }

  // Upload zone
  const zone = document.getElementById('uploadZone');
  const fileInput = document.getElementById('fileInput');
  if (zone && fileInput) {
    zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
    zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
    zone.addEventListener('drop', e => {
      e.preventDefault(); zone.classList.remove('dragover');
      handleEditorFiles(e.dataTransfer.files);
    });
    fileInput.addEventListener('change', () => handleEditorFiles(fileInput.files));
  }
}

function handleEditorFiles(files) {
  Array.from(files).forEach(file => {
    if (!file.type.startsWith('video/')) return;
    const clip = {
      id: generateId(),
      name: file.name.replace(/\.[^/.]+$/, ''),
      file: file,
      url: URL.createObjectURL(file),
      size: file.size,
      tags: [],
      collection: 'all',
      notes: '',
      duration: null
    };
    STATE.clips.push(clip);
    addClipToEditorList(clip);
  });
}

function addClipToEditorList(clip) {
  const list = document.getElementById('clipList');
  if (!list) return;

  const item = document.createElement('div');
  item.className = 'clip-item';
  item.dataset.id = clip.id;

  const thumb = document.createElement('div');
  thumb.className = 'clip-thumb';
  const vid = document.createElement('video');
  vid.src = clip.url;
  vid.muted = true;
  vid.preload = 'metadata';
  vid.addEventListener('loadedmetadata', () => {
    clip.duration = vid.duration;
    vid.currentTime = Math.min(1, vid.duration / 2);
  });
  thumb.appendChild(vid);

  const name = document.createElement('div');
  name.className = 'clip-name';
  name.textContent = clip.name;

  const size = document.createElement('div');
  size.className = 'clip-size';
  size.textContent = formatSize(clip.size);

  item.appendChild(thumb);
  item.appendChild(name);
  item.appendChild(size);

  item.addEventListener('click', () => {
    item.classList.toggle('selected');
  });

  list.appendChild(item);
}

// ===== GENERATE BLUEPRINT (AI-Powered) =====
async function generateBlueprint() {
  const desc = document.getElementById('editDesc')?.value?.trim();
  const duration = document.getElementById('duration')?.value;
  const pacing = document.getElementById('pacing')?.value;
  const platform = document.getElementById('platform')?.value;
  const effects = document.getElementById('effects')?.value;
  const template = TEMPLATES[STATE.selectedTemplate];

  if (!desc) {
    alert('Please describe your edit before generating.');
    return;
  }

  const btn = document.getElementById('generateBtn');
  const btnText = document.getElementById('btnText');
  const btnLoader = document.getElementById('btnLoader');

  btn.disabled = true;
  btnText.style.display = 'none';
  btnLoader.style.display = 'inline';

  document.getElementById('outputEmpty').style.display = 'none';
  document.getElementById('outputContainer').style.display = 'block';

  // Show loading skeleton
  showLoadingSkeleton();

  const clipNames = STATE.clips.map(c => c.name).join(', ') || 'No clips uploaded (generate based on description only)';

  const prompt = `You are a professional short-form video editor specializing in cinematic, Marvel-style edits. A user wants you to generate a complete editing blueprint for their video reel.

USER'S CLIPS: ${clipNames}
EDIT TEMPLATE: ${template.name} — ${template.description}
DURATION: ${duration} seconds
PACING: ${pacing}
PLATFORM: ${platform}
EFFECT INTENSITY: ${effects}
USER'S DESCRIPTION: ${desc}

Generate a detailed editing blueprint. Return ONLY valid JSON in exactly this structure:

{
  "title": "Short cinematic title for this edit",
  "template": "${template.name}",
  "timeline": [
    {
      "timestamp": "0:00–0:08",
      "clip": "clip name or description",
      "action": "What happens — cut, hold, transition",
      "emotion": "What feeling this should evoke",
      "notes": "Specific editor instruction"
    }
  ],
  "music": {
    "intro": "When and how music starts",
    "build": "How music builds and where",
    "beatDrop": "Exact timestamp for beat drop",
    "cuts": "How cuts align to rhythm",
    "close": "How music ends"
  },
  "effects": [
    { "timestamp": "time", "effect": "effect name", "description": "how to apply it", "intensity": "subtle/moderate" }
  ],
  "overlays": [
    { "timestamp": "time", "text": "overlay text", "style": "placement and style note" }
  ],
  "caption": "Full social media caption text (2-4 sentences)",
  "hashtags": "#tag1 #tag2 #tag3 (8-12 hashtags)",
  "directorNotes": "3-5 sentences of overall creative direction and key priorities for this edit"
}

Generate at least 6-8 timeline segments. Keep effects subtle and realistic — no heavy glitch, no over-sharpening. Effects like: light slow-mo (0.5x), micro-zoom, soft cuts, basic brightness/contrast. Make overlay text minimal and cinematic.`;

  try {
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1000,
        messages: [{ role: "user", content: prompt }]
      })
    });

    const data = await response.json();
    const raw = data.content.map(i => i.text || '').join('');
    const clean = raw.replace(/```json|```/g, '').trim();
    const blueprint = JSON.parse(clean);
    renderBlueprint(blueprint);

  } catch (err) {
    // Fallback: generate a local blueprint if API fails
    renderBlueprint(generateFallbackBlueprint(desc, template, duration));
  }

  btn.disabled = false;
  btnText.style.display = 'inline';
  btnLoader.style.display = 'none';
}

function showLoadingSkeleton() {
  const sections = ['timelineOutput', 'musicOutput', 'effectsOutput', 'overlaysOutput', 'captionOutput', 'notesOutput'];
  sections.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.innerHTML = `<div class="loading-output">
        <div class="loading-line" style="width:80%"></div>
        <div class="loading-line" style="width:60%"></div>
        <div class="loading-line" style="width:90%"></div>
      </div>`;
    }
  });
}

function generateFallbackBlueprint(desc, template, duration) {
  const dur = parseInt(duration) || 60;
  return {
    title: "Cinematic Edit Blueprint",
    template: template.name,
    timeline: [
      { timestamp: "0:00–0:06", clip: "Opening clip", action: "Slow reveal, fade in from black", emotion: "Anticipation, curiosity", notes: "Hold the first frame 1 second before motion begins. Let the silence breathe." },
      { timestamp: "0:06–0:14", clip: "Character/subject intro", action: "Medium cut sequence, 3–4s each", emotion: "Establishing presence", notes: "Show the subject in their environment. Don't rush." },
      { timestamp: "0:14–0:26", clip: "Rising action clips", action: "Slightly faster cuts, 2–3s each", emotion: "Building tension", notes: "Music should be fully present here. Align each cut to a beat." },
      { timestamp: "0:26–0:34", clip: "Key moment approach", action: "0.5x slow-motion", emotion: "Weight, importance", notes: "This is the pre-drop moment. Slow everything down. Let the audience feel the pause." },
      { timestamp: "0:34–0:42", clip: "Peak action / climax", action: "Rapid cuts 0.5–1s, beat-synced", emotion: "Release, power, emotion", notes: "Beat drop hits here. Cut on every beat. Maximum energy." },
      { timestamp: "0:42–0:52", clip: "Resolution clips", action: "Return to medium pacing 2–3s", emotion: "Reflection, satisfaction", notes: "Let the energy settle. The viewer needs a landing." },
      { timestamp: "0:52–" + formatDuration(dur), clip: "Closing shot", action: "Long hold, slow fade or freeze frame", emotion: "Resonance, memory", notes: "End on your strongest image. Fade to black over 1–2 seconds." }
    ],
    music: {
      intro: "Music begins quietly at 0:02 — ambient or low instrumental layer only",
      build: "Full track enters at 0:08, building consistently to 0:34",
      beatDrop: "0:34 — the single most important moment. All cuts align here.",
      cuts: "Before beat drop: cut to rhythm of melody. At and after beat drop: cut to kick/snare.",
      close: "Music softens at 0:50, final few notes carry the closing shot, fade out with video"
    },
    effects: [
      { timestamp: "0:00–0:06", effect: "Fade In", description: "Simple black to full opacity over 1.5 seconds", intensity: "subtle" },
      { timestamp: "0:26–0:34", effect: "Slow Motion 0.5x", description: "Reduce playback to half speed on the pre-drop moment. No added blur.", intensity: "subtle" },
      { timestamp: "0:34", effect: "Micro Zoom In", description: "1.0x to 1.06x scale over 0.5 seconds on the beat drop cut", intensity: "subtle" },
      { timestamp: "Throughout", effect: "Brightness +10 / Contrast +8", description: "Slight overall lift. Make the footage pop without looking processed.", intensity: "subtle" },
      { timestamp: "0:52–end", effect: "Slow Fade to Black", description: "Gradual opacity fade starting at 0:55, black by end", intensity: "subtle" }
    ],
    overlays: [
      { timestamp: "0:08", text: desc.split(' ').slice(0, 4).join(' ').toUpperCase(), style: "Bottom-left, small tracking font, appears with 0.5s fade-in" },
      { timestamp: "0:34", text: "[ KEY MOMENT ]", style: "Centered, minimal, all-caps, disappears after 2 seconds" },
      { timestamp: "0:54", text: "— End —", style: "Centered, italic, fades in with closing shot" }
    ],
    caption: `This edit captures the essence of ${desc.slice(0, 60)}... A cinematic short-form video built for emotional impact and visual precision. Every cut was intentional.`,
    hashtags: "#edit #cinematic #shortfilm #videoediting #reelforge #fyp #viral #trending #cinemaedits #contentcreator",
    directorNotes: `Focus above all on the moment just before the beat drop — the slow-motion pause at 0:26 is the emotional hinge of this entire edit. If that moment doesn't feel heavy and deliberate, the release at 0:34 won't land. Keep effects minimal and invisible. The best edits feel like they weren't edited at all. Trust the footage and the music to carry the emotion — your job is to get out of the way and let the story breathe. ${template.description}.`
  };
}

function renderBlueprint(b) {
  document.getElementById('outputBadge') && (document.getElementById('outputBadge').textContent = b.template);
  document.getElementById('outputTitle').textContent = b.title || 'Edit Blueprint';
  document.getElementById('outputTemplate') && (document.getElementById('outputTemplate').textContent = b.template);

  // Timeline
  const tl = document.getElementById('timelineOutput');
  if (tl && b.timeline) {
    tl.innerHTML = b.timeline.map(seg => `
      <div class="timeline-entry">
        <div class="timeline-time">${seg.timestamp}</div>
        <div class="timeline-detail">
          <strong>${seg.action}</strong>
          <span>${seg.clip} — <em>${seg.emotion}</em></span>
          <br><span style="color:var(--text3); font-size:12px; margin-top:0.2rem; display:block">${seg.notes}</span>
        </div>
      </div>
    `).join('');
  }

  // Music
  const music = document.getElementById('musicOutput');
  if (music && b.music) {
    music.innerHTML = `
      <div class="output-card"><strong>Intro</strong><p>${b.music.intro}</p></div>
      <div class="output-card"><strong>Build</strong><p>${b.music.build}</p></div>
      <div class="output-card" style="border-color:var(--accent)"><strong>Beat Drop ✦</strong><p>${b.music.beatDrop}</p></div>
      <div class="output-card"><strong>Cut Rhythm</strong><p>${b.music.cuts}</p></div>
      <div class="output-card"><strong>Close</strong><p>${b.music.close}</p></div>
    `;
  }

  // Effects
  const eff = document.getElementById('effectsOutput');
  if (eff && b.effects) {
    eff.innerHTML = b.effects.map(e => `
      <div class="output-card">
        <strong>${e.effect} <span style="font-size:11px; color:var(--text3)">@ ${e.timestamp} — ${e.intensity}</span></strong>
        <p>${e.description}</p>
      </div>
    `).join('');
  }

  // Overlays
  const ov = document.getElementById('overlaysOutput');
  if (ov && b.overlays) {
    ov.innerHTML = b.overlays.map(o => `
      <div class="output-card">
        <strong>"${o.text}" <span style="font-size:11px; color:var(--text3)">@ ${o.timestamp}</span></strong>
        <p>${o.style}</p>
      </div>
    `).join('');
  }

  // Caption
  const cap = document.getElementById('captionOutput');
  if (cap) {
    cap.innerHTML = `
      <div class="caption-box">
        <div>${b.caption}</div>
        <div class="hashtags">${b.hashtags}</div>
      </div>
    `;
  }

  // Notes
  const notes = document.getElementById('notesOutput');
  if (notes && b.directorNotes) {
    notes.innerHTML = `<div class="output-card"><p>${b.directorNotes}</p></div>`;
  }
}

function copyBlueprint() {
  const container = document.getElementById('outputContainer');
  if (!container) return;
  const text = container.innerText;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector('.copy-btn');
    if (btn) { btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = 'Copy All', 2000); }
  });
}

// ===== LIBRARY =====
function initLibrary() {
  const upload = document.getElementById('libUpload');
  if (upload) {
    upload.addEventListener('change', () => handleLibraryFiles(upload.files));
  }
  renderLibrary();
}

function handleLibraryFiles(files) {
  Array.from(files).forEach(file => {
    if (!file.type.startsWith('video/')) return;
    const clip = {
      id: generateId(),
      name: file.name.replace(/\.[^/.]+$/, ''),
      file: file,
      url: URL.createObjectURL(file),
      size: file.size,
      tags: [],
      collection: 'all',
      notes: '',
      duration: null
    };
    STATE.clips.push(clip);
  });
  saveToStorage();
  renderLibrary();
}

function renderLibrary() {
  const count = STATE.clips.length;
  const countEl = document.getElementById('clipCount');
  if (countEl) countEl.textContent = `${count} clip${count !== 1 ? 's' : ''} stored`;

  const empty = document.getElementById('libraryEmpty');
  const grid = document.getElementById('clipGrid');
  const listView = document.getElementById('clipListView');

  if (count === 0) {
    if (empty) empty.style.display = 'block';
    if (grid) grid.style.display = 'none';
    if (listView) listView.style.display = 'none';
    return;
  }

  if (empty) empty.style.display = 'none';

  let filtered = STATE.clips.filter(c => {
    const matchFilter = STATE.currentFilter === 'all' || c.tags.includes(STATE.currentFilter);
    const matchCollection = STATE.currentCollection === 'all' || c.collection === STATE.currentCollection;
    const search = document.getElementById('searchInput')?.value?.toLowerCase() || '';
    const matchSearch = !search || c.name.toLowerCase().includes(search) || c.tags.some(t => t.includes(search));
    return matchFilter && matchCollection && matchSearch;
  });

  if (STATE.currentView === 'grid') {
    if (grid) grid.style.display = 'grid';
    if (listView) listView.style.display = 'none';
    renderGridView(grid, filtered);
  } else {
    if (grid) grid.style.display = 'none';
    if (listView) listView.style.display = 'block';
    renderListView(filtered);
  }
}

function renderGridView(container, clips) {
  if (!container) return;
  container.innerHTML = '';
  clips.forEach(clip => {
    const card = document.createElement('div');
    card.className = 'grid-clip-card';
    card.innerHTML = `
      <div class="grid-clip-preview">
        <video src="${clip.url}" muted preload="metadata" onloadedmetadata="this.currentTime=1"></video>
        <div class="play-overlay">▶</div>
      </div>
      <div class="grid-clip-info">
        <div class="grid-clip-name">${clip.name}</div>
        <div class="grid-clip-tags">
          ${clip.tags.slice(0,3).map(t => `<span class="tag-chip">${t}</span>`).join('')}
          ${clip.tags.length === 0 ? '<span class="tag-chip" style="color:var(--text3)">no tags</span>' : ''}
        </div>
      </div>
    `;
    card.addEventListener('click', () => openClipModal(clip.id));
    container.appendChild(card);
  });
}

function renderListView(clips) {
  const container = document.getElementById('clipListItems');
  if (!container) return;
  container.innerHTML = '';
  clips.forEach(clip => {
    const row = document.createElement('div');
    row.className = 'list-clip-row';
    row.innerHTML = `
      <span class="clip-name">${clip.name}</span>
      <span style="color:var(--text2); font-family:var(--font-mono); font-size:12px">${formatDuration(clip.duration)}</span>
      <span style="color:var(--text2); font-size:12px">${clip.tags.join(', ') || '—'}</span>
      <span style="color:var(--text2); font-size:12px">${clip.collection === 'all' ? '—' : clip.collection}</span>
      <div class="list-actions">
        <button class="list-action-btn" onclick="openClipModal('${clip.id}')">Edit</button>
        <button class="list-action-btn delete" onclick="deleteClip('${clip.id}')">✕</button>
      </div>
    `;
    container.appendChild(row);
  });
}

function openClipModal(id) {
  const clip = STATE.clips.find(c => c.id === id);
  if (!clip) return;

  STATE.editingClipId = id;

  document.getElementById('modalTitle').textContent = clip.name;
  document.getElementById('modalName').value = clip.name;
  document.getElementById('modalTags').value = clip.tags.join(', ');
  document.getElementById('modalCollection').value = clip.collection || 'all';
  document.getElementById('modalNotes').value = clip.notes || '';

  const video = document.getElementById('modalVideo');
  if (video) video.src = clip.url;

  document.getElementById('clipModal').style.display = 'flex';
}

function closeModal(event) {
  if (!event || event.target.classList.contains('modal-overlay') || event.currentTarget.classList.contains('modal-close')) {
    document.getElementById('clipModal').style.display = 'none';
    const video = document.getElementById('modalVideo');
    if (video) video.pause();
  }
}

function saveClipData() {
  const clip = STATE.clips.find(c => c.id === STATE.editingClipId);
  if (!clip) return;

  clip.name = document.getElementById('modalName').value.trim() || clip.name;
  clip.tags = document.getElementById('modalTags').value.split(',').map(t => t.trim().toLowerCase()).filter(Boolean);
  clip.collection = document.getElementById('modalCollection').value;
  clip.notes = document.getElementById('modalNotes').value;

  saveToStorage();
  document.getElementById('clipModal').style.display = 'none';
  const video = document.getElementById('modalVideo');
  if (video) video.pause();
  renderLibrary();
}

function deleteClipFromModal() {
  deleteClip(STATE.editingClipId);
  document.getElementById('clipModal').style.display = 'none';
}

function deleteClip(id) {
  STATE.clips = STATE.clips.filter(c => c.id !== id);
  saveToStorage();
  renderLibrary();
}

function clearLibrary() {
  if (confirm('Clear all clips from the library? This cannot be undone.')) {
    STATE.clips = [];
    saveToStorage();
    renderLibrary();
  }
}

function setFilter(filter, el) {
  STATE.currentFilter = filter;
  document.querySelectorAll('.tag-filter').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  renderLibrary();
}

function setCollection(col, el) {
  STATE.currentCollection = col;
  document.querySelectorAll('.collection-pill').forEach(p => p.classList.remove('active'));
  el.classList.add('active');
  renderLibrary();
}

function setView(view) {
  STATE.currentView = view;
  document.getElementById('gridViewBtn')?.classList.toggle('active', view === 'grid');
  document.getElementById('listViewBtn')?.classList.toggle('active', view === 'list');
  renderLibrary();
}

function filterClips() {
  renderLibrary();
}

function addCollection() {
  const name = prompt('Collection name:');
  if (!name) return;
  const slug = name.toLowerCase().replace(/\s+/g, '_');
  STATE.collections.push(slug);

  const bar = document.querySelector('.collections-bar');
  const addBtn = document.querySelector('.collection-add');
  if (bar && addBtn) {
    const pill = document.createElement('div');
    pill.className = 'collection-pill';
    pill.dataset.collection = slug;
    pill.textContent = name;
    pill.onclick = () => setCollection(slug, pill);
    bar.insertBefore(pill, addBtn);

    const select = document.getElementById('modalCollection');
    if (select) {
      const opt = document.createElement('option');
      opt.value = slug;
      opt.textContent = name;
      select.appendChild(opt);
    }
  }
}
