def line_by_line_explanation(code):
    explanations = []
    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Print statement
        if stripped.startswith("print"):
            explanations.append(
                f"Line {i}: This line prints output to the screen."
            )

        # Function definition
        elif stripped.startswith("def "):
            explanations.append(
                f"Line {i}: This line defines a function."
            )

        # For loop
        elif stripped.startswith("for "):
            explanations.append(
                f"Line {i}: This line starts a loop that repeats actions."
            )

        # While loop
        elif stripped.startswith("while "):
            explanations.append(
                f"Line {i}: This line starts a loop that runs while a condition is true."
            )

        # If condition
        elif stripped.startswith("if "):
            explanations.append(
                f"Line {i}: This line checks a condition."
            )

        # Else condition
        elif stripped.startswith("else"):
            explanations.append(
                f"Line {i}: This line runs when the previous condition is false."
            )

        # Addition operation
        elif "=" in stripped and "+" in stripped:
            explanations.append(
                f"Line {i}: Two values are added and stored in a variable."
            )

        # Subtraction
        elif "=" in stripped and "-" in stripped:
            explanations.append(
                f"Line {i}: A subtraction result is stored in a variable."
            )

        # Multiplication
        elif "=" in stripped and "*" in stripped:
            explanations.append(
                f"Line {i}: Two values are multiplied and stored in a variable."
            )

        # Division
        elif "=" in stripped and "/" in stripped:
            explanations.append(
                f"Line {i}: A value is divided and stored in a variable."
            )

        # Variable assignment
        elif "=" in stripped:
            explanations.append(
                f"Line {i}: A variable is assigned a value."
            )

        # Return statement
        elif stripped.startswith("return"):
            explanations.append(
                f"Line {i}: This line returns a value from the function."
            )

        # Input
        elif "input(" in stripped:
            explanations.append(
                f"Line {i}: This line takes input from the user."
            )

        # Default case
        else:
            explanations.append(
                f"Line {i}: This line executes a Python statement."
            )

    return explanations
