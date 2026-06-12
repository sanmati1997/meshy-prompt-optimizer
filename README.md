# Meshy Prompt Optimizer

> Turns weak 3D prompts into production-ready ones - built to reduce activation drop-off on Meshy.ai.

**[Live demo](https://meshy-optimizer.streamlit.app)** | **[Case study](CASE_STUDY.md)** | Built in one night

---

## What It Does

Takes a plain-English prompt → rewrites it using patterns reverse-engineered from Meshy's failure patterns → explains every change → scores the generated mesh on objective topology metrics.

```
Input:   "a cool sword"
Output:  "3D model of Fantasy sword, enchanted steel blade,
          clean quad topology, isolated object, no background"

Changes: 5 — each one explained with a reason
```

---

## Results

### Dragon — +20.8% geometry, topology fully confirmed

| Naive: `dragon` | Optimized |
|:---:|:---:|
| ![Dragon Naive](assets/results/dragon_naive.png) | ![Dragon Optimized](assets/results/dragon_optimized.png) |

| Metric | Naive | Optimized | Delta |
|---|---|---|---|
| Faces | 992,658 | 1,199,452 | **+20.8%** |
| Watertight | — | **Yes** | ✅ |
| Holes | — | **0** | ✅ |
| Non-manifold edges | — | **0** | ✅ |

---

### Sword — material inference risk identified and fixed

| Naive: `a cool sword` | Wrong optimized | Fixed optimized |
|:---:|:---:|:---:|
| ![Sword Naive](assets/results/sword_naive.png) | ![Sword Optimized](assets/results/sword_optimized.png) | ![Fantasy Sword](assets/results/sword_fantasy_optimized.png) |

`"tempered steel blade"` overrode the fantasy intent → combat knife instead of longsword. Fix: explicit object-type framing (`"Fantasy sword"`) preserves the archetype. **Object framing beats material hints.**

---

### Warrior — T-pose + isolation produces rigging-ready assets

| Naive: `warrior` | Optimized (T-pose) |
|:---:|:---:|
| ![Warrior Naive](assets/results/warrior_naive.png) | ![Warrior Optimized](assets/results/warrior_optimized.png) |

| Metric | Naive | Optimized | Delta |
|---|---|---|---|
| Faces | 992,234 | 574,084 | **-42.1%** |
| Pose | Action pose on pedestal | Clean T-pose, isolated | rigging-ready |
| Watertight | ✅ | ✅ | same |

Fewer faces = fewer wasted polygons on base geometry. Optimization redirected the budget to the character mesh itself.

---

### Dota 2 SF — IP characters need image-to-3D, not text optimization

| Official art | Naive: `dota 2 sf` | Optimized |
|:---:|:---:|:---:|
| ![SF Reference](assets/results/sf_reference.png) | ![SF Naive](assets/results/sf_naive.png) | ![SF Optimized](assets/results/sf_optimized.png) |

Optimized prompt produced a better hero structure (+16.7% geometry), but neither output is Shadow Fiend. This is a training data gap — no prompt fixes it. The tool now detects IP characters and routes to image-to-3D.

---

### Crate — diminishing returns on simple props, topology still improves

| Naive: `crate` | Optimized |
|:---:|:---:|
| ![Crate Naive](assets/results/crate_naive.png) | ![Crate Optimized](assets/results/crate_optimized.png) |

| Metric | Naive | Optimized | Delta |
|---|---|---|---|
| Faces | 1,083,828 | 1,191,605 | **+9.9%** |
| Holes | 13 | 4 | **-69.2%** |
| Non-manifold edges | 426 | 183 | **-57.0%** |

Smallest geometry lift of all tests — confirms the secondary hypothesis. Simple objects benefit less. But topology cleanup is still real.

---

## The Problem

Meshy has 6M users but most never convert to paid. The biggest activation killer: prompt sensitivity.

Text-to-3D is 10x harder to prompt than text-to-image. New users have no mental model for it — they type one word, get a mediocre mesh, burn free credits, and leave before the "aha moment."

**Evidence:**
- G2: *"small wording changes produce wildly different results"*
- Trustpilot: users reporting wasted credits on bad first outputs
- Meshy's own prompt tips doc — companies only write those when support tickets pile up

---

## Key Findings

### ✅ Finding 1 — Optimization works best on complex objects
Dragon: +20.8% geometry, watertight, 0 holes, 0 non-manifold edges. Patterns push Meshy toward production-ready outputs on ambiguous objects.

### ⚠️ Finding 2 — Material hints can override style intent
`"tempered steel blade"` turned a fantasy sword into a combat knife. Fix: use explicit object-type framing to preserve intent before adding material hints.

### ✅ Finding 3 — T-pose + isolation is the highest-impact pattern for characters
`warrior` naive: 992K faces on a pedestal. Optimized: 574K faces, T-pose, no base — 42% smaller and actually usable in a game engine.

### 🔍 Finding 4 — IP characters can't be reproduced from text alone
Neither prompt produced a recognizable Shadow Fiend. The tool now detects IP characters and flags the image-to-3D workflow.

### 📊 Finding 5 — Simple props: smaller geometry lift, topology gains still real
Crate: only +9.9% geometry improvement vs. +20.8% for the dragon. But holes dropped 69%, non-manifold edges dropped 57%.

### 🔍 Finding 6 — Free tier download gating breaks the evaluation loop
Free users can generate but can't export. They can't validate quality before paying. The try-before-you-buy loop is broken.

---

## How It Works

**Rewriter patterns** — deterministic, fully explainable:

| Pattern | Reason |
|---|---|
| Add `3D model of` prefix | Meshy responds better to explicit 3D framing |
| Detect object type | Enables context-aware downstream patterns |
| Add style tag | Style-less prompts produce inconsistent outputs |
| Add material hint | Material ambiguity causes texture inconsistency |
| Add `clean quad topology` | Improves mesh quality for rigging and sculpting |
| Add isolation context | Prevents unwanted scene elements and base objects |
| Add T-pose for characters | Critical for rigging compatibility |
| Replace vague adjectives | `"cool"` → `"detailed"`, `"nice"` → `"well-crafted"` |

**Mesh scorer** — 4 objective topology metrics:

| Metric | Weight |
|---|---|
| Watertight | 35 pts |
| Is Volume | 25 pts |
| Non-manifold edges | 25 pts |
| Degenerate faces | 15 pts |

---

## Setup

```bash
git clone https://github.com/sanmati1997/meshy-prompt-optimizer
cd meshy-prompt-optimizer
pip install -r requirements.txt
streamlit run app.py
```

**CLI:**
```bash
python run.py rewrite "a cool sword"
python run.py score model.glb
python run.py compare naive.glb optimized.glb
```

**Stack:** Python · trimesh · Streamlit · Plotly · Meshy free tier · $0

---

Built by [Sanmati Sawalwade](https://linkedin.com/in/sanmati-sawalwade) — MS Information Systems, Northeastern University Silicon Valley  
sawalwade.s@northeastern.edu
