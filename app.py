"""
Milestone 5 — query interface (Gradio).

A minimal web UI over ask() from generate.py: type a question, get a grounded answer plus
the source documents it was drawn from.

Run:  python app.py     then open http://localhost:7860
"""

import gradio as gr

from generate import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources or "(no sources — not enough information in the guide)"


with gr.Blocks(title="The Unofficial Minecraft Guide") as demo:
    gr.Markdown(
        "# The Unofficial Minecraft Guide\n"
        "Ask about mobs, dimensions, structures, and mechanics. "
        "Answers come **only** from the ingested Minecraft Wiki pages — if the guide "
        "doesn't cover it, the assistant says so instead of guessing."
    )
    inp = gr.Textbox(label="Your question", placeholder="How do I go to the Nether?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

    gr.Examples(
        examples=[
            "How do I go to the Nether in the first place?",
            "How do I get more villagers without finding a village?",
            "What is the enchantment that lets me automatically repair my items?",
        ],
        inputs=inp,
    )


if __name__ == "__main__":
    demo.launch()
