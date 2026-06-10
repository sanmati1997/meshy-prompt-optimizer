import streamlit as st
import json
import os
import csv
import plotly.graph_objects as go
import tempfile

from rewriter import rewrite
from scorer import score_mesh

st.set_page_config(
    page_title="Meshy Prompt Optimizer",
    page_icon="🔺",
    layout="wide"
)

st.markdown("""
    <style>
    .metric-card {
        background: #1e1e2e;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .change-item {
        background: #2a2a3e;
        border-left: 3px solid #00ff88;
        padding: 0.5rem 1rem;
        margin: 0.3rem 0;
        border-radius: 0 5px 5px 0;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔺 Meshy Prompt Optimizer")
st.caption("Turns weak 3D prompts into production-ready ones. Built to reduce activation drop-off on Meshy.ai.")

tab1, tab2, tab3 = st.tabs(["Prompt Optimizer", "Mesh Scorer", "Results Dashboard"])


# ─── Tab 1: Prompt Optimizer ─────────────────────────────────────────────────

with tab1:
    st.subheader("Prompt Optimizer")
    st.write("Type a plain-English prompt. The optimizer rewrites it using rules reverse-engineered from Meshy's failure patterns.")

    col1, col2 = st.columns([1, 1])

    with col1:
        user_prompt = st.text_area(
            "Your prompt",
            placeholder="e.g. a cool sword",
            height=80
        )
        run_btn = st.button("Optimize →", type="primary", use_container_width=True)

    if run_btn and user_prompt.strip():
        result = rewrite(user_prompt.strip())

        with col1:
            st.markdown("**Original**")
            st.code(result["original"], language=None)
            st.markdown(f"Object type detected: `{result['object_type']}`")

        with col2:
            st.markdown("**Optimized**")
            st.code(result["optimized"], language=None)
            st.markdown(f"**{result['change_count']} changes made:**")
            for change in result["changes"]:
                st.markdown(f'<div class="change-item">✦ {change}</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown("**Next step:** Copy both prompts into [meshy.ai](https://meshy.ai), generate both models, download the GLBs, then score them in the Mesh Scorer tab.")

    elif run_btn:
        st.warning("Enter a prompt first.")


# ─── Tab 2: Mesh Scorer ──────────────────────────────────────────────────────

with tab2:
    st.subheader("Mesh Quality Scorer")
    st.write("Upload two GLB files — the naive result and the optimized result — to measure the difference.")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Naive model (original prompt)**")
        naive_file = st.file_uploader("Upload naive GLB", type=["glb", "obj"], key="naive")

    with col_b:
        st.markdown("**Optimized model (rewritten prompt)**")
        opt_file = st.file_uploader("Upload optimized GLB", type=["glb", "obj"], key="opt")

    if naive_file and opt_file:
        with tempfile.NamedTemporaryFile(suffix=".glb", delete=False) as tmp_n:
            tmp_n.write(naive_file.read())
            naive_path = tmp_n.name

        with tempfile.NamedTemporaryFile(suffix=".glb", delete=False) as tmp_o:
            tmp_o.write(opt_file.read())
            opt_path = tmp_o.name

        with st.spinner("Scoring meshes..."):
            naive_score = score_mesh(naive_path)
            opt_score = score_mesh(opt_path)

        os.unlink(naive_path)
        os.unlink(opt_path)

        n = naive_score.get("composite_score", 0)
        o = opt_score.get("composite_score", 0)
        delta = o - n

        st.divider()

        # Big numbers
        m1, m2, m3 = st.columns(3)
        m1.metric("Naive Score", f"{n}/100")
        m2.metric("Optimized Score", f"{o}/100")
        m3.metric("Improvement", f"{delta:+d} pts", delta_color="normal" if delta >= 0 else "inverse")

        st.divider()

        # Detail comparison table
        cols = ["watertight", "is_volume", "non_manifold_edges", "degenerate_faces", "face_count", "vertex_count"]
        labels = ["Watertight", "Is Volume", "Non-manifold Edges", "Degenerate Faces", "Face Count", "Vertex Count"]

        c1, c2, c3 = st.columns([2, 1, 1])
        c1.markdown("**Metric**")
        c2.markdown("**Naive**")
        c3.markdown("**Optimized**")

        for key, label in zip(cols, labels):
            v_n = naive_score.get(key, "—")
            v_o = opt_score.get(key, "—")
            c1.write(label)
            c2.write(str(v_n))
            c3.write(str(v_o))

        # Bar chart
        fig = go.Figure(data=[
            go.Bar(name="Naive", x=["Composite Score"], y=[n], marker_color="#ff4b4b"),
            go.Bar(name="Optimized", x=["Composite Score"], y=[o], marker_color="#00ff88"),
        ])
        fig.update_layout(
            barmode="group",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            height=300,
            margin=dict(t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Save to results CSV
        results_dir = os.path.join(os.path.dirname(__file__), "results")
        os.makedirs(results_dir, exist_ok=True)
        results_file = os.path.join(results_dir, "results.csv")
        prompt_label = st.text_input("Label this comparison (optional)", placeholder="e.g. sword prompt")
        if st.button("Save to results", use_container_width=True):
            row = {
                "id": "manual",
                "category": "manual",
                "naive_prompt": prompt_label or "—",
                "optimized_prompt": "—",
                "change_count": "—",
                "naive_score": n,
                "optimized_score": o,
                "delta": delta,
                "improved": delta > 0,
                "timestamp": __import__("datetime").datetime.now().isoformat(),
            }
            file_exists = os.path.isfile(results_file)
            with open(results_file, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=row.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)
            st.success("Saved to results/results.csv")


# ─── Tab 3: Results Dashboard ────────────────────────────────────────────────

with tab3:
    st.subheader("Results Dashboard")

    results_file = os.path.join(os.path.dirname(__file__), "results", "results.csv")

    if not os.path.isfile(results_file):
        st.info("No results yet. Score some meshes in the Mesh Scorer tab first.")
    else:
        with open(results_file) as f:
            rows = list(csv.DictReader(f))

        if not rows:
            st.info("Results file is empty.")
        else:
            ids = [r.get("naive_prompt", r["id"])[:20] for r in rows]
            naive_scores = [int(r["naive_score"]) for r in rows]
            opt_scores = [int(r["optimized_score"]) for r in rows]
            deltas = [int(r["delta"]) for r in rows]

            improved = sum(1 for d in deltas if d > 0)
            avg_lift = sum(deltas) / len(deltas)

            # Summary metrics
            s1, s2, s3 = st.columns(3)
            s1.metric("Prompts Tested", len(rows))
            s2.metric("Improvement Rate", f"{improved/len(rows)*100:.0f}%")
            s3.metric("Avg Score Lift", f"{avg_lift:+.1f} pts")

            st.divider()

            # Before/after chart
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Naive", x=ids, y=naive_scores, marker_color="#ff4b4b"))
            fig.add_trace(go.Bar(name="Optimized", x=ids, y=opt_scores, marker_color="#00ff88"))
            fig.update_layout(
                barmode="group",
                title="Naive vs Optimized Mesh Score by Prompt",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                yaxis=dict(range=[0, 100], title="Composite Score (0–100)"),
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)

            # Delta chart
            colors = ["#00ff88" if d > 0 else "#ff4b4b" for d in deltas]
            fig2 = go.Figure(go.Bar(x=ids, y=deltas, marker_color=colors))
            fig2.update_layout(
                title="Score Delta per Prompt (green = improved)",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                yaxis=dict(title="Delta (points)"),
                height=300,
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Raw table
            st.markdown("**Raw results**")
            st.dataframe(
                rows,
                use_container_width=True,
            )

            # Download
            with open(results_file) as f:
                st.download_button(
                    "Download results.csv",
                    f.read(),
                    file_name="meshy_prompt_optimizer_results.csv",
                    mime="text/csv",
                )
