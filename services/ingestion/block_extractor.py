# proj-grag\GRAG_V3\services\ingestion\block_extractor.py
import re
import uuid


def is_valid_section_heading(line):
    line_clean = line.strip()

    # heuristic 1: short + capitalized
    if len(line_clean.split()) <= 10 and line_clean.istitle():
        return True

    # heuristic 2: ALL CAPS
    if line_clean.isupper() and len(line_clean.split()) >= 2:
        return True

    # heuristic 3: known generic keywords (safe across domains)
    keywords = [
        "abstract", "introduction", "summary", "conclusion",
        "background", "method", "results", "discussion"
    ]

    lower = line_clean.lower()
    for kw in keywords:
        if kw in lower:
            return True

    return False


def looks_like_field_label(line):
    line = line.strip()

    if len(line.split()) <= 6 and line.endswith(":"):
        return True

    if len(line.split()) <= 6 and line.istitle():
        return True

    return False


def classify_line(line):
    line = line.strip()

    if not line:
        return "empty"

    # numbered clause
    if re.match(r"^\[\d+\]", line):
        return "numbered_clause"

    # heading
    if is_valid_section_heading(line):
        return "heading"

    # key-value (generic)
    if ":" in line:
        parts = line.split(":", 1)
        if len(parts[0].split()) <= 15 and parts[1].strip():
            return "key_value"

    # table row (important for generic docs)
    if len(re.split(r"\s{2,}", line)) >= 3:
        return "table_row"

    return "paragraph"


def build_blocks_from_lines(lines):
    blocks = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # CASE 1: inline key:value
        parts = re.split(r"\s*:\s*", line, maxsplit=1)
        if len(parts) == 2 and parts[0] and parts[1]:
            blocks.append({
                "type": "key_value",
                "key": parts[0].strip(),
                "value": parts[1].strip()
            })
            i += 1
            continue

        # CASE 2: label followed by value lines
        if looks_like_field_label(line):
            value_parts = []
            j = i + 1

            while j < len(lines):
                next_line = lines[j].strip()

                if not next_line:
                    j += 1
                    continue

                if looks_like_field_label(next_line):
                    break

                if is_valid_section_heading(next_line):
                    break

                value_parts.append(next_line)
                j += 1

            if value_parts:
                blocks.append({
                    "type": "key_value",
                    "key": line.replace(":", "").strip(),
                    "value": " ".join(value_parts)
                })
                i = j
                continue

        # fallback classification
        line_type = classify_line(line)

        if line_type != "empty":
            blocks.append({
                "type": line_type,
                "content": line
            })

        i += 1

    return blocks


def extract_blocks_from_page(page):
    raw_blocks = page["blocks"]

    # flatten layout blocks into ordered lines
    lines = []
    for b in raw_blocks:
        lines.extend(b["text"].split("\n"))

    blocks = build_blocks_from_lines(lines)

    final_blocks = []
    current_para = []
    current_section = None

    for b in blocks:
        btype = b["type"]

        if btype == "heading":
            if current_para:
                final_blocks.append({
                    "type": "paragraph",
                    "content": " ".join(current_para),
                    "section": current_section
                })
                current_para = []

            current_section = b["content"]
            b["section"] = current_section
            final_blocks.append(b)

        elif btype in ["key_value", "numbered_clause", "table_row"]:
            if current_para:
                final_blocks.append({
                    "type": "paragraph",
                    "content": " ".join(current_para),
                    "section": current_section
                })
                current_para = []

            b["section"] = current_section
            final_blocks.append(b)

        elif btype == "paragraph":
            current_para.append(b["content"])

        else:
            current_para.append(b["content"])

    if current_para:
        final_blocks.append({
            "type": "paragraph",
            "content": " ".join(current_para),
            "section": current_section
        })

    # attach metadata (important for GraphRAG)
    for b in final_blocks:
        b["block_id"] = str(uuid.uuid4())
        b["page_number"] = page["page_number"]
        b["source"] = page["source"]

    return final_blocks


def extract_blocks(pages):
    all_blocks = []

    for page in pages:
        page_blocks = extract_blocks_from_page(page)
        all_blocks.extend(page_blocks)

    return all_blocks
