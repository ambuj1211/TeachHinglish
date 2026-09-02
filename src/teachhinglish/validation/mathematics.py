import re

import sympy as sp
from teachhinglish.validation.base import ValidationResult
from teachhinglish.core.models import TeachingRequest

MATH_LINE_PATTERN = re.compile(
    r"^\s*([A-Za-z][A-Za-z0-9_]*\s*=\s*[^=\n]+)\s*$"
)

LATEX_BLOCK_PATTERN = re.compile(
    r"\$\$(.*?)\$\$",
    re.DOTALL,
)

LATEX_INLINE_PATTERN = re.compile(
    r"\\\((.*?)\\\)",
    re.DOTALL,
)


def validate_mathematical_expressions(script: str) -> list[str]:
    """
    Validate mathematical expressions appearing in a teaching script.

    Supports:
    - Plain assignments such as: F = m*a
    - Inline LaTeX: \\( F = ma \\)
    - Block LaTeX: $$ F = ma $$
    """

    errors: list[str] = []

    # Validate plain mathematical assignments.
    for line_number, line in enumerate(script.splitlines(), start=1):
        match = MATH_LINE_PATTERN.match(line)

        if not match:
            continue

        expression = match.group(1)

        if not _looks_like_mathematical_expression(expression):
            continue

        try:
            _validate_expression(expression)
        except ValueError as exc:
            errors.append(
                f"Line {line_number}: mathematical expression is invalid: {exc}"
            )

    # Validate block LaTeX.
    errors.extend(_validate_latex_blocks(script))

    # Validate inline LaTeX.
    errors.extend(_validate_inline_latex(script))

    return errors


def _validate_latex_blocks(script: str) -> list[str]:
    """Validate $$ ... $$ LaTeX blocks."""

    errors: list[str] = []

    # Detect an unmatched opening/closing block delimiter.
    if script.count("$$") % 2 != 0:
        errors.append(
            "LaTeX expression is invalid: unmatched '$$' delimiter."
        )
        return errors

    for match in LATEX_BLOCK_PATTERN.finditer(script):
        expression = match.group(1).strip()

        if not expression:
            errors.append(
                "LaTeX expression is invalid: empty expression."
            )
            continue

        try:
            _validate_latex_expression(expression)
        except ValueError as exc:
            errors.append(
                f"LaTeX expression is invalid: {exc}"
            )

    return errors


def _validate_inline_latex(script: str) -> list[str]:
    """Validate \\( ... \\) inline LaTeX expressions."""

    errors: list[str] = []

    # Detect unmatched inline delimiters.
    if script.count(r"\(") != script.count(r"\)"):
        errors.append(
            "LaTeX expression is invalid: unmatched inline delimiter."
        )
        return errors

    for match in LATEX_INLINE_PATTERN.finditer(script):
        expression = match.group(1).strip()

        if not expression:
            errors.append(
                "LaTeX expression is invalid: empty expression."
            )
            continue

        try:
            _validate_latex_expression(expression)
        except ValueError as exc:
            errors.append(
                f"LaTeX expression is invalid: {exc}"
            )

    return errors


def _validate_latex_expression(expression: str) -> None:
    """
    Perform deterministic structural checks on a LaTeX expression.

    This intentionally does not attempt to prove mathematical correctness.
    """

    # Balanced braces.
    if expression.count("{") != expression.count("}"):
        raise ValueError("unbalanced braces.")

    # Common LaTeX commands that require an argument.
    for command in (r"\frac", r"\sqrt"):
        position = 0

        while True:
            position = expression.find(command, position)

            if position == -1:
                break

            position += len(command)

            if position >= len(expression) or expression[position] != "{":
                raise ValueError(
                    f"{command} is missing its argument."
                )

    # Basic malformed fraction detection.
    for match in re.finditer(r"\\frac\s*", expression):
        start = match.end()

        if start >= len(expression) or expression[start] != "{":
            raise ValueError(r"\frac is missing its numerator.")

        numerator_end = _find_matching_brace(expression, start)

        if numerator_end is None:
            raise ValueError(r"\frac has an unbalanced numerator.")

        denominator_start = numerator_end + 1

        if (
            denominator_start >= len(expression)
            or expression[denominator_start] != "{"
        ):
            raise ValueError(r"\frac is missing its denominator.")

        denominator_end = _find_matching_brace(
            expression,
            denominator_start,
        )

        if denominator_end is None:
            raise ValueError(r"\frac has an unbalanced denominator.")


def _find_matching_brace(expression: str, opening_index: int) -> int | None:
    """Find the closing brace matching the brace at opening_index."""

    depth = 0

    for index in range(opening_index, len(expression)):
        character = expression[index]

        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1

            if depth == 0:
                return index

    return None


def _looks_like_mathematical_expression(expression: str) -> bool:
    """Return True when an assignment looks mathematical."""

    return bool(
        re.search(r"\d", expression)
        or re.search(
            r"\b(sin|cos|tan|log|sqrt)\b",
            expression,
            re.IGNORECASE,
        )
        or re.search(r"[\+\-\*/\^]", expression)
    )


def _validate_expression(expression: str) -> None:
    """Parse and validate a mathematical assignment."""

    left, right = expression.split("=", 1)

    left = left.strip()
    right = right.strip()

    if not left:
        raise ValueError("missing left-hand side.")

    if not right:
        raise ValueError("missing right-hand side.")

    try:
        sp.sympify(right)
    except (sp.SympifyError, SyntaxError, TypeError) as exc:
        raise ValueError(f"cannot parse '{right}'") from exc

class MathematicsValidator:
    """Adapter exposing mathematical validation through ScriptValidator."""

    def validate(
        self,
        script_or_request,
        script: str | None = None,
    ) -> ValidationResult:
        if script is None:
            script = script_or_request

        return ValidationResult(
            errors=validate_mathematical_expressions(script)
        )