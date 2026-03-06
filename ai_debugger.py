def debug_code(code: str):

    suggestions = []

    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Missing colon
        if stripped.startswith(("if", "for", "while")) and not stripped.endswith(":"):
            suggestions.append(
                f"Line {i}: Missing ':' at end of statement. Add ':' to fix syntax error."
            )

        # Indentation check
        if stripped and line.startswith(" "):
            if len(line) - len(line.lstrip(" ")) % 4 != 0:
                suggestions.append(
                    f"Line {i}: Indentation should be multiple of 4 spaces."
                )

        # Undefined variable guess
        if "=" not in stripped and stripped.isidentifier():
            suggestions.append(
                f"Line {i}: Possible undefined variable '{stripped}'. Assign value before use."
            )

        # Infinite loop detection
        if stripped.startswith("while True"):
            suggestions.append(
                f"Line {i}: Infinite loop detected. Add break condition."
            )

        # Print inside loop
        if stripped.startswith("print") and i > 1:
            prev = lines[i-2].strip()
            if prev.startswith(("for", "while")):
                suggestions.append(
                    f"Line {i}: Print inside loop will repeat many times. Check if intended."
                )

    if not suggestions:
        return ["✅ No common errors detected. Code looks good!"]

    return suggestions