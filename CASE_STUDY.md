# Meshy Prompt Forge — Case Study

**Author:** Sanmati Walwade  
**Background:** MS Information Systems, Northeastern University (Silicon Valley) | Ex-Gameskraft | Startup Founder  
**Built in:** One night  
**Repo:** github.com/YOUR_USERNAME/meshy-prompt-forge  
**Live demo:** [link]

---

## The Problem

Meshy has 6 million users but $15M ARR — roughly $2.50 average revenue per user. Most users are free and never convert to paid.

The biggest reason: **bad first experience.**

Text-to-3D is fundamentally harder to prompt than text-to-image. Users have mental models for Midjourney and DALL-E — those don't transfer to 3D generation. A new Meshy user types a vague prompt, gets a mediocre or wrong model, burns free credits, and leaves before the "aha moment."

### Evidence from public sources

- **G2 reviewer:** *"Small wording changes produce wildly different results"*
- **G2 reviewer:** *"Limited prompt character space is frustrating"*
- **Trustpilot:** Multiple users reporting wasted credits on poor first outputs
- **Meshy's own docs:** A "prompt tips" section exists — companies only write those when support tickets pile up
- **Pricing page:** Free tier caps downloads — users can't even evaluate what they generated without upgrading

This is an activation problem. Users hit the friction wall before they see the product's real value.

---

## Hypothesis

> Optimized prompts — prompts that include explicit style tags, material hints, topology context, and isolation framing — will produce meaningfully better 3D models than naive prompts on complex objects.

The secondary hypothesis: **prompt sensitivity is highest on ambiguous, complex objects** (creatures, characters) and lowest on simple geometric objects (swords, barrels).

---

## What I Built

A rule-based prompt optimizer + mesh quality scorer, built in one night on Meshy's free tier.

**Stack:** Python, Streamlit, trimesh, Plotly. Zero dollars. No paid APIs.

### How the optimizer works

The rewriter applies 8 deterministic rules reverse-engineered from Meshy's failure patterns:

| Rule | Why |
|---|---|
| Add "3D model of" prefix | Meshy responds better to explicit 3D framing |
| Detect object type (character / weapon / vehicle / prop / creature) | Enables context-aware downstream rules |
| Add style tag if missing | Style-less prompts produce inconsistent results |
| Add material hint if missing | Material ambiguity is the top cause of texture inconsistency |
| Add "clean quad topology" | Improves mesh quality for rigging and sculpting |
| Add isolation context | Prevents unwanted scene elements |
| Add T-pose for characters | Critical for rigging compatibility |
| Replace vague adjectives | "cool" → "detailed", "nice" → "well-crafted" |

Every change is explainable. No black-box LLM. A PM can audit every decision.

### Bonus: Game IP detection

The tool also detects known game IPs (Dota 2, League of Legends, Overwatch) and applies IP-specific art style tags automatically:

- Input: `dota 2 invoker`
- Output: `3D model of dota 2 invoker, Dota 2 stylized hero model, Valve art style, detailed armor and fabric, game-ready PBR materials, clean quad topology, isolated object, no background, standing upright in T-pose`

### Mesh scorer

For downloadable GLBs, the tool scores on 5 objective topology metrics:

| Metric | Weight | Why It Matters |
|---|---|---|
| Watertight | 35 pts | Printability and rigging |
| Is Volume | 25 pts | Manifold + consistent normals |
| Non-manifold edges | 25 pts | Topology quality |
| Degenerate faces | 15 pts | Mesh cleanliness |

---

## Findings

### Finding 1 — Hypothesis confirmed on complex objects

**Test:** Generated "dragon" (naive) vs the optimized prompt.

- **Naive result:** Baby dragon — Meshy interpreted the single word ambiguously and defaulted to a small, cute variant
- **Optimized result:** Full-scale dragon — correct scale, creature type, and visual fidelity

One word ("dragon") left too much ambiguity. The optimizer added style, scale framing, and material context — enough for Meshy to produce the intended result.

**Implication:** On ambiguous prompts, the optimizer resolves intent that the model would otherwise guess wrong.

---

### Finding 2 — Low impact on simple geometric objects

**Test:** Generated "a cool sword" (naive) vs the optimized prompt.

Both produced recognizable swords. The optimized version was marginally better but the difference was minimal.

**Why:** Swords are simple, well-represented shapes in Meshy's training data. The model doesn't need much guidance. Prompt sensitivity is low.

**Implication:** The optimizer's value scales with prompt ambiguity and object complexity. It's most useful for characters, creatures, and environments — Meshy's highest-value use cases.

---

### Finding 3 — IP characters require image-to-3D, not text optimization

**Test:** Generated "dota 2 sf" (Shadow Fiend) with both naive and optimized prompts.

Neither produced a model resembling Shadow Fiend. The game IP detection correctly identified it as a Dota 2 character and added the right style tags — but Meshy's model doesn't have enough hero-specific training data to reconstruct a specific character from text alone.

**Implication:** Meshy should surface its image-to-3D workflow more prominently for users asking for specific IP characters. This is a navigation/onboarding gap, not a model gap.

---

### Finding 4 — Free tier download gating creates a broken evaluation loop

While running this experiment, I hit a blocker: **the free tier doesn't allow GLB downloads.** This means:

1. Free users can generate models but can't export or evaluate them properly
2. The "try before you buy" loop is broken — users can't take a generated model into Blender to check if it meets their needs
3. This is likely a significant conversion friction point: users who can't evaluate quality won't upgrade

This finding came from building the tool, not from a dashboard. It's a real friction point in the free-to-paid conversion funnel.

---

## Business Implications

| Finding | Business Impact |
|---|---|
| Prompt optimizer lifts first-result quality on complex objects | Higher first-session success → lower churn → higher conversion |
| Simple objects need less optimization | Prioritize optimizer for character/creature use cases, not generic props |
| IP characters need image-to-3D guidance | Add in-product routing: "Looking for a specific character? Try image-to-3D" |
| Download gating breaks evaluation loop | A/B test allowing 1-3 free downloads — conversion uplift likely exceeds cost |

---

## Limitations

- Test set is small (6 prompts, 1 session). Findings are directional, not statistically significant.
- No access to Meshy's real funnel data — implications are inferred, not measured.
- Mesh scoring was blocked by free-tier download limits on Meshy. Scoring infrastructure is built and validated on external GLBs but not yet run on paired Meshy outputs.
- Rule-based rewriter has no feedback loop — rules were hand-authored, not learned from real user failure data.

Being explicit about these limits is intentional. A PM or data scientist at Meshy would catch overclaiming immediately.

---

## What's Next

If I had access to Meshy's internal data, the three highest-value experiments would be:

1. **A/B test the optimizer in-product** — surface prompt suggestions at generation time, measure first-session success rate lift
2. **Segment by object type** — confirm the complexity-sensitivity relationship at scale
3. **Free download A/B test** — measure conversion impact of allowing 1-3 free GLB downloads

---

## About This Project

Built in one night as a research project to understand Meshy's activation funnel.

The goal was not to build a polished product — it was to identify a real problem, build a working artifact, and produce evidence-backed findings. The tool is fully external — no internal Meshy data was used or required.

**Repo:** github.com/YOUR_USERNAME/meshy-prompt-forge  
**Live demo:** [link]  
**Contact:** sawalwade.s@northeastern.edu | linkedin.com/in/sanmatiwalwade
