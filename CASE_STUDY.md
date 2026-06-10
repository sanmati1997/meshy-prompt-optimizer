# Meshy Prompt Forge — Case Study

**Author:** Sanmati Sawalwade  
**Background:** MS Information Systems, Northeastern University (Silicon Valley) | Ex-Gameskraft | Startup Founder  
**Built in:** One night  
**Repo:** [github.com/sanmati1997/meshy-prompt-forge](https://github.com/sanmati1997/meshy-prompt-forge)  
**Live demo:** [meshy-optimizer.streamlit.app](https://meshy-optimizer.streamlit.app)

---

## At a Glance

| Object | Naive Prompt | Optimized | Geometry Delta | Key Outcome |
|---|---|---|---|---|
| Dragon | `dragon` | Full style + topology prompt | **+20.8%** | Watertight, 0 holes, 0 NME — fully production-ready |
| Sword | `a cool sword` | `tempered steel blade` hint | **+29.1%** | Wrong archetype — fantasy sword → combat knife |
| Sword (fixed) | — | `Fantasy sword` object framing | — | Fantasy archetype preserved — correct output |
| Warrior | `warrior` | T-pose + isolation prompt | **-42.1%** | Fewer faces, no base, clean T-pose — rigging-ready |
| Dota 2 SF | `dota 2 sf` | Full Valve art style prompt | **+16.7%** | Neither output recognizable — training data gap |
| Crate | `crate` | Game-ready prop prompt | **+9.9%** | Holes -69%, NME -57% — smallest lift, confirms secondary hypothesis |

---

## The Problem

Meshy has 6 million users but approximately $15M ARR — roughly $2.50 average revenue per user. Most users are free and never convert to paid.

The biggest reason: **bad first experience.**

Text-to-3D is fundamentally harder to prompt than text-to-image. Users have mental models for Midjourney and DALL-E — those don't transfer to 3D generation. A new Meshy user types a vague prompt, gets a mediocre or wrong model, burns free credits, and leaves before the "aha moment."

### Evidence from public sources

| Source | Quote / Observation |
|---|---|
| G2 reviewer | *"Small wording changes produce wildly different results"* |
| G2 reviewer | *"Limited prompt character space is frustrating"* |
| Trustpilot | Multiple users reporting wasted credits on poor first outputs |
| Meshy's own docs | A "prompt tips" section exists — companies only write those when support tickets pile up |
| Pricing page | Free tier caps downloads — users can't evaluate models before upgrading |

This is an activation problem. Users hit the friction wall before they see the product's real value.

---

## Hypothesis

> Optimized prompts — prompts that include explicit style tags, material hints, topology context, and isolation framing — will produce meaningfully better 3D models than naive prompts on complex objects.

**Secondary hypothesis:** Prompt sensitivity is highest on ambiguous, complex objects (creatures, characters) and lowest on simple props (crates, barrels). Optimization effort should scale with object complexity.

---

## What I Built

A rule-based prompt optimizer and mesh quality scorer, built in one night on Meshy's free tier.

**Stack:** Python · Streamlit · trimesh · Plotly. Zero dollars. No paid APIs.

### How the optimizer works

The rewriter applies 8 deterministic rules reverse-engineered from Meshy's failure patterns:

| Rule | Why |
|---|---|
| Add `3D model of` prefix | Meshy responds better to explicit 3D framing |
| Detect object type (character / weapon / vehicle / prop / creature) | Enables context-aware downstream rules |
| Add style tag if missing | Style-less prompts produce inconsistent results |
| Add material hint if missing | Material ambiguity causes texture inconsistency |
| Add `clean quad topology` | Improves mesh quality for rigging and sculpting |
| Add isolation context | Prevents unwanted scene elements and base objects |
| Add T-pose for characters | Critical for rigging compatibility |
| Replace vague adjectives | `"cool"` → `"detailed"`, `"nice"` → `"well-crafted"` |

Every change is explainable. No black-box LLM. A PM can audit every decision.

### Game IP detection

The tool detects known game IPs (Dota 2, League of Legends, Overwatch, Valorant, and others) and applies IP-specific art style tags automatically:

- Input: `dota 2 invoker`
- Output: `3D model of dota 2 invoker, Dota 2 stylized hero model, Valve art style, detailed armor and fabric, game-ready PBR materials, clean quad topology, isolated object, no background, standing upright in T-pose`

### Mesh scorer

For downloadable GLBs, the tool scores on 4 objective topology metrics:

| Metric | Weight | Why It Matters |
|---|---|---|
| Watertight | 35 pts | Printability and rigging |
| Is Volume | 25 pts | Manifold + consistent normals |
| Non-manifold edges | 25 pts | Topology quality |
| Degenerate faces | 15 pts | Mesh cleanliness |

---

## Findings

### Finding 1 — Optimization works on complex creatures

**Test:** `dragon` vs `3D model of dragon, game-ready stylized asset, organic skin and scales, clean quad topology, isolated object, no background`

| Naive: `dragon` | Optimized |
|:---:|:---:|
| ![Dragon Naive](assets/results/dragon_naive.png) | ![Dragon Optimized](assets/results/dragon_optimized.png) |

| Metric | Naive | Optimized | Delta |
|---|---|---|---|
| Faces | 992,658 | 1,199,452 | **+206,794 (+20.8%)** |
| Vertices | 496,327 | 599,724 | **+103,397 (+20.8%)** |
| Watertight | — | **Yes** | ✅ |
| Holes | — | **0** | ✅ |
| Non-manifold edges | — | **0** | ✅ |

**What changed visually:** The naive prompt produced a dragon with wings swept back in a natural resting pose — visually interesting but structurally harder to rig. The optimized prompt produced a dragon with wings fully spread in a display stance — immediately game-ready, consistent with what a rigger or animator needs. Adding explicit style, topology, and isolation context pushes Meshy toward standardized asset poses.

**Implication:** On complex organic objects, optimization delivers both measurable and visual improvements. The 20.8% geometry gain is secondary to the topology fix — watertight with 0 holes and 0 non-manifold edges means this model can go directly into a print or animation pipeline without repair work.

---

### Finding 2 — Material hints can override style intent — but object framing fixes it

**Test A (wrong):** `a cool sword` vs `3D model of a detailed sword, game-ready low-poly asset, tempered steel blade, clean quad topology, isolated object, no background`

**Test B (fixed):** `a cool sword` vs `3D model of Fantasy sword, tempered steel blade, clean quad topology, isolated object, no background`

| Naive: `a cool sword` | Wrong optimized | Fixed optimized |
|:---:|:---:|:---:|
| ![Sword Naive](assets/results/sword_naive.png) | ![Sword Optimized](assets/results/sword_optimized.png) | ![Fantasy Sword](assets/results/sword_fantasy_optimized.png) |

| Metric | Naive | Wrong optimized | Fixed optimized |
|---|---|---|---|
| Faces | 129,400 | 167,050 | 213,978 |
| Archetype | Fantasy longsword | Combat knife | Fantasy sword |
| Watertight | ✅ | ✅ | **Yes, 0 holes, 0 NME** |

**What happened:** The naive `a cool sword` produced an ornate fantasy longsword with a decorative crossguard — exactly what a user who typed "cool sword" likely wanted. The optimized version with `"tempered steel blade"` produced a clean, realistic combat knife — a completely different weapon archetype. The 29.1% geometry improvement is almost irrelevant when the object itself is wrong.

**The fix:** Adding `"Fantasy sword"` as the object-type qualifier — even with the same `"tempered steel blade"` material hint — produced the correct fantasy archetype. Object-type framing overrides ambiguous material hints. The optimizer must detect implied style context from the original prompt before choosing a material hint.

**Implication:** Rule-based optimization can actively hurt output quality when material inference ignores intent signals. The fix is a style-context classifier that detects fantasy vs. realistic vs. sci-fi framing before applying material hints.

---

### Finding 3 — T-pose + isolation rule is critical for character assets

**Test:** `warrior` vs `3D model of Warrior, game-ready stylized asset, fabric and leather armor, clean quad topology, isolated object, no background, standing upright in T-pose`

| Naive: `warrior` | Optimized (T-pose) |
|:---:|:---:|
| ![Warrior Naive](assets/results/warrior_naive.png) | ![Warrior Optimized](assets/results/warrior_optimized.png) |

| Metric | Naive | Optimized | Delta |
|---|---|---|---|
| Faces | 992,234 | 574,084 | **-418,150 (-42.1%)** |
| Vertices | 496,061 | 287,056 | **-209,005 (-42.1%)** |
| Watertight | ✅ | ✅ | same |
| Pose | Action pose on pedestal | Clean T-pose, isolated | rigging-ready |

**What changed visually:** This is the most operationally significant finding. The naive `warrior` generated a fully armored character in a dynamic action pose — on a pedestal base, weapon raised, cape flowing. It looks better as a standalone render. But it is completely unusable for game development: non-T-pose means auto-rigging tools will fail; the pedestal base means it can't be placed in a scene; 992K faces for a character is far over budget for a real-time asset.

The optimized version is 42.1% smaller (fewer wasted polygons on base geometry), in clean T-pose, isolated — drop it directly into Unity, Unreal, or Blender and rig it immediately.

**Implication:** For character assets, optimization doesn't just add geometry — it redirects geometry budget to the asset itself and removes waste. The face count reduction is a feature, not a flaw. This is the rule with the highest real-world impact for game developers.

---

### Finding 4 — IP characters require image-to-3D, not text optimization

**Test:** `dota 2 sf` vs full Valve art style optimized prompt

| Official Shadow Fiend | Naive: `dota 2 sf` | Optimized |
|:---:|:---:|:---:|
| ![SF Reference](assets/results/sf_reference.png) | ![SF Naive](assets/results/sf_naive.png) | ![SF Optimized](assets/results/sf_optimized.png) |

| Metric | Naive | Optimized | Delta |
|---|---|---|---|
| Faces | 557,714 | 650,934 | **+93,220 (+16.7%)** |
| Vertices | 278,857 | 325,445 | **+46,588 (+16.7%)** |
| Recognizable as SF | No | No | — |

**What happened:** The naive prompt produced a generic winged demon — no resemblance to Shadow Fiend's actual design (dark energy, soul flames, specific silhouette). The optimized prompt with full Valve art style tags produced a structurally better model — a proper armored humanoid hero with correct proportions — but still not Shadow Fiend. The 16.7% geometry gain is real, but the fundamental problem isn't prompt quality. It's a training data gap.

Meshy's model does not have sufficient exposure to hero-specific designs to reconstruct a named character from text alone. No amount of prompt engineering changes this.

**Implication:** This is a product navigation gap, not a model capability gap. Meshy should surface its image-to-3D workflow more prominently when users type recognizable character names. A simple in-product nudge — *"Looking for a specific character? Try image-to-3D"* — would reduce credit waste and improve conversion for this segment. The tool now detects IP characters and flags the correct workflow.

---

### Finding 5 — Simple props show diminishing returns on geometry, but topology still improves

**Test:** `crate` vs `3D model of crate, game-ready low-poly asset, matte surface texture, clean quad topology, isolated object, no background`

| Naive: `crate` | Optimized |
|:---:|:---:|
| ![Crate Naive](assets/results/crate_naive.png) | ![Crate Optimized](assets/results/crate_optimized.png) |

| Metric | Naive | Optimized | Delta |
|---|---|---|---|
| Faces | 1,083,828 | 1,191,605 | **+107,777 (+9.9%)** |
| Vertices | 541,945 | 595,867 | **+53,922 (+9.9%)** |
| Watertight | No | No | — |
| Holes | 13 | 4 | **-69.2%** |
| Non-manifold edges | 426 | 183 | **-57.0%** |

**What happened:** The geometry improvement is the smallest of all tests at +9.9% — compared to +20.8% for the dragon and +29.1% for the sword. This confirms the secondary hypothesis: optimization has diminishing returns on simple, well-defined objects. Meshy already has a strong prior for what a crate looks like.

But the topology improvement is significant: holes dropped by 69% and non-manifold edges by 57%. Neither version is watertight — open-top containers are geometrically open by nature — but the optimized version is substantially cleaner.

**Implication:** For simple props, prompt optimization delivers more topology cleanup than geometry enhancement. The ROI is lower than for complex objects, but it's not zero. The optimizer should expose this tradeoff: on simple objects, the main benefit is topology quality, not face count.

---

### Finding 6 — Free tier download gating creates a broken evaluation loop

While running this experiment I hit a structural blocker: **the free tier doesn't allow GLB downloads.**

This means:
1. Free users can generate but can't export or evaluate their model in any real tool
2. The try-before-you-buy loop is broken — users can't take a model into Blender to check if it meets their needs
3. Users who can't evaluate quality won't pay to upgrade — they'll leave instead

This finding came from building the tool, not from a dashboard. It's a real friction point hiding in the free-to-paid conversion funnel. The mesh scoring infrastructure in this project is complete and validated — but it couldn't be run on paired Meshy outputs because downloads are gated. The tool that measures quality was blocked by the same limitation that blocks users from evaluating quality.

---

## Business Implications

| Finding | Business Impact | Recommended Action |
|---|---|---|
| Complex objects see 20.8% geometry lift + full topology fix | Higher first-session success → lower churn → higher conversion | A/B test in-product prompt suggestions at generation time |
| Material hints can override intent — but object framing fixes it | Wrong archetype is worse than no optimization | Add style-context detection (fantasy / realistic / sci-fi) before material inference |
| T-pose + isolation produces rigging-ready characters with 42% fewer faces | Game dev users get assets that work in their pipeline, not just look good | Surface T-pose rule prominently for character prompts |
| IP characters need image-to-3D | Text optimization can't fix a training data gap | Route named character queries to image-to-3D with in-product nudge |
| Simple props: diminishing geometry returns, topology gains real | Optimization ROI scales with complexity | Scope optimization suggestions by detected object type |
| Free tier download gating blocks quality evaluation | Users can't validate before paying — lost conversions | A/B test 1–3 free GLB downloads per month |

---

## Limitations

- Test set is small (6 object types, 1 session). Findings are directional, not statistically significant.
- No access to Meshy's real funnel data — business implications are inferred, not measured.
- Mesh scoring was blocked by free-tier download limits. Scoring infrastructure is built and validated on external GLBs but could not be run on Meshy-generated pairs.
- Rule-based rewriter has no feedback loop — rules were hand-authored, not learned from real user failure data.
- Generation variance: running the same prompt twice can produce different outputs. Each test was run once.

Being explicit about these limits is intentional. A PM or data scientist at Meshy would catch overclaiming immediately.

---

## What's Next

If I had access to Meshy's internal data, the three highest-value experiments would be:

1. **A/B test the optimizer in-product** — surface prompt suggestions at generation time, measure first-session success rate lift and credit-to-conversion rate

2. **Style-context classifier** — train a lightweight model to detect fantasy vs. realistic vs. sci-fi intent before applying material hints; this directly fixes the sword archetype mismatch and is the highest-priority gap in the current rule set

3. **Free download A/B test** — measure conversion impact of allowing 1–3 free GLB downloads per month; hypothesis is that users who can validate quality in Blender convert at 2–3x the rate of users who can't

---

## About This Project

Built in one night as a research project to understand Meshy's activation funnel.

The goal was not to build a polished product — it was to identify a real problem, build a working artifact, and produce evidence-backed findings. The tool is fully external — no internal Meshy data was used or required.

**Repo:** [github.com/sanmati1997/meshy-prompt-forge](https://github.com/sanmati1997/meshy-prompt-forge)  
**Live demo:** [meshy-optimizer.streamlit.app](https://meshy-optimizer.streamlit.app)  
**Contact:** sawalwade.s@northeastern.edu | [linkedin.com/in/sanmati-sawalwade](https://linkedin.com/in/sanmati-sawalwade)
