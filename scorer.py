"""
Mesh quality scorer for GLB/OBJ files.
Scores on printability and topology quality metrics used in 3D printing literature.
"""

import numpy as np
import sys


def score_mesh(file_path: str) -> dict:
    try:
        import trimesh
    except ImportError:
        return {"error": "trimesh not installed. Run: pip install trimesh", "composite_score": 0}

    try:
        loaded = trimesh.load(file_path, force="mesh")
    except Exception as e:
        try:
            loaded = trimesh.load(file_path)
        except Exception as e2:
            return {"error": str(e2), "composite_score": 0}

    # Flatten scene to single mesh
    if isinstance(loaded, trimesh.Scene):
        if not loaded.geometry:
            return {"error": "empty scene", "composite_score": 0}
        try:
            mesh = trimesh.util.concatenate(list(loaded.geometry.values()))
        except Exception as e:
            return {"error": f"could not merge scene: {e}", "composite_score": 0}
    else:
        mesh = loaded

    if len(mesh.faces) == 0:
        return {"error": "mesh has no faces", "composite_score": 0}

    # --- Core metrics ---

    watertight = bool(mesh.is_watertight)
    is_volume = bool(mesh.is_volume)
    face_count = int(len(mesh.faces))
    vertex_count = int(len(mesh.vertices))

    # Degenerate faces (area near zero — bad topology)
    face_areas = mesh.area_faces
    degenerate_faces = int(np.sum(face_areas < 1e-10))
    degenerate_ratio = degenerate_faces / max(face_count, 1)

    # Non-manifold edges (edges shared by != 2 faces)
    edge_face_count: dict = {}
    for face in mesh.faces:
        for i in range(3):
            edge = tuple(sorted([int(face[i]), int(face[(i + 1) % 3])]))
            edge_face_count[edge] = edge_face_count.get(edge, 0) + 1
    non_manifold_edges = int(sum(1 for c in edge_face_count.values() if c != 2))
    non_manifold_ratio = non_manifold_edges / max(len(edge_face_count), 1)

    # Duplicate vertices (inefficiency)
    unique_verts = len(np.unique(mesh.vertices, axis=0))
    duplicate_verts = vertex_count - unique_verts

    # Bounding box aspect ratio (extreme ratios suggest malformed mesh)
    bounds = mesh.bounds
    if bounds is not None:
        dims = bounds[1] - bounds[0]
        dims = dims[dims > 0]
        aspect_ratio = float(np.max(dims) / np.min(dims)) if len(dims) > 1 else 1.0
    else:
        aspect_ratio = 1.0

    # --- Composite score (0–100) ---
    score = 0

    # Watertight: 35 pts — most important for printability/rigging
    if watertight:
        score += 35

    # Volume: 25 pts — manifold + consistent normals
    if is_volume:
        score += 25

    # Non-manifold edges: up to 25 pts
    nm_score = int(25 * max(0.0, 1.0 - non_manifold_ratio * 5))
    score += nm_score

    # Degenerate faces: up to 15 pts
    degen_score = int(15 * max(0.0, 1.0 - degenerate_ratio * 50))
    score += degen_score

    return {
        "file": file_path,
        "watertight": watertight,
        "is_volume": is_volume,
        "face_count": face_count,
        "vertex_count": vertex_count,
        "non_manifold_edges": non_manifold_edges,
        "degenerate_faces": degenerate_faces,
        "duplicate_vertices": duplicate_verts,
        "aspect_ratio": round(aspect_ratio, 2),
        "composite_score": score,
    }


def print_score(result: dict, label: str = ""):
    tag = f" [{label}]" if label else ""
    print(f"\nMesh Score{tag}")
    print("-" * 40)
    if "error" in result:
        print(f"  ERROR: {result['error']}")
        return
    print(f"  Composite score:     {result['composite_score']}/100")
    print(f"  Watertight:          {'YES' if result['watertight'] else 'NO'}")
    print(f"  Is volume:           {'YES' if result['is_volume'] else 'NO'}")
    print(f"  Faces:               {result['face_count']:,}")
    print(f"  Vertices:            {result['vertex_count']:,}")
    print(f"  Non-manifold edges:  {result['non_manifold_edges']}")
    print(f"  Degenerate faces:    {result['degenerate_faces']}")
    print(f"  Duplicate vertices:  {result['duplicate_vertices']}")
    print(f"  Bounding box ratio:  {result['aspect_ratio']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scorer.py path/to/model.glb")
        sys.exit(1)

    result = score_mesh(sys.argv[1])
    print_score(result)
