import json
from typing import List, Tuple

def parse_voucher_json(raw_text: str) -> Tuple[List[str], int, str]:
    """
    Parses JSON voucher imports.
    Supports:
    - Line-delimited JSON
    - Adjacent JSON objects without line breaks: {"voucher":"A"}{"voucher":"B"}
    - Nested JSON objects
    Filters out account credentials and tokens.
    """
    text = raw_text.strip()
    if not text:
        return [], 0, ""

    objects = []
    in_string = False
    escape_next = False
    brace_depth = 0
    obj_start = -1

    for i, char in enumerate(text):
        if in_string:
            if escape_next:
                escape_next = False
            elif char == '\\':
                escape_next = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue

        if char == '{':
            if brace_depth == 0:
                obj_start = i
            brace_depth += 1
        elif char == '}':
            if brace_depth == 0:
                return [], 0, f"Unexpected closing brace at index {i}"
            brace_depth -= 1
            if brace_depth == 0 and obj_start != -1:
                objects.append(text[obj_start:i+1].strip())
                obj_start = -1

    if brace_depth != 0:
        return [], 0, "Malformed JSON: Unclosed curly braces."

    valid = []
    rejected_credentials = 0

    for item in objects:
        try:
            parsed = json.loads(item)
        except Exception as e:
            return [], 0, f"JSON parse error: {str(e)}"

        lower = item.lower()
        if any(bad in lower for bad in ['"password"', '"sessid"', '"cookie"', '"auth_token"', '"api_key"']):
            rejected_credentials += 1
            continue

        valid.append(item)

    return valid, rejected_credentials, ""
