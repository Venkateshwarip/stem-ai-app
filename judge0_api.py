# backend/judge0_api.py
import time
from typing import Dict

def run_code_simulated(source_code: str, language: str = "python"):
    """
    Simulates code execution (safe). For real execution integrate Judge0 or a sandboxed runner.
    This function returns a simulated output object.
    """
    # very naive simulation: if 'print(' present, show that expression (not evaluated)
    time.sleep(0.5)
    out = ""
    if "print(" in source_code:
        # crude extract between print(...)
        try:
            start = source_code.index("print(") + 6
            end = source_code.index(")", start)
            out = source_code[start:end].strip().strip("'\"")
        except Exception:
            out = "Simulated print output"
    else:
        out = "No print statements detected. (Simulation)"
    return {
        "stdout": out,
        "stderr": "",
        "status": "simulated"
    }

# If you want real Judge0 integration, implement a function here that calls your Judge0 endpoint securely.