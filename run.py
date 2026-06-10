"""
Meshy Prompt Optimizer — main CLI
Usage:
  python run.py rewrite "a cool sword"
  python run.py score model.glb
  python run.py compare naive.glb optimized.glb
  python run.py batch          — walks through all prompts in prompts.json
  python run.py report         — prints results table from saved CSV
"""

import sys
import os
import json
import csv
from datetime import datetime

from rewriter import rewrite
from scorer import score_mesh, print_score

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "results", "results.csv")


# ─── helpers ──────────────────────────────────────────────────────────────────

def save_result(row: dict):
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    file_exists = os.path.isfile(RESULTS_FILE)
    with open(RESULTS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def separator(char="=", width=60):
    print(char * width)


# ─── commands ─────────────────────────────────────────────────────────────────

def cmd_rewrite(prompt: str):
    result = rewrite(prompt)
    separator()
    print(f"ORIGINAL:   {result['original']}")
    print(f"OPTIMIZED:  {result['optimized']}")
    print(f"\nObject type: {result['object_type']}")
    print(f"\n{result['change_count']} changes made:")
    for i, change in enumerate(result["changes"], 1):
        print(f"  {i}. {change}")
    separator()


def cmd_score(file_path: str):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    result = score_mesh(file_path)
    print_score(result)


def cmd_compare(naive_path: str, optimized_path: str, prompt: str = ""):
    print(f"\nComparing meshes...")
    if prompt:
        print(f"Prompt: {prompt}")

    naive_score = score_mesh(naive_path)
    opt_score = score_mesh(optimized_path)

    print_score(naive_score, label="NAIVE")
    print_score(opt_score, label="OPTIMIZED")

    separator()
    n = naive_score.get("composite_score", 0)
    o = opt_score.get("composite_score", 0)
    delta = o - n
    direction = "+" if delta >= 0 else ""
    print(f"  Naive score:     {n}/100")
    print(f"  Optimized score: {o}/100")
    print(f"  Delta:           {direction}{delta} points  ({'IMPROVED' if delta > 0 else 'NO IMPROVEMENT' if delta == 0 else 'WORSE'})")
    separator()

    return n, o, delta


def cmd_batch():
    with open(os.path.join(os.path.dirname(__file__), "prompts.json")) as f:
        prompts = json.load(f)

    print("\nMeshy Prompt Optimizer — Batch Mode")
    print("You will generate each model manually in Meshy, then provide the file paths.\n")
    separator()

    for item in prompts:
        pid = item["id"]
        category = item["category"]
        naive_prompt = item["naive"]

        print(f"\n[Prompt {pid}/{len(prompts)}] Category: {category}")
        separator("-")

        # Rewrite
        result = rewrite(naive_prompt)
        print(f"NAIVE:      {result['original']}")
        print(f"OPTIMIZED:  {result['optimized']}")
        print(f"\n{result['change_count']} changes: {', '.join(result['changes'][:2])}...")

        print("\n--- ACTION REQUIRED ---")
        print(f"1. Go to meshy.ai")
        print(f"2. Generate with NAIVE prompt:     {result['original']}")
        print(f"3. Download GLB → save as:         results/naive_{pid}.glb")
        print(f"4. Generate with OPTIMIZED prompt: {result['optimized']}")
        print(f"5. Download GLB → save as:         results/optimized_{pid}.glb")
        input("\nPress ENTER when both files are downloaded...")

        naive_path = f"results/naive_{pid}.glb"
        opt_path = f"results/optimized_{pid}.glb"

        if not os.path.isfile(naive_path) or not os.path.isfile(opt_path):
            print(f"Files not found. Skipping prompt {pid}.")
            continue

        n, o, delta = cmd_compare(naive_path, opt_path, naive_prompt)

        save_result({
            "timestamp": datetime.now().isoformat(),
            "id": pid,
            "category": category,
            "naive_prompt": result["original"],
            "optimized_prompt": result["optimized"],
            "change_count": result["change_count"],
            "naive_score": n,
            "optimized_score": o,
            "delta": delta,
            "improved": delta > 0,
        })
        print(f"Saved to results.csv")

    cmd_report()


def cmd_report():
    if not os.path.isfile(RESULTS_FILE):
        print("No results yet. Run: python run.py batch")
        return

    with open(RESULTS_FILE) as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("Results file is empty.")
        return

    separator()
    print(f"{'ID':<4} {'Category':<12} {'Naive':>6} {'Opt':>6} {'Delta':>7} {'Result':<12}")
    separator("-")

    total_naive = 0
    total_opt = 0
    improved = 0

    for row in rows:
        n = int(row["naive_score"])
        o = int(row["optimized_score"])
        d = int(row["delta"])
        flag = "IMPROVED" if d > 0 else ("SAME" if d == 0 else "worse")
        print(f"{row['id']:<4} {row['category']:<12} {n:>6} {o:>6} {d:>+7} {flag:<12}")
        total_naive += n
        total_opt += o
        if d > 0:
            improved += 1

    separator("-")
    n_rows = len(rows)
    avg_n = total_naive / n_rows
    avg_o = total_opt / n_rows
    avg_delta = avg_o - avg_n
    improvement_rate = improved / n_rows * 100

    print(f"{'AVG':<4} {'':<12} {avg_n:>6.1f} {avg_o:>6.1f} {avg_delta:>+7.1f}")
    separator()
    print(f"\nSummary:")
    print(f"  Prompts tested:     {n_rows}")
    print(f"  Improved:           {improved}/{n_rows} ({improvement_rate:.0f}%)")
    print(f"  Average score lift: {avg_delta:+.1f} points")
    print(f"  Avg naive score:    {avg_n:.1f}/100")
    print(f"  Avg optimized:      {avg_o:.1f}/100")
    separator()


# ─── entry point ──────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "rewrite":
        if len(args) < 2:
            print('Usage: python run.py rewrite "your prompt"')
            sys.exit(1)
        cmd_rewrite(" ".join(args[1:]))

    elif cmd == "score":
        if len(args) < 2:
            print("Usage: python run.py score path/to/model.glb")
            sys.exit(1)
        cmd_score(args[1])

    elif cmd == "compare":
        if len(args) < 3:
            print("Usage: python run.py compare naive.glb optimized.glb")
            sys.exit(1)
        prompt = " ".join(args[3:]) if len(args) > 3 else ""
        cmd_compare(args[1], args[2], prompt)

    elif cmd == "batch":
        cmd_batch()

    elif cmd == "report":
        cmd_report()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
