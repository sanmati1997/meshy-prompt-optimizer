# Meshy Prompt Forge

> Turns weak 3D prompts into production-ready ones — built to reduce activation drop-off on Meshy.ai.

**Live demo:** [link] | **Case study:** [CASE_STUDY.md](CASE_STUDY.md) | **Built in:** one night

---

## What It Does

Takes a plain-English prompt → rewrites it using rules reverse-engineered from Meshy's failure patterns → explains every change → scores the generated mesh on objective topology metrics.

```
Input:   "a cool sword"
Output:  "3D model of a detailed sword, game-ready low-poly asset, 
          tempered steel blade, clean quad topology, isolated object, 
          no background"

Changes: 6 — each one explained with a reason
```

---

## Results

### Dragon — +20.8% geometry, clean topology confirmed

| Metric | Naive `dragon` | Optimized | Delta |
|---|---|---|---|
| Faces | 992,658 | 1,199,452 | **+206,794 (+20.8%)** |
| Vertices | 496,327 | 599,724 | **+103,397 (+20.8%)** |
| Watertight | — | **Yes** | ✅ |
| Holes | — | **0** | ✅ |
| Non-manifold edges | — | **0** | ✅ |

### Sword — +29.1% geometry, archetype shift identified

| Metric | Naive `a cool sword` | Optimized | Delta |
|---|---|---|---|
| Faces | 129,400 | 167,050 | **+37,650 (+29.1%)** |
| Vertices | 64,690 | 83,527 | **+18,837 (+29.1%)** |

Naive produced an ornate fantasy longsword. Optimized produced a realistic combat knife. More geometry — but wrong archetype. This exposed a flaw in the material inference logic (see Findings below).

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

### ✅ Finding 1 — Works on complex objects
Optimized dragon prompt produced 20.8% more geometry, confirmed watertight with 0 holes and 0 non-manifold edges. The optimizer adds enough context to push Meshy toward higher-fidelity outputs on ambiguous objects.

### ⚠️ Finding 2 — Material hints can override style intent
"Tempered steel blade" steered Meshy from a fantasy sword to a realistic knife. **Fix needed:** material inference must detect implied style context (fantasy vs realistic) before choosing a hint.

### 🔍 Finding 3 — IP characters need image-to-3D, not text
Neither naive nor optimized prompts produced a recognizable Shadow Fiend. The tool now detects IP characters and routes to image-to-3D automatically.

### 🔍 Finding 4 — Free tier download gating breaks evaluation loop
Free users can generate but can't export GLBs. They can't evaluate quality in Blender or a game engine. The try-before-you-buy loop is broken — likely a fixable conversion drag.

---

## Improvements Built During Experiment

**Game IP detection** — detects Dota 2, LoL, Overwatch, Valorant, Fortnite, WoW, Minecraft, Pokemon and applies IP-specific art styles automatically.

**Named character recognition** — Shadow Fiend, Invoker, Yasuo, Tracer and others correctly detected as characters, not generic objects.

**Image-to-3D routing** — when IP character is detected, tool flags the correct workflow instead of over-optimizing a text prompt that won't work.

---

## Pending Improvements

- [ ] Context-aware material inference (detect fantasy vs realistic from prompt tone before adding material hint)
- [ ] Hero/character database for IP-specific style hints beyond generic "Valve art style"
- [ ] Mesh scoring on Meshy outputs (blocked by free tier download limit — infrastructure is ready)
- [ ] A/B test pipeline to validate rules at scale

---

## How It Works

**Rewriter rules** — deterministic, fully explainable:

| Rule | Reason |
|---|---|
| Add "3D model of" prefix | Meshy responds better to explicit 3D framing |
| Detect object type | Enables context-aware downstream rules |
| Add style tag | Style-less prompts produce inconsistent outputs |
| Add material hint | Material ambiguity causes texture inconsistency |
| Add "clean quad topology" | Improves mesh quality for rigging and sculpting |
| Add isolation context | Prevents unwanted scene elements |
| Add T-pose for characters | Critical for rigging compatibility |
| Replace vague adjectives | "cool" → "detailed", "nice" → "well-crafted" |

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
git clone https://github.com/sanmati1997/meshy-prompt-forge
cd meshy-prompt-forge
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

Built by [Sanmati Sawalwade](https://linkedin.com/in/sanmatiwalwade) — MS Information Systems, Northeastern University Silicon Valley  
sawalwade.s@northeastern.edu
