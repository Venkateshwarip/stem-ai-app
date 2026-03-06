import io
import contextlib

def run_code_simulated(code: str) -> str:
    """
    Executes Python code safely and captures print output.
    """
    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {})   # isolated execution
        return output_buffer.getvalue().strip()
    except Exception as e:
        return f"Error: {e}"
