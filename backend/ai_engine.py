# backend/ai_engine.py

import config.settings as settings
import openai
import os
from models import code_explainer

# ================= OPENAI SETUP =================

OPENAI_KEY = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY


# ================= LINE BY LINE EXPLANATION =================

def explain_code_snippet(source_code: str):
    res = code_explainer.explain_code(source_code)

    if res.get("success"):
        return "\n".join(res.get("explanations"))

    # Fallback to OpenAI if available
    if OPENAI_KEY:
        return _call_openai(f"Explain this code line by line:\n{source_code}")

    return "Code explainer error: " + (res.get("error") or "Could not parse code.")


# ================= OPENAI CALL =================

def _call_openai(prompt: str):
    try:
        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.2
        )
        return resp.choices[0].text.strip()
    except Exception as e:
        return f"OpenAI error or missing key: {e}"


# ============================================================
# ================= AI EXPLANATION + DEBUGGING (NO OPENAI) ===
# ============================================================

def smart_ai_explanation_with_debug(code: str):

    explanation = []
    debug_tips = []

    lines = code.split("\n")

    # ---------- AI EXPLANATION ----------

    if "=" in code:
        explanation.append("The program stores values using variables.")

    if "+" in code:
        explanation.append("It performs addition to compute a result.")

    if "-" in code:
        explanation.append("It performs subtraction operation.")

    if "*" in code:
        explanation.append("It performs multiplication operation.")

    if "/" in code:
        explanation.append("It performs division operation.")

    if "input(" in code:
        explanation.append("The program takes input from the user.")

    if "print(" in code:
        explanation.append("The program displays output on the screen.")

    if "for " in code:
        explanation.append("A for loop repeats instructions multiple times.")

    if "while " in code:
        explanation.append("A while loop runs while a condition is true.")

    if "if " in code:
        explanation.append("The program makes decisions using conditions.")

    if "def " in code:
        explanation.append("A function is created for reusable logic.")

    if not explanation:
        explanation.append("This program executes Python instructions.")


    # ---------- DEBUGGING ----------

    for i, line in enumerate(lines):

        clean = line.strip()

        # Missing colon
        if clean.startswith(("if", "for", "while", "def")) and not clean.endswith(":"):
            debug_tips.append(f"Line {i+1}: Missing ':' at end of statement.")

        # Wrong comparison
        if "if" in line and "=" in line and "==" not in line:
            debug_tips.append(f"Line {i+1}: Use '==' for comparison instead of '='.")

        # Bad variable name
        if clean.startswith("sum ="):
            debug_tips.append(f"Line {i+1}: Avoid using 'sum' as variable name (built-in function).")

        # Print format issue
        if "print(" in line and "{sum}" in line and "f\"" not in line:
            debug_tips.append(f"Line {i+1}: Use f-string for variable inside print().")

    return " ".join(explanation), debug_tips
