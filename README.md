# Meshy Prompt Forge

> Turns weak 3D prompts into production-ready ones — built to reduce activation drop-off on Meshy.ai.

**Live demo:** [link] | **Case study:** [CASE_STUDY.md](CASE_STUDY.md)

---

## The Problem

Meshy has 6M users but most never convert to paid. The biggest activation killer: prompt sensitivity.

A user types `"a cool sword"`, gets a mediocre mesh, and leaves before the "aha moment."

Public evidence:
- G2 reviewer: *"small wording changes produce wildly different results"*
- Trustpilot: users reporting wasted credits on bad first outputs
- Meshy's own prompt tips doc — companies only write those when support tickets pile up

Text-to-3D is 10x harder to prompt than text-to-image. There's no established mental model for new users. This tool fills that gap.

---

## What It Does

1. Takes a plain-English prompt
2. Applies rules reverse-engineered from Meshy's failure patterns
3. Outputs an optimized prompt + explains every change
4. Scores both generated meshes on objective quality metrics
5. Quantifies the improvement

---

## Key Findings

### Finding 1 — Optimizer produces measurably better geometry on complex objects

**Test: `dragon` vs `3D model of dragon, game-ready stylized asset, organic skin and scales, clean quad topology, isolated object, no background`**

| Metric | Naive `dragon` | Optimized | Delta |
|---|---|---|---|
| Faces | 992,658 | 1,199,452 | **+206,794 (+20.8%)** |
| Vertices | 496,327 | 599,724 | **+103,397 (+20.8%)** |
| Watertight | — | **Yes** | ✅ |
| Holes | — | **0** | ✅ |
| Non-manifold edges | — | **0** | ✅ |
| Printability | ✅ | ✅ | same |

The optimized prompt produced 20% more geometric detail and confirmed clean topology — watertight, zero holes, zero non-manifold edges. These are the exact metrics that matter for rigging, animation, and 3D printing workflows.

The naive prompt generated a recognizable dragon. The optimized prompt generated a better one — measurably, not just visually.

---

### Finding 2 — Minimal impact on simple geometric objects

**Test: `a cool sword` vs optimized prompt**

Both produced recognizable swords. The optimized version was marginally cleaner but the difference was small.

**Why:** Swords are simple, well-represented shapes. Meshy handles them well regardless of prompt quality. Prompt sensitivity is low for simple objects.

**Takeaway:** The optimizer's value scales with object complexity and ambiguity. Characters, creatures, and environments benefit most.

---

### Finding 3 — IP characters need image-to-3D, not text optimization

**Test: `dota 2 sf` (Shadow Fiend)**

Neither naive nor optimized text prompts produced a model resembling Shadow Fiend. The tool correctly identified it as a Dota 2 character and added the right style tags — but Meshy's model doesn't have enough hero-specific training data to reconstruct a specific character from text alone.

**Fix:** Meshy's image-to-3D workflow solves this. The tool now surfaces this recommendation automatically.

**Product insight:** Meshy should route users asking for specific IP characters toward image-to-3D more prominently in the UI.

---

### Finding 4 — Free tier download gating breaks the evaluation loop

While running this experiment, a real friction point surfaced: **the free tier doesn't allow GLB downloads.**

This means free users can generate models but can't export, evaluate, or use them in Blender or game engines. The "try before you buy" loop is broken — users who can't evaluate quality won't upgrade.

This is likely a significant, fixable conversion drag.

---

## Improvements Made During Experiment

### Game IP detection
After testing Dota 2 characters, the rewriter was upgraded to detect known game IPs and apply IP-specific art styles:

```
Input:  dota 2 invoker
Output: 3D model of dota 2 invoker, Dota 2 stylized hero model, 
        Valve art style, detailed armor and fabric, game-ready PBR 
        materials, clean quad topology, isolated object, no background, 
        standing upright in T-pose
```

Supported IPs: Dota 2, League of Legends, Overwatch, Valorant, Fortnite, World of Warcraft, Minecraft, Pokemon.

### Named character recognition
Added a known character list (Shadow Fiend, Invoker, Pudge, Yasuo, Tracer, etc.) so abbreviated or named inputs are correctly detected as characters rather than generic objects.

### Honest routing
When the optimizer detects an IP character, it now flags that image-to-3D is the correct workflow — rather than producing an over-optimized text prompt that still won't work.

---

## Rewriter Rules

Every change is deterministic and explainable — no black-box LLM:

| Rule | Reason |
|---|---|
| Add "3D model of" prefix | Meshy responds better to explicit 3D framing |
| Detect object type | Enables context-aware downstream rules |
| Add style tag | Style-less prompts produce inconsistent results |
| Add material hint | Material ambiguity causes texture inconsistency |
| Add "clean quad topology" | Improves mesh quality for rigging and sculpting |
| Add isolation context | Prevents unwanted scene elements |
| Add T-pose for characters | Critical for rigging compatibility |
| Replace vague adjectives | "cool" → "detailed", "nice" → "well-crafted" |

---

## Mesh Scoring Methodology

Each GLB is scored on 4 objective topology metrics:

| Metric | Weight | Why It Matters |
|---|---|---|
| Watertight | 35 pts | Printability, rigging |
| Is Volume | 25 pts | Manifold + consistent normals |
| Non-manifold edges | 25 pts | Topology quality |
| Degenerate faces | 15 pts | Mesh cleanliness |

Composite score: 0–100. Scoring was blocked on Meshy free tier (no GLB downloads) — infrastructure is built and validated on external GLBs.

---

## Setup

```bash
git clone https://github.com/sanmati1997/meshy-prompt-forge
cd meshy-prompt-forge
pip install -r requirements.txt
```

**Web app:**
```bash
streamlit run app.py
```

**CLI:**
```bash
python run.py rewrite "a cool sword"
python run.py score model.glb
python run.py compare naive.glb optimized.glb
python run.py batch
```

---

## Stack

- Python, trimesh, numpy — mesh scoring
- Streamlit, Plotly — web UI
- Rule-based rewriter — transparent, auditable, no LLM dependency
- Meshy free tier — 3D generation

---

Built by [Sanmati Sawalwade](https://linkedin.com/in/sanmatiwalwade) — MS Information Systems, Northeastern University Silicon Valley  
Email: sawalwade.s@northeastern.edu
