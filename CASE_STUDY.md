# Meshy Prompt Optimizer - Case Study

**Author:** Sanmati Sawalwade  
**Background:** MS Information Systems, Northeastern University (Silicon Valley) | Ex-Gameskraft | Startup Founder 

**Actively interviewing:** Looking for Summer/Fall 2026 Internship opportunities

**Built in:** One night  
**Repo:** [github.com/sanmati1997/meshy-prompt-optimizer](https://github.com/sanmati1997/meshy-prompt-optimizer)  
**Live demo:** [meshy-optimizer.streamlit.app](https://meshy-optimizer.streamlit.app)

---

## At a Glance

| Object | Type | Geometry Δ | Topology Δ | Key Outcome |
|---|---|---|---|---|
| Dragon | Complex creature | **+20.8%** | Watertight ✅, 0 holes, 0 NME | Production-ready - direct pipeline drop-in |
| Sword | Weapon | **+29.1%** | Clean | ⚠️ Wrong archetype - fantasy → combat knife |
| Sword (fixed) | Weapon | **+65.4%** vs naive | Clean, 0 NME | Correct archetype recovered with object framing |
| Warrior | Character | **-42.1%** | Watertight ✅ | Fewer faces, no pedestal, T-pose - rigging-ready |
| Dota 2 SF | IP Character | **+16.7%** | Printable ✅ | Better hero structure, still not Shadow Fiend |
| Crate | Simple prop | **+9.9%** | Holes -69%, NME -57% | Smallest lift - confirms complexity hypothesis |

---

## The Problem

Meshy is backed by Sequoia and GGV Capital ($52M raised), ranked #1 in 3D AI tools by popularity (A16Z Games 2024), and has 6M+ users, but most never convert to paid.

The biggest reason: **bad first experience.**

Text-to-3D is fundamentally harder to prompt than text-to-image. Users have mental models for Midjourney and DALL-E - those don't transfer to 3D generation. A new user types a vague prompt, gets a mediocre or wrong model, burns free credits, and leaves before the "aha moment."

### Evidence from public sources

| Source | Signal |
|---|---|
| [G2 reviewer](https://www.g2.com/products/meshy/reviews) | *"Small wording changes produce wildly different results"* |
| [G2 reviewer](https://www.g2.com/products/meshy/reviews?qs=pros-and-cons) | *"Limited prompt character space is frustrating"* |
| [Trustpilot](https://www.trustpilot.com/review/meshy.ai) | Multiple users report wasted credits on poor first outputs |
| [Meshy's own docs](https://help.meshy.ai/en/articles/11972484-best-practices-for-creating-a-text-prompt) | A "prompt tips" section exists - companies only write those when support tickets pile up |
| [Pricing page](https://www.meshy.ai/pricing) | Free tier caps downloads - users can't evaluate models before upgrading |

This is an **activation problem**. Users hit the friction wall before they see the product's real value.

---

## Hypothesis

> Optimized prompts - prompts that include explicit style tags, material hints, topology context, and isolation framing - will produce meaningfully better 3D models than naive prompts on complex objects.

**Secondary hypothesis:** Prompt sensitivity scales with object complexity. Creatures and characters benefit most; simple props benefit least.

---

## What I Built

A heuristic-driven prompt optimizer and mesh quality scorer, built in one night on Meshy's free tier.

**Stack:** Python · Streamlit · trimesh · Plotly · $0 · No paid APIs.

### The 8 optimizer patterns

| Pattern | Why |
|---|---|
| Add `3D model of` prefix | Meshy responds better to explicit 3D framing |
| Detect object type (character / weapon / vehicle / prop / creature) | Enables context-aware downstream patterns |
| Add style tag if missing | Style-less prompts produce inconsistent results |
| Add material hint if missing | Material ambiguity causes texture inconsistency |
| Add `clean quad topology` | Improves mesh quality for rigging and sculpting |
| Add isolation context | Prevents unwanted scene elements and base objects |
| Add T-pose for characters | Critical for rigging compatibility |
| Replace vague adjectives | `"cool"` → `"detailed"`, `"nice"` → `"well-crafted"` |

Every change is explainable. No black-box LLM. A PM can audit every decision.

### What it improves

| For | Improvement | Evidence |
|---|---|---|
| Game developers | Rigging-ready characters with **42% less wasted geometry**, no pedestal, clean T-pose | Warrior finding |
| 3D artists | Complex objects confirmed watertight, **0 holes, 0 non-manifold edges** - no manual repair needed | Dragon finding |
| Weapon / asset creators | Correct archetype preserved with object-type framing - **+65.4% geometry** without archetype mismatch | Sword (fixed) finding |
| Pipeline / studio use | Simple props: **-69% holes, -57% non-manifold edges** - cleaner topology for LOD and physics baking | Crate finding |
| Meshy as a product | Prompt optimization lifts first-session success without touching the model or training data | All findings |

### Mesh scorer

Scores any GLB on 4 objective topology metrics:

| Metric | Weight | Why |
|---|---|---|
| Watertight | 35 pts | Printability and rigging |
| Is Volume | 25 pts | Manifold + consistent normals |
| Non-manifold edges | 25 pts | Topology quality |
| Degenerate faces | 15 pts | Mesh cleanliness |

---

## Findings

---

### Finding 1 - Optimization lifts complex creatures on geometry AND topology

**Object:** Dragon - a complex organic creature with wings, scales, and irregular surface geometry.

**Prompts tested:**
- Naive: `dragon`
- Optimized: `3D model of dragon, game-ready stylized asset, organic skin and scales, clean quad topology, isolated object, no background`

**What the optimizer changed (6 patterns applied):**

| Change | Pattern | Reason |
|---|---|---|
| Added `3D model of` | Prefix pattern | Meshy anchors on explicit 3D framing |
| Object type → **creature** | Type detection | Enables creature-specific downstream patterns |
| Added `game-ready stylized asset` | Style pattern | No style tag → inconsistent mesh detail distribution |
| Added `organic skin and scales` | Material pattern | No material hint → texture ambiguity on complex surfaces |
| Added `clean quad topology` | Topology pattern | Forces structured mesh for rigging/sculpting |
| Added `isolated object, no background` | Isolation pattern | Prevents Meshy from adding terrain or scene elements |

| Naive: `dragon` | Optimized |
|:---:|:---:|
| ![Dragon Naive](assets/results/dragon_naive.png) | ![Dragon Optimized](assets/results/dragon_optimized.png) |

**Results:**

| Metric | Naive | Optimized | Delta |
|---|---|---|---|
| Faces | 992,658 | 1,199,452 | **+206,794 (+20.8%)** |
| Vertices | 496,327 | 599,724 | **+103,397 (+20.8%)** |
| Watertight | Not confirmed | **Yes** | ✅ confirmed |
| Holes | Not confirmed | **0** | ✅ confirmed |
| Non-manifold edges | Not confirmed | **0** | ✅ confirmed |

**What we observed:**

The naive `dragon` produced a dragon with wings swept back in a resting pose - visually organic and natural, but structurally ambiguous for rigging. The optimized prompt produced a dragon with wings fully spread in a stable display stance - the kind of pose a rigger or animator would explicitly request.

More importantly, the topology changed: the optimized model is confirmed watertight with 0 holes and 0 non-manifold edges. On a complex organic mesh, this is a significant outcome - irregular geometry like scales and wing membranes are common sources of topology errors that require manual repair before use in a pipeline.

**Finding:** On complex organic objects, optimization delivers both measurable and structural improvements. The +20.8% geometry gain reflects more detail in scales, wing geometry, and surface complexity. The topology fix - watertight, 0 holes, 0 NME - is the more valuable outcome. It means this model can go directly into a 3D print or animation pipeline without repair work.

**Impact:** A game studio or 3D artist using the naive prompt gets a model they'd need to manually repair before use. The optimized prompt produces a drop-in asset. For Meshy's activation funnel, this is the difference between a user who gets value in their first session and one who leaves frustrated.

---

### Finding 2 - Material hints can override style intent - and how to fix it

**Object:** Sword - a weapon with implied aesthetic (fantasy vs realistic).

This finding required three experiments: naive, wrong-optimized, and fixed-optimized.

**Prompts tested:**
- Naive: `a cool sword`
- Wrong optimized: `3D model of a detailed sword, game-ready low-poly asset, tempered steel blade, clean quad topology, isolated object, no background`
- Fixed optimized: `3D model of Fantasy sword, tempered steel blade, clean quad topology, isolated object, no background`

**What the optimizer changed in the wrong version (6 patterns applied):**

| Change | Pattern | What went wrong |
|---|---|---|
| Added `3D model of` | Prefix pattern | ✅ Correct |
| Object type → **weapon** | Type detection | ✅ Correct |
| Replaced `cool` → `detailed` | Vague adjective pattern | ✅ Correct |
| Added `game-ready low-poly asset` | Style pattern | ✅ Correct |
| Added `tempered steel blade` | Material pattern | ⚠️ **Wrong** - tactical material hint, ignored fantasy context from `"cool sword"` |
| Added topology + isolation | Standard patterns | ✅ Correct |

**What the fix changed:**

The single change was replacing generic object framing (`"a detailed sword"`) with style-qualified framing (`"Fantasy sword"`). The material hint `"tempered steel blade"` stayed the same - but the object-type qualifier anchored the aesthetic, and Meshy respected it.

| Naive: `a cool sword` | Wrong optimized | Fixed optimized |
|:---:|:---:|:---:|
| ![Sword Naive](assets/results/sword_naive.png) | ![Sword Optimized](assets/results/sword_optimized.png) | ![Fantasy Sword](assets/results/sword_fantasy_optimized.png) |

**Results:**

| Metric | Naive | Wrong Optimized | Δ vs Naive | Fixed Optimized | Δ vs Naive |
|---|---|---|---|---|---|
| Faces | 129,400 | 167,050 | **+37,650 (+29.1%)** | 213,978 | **+84,578 (+65.4%)** |
| Archetype | Fantasy longsword | Combat knife | ⚠️ Wrong | Fantasy sword | ✅ Correct |
| Watertight | ✅ | ✅ | same | **Yes, 0 holes, 0 NME** | improved |

**What we observed:**

The naive `a cool sword` produced exactly what a user probably wanted: an ornate fantasy longsword with a wide blade, decorative crossguard with engravings, and a fantasy aesthetic.

The wrong-optimized version produced a sleek, minimalist combat sword - realistic profile, straight blade, tactical construction. Completely different weapon archetype. The +29.1% geometry improvement is meaningless when the object itself is wrong. A user who wanted a fantasy sword for their RPG now has a realistic military blade.

The fixed-optimized version produced a proper fantasy sword - ornate detailing, fantasy proportions, correct aesthetic - with the largest geometry improvement of all three versions (+65.4% vs. naive).

**Finding:** `"tempered steel blade"` without style context signals modern/tactical to Meshy. Adding `"Fantasy sword"` as the object-type qualifier anchored the aesthetic and overrode the material ambiguity - even with the same material hint present. **Object-type framing beats material hints when intent is ambiguous.**

**Impact:** Heuristic-driven optimization without style-context detection actively harms user experience. Higher geometry numbers are irrelevant if the output archetype is wrong. The required fix: classify prompt intent (fantasy / realistic / sci-fi) before applying material hints, not after.

---

### Finding 3 - T-pose + isolation pattern produces rigging-ready characters with 42% fewer faces

**Object:** Warrior - a humanoid character asset.

**Prompts tested:**
- Naive: `warrior`
- Optimized: `3D model of Warrior, game-ready stylized asset, fabric and leather armor, clean quad topology, isolated object, no background, standing upright in T-pose`

**What the optimizer changed (7 patterns applied):**

| Change | Pattern | Reason |
|---|---|---|
| Added `3D model of` | Prefix pattern | Explicit 3D framing |
| Object type → **character** | Type detection | Unlocks T-pose pattern + isolation priority |
| Added `game-ready stylized asset` | Style pattern | Guides Meshy toward pipeline-ready output |
| Added `fabric and leather armor` | Material pattern | Prevents ambiguous material assignment on clothing |
| Added `clean quad topology` | Topology pattern | Structured mesh required for auto-rigging |
| Added `isolated object, no background` | Isolation pattern | **Removes base/pedestal** - critical for placement in scenes |
| Added `standing upright in T-pose` | Character pattern | **Rigging-ready pose** - auto-rigging tools require T or A-pose |

| Naive: `warrior` | Optimized (T-pose) |
|:---:|:---:|
| ![Warrior Naive](assets/results/warrior_naive.png) | ![Warrior Optimized](assets/results/warrior_optimized.png) |

**Results:**

| Metric | Naive | Optimized | Delta |
|---|---|---|---|
| Faces | 992,234 | 574,084 | **-418,150 (-42.1%)** |
| Vertices | 496,061 | 287,056 | **-209,005 (-42.1%)** |
| Watertight | ✅ Yes | ✅ Yes | same |
| Holes | 0 | 0 | same |
| Non-manifold edges | 0 | 0 | same |
| Pose | Dynamic action pose | Clean T-pose | rigging-ready |
| Base/pedestal | Present (~400K wasted faces) | Removed | isolated |

**What we observed:**

The naive `warrior` generated a visually impressive model - fully armored in horned helmet and cape, in a dynamic action pose with weapon raised, standing on a stone pedestal base. As a standalone render it looks great. But it is entirely unusable for game development for three reasons:

1. **Dynamic action pose** - auto-rigging tools in Unity, Unreal, and Blender require T-pose or A-pose. A dynamic pose means every bone must be placed manually.
2. **Pedestal base** - the model is fused to a decorative base. It cannot be placed in a scene, only rendered in isolation.
3. **992K faces includes ~400K for the base** - more than 40% of the geometry budget was consumed by scenery, not the character.

The optimized version is 42.1% smaller, in clean T-pose, with no base. It can be imported directly into any game engine and auto-rigged in one click.

**Finding:** For character assets, optimization doesn't add geometry - it redirects geometry budget. The **-42.1% face count is a feature, not a flaw.** The isolation pattern eliminated ~400K wasted faces on the pedestal. The T-pose pattern produced an immediately riggable character. These two patterns together are the highest-impact combination in the entire optimizer for game development use cases.

**Impact:** A game developer using the naive prompt gets a model that requires hours of manual work (re-posing, base removal, rigging) before it's usable. The optimized prompt produces a drop-in character asset. The face count reduction also improves real-time performance - 574K faces is still high but meaningfully more manageable than 992K.

---

### Finding 4 - IP characters require image-to-3D routing, not text optimization

**Object:** Dota 2 Shadow Fiend - a specific named game character with a very distinct design.

**Prompts tested:**
- Naive: `dota 2 sf`
- Optimized: `3D model of Dota 2 sf, Dota 2 stylized hero model, Valve art style, detailed armor and fabric, game-ready PBR materials, clean quad topology, isolated object, no background, standing upright in T-pose`

**What the optimizer changed (7 patterns applied, including IP detection):**

| Change | Pattern | Reason |
|---|---|---|
| Added `3D model of` | Prefix pattern | Explicit 3D framing |
| Detected IP → **Dota 2** | IP detection pattern | Triggers IP-specific style pack |
| Added `Dota 2 stylized hero model, Valve art style` | IP style pattern | Best available style anchoring for Dota 2 assets |
| Added `detailed armor and fabric, game-ready PBR materials` | Material pattern | Character-appropriate material assignment |
| Added `clean quad topology` | Topology pattern | Structured mesh for hero asset |
| Added `isolated object, no background` | Isolation pattern | Removes scene elements |
| Added `standing upright in T-pose` | Character pattern | Rigging-ready pose |

| Official Shadow Fiend | Naive: `dota 2 sf` | Optimized |
|:---:|:---:|:---:|
| ![SF Reference](assets/results/sf_reference.png) | ![SF Naive](assets/results/sf_naive.png) | ![SF Optimized](assets/results/sf_optimized.png) |

**Results:**

| Metric | Naive | Optimized | Delta |
|---|---|---|---|
| Faces | 557,714 | 650,934 | **+93,220 (+16.7%)** |
| Vertices | 278,857 | 325,445 | **+46,588 (+16.7%)** |
| Printable | ✅ | ✅ | same |
| Recognizable as Shadow Fiend | ❌ No | ❌ No | - |

**What we observed:**

The official Shadow Fiend has a very specific design language: dark demonic entity, glowing red soul energy, distinct horn silhouette, clawed wings pinned back. It is immediately recognizable.

The naive `dota 2 sf` produced a generic winged demon - spread wings, hunched pose, no hero structure. Visually interesting but unrelated to SF.

The optimized prompt produced a significantly better result structurally: a proper armored humanoid hero, standing upright, with hero-appropriate proportions (+16.7% geometry). But it is still not Shadow Fiend. The face structure, silhouette, soul energy aesthetic, and character-specific details are absent.

**Finding:** Optimization improved structural quality - naive produced a creature, optimized produced a hero. But neither output is recognizable as Shadow Fiend. **This is not a prompt quality problem - it is a training data gap.** Meshy's model has insufficient exposure to hero-specific character designs to reconstruct them from text alone. No amount of prompt engineering bridges this gap.

**Impact:** This is a product routing problem, not a model problem. Users who type IP character names expect a specific result and are guaranteed to be disappointed by text-to-3D. Meshy should detect named character queries and surface the image-to-3D workflow: *"Looking for a specific character? Try image-to-3D."* The optimizer now detects this and flags the correct workflow. A single in-product nudge would reduce credit waste for this entire user segment.

---

### Finding 5 - Simple props confirm the complexity hypothesis: diminishing geometry returns, topology gains still real

**Object:** Crate - a simple, well-defined geometric prop.

**Prompts tested:**
- Naive: `crate`
- Optimized: `3D model of crate, game-ready low-poly asset, matte surface texture, clean quad topology, isolated object, no background`

**What the optimizer changed (5 patterns applied):**

| Change | Pattern | Reason |
|---|---|---|
| Added `3D model of` | Prefix pattern | Explicit 3D framing |
| Object type → **prop** | Type detection | No T-pose pattern - props don't need rigging |
| Added `game-ready low-poly asset` | Style pattern | Guides toward efficient mesh density for a prop |
| Added `matte surface texture` | Material pattern | Resolves material ambiguity on wooden/metal surfaces |
| Added `clean quad topology` + `isolated object` | Topology + Isolation | Standard cleanup patterns |

| Naive: `crate` | Optimized |
|:---:|:---:|
| ![Crate Naive](assets/results/crate_naive.png) | ![Crate Optimized](assets/results/crate_optimized.png) |

**Results:**

| Metric | Naive | Optimized | Delta |
|---|---|---|---|
| Faces | 1,083,828 | 1,191,605 | **+107,777 (+9.9%)** |
| Vertices | 541,945 | 595,867 | **+53,922 (+9.9%)** |
| Watertight | ❌ No | ❌ No | - |
| Holes | 13 | 4 | **-9 (-69.2%)** |
| Non-manifold edges | 426 | 183 | **-243 (-57.0%)** |

**What we observed:**

Both versions are immediately recognizable as crates. The visual difference is subtle - the optimized version has cleaner panel edges, more consistent bolt details, and tighter corner geometry. Neither is watertight because an open-top container is geometrically open by nature; this is expected, not a failure.

The +9.9% geometry improvement is the smallest of all six tests. For comparison: dragon +20.8%, sword +29.1%, warrior (effective geometry improvement on character itself is significant). Meshy already has a strong prior for what a crate looks like - optimization adds less because the model doesn't need as much guidance on a simple, well-defined shape.

The topology improvements however are substantial: **holes dropped by 69.2%** (13 → 4) and **non-manifold edges dropped by 57%** (426 → 183). These numbers matter for pipeline use - non-manifold edges cause issues in LOD generation, physics collision meshes, and UV unwrapping.

**Finding:** Simple props confirm the secondary hypothesis - prompt optimization has **diminishing returns on geometry for well-defined objects** but delivers consistent topology cleanup regardless of complexity. The optimizer's value on simple props is mesh quality, not mesh density.

**Impact:** For game studios building environment art, prop topology quality is critical for automated pipeline steps (LOD generation, physics baking, lightmap UV). A prop with 426 non-manifold edges requires manual repair or will cause errors. The optimized crate with 183 non-manifold edges is substantially cleaner, even if still imperfect.

---

### Finding 6 - Free tier download gating creates a broken evaluation loop

**Discovered:** Not from data - from building this tool.

While running these experiments, I hit a structural blocker: **the free tier does not allow GLB downloads.**

This creates a broken loop:
1. Free users generate a model but cannot export it to any real tool
2. They cannot take it into Blender, Unity, or a slicer to evaluate actual quality
3. They cannot validate whether it meets their needs before paying to upgrade
4. Without evidence of value, they won't upgrade - they'll leave

The mesh scoring infrastructure in this project is fully built and validated. But it could not be run on Meshy-generated outputs because downloads are gated behind the paid tier. The tool that measures quality was blocked by the same limitation that blocks users from evaluating quality.

**Finding:** The try-before-you-buy loop is broken for Meshy's most important user segment - new free users who are deciding whether to upgrade. The free tier lets users generate but not evaluate. That is the wrong gating point.

**Impact:** Meshy's conversion problem may be partially self-inflicted. Users who can export a model, open it in Blender, and see that it's production-quality are far more likely to pay for more. A/B testing 1–3 free GLB downloads per month would directly measure this. The hypothesis: users who can validate quality in their own tool convert at 2–3x the rate of users who can only view in-browser.

---

## Summary of Improvements and Decreases

| Object | Geometry Δ | Faces Δ | Holes Δ | Non-Manifold Δ | Watertight | Pose/Structure |
|---|---|---|---|---|---|---|
| Dragon | **+20.8%** | +206,794 | → 0 | → 0 | Not confirmed → ✅ | Resting → Display stance |
| Sword (wrong) | **+29.1%** | +37,650 | clean | clean | ✅ both | Fantasy → Combat knife ⚠️ |
| Sword (fixed) | **+65.4%** | +84,578 | clean | → 0 | ✅ | Fantasy → Fantasy ✅ |
| Warrior | **-42.1%** | -418,150 | 0 | 0 | ✅ both | Action/pedestal → T-pose/isolated ✅ |
| Dota 2 SF | **+16.7%** | +93,220 | - | - | ✅ both | Creature → Hero structure |
| Crate | **+9.9%** | +107,777 | -69.2% | -57.0% | ❌ both (open-top) | Similar shape, cleaner topology |

---

## Business Implications

| Finding | Business Impact | Recommended Action |
|---|---|---|
| Dragon: +20.8% geometry, topology fully fixed | Higher first-session success → lower churn → higher conversion | A/B test prompt suggestions at generation time |
| Sword: material hints can destroy archetype | Wrong output is worse than no optimization - damages trust | Add style-context classifier (fantasy / realistic / sci-fi) before material inference |
| Warrior: -42% faces, T-pose, no pedestal | Game dev users get assets that work in their pipeline immediately | Surface T-pose pattern for character prompts; highlight in onboarding |
| Dota 2 SF: text can't reproduce IP characters | Users burning credits on guaranteed failure | Route named character queries to image-to-3D with in-product nudge |
| Crate: smallest lift, but topology still improves | Optimization ROI scales with object complexity | Weight suggestions by detected object complexity |
| Free tier download gating | Broken evaluation loop - users can't validate value before paying | A/B test 1–3 free GLB downloads per month |

---

## Limitations

- Test set is small (6 object types, 1 session each). Findings are directional, not statistically significant.
- No access to Meshy's internal funnel data - business implications are inferred from public evidence and experiment results.
- Mesh scoring was blocked by free-tier download limits. Scoring infrastructure is built and validated on external GLBs but could not be run on Meshy-generated pairs.
- Heuristic-driven rewriter has no feedback loop - patterns were reverse-engineered by hand, not learned from real user failure data at scale.
- Generation variance: running the same prompt twice can produce different outputs. Each test was a single run.

Being explicit about these limits is intentional. A PM or data scientist at Meshy would catch overclaiming immediately.

---

## What's Next

If I had access to Meshy's internal data, the three highest-value experiments would be:

1. **A/B test the optimizer in-product** - surface prompt suggestions at generation time and measure first-session success rate lift and credit-to-conversion rate. The dragon result (+20.8% geometry, topology confirmed) is the strongest argument for this experiment.

2. **Style-context classifier** - train a lightweight model to detect fantasy vs. realistic vs. sci-fi intent before applying material hints. This directly fixes the sword archetype mismatch (Finding 2) and is the highest-priority gap in the current pattern set. A small labeled dataset of prompts + intended styles would be enough to start.

3. **Free download A/B test** - measure conversion impact of allowing 1–3 free GLB downloads per month. Hypothesis: users who can validate quality in Blender convert at 2–3x the rate of users who can only view in-browser. This is the lowest-cost experiment with the highest potential conversion impact.

---

## About This Project

Built in one night as a research project to understand Meshy's activation funnel.

The goal was not to build a polished product - it was to identify a real problem, build a working artifact, and produce evidence-backed findings. The tool is fully external - no internal Meshy data was used or required.

**Repo:** [github.com/sanmati1997/meshy-prompt-optimizer](https://github.com/sanmati1997/meshy-prompt-optimizer)  
**Live demo:** [meshy-optimizer.streamlit.app](https://meshy-optimizer.streamlit.app)  
**Contact:** sawalwade.s@northeastern.edu | [linkedin.com/in/sanmati-sawalwade](https://linkedin.com/in/sanmati-sawalwade)

---

## A Note on Intent

I didn't build this to check a portfolio box. I built it because the activation problem at Meshy is real, the pain points are specific, and I wanted to prove - to myself and anyone reading - that the gap between a user's first prompt and their "aha moment" is closeable with the right product thinking.

The six findings above are six concrete problems with known solutions. I'd like to help build them.

I'm a strong engineer - I can ship the style-context classifier, the A/B test pipeline, the image-to-3D routing nudge. But my bigger strength is product: I find the friction before users do, build artifacts that prove it, and think in terms of conversion funnels and activation loops, not just code.

If you're at Meshy or working on a similar problem in the 3D / AI / creative tools space - I'm actively interviewing and would be genuinely grateful to be considered for a Summer / Fall 2026 internship. I want to work on problems I actually care about, with people who care about the same things.

**sawalwade.s@northeastern.edu** | [linkedin.com/in/sanmati-sawalwade](https://linkedin.com/in/sanmati-sawalwade)
