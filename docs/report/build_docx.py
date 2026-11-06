"""Builds the report as a Word file from ILP_Report_Skeleton.docx and the chapters beside it.

The skeleton gives the title page, the styles and the section order. Its guidance boxes are dropped.
A section with a chapter behind it gets that chapter; a section without one keeps a marked gap that
names its owner, so nothing is invented and the file can be rebuilt as sections arrive.

    python docs/report/build_docx.py [pages.json]

pages.json, if given, maps a heading to its page, for the contents list. Word refreshes the list on
opening either way. Add a section by writing its chapter here and changing `body` below.
"""

import json
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
SKELETON = HERE / "ILP_Report_Skeleton.docx"
OUTPUT = HERE / "Project Parrot Final Report (draft).docx"
WIDTH = 8882  # A4 less the skeleton's margins; its own tables are 9360 and overhang the right edge
GREEN, AMBER, GREY, INK = "0F5F52", "8A6224", "5A6560", "1A1A1A"
SPACER = '<w:p><w:pPr><w:spacing w:after="0" w:line="120" w:lineRule="exact"/></w:pPr></w:p>'
FONT = '<w:rFonts w:ascii="{0}" w:cs="{0}" w:eastAsia="{0}" w:hAnsi="{0}"/>'

# Skeleton element -> who owes that passage, for each gap. The text is the skeleton's own brief.
GAPS = {
    36: "Christian",
    41: "Christian",
    44: "Christian",
    54: "Christian",
    57: "Christian",
    62: "Siew",
    64: "Siew",
    66: "Siew",
    71: "Christian",
    73: "Christian",
    81: "Christian",
    86: "Christian",
    88: "Christian",
    95: "Christian",
    120: "Siew",
    123: "Siew",
    125: "Siew",
    128: "Siew",
    130: "Siew",
    135: "Christian and Zee",
    137: "Christian and Zee",
    139: "Christian and Zee",
    141: "Christian and Zee",
    148: "Christian",
    152: "Siew, with everyone's sources",
}
SCAFFOLD_ONLY = {
    "[Draft in week 8.]",
    "[Quarter page.]",
    "[Half a page.]",
    "[One page including the selection table.]",
    "[Half a page including the stage-by-process table.]",
}


def elements(body: str) -> list[str]:
    """The body's top-level elements, in order."""
    found, pos = [], 0
    pattern = re.compile(r"<w:(p|tbl|sectPr|sdt)[ >/]")
    while match := pattern.search(body, pos):
        close = f"</w:{match.group(1)}>"
        end = body.index(close, match.start()) + len(close)
        found.append(body[match.start() : end])
        pos = end
    return found


def run(
    text: str,
    *,
    size: int = 21,
    color: str = INK,
    flags: str = "",
    font: str = "Aptos",
    track: int = 0,
) -> str:
    props = FONT.format(font) + flags + f'<w:color w:val="{color}"/>'
    props += f'<w:spacing w:val="{track}"/>' if track else ""
    props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    return f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def inline(text: str, size: int = 21, color: str = INK) -> str:
    """Markdown bold, italic, code and links, as runs."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    out, bold, italic = [], False, False
    for part in re.split(
        r"(`[^`]+`|\*\*|(?<![\w*])\*(?=\S)|(?<=\S)\*(?![\w*])|(?<![\w_])_(?=\S)|(?<=\S)_(?![\w_]))",
        text,
    ):
        if not part:
            continue
        if part == "**":
            bold = not bold
        elif part in ("*", "_"):
            italic = not italic
        else:
            flags = ("<w:b/><w:bCs/>" if bold else "") + ("<w:i/><w:iCs/>" if italic else "")
            if part.startswith("`"):
                out.append(
                    run(part[1:-1], size=size - 2, color=color, flags=flags, font="Consolas")
                )
                continue
            for piece in re.split("(⟨holdout⟩)", part):
                if piece == "⟨holdout⟩":
                    out.append(run(piece, size=size, color=AMBER, flags="<w:b/><w:bCs/>"))
                elif piece:
                    out.append(run(piece, size=size, color=color, flags=flags))
    return "".join(out)


def para(text: str, *, after: int = 140, extra: str = "", size: int = 21) -> str:
    props = f'<w:spacing w:after="{after}" w:line="288"/>{extra}'
    return f"<w:p><w:pPr>{props}</w:pPr>{inline(text, size)}</w:p>"


def bullet(text: str) -> str:
    props = '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
    props += '<w:spacing w:after="80" w:line="288"/><w:ind w:left="400" w:hanging="260"/>'
    return f"<w:p><w:pPr>{props}</w:pPr>{inline(text)}</w:p>"


def numbered(number: str, text: str) -> str:
    props = '<w:tabs><w:tab w:val="left" w:pos="400"/></w:tabs>'
    props += '<w:spacing w:after="80" w:line="288"/><w:ind w:left="400" w:hanging="400"/>'
    tab = "<w:r><w:tab/></w:r>"
    return f"<w:p><w:pPr>{props}</w:pPr>{inline(number)}{tab}{inline(text)}</w:p>"


def heading(text: str, level: int) -> str:
    size, color = {1: (30, INK), 3: (21, INK), 4: (21, GREEN)}[level]
    props = (
        f'<w:pStyle w:val="Heading{level}"/><w:keepNext/><w:spacing w:after="80" w:before="220"/>'
    )
    text_run = run(text, size=size, color=color, flags="<w:b/><w:bCs/>", font="Aptos Display")
    return f"<w:p><w:pPr>{props}</w:pPr>{text_run}</w:p>"


def callout(label: str, text: str, color: str = AMBER, fill: str = "F5EEE0") -> str:
    borders = (
        f'<w:top w:val="none"/><w:left w:val="single" w:color="{color}" w:sz="14"/>'
        '<w:bottom w:val="none"/><w:right w:val="none"/>'
        '<w:insideH w:val="none"/><w:insideV w:val="none"/>'
    )
    head = run(label + "  ", size=17, color=color, flags="<w:b/><w:bCs/><w:caps/>", track=12)
    spacing = '<w:spacing w:after="40" w:before="40" w:line="264"/>'
    inner = f"<w:p><w:pPr>{spacing}</w:pPr>{head}{inline(text, 19, GREY)}</w:p>"
    margins = "".join(
        f'<w:{side} w:type="dxa" w:w="{w}"/>'
        for side, w in (("top", 130), ("left", 200), ("bottom", 130), ("right", 180))
    )
    cell = (
        f'<w:tcPr><w:tcW w:type="dxa" w:w="{WIDTH}"/><w:shd w:fill="{fill}" w:val="clear"/>'
        f"<w:tcMar>{margins}</w:tcMar></w:tcPr>"
    )
    return (
        f'<w:tbl><w:tblPr><w:tblW w:type="dxa" w:w="{WIDTH}"/>'
        f"<w:tblBorders>{borders}</w:tblBorders></w:tblPr>"
        f'<w:tblGrid><w:gridCol w:w="{WIDTH}"/></w:tblGrid>'
        f"<w:tr><w:tc>{cell}{inner}</w:tc></w:tr></w:tbl>" + SPACER
    )


def table(rows: list[list[str]]) -> str:
    size = 16 if max(len(c) for r in rows for c in r) > 90 else 18
    columns = len(rows[0])
    weights = [
        max(min(max(len(r[i]) for r in rows), 60), len(rows[0][i]) + 4) for i in range(columns)
    ]
    widths = [round(WIDTH * w / sum(weights)) for w in weights]
    widths[-1] += WIDTH - sum(widths)
    borders = (
        '<w:top w:val="single" w:color="C9D2CD" w:sz="4"/><w:left w:val="none"/>'
        '<w:bottom w:val="single" w:color="C9D2CD" w:sz="4"/><w:right w:val="none"/>'
        '<w:insideH w:val="single" w:color="E2E8E4" w:sz="2"/><w:insideV w:val="none"/>'
    )
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    out = [
        f'<w:tbl><w:tblPr><w:tblW w:type="dxa" w:w="{WIDTH}"/>'
        f"<w:tblBorders>{borders}</w:tblBorders>"
        f'<w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>{grid}</w:tblGrid>'
    ]
    margins = (
        '<w:tcMar><w:top w:type="dxa" w:w="50"/><w:left w:type="dxa" w:w="80"/>'
        '<w:bottom w:type="dxa" w:w="50"/><w:right w:type="dxa" w:w="80"/></w:tcMar>'
    )
    keep = "<w:keepNext/>" if len(rows) <= 10 else ""  # a short table stays on one page
    for number, row in enumerate(rows):
        props = "<w:cantSplit/>" + ("<w:tblHeader/>" if number == 0 else "")
        out.append(f"<w:tr><w:trPr>{props}</w:trPr>")
        for width, cell in zip(widths, row, strict=True):
            shade = '<w:shd w:fill="EEF3F0" w:val="clear"/>' if number == 0 else ""
            text = f"**{cell}**" if number == 0 and cell and "**" not in cell else cell
            out.append(
                f'<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="{width}"/>{shade}{margins}</w:tcPr>'
                f'<w:p><w:pPr>{keep}<w:spacing w:after="0" w:line="252"/></w:pPr>'
                f"{inline(text, size)}</w:p></w:tc>"
            )
        out.append("</w:tr>")
    out.append("</w:tbl>" + SPACER)
    return "".join(out)


def markdown(text: str) -> str:
    """The Markdown these chapters use, as Word paragraphs and tables."""
    out, lines, i = [], text.strip().splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip() == "---":
            i += 1
        elif line.startswith("#"):
            out.append(heading(line.lstrip("# ").strip(), 4))
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in re.split(r"(?<!\\)\|", lines[i].strip())[1:-1]]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            out.append(table(rows))
        elif line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> ").strip())
                i += 1
            out.append(callout("Note", " ".join(quote), GREEN, "E7F1EE"))
        elif item := re.match(r"(\d+\.|-) (.*)", line):
            words = [item.group(2)]
            i += 1
            while i < len(lines) and lines[i].startswith("  ") and lines[i].strip():
                words.append(lines[i].strip())
                i += 1
            joined = " ".join(words)
            out.append(bullet(joined) if item.group(1) == "-" else numbered(item.group(1), joined))
        else:
            words = []
            while (
                i < len(lines) and lines[i].strip() and not re.match(r"[#|>]|\d+\. |- ", lines[i])
            ):
                words.append(lines[i].strip())
                i += 1
            out.append(para(" ".join(words)))
    return "".join(out)


def sections(text: str, level: str = "## ") -> dict[str, str]:
    """A chapter split at its headings, keyed by heading."""
    parts = re.split(rf"^{level}(.+)$", text, flags=re.M)
    return {parts[n].strip(): parts[n + 1] for n in range(1, len(parts) - 1, 2)}


def gap(element: str, owner: str) -> str:
    brief = "".join(re.findall(r"<w:t[^>]*>([^<]*)", element))
    brief = brief.replace("&apos;", "'").replace("&amp;", "&").replace("&quot;", '"')
    unwritten = brief in SCAFFOLD_ONLY or brief.startswith("[Write ")
    text = "Not yet written." if unwritten else brief.strip("[]")
    return callout(f"To write · {owner}", text)


def zee_section(chapter: dict[str, str], title: str) -> str:
    key = next(k for k in chapter if k.startswith(title))
    name = re.sub(r"^\d · ", "", re.sub(r" \((feeds|ADR).*\)$", "", key))
    return heading(name, 4) + markdown(chapter[key])


def contents(body: list[str], pages: dict[str, int]) -> str:
    """The contents field, filled in so it reads before Word has refreshed it."""
    entries = []
    for element in body:
        style = re.search(r'<w:pStyle w:val="Heading([123])"/>', element)
        if style and not element.startswith("<w:tbl"):
            name = "".join(re.findall(r"<w:t[^>]*>([^<]*)", element)).replace("&amp;", "&")
            if name != "Contents":
                entries.append((int(style.group(1)), name))
    out, instruction = [], 'TOC \\h \\o "1-3"'
    for number, (level, name) in enumerate(entries):
        indent = 0 if level == 1 else 240
        props = (
            f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{WIDTH}"/></w:tabs>'
            f'<w:spacing w:after="30" w:before="{70 if level == 1 else 0}" w:line="240"/>'
            f'<w:ind w:left="{indent}"/>'
        )
        field = ""
        if number == 0:
            field = (
                '<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
                f'<w:r><w:instrText xml:space="preserve">{escape(instruction)}</w:instrText></w:r>'
                '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            )
        tail = '<w:r><w:fldChar w:fldCharType="end"/></w:r>' if number == len(entries) - 1 else ""
        flags = "<w:b/><w:bCs/>" if level == 1 else ""
        page = run(str(pages.get(name, "")), size=19)
        out.append(
            f"<w:p><w:pPr>{props}</w:pPr>{field}{run(name, size=19, flags=flags)}"
            f"<w:r><w:tab/></w:r>{page}{tail}</w:p>"
        )
    return (
        '<w:sdt><w:sdtPr><w:alias w:val="Contents"/></w:sdtPr><w:sdtContent>'
        + "".join(out)
        + "</w:sdtContent></w:sdt>"
    )


def main() -> None:
    pages = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else {}
    package = zipfile.ZipFile(SKELETON)
    document = package.read("word/document.xml").decode()
    start, end = document.index("<w:body>") + 8, document.index("</w:body>")
    old = elements(document[start:end])

    evaluation = (HERE / "05-evaluation-and-results.md").read_text()
    results = sections(evaluation[: evaluation.index("### References used")])
    opening = evaluation[evaluation.index("A household document assistant") :].split("## 5.1")[0]
    status = re.search(r"> \*\*Status\.\*\* (.*?)\n\n", evaluation, re.S).group(1)
    status = " ".join(line.lstrip("> ") for line in status.splitlines())
    selection = (HERE / "03-4-technology-selection.md").read_text()
    table_part, cited = selection.split("### References used in this section")
    table_part = table_part[table_part.index("Every layer runs") :]
    references = evaluation[evaluation.index("### References used") :].split("\n", 1)[1]
    entries = sorted(
        {" ".join(e.split()) for e in (references + "\n\n" + cited).strip().split("\n\n")},
        key=str.lower,
    )
    packs = sections((HERE / "04-packs-and-interface.md").read_text())
    roadmap = (HERE / "07-commercialisation-roadmap.md").read_text()
    roadmap = "It claims no price" + roadmap.split("It claims no price", 1)[1]
    limits = (HERE / "08-limitations-and-future-work.md").read_text()
    limits = limits[limits.index("## What ten weeks") :]
    appendix = (HERE / "appendix-c-evaluation-results.md").read_text()
    appendix = appendix[appendix.index("## C.1") :]
    sample = (HERE / "appendix-d-golden-set-sample.md").read_text()
    sample = sample[sample.index("The sample is chosen") :]
    result = {key.split(" ")[0]: value for key, value in results.items()}

    zee_note = callout(
        "Draft · Zee",
        "From the longer packs chapter, not yet condensed to the budget or re-checked after the "
        "28 October freeze.",
    )
    replaced = {
        75: zee_note
        + markdown(packs["The argument"])
        + zee_section(packs, "1 ·")
        + zee_section(packs, "5 ·")
        + gap("<w:t>[Figure 2 is still to draw.]</w:t>", "Christian and Zee"),
        90: zee_note
        + zee_section(packs, "2 ·")
        + zee_section(packs, "3 ·")
        + zee_section(packs, "4 ·"),
        92: zee_note
        + zee_section(packs, "6 ·")
        + heading("What this chapter does not claim", 4)
        + markdown(packs["What this chapter does not claim"]),
        78: callout("Draft · Yew Mun", "For Christian to review.") + markdown(table_part),
        100: markdown(result["5.1"]),
        103: markdown(result["5.2"]),
        105: markdown(result["5.3"]),
        107: markdown(result["5.4"]),
        110: markdown(result["5.5"]),
        112: markdown(result["5.6"]),
        115: markdown(result["5.7"]),
        145: callout("Draft · Yew Mun", "For Desmond to review and add to.") + markdown(limits),
        152: "".join(
            para(entry, extra='<w:ind w:left="480" w:hanging="480"/>') for entry in entries
        )
        + gap(old[152], GAPS[152]),
    }
    body: list[str] = []
    for number, element in enumerate(old):
        is_table = element.startswith("<w:tbl")
        if number > 32 and 'w:type="page"' in element:
            continue  # the heading it precedes carries the break, so it cannot strand a blank page
        if number > 32 and 'w:type="page"' in old[number - 1]:
            element = element.replace(
                '<w:pStyle w:val="Heading1"/>', '<w:pStyle w:val="Heading1"/><w:pageBreakBefore/>'
            )
        if number == 5 or 8 <= number <= 29 or number in (31, 47, 50, 51, 155, 157, 158):
            continue  # the working-title note, the guidance pages, the notes beside the thesis
        if is_table and number not in (6, 49, 156):
            continue  # a guidance box
        if number == 32:
            body.append("CONTENTS")
        elif number == 48:
            body.append(
                callout(
                    "To refine · Christian",
                    "The skeleton's working thesis, to be refined but not weakened.",
                )
            )
        elif number == 97:
            body.append(element)
            body.append(callout("Status", status))
            body.append(markdown(opening))
        elif number == 108:
            body.append(
                element.replace(
                    "5.5 Abstention, and why it is the headline", "5.5 Unsupported claims"
                )
            )
        elif number == 141:
            body.append(
                callout("Draft · Zee", "The commercialisation roadmap, for Christian's §7.")
            )
            body.append(markdown(roadmap))
            body.append(gap(element, GAPS[number]))
        elif number in replaced:
            body.append(replaced[number])
        elif number in GAPS:
            body.append(gap(element, GAPS[number]))
        elif number == 156:
            body.append(element.replace('w:w="9360"', f'w:w="{WIDTH}"'))
            title = heading("Appendix C · Full evaluation results", 1)
            body.append(title.replace("<w:keepNext/>", "<w:keepNext/><w:pageBreakBefore/>"))
            body.append(
                para("Excluded from the twenty-page body. The raw runs are in `eval/results/`.")
            )
            body.append(callout("Status", status.split(" §5.6")[0]))
            body.append(markdown(appendix))
            title = heading("Appendix D · Golden set: sample questions", 1)
            body.append(title.replace("<w:keepNext/>", "<w:keepNext/><w:pageBreakBefore/>"))
            body.append(markdown(sample))
        elif number == 6:
            body.append(
                element.replace('w:w="9360"', f'w:w="{WIDTH}"').replace(
                    'w:w="6960"', f'w:w="{WIDTH - 2400}"'
                )
            )
        else:
            body.append(element)
    joined = [contents(body, pages) if part == "CONTENTS" else part for part in body]
    document = document[:start] + "".join(joined) + document[end:]

    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as out:
        for item in package.infolist():
            if item.filename.endswith("/"):
                continue
            data = package.read(item.filename)
            if item.filename == "word/document.xml":
                data = document.encode()
            elif item.filename == "word/header1.xml":
                data = data.replace(b"skeleton", b"draft")
            elif item.filename == "docProps/core.xml":
                data = data.replace(
                    "ILP Project Report — skeleton".encode(),
                    b"Project Parrot: final report (draft)",
                )
                data = data.replace(b"Report skeleton for", b"Report draft for")
            out.writestr(item.filename, data)
    print(OUTPUT)


if __name__ == "__main__":
    main()
