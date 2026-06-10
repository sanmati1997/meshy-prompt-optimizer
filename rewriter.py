"""
Prompt rewriter for Meshy 3D generation.
Takes a plain-English prompt and rewrites it for better Meshy output.
Rule-based: every change is explainable, no black-box LLM needed.
"""

STYLE_KEYWORDS = [
    "realistic", "cartoon", "low-poly", "low poly", "stylized", "pbr",
    "game-ready", "game ready", "anime", "sci-fi", "fantasy", "toon",
    "photorealistic", "hand-painted", "cel-shaded"
]

MATERIAL_KEYWORDS = [
    "metal", "metallic", "steel", "iron", "gold", "silver", "bronze", "copper",
    "wood", "wooden", "stone", "rock", "marble", "granite",
    "plastic", "rubber", "glass", "crystal", "ceramic",
    "fabric", "cloth", "leather", "skin", "fur", "scales",
    "concrete", "brick", "clay", "bone", "flesh"
]

TOPOLOGY_KEYWORDS = ["topology", "quad", "manifold", "watertight", "polygon", "retopology"]

VAGUE_WORDS = {
    "cool": "detailed",
    "nice": "well-crafted",
    "awesome": "intricate",
    "amazing": "high-fidelity",
    "great": "refined",
    "good": "clean",
    "beautiful": "ornate",
    "pretty": "elegant",
    "ugly": "weathered",
    "weird": "stylized",
    "interesting": "unique",
    "epic": "imposing",
    "sick": "striking",
    "random": "",
}

CHARACTER_WORDS = [
    "person", "human", "man", "woman", "warrior", "knight", "wizard", "mage",
    "soldier", "hero", "villain", "character", "robot", "alien", "demon",
    "angel", "elf", "dwarf", "orc", "goblin", "samurai", "ninja", "pirate"
]

CREATURE_WORDS = [
    "dragon", "monster", "beast", "creature", "animal", "lion", "wolf",
    "bear", "tiger", "snake", "spider", "dinosaur", "phoenix", "griffin"
]

WEAPON_WORDS = [
    "sword", "axe", "gun", "rifle", "pistol", "bow", "dagger", "knife",
    "spear", "hammer", "mace", "staff", "wand", "shield", "cannon", "blade"
]

VEHICLE_WORDS = [
    "car", "truck", "tank", "ship", "spaceship", "rocket", "plane",
    "helicopter", "boat", "motorcycle", "bicycle", "train", "submarine"
]

PROP_WORDS = [
    "table", "chair", "tree", "rock", "building", "house", "pot", "vase",
    "barrel", "chest", "box", "crate", "pillar", "column", "lantern",
    "lamp", "bottle", "book", "mushroom", "flower", "crystal", "gem",
    "throne", "altar", "statue", "door", "gate", "bridge", "tower"
]


def detect_object_type(prompt: str) -> str:
    p = prompt.lower()
    if any(w in p for w in CHARACTER_WORDS):
        return "character"
    if any(w in p for w in CREATURE_WORDS):
        return "creature"
    if any(w in p for w in WEAPON_WORDS):
        return "weapon"
    if any(w in p for w in VEHICLE_WORDS):
        return "vehicle"
    if any(w in p for w in PROP_WORDS):
        return "prop"
    return "object"


def infer_style(object_type: str, prompt: str) -> str:
    p = prompt.lower()
    if any(w in p for w in ["fantasy", "magic", "medieval", "mythical"]):
        return "fantasy game-ready asset"
    if any(w in p for w in ["sci-fi", "futuristic", "space", "cyber", "mech"]):
        return "sci-fi game-ready asset"
    if any(w in p for w in ["cartoon", "cute", "chibi"]):
        return "cartoon stylized"
    if object_type in ("character", "creature"):
        return "game-ready stylized asset"
    if object_type == "weapon":
        return "game-ready low-poly asset"
    if object_type == "vehicle":
        return "realistic PBR"
    return "game-ready low-poly asset"


def infer_material(object_type: str, prompt: str) -> str:
    p = prompt.lower()
    if any(w in p for w in ["gold", "golden"]):
        return "gold metallic surface"
    if any(w in p for w in ["silver", "steel", "iron", "metal"]):
        return "brushed steel metallic surface"
    if any(w in p for w in ["wood", "wooden"]):
        return "worn wooden surface"
    if any(w in p for w in ["stone", "rock", "marble"]):
        return "rough stone texture"
    if any(w in p for w in ["glass", "crystal"]):
        return "translucent glass material"
    if object_type == "weapon":
        return "tempered steel blade"
    if object_type == "character":
        return "fabric and leather armor"
    if object_type == "creature":
        return "organic skin and scales"
    if object_type == "vehicle":
        return "painted metal body"
    return "matte surface texture"


def replace_vague_words(prompt: str) -> tuple[str, list[str]]:
    changes = []
    words = prompt.split()
    result = []
    for word in words:
        clean = word.lower().strip(".,!?")
        if clean in VAGUE_WORDS:
            replacement = VAGUE_WORDS[clean]
            if replacement:
                result.append(replacement)
                changes.append(f'replaced "{clean}" → "{replacement}"')
            else:
                changes.append(f'removed vague word "{clean}"')
        else:
            result.append(word)
    return " ".join(result).strip(), changes


def rewrite(prompt: str) -> dict:
    """
    Returns:
        original: the input prompt
        optimized: the improved prompt
        changes: list of what was changed and why
        object_type: detected category
    """
    changes = []
    p = prompt.strip()

    # Step 1: Replace vague words
    p, vague_changes = replace_vague_words(p)
    changes.extend(vague_changes)

    # Step 2: Add "3D model of" prefix
    lower = p.lower()
    if not any(lower.startswith(prefix) for prefix in ["3d model", "a 3d", "an 3d", "3d asset"]):
        p = "3D model of " + p
        changes.append('added "3D model of" prefix — Meshy responds better to explicit 3D framing')

    # Step 3: Detect object type
    object_type = detect_object_type(p)

    # Step 4: Add style tag if missing
    if not any(kw in p.lower() for kw in STYLE_KEYWORDS):
        style = infer_style(object_type, p)
        p = p + f", {style}"
        changes.append(f'added style tag "{style}" — style-less prompts produce inconsistent results')

    # Step 5: Add material hint if missing
    if not any(kw in p.lower() for kw in MATERIAL_KEYWORDS):
        material = infer_material(object_type, p)
        p = p + f", {material}"
        changes.append(f'added material "{material}" — material ambiguity is top cause of texture inconsistency')

    # Step 6: Add topology hint
    if not any(kw in p.lower() for kw in TOPOLOGY_KEYWORDS):
        p = p + ", clean quad topology"
        changes.append('added "clean quad topology" — improves mesh quality for rigging and sculpting')

    # Step 7: Add isolation context
    isolation_words = ["background", "scene", "isolated", "white background", "no background"]
    if not any(w in p.lower() for w in isolation_words):
        p = p + ", isolated object, no background"
        changes.append('added isolation context — prevents Meshy from adding unwanted scene elements')

    # Step 8: Character-specific orientation
    if object_type == "character":
        orientation_words = ["t-pose", "t pose", "standing", "upright", "idle"]
        if not any(w in p.lower() for w in orientation_words):
            p = p + ", standing upright in T-pose"
            changes.append('added T-pose orientation — critical for rigging compatibility')

    return {
        "original": prompt,
        "optimized": p,
        "changes": changes,
        "object_type": object_type,
        "change_count": len(changes)
    }


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python rewriter.py \"your prompt here\"")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    result = rewrite(prompt)

    print("\n" + "="*60)
    print("ORIGINAL:  ", result["original"])
    print("OPTIMIZED: ", result["optimized"])
    print(f"\nObject type detected: {result['object_type']}")
    print(f"\n{result['change_count']} changes made:")
    for i, change in enumerate(result["changes"], 1):
        print(f"  {i}. {change}")
    print("="*60 + "\n")
