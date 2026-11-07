"""Builds the report as a Word file, in the format the course brief sets.

The brief's Formatting Standard is Arial, 12 pt main text, 14 pt bold section titles, 1.5 line
spacing, justified, and 20 pages. ILP_Report_Skeleton.docx is not in that format, so it gives only
the title page and the styles; the chapters beside this script give the text. A chapter whose owner
has not yet rewritten it carries a visible note saying so: set its owner to "" in CHAPTERS, or pass
--clean, only once that is true.

    python3 docs/report/build_docx.py [--clean] [pages.json]

pages.json, if given, maps a heading to its page, for the contents list. Word refreshes the list on
opening either way.
"""

import json
import re
import struct
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
SKELETON = HERE / "ILP_Report_Skeleton.docx"
OUTPUT = HERE / "Report rebuilt from chapters (not the master).docx"  # the master is edited in Word
WIDTH = 9026  # A4 with one-inch margins
BODY, SMALL = 24, 20
GREEN, AMBER, GREY, INK = "0F5F52", "8A6224", "5A6560", "1A1A1A"
FONT = '<w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>'
JUSTIFY = '<w:jc w:val="both"/>'
SPACER = '<w:p><w:pPr><w:spacing w:after="0" w:line="120" w:lineRule="exact"/></w:pPr></w:p>'

# (title, file, who still has to rewrite it). "" means the text is its owner's own.
CHAPTERS = [
    ("Abstract", "00-abstract.md", "Christian"),
    ("1 · Introduction: the problem and the argument", "01-introduction.md", "Christian"),
    ("2 · Background and landscape", "02-background.md", "Siew"),
    ("3 · Solution design and architecture", "03-design.md", "Christian"),
    ("4 · Implementation", "04-implementation.md", "Christian and Zee"),
    ("5 · Evaluation and results", "05-evaluation-and-results.md", ""),
    ("6 · Governance, ethics and risk", "06-governance.md", "Siew"),
    (
        "7 · Value creation and organisational readiness",
        "07-value-creation.md",
        "Christian and Zee",
    ),
    ("8 · Limitations and future work", "08-limitations-and-future-work.md", "Desmond"),
    ("9 · Key findings, recommendations and conclusion", "09-conclusion.md", "Christian"),
]
CONTENTS_STYLES = "".join(  # so the list keeps its shape when Word refreshes it
    f'<w:style w:type="paragraph" w:styleId="TOC{n}"><w:name w:val="toc {n}"/>'
    f'<w:uiPriority w:val="39"/><w:pPr>'
    f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{WIDTH}"/></w:tabs>'
    f'<w:spacing w:before="{before}" w:after="10" w:line="240" w:lineRule="auto"/>'
    f'<w:ind w:left="{left}"/></w:pPr><w:rPr>{FONT}{bold}<w:sz w:val="19"/><w:szCs w:val="19"/>'
    "</w:rPr></w:style>"
    for n, before, left, bold in ((1, 50, 0, "<w:b/><w:bCs/>"), (2, 0, 240, ""))
)
SELECTION = "03-4-technology-selection.md"  # §3.4, placed between §3.3 and §3.5
REFERENCE_FILES = ("05-evaluation-and-results.md", SELECTION, "references-verified.md")


class Media:
    """Pictures used so far, for the package."""

    def __init__(self) -> None:
        self.files: list[Path] = []

    def add(self, path: Path) -> tuple[int, int, int]:
        self.files.append(path)
        width, height = image_size(path)
        return len(self.files), width, height


def image_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    at = 2
    while at < len(data):  # a JPEG's frame header holds its size
        marker, length = data[at + 1], struct.unpack(">H", data[at + 2 : at + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height, width = struct.unpack(">HH", data[at + 5 : at + 9])
            return width, height
        at += 2 + length
    raise ValueError(f"no size found in {path}")


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


def run(text: str, *, size: int = BODY, color: str = INK, flags: str = "", track: int = 0) -> str:
    props = FONT + flags + f'<w:color w:val="{color}"/>'
    props += f'<w:spacing w:val="{track}"/>' if track else ""
    props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    return f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def inline(text: str, size: int = BODY, color: str = INK) -> str:
    """Markdown bold, italic, code and links, as runs. The brief sets one font, so code uses it."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    out, bold, italic = [], False, False
    marks = (
        r"(`[^`]+`|\*\*|(?<![\w*])\*(?=\S)|(?<=\S)\*(?![\w*])|(?<![\w_])_(?=\S)|(?<=\S)_(?![\w_]))"
    )
    for part in re.split(marks, text):
        if not part:
            continue
        if part == "**":
            bold = not bold
        elif part in ("*", "_"):
            italic = not italic
        else:
            flags = ("<w:b/><w:bCs/>" if bold else "") + ("<w:i/><w:iCs/>" if italic else "")
            out.append(run(part.strip("`"), size=size, color=color, flags=flags))
    return "".join(out)


def para(text: str, *, after: int = 80, props: str = "", line: int = 360, jc: str = JUSTIFY) -> str:
    spacing = f'<w:spacing w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
    return f"<w:p><w:pPr>{spacing}{props}{jc}</w:pPr>{inline(text)}</w:p>"


def bullet(text: str) -> str:
    props = '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
    props += '<w:spacing w:after="40" w:line="360" w:lineRule="auto"/>'
    props += f'<w:ind w:left="400" w:hanging="280"/>{JUSTIFY}'
    return f"<w:p><w:pPr>{props}</w:pPr>{inline(text)}</w:p>"


def numbered(number: str, text: str) -> str:
    props = '<w:tabs><w:tab w:val="left" w:pos="400"/></w:tabs>'
    props += '<w:spacing w:after="40" w:line="360" w:lineRule="auto"/>'
    props += f'<w:ind w:left="400" w:hanging="400"/>{JUSTIFY}'
    return f"<w:p><w:pPr>{props}</w:pPr>{inline(number)}<w:r><w:tab/></w:r>{inline(text)}</w:p>"


def heading(text: str, level: int, *, new_page: bool = False) -> str:
    size = 28 if level == 1 else BODY
    before, after = (200, 80) if level == 1 else (120, 50)
    flags = "<w:b/><w:bCs/>" + ("<w:i/><w:iCs/>" if level == 3 else "")
    props = f'<w:pStyle w:val="Heading{level}"/><w:keepNext/>'
    props += "<w:pageBreakBefore/>" if new_page else ""
    props += f'<w:spacing w:after="{after}" w:before="{before}" w:line="276" w:lineRule="auto"/>'
    return f"<w:p><w:pPr>{props}</w:pPr>{run(text, size=size, flags=flags)}</w:p>"


def callout(label: str, text: str, color: str = AMBER, fill: str = "F5EEE0") -> str:
    borders = (
        f'<w:top w:val="none"/><w:left w:val="single" w:color="{color}" w:sz="14"/>'
        '<w:bottom w:val="none"/><w:right w:val="none"/>'
        '<w:insideH w:val="none"/><w:insideV w:val="none"/>'
    )
    head = run(label + "  ", size=17, color=color, flags="<w:b/><w:bCs/><w:caps/>", track=12)
    inner = (
        '<w:p><w:pPr><w:spacing w:after="20" w:before="20" w:line="252" w:lineRule="auto"/></w:pPr>'
        f"{head}{inline(text, SMALL, GREY)}</w:p>"
    )
    margins = "".join(
        f'<w:{side} w:type="dxa" w:w="{w}"/>'
        for side, w in (("top", 70), ("left", 180), ("bottom", 70), ("right", 160))
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
    size = 16 if max(len(c) for r in rows for c in r) > 150 else 19
    columns = len(rows[0])
    weights = [
        max(
            min(max(len(r[i]) for r in rows), 60),
            max(len(word) for r in rows for word in r[i].split()) * 2 + 2,
        )
        for i in range(columns)
    ]
    widths = [round(WIDTH * w / sum(weights)) for w in weights]
    widths[-1] += WIDTH - sum(widths)
    borders = (
        '<w:top w:val="single" w:color="9FB0A8" w:sz="4"/><w:left w:val="none"/>'
        '<w:bottom w:val="single" w:color="9FB0A8" w:sz="4"/><w:right w:val="none"/>'
        '<w:insideH w:val="single" w:color="D5DDD9" w:sz="2"/><w:insideV w:val="none"/>'
    )
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    out = [
        f'<w:tbl><w:tblPr><w:tblW w:type="dxa" w:w="{WIDTH}"/>'
        f'<w:tblBorders>{borders}</w:tblBorders><w:tblLayout w:type="fixed"/></w:tblPr>'
        f"<w:tblGrid>{grid}</w:tblGrid>"
    ]
    margins = (
        '<w:tcMar><w:top w:type="dxa" w:w="35"/><w:left w:type="dxa" w:w="70"/>'
        '<w:bottom w:type="dxa" w:w="35"/><w:right w:type="dxa" w:w="70"/></w:tcMar>'
    )
    keep = "<w:keepNext/>" if len(rows) <= 11 else ""  # a short table stays on one page
    for number, row in enumerate(rows):
        props = "<w:cantSplit/>" + ("<w:tblHeader/>" if number == 0 else "")
        out.append(f"<w:tr><w:trPr>{props}</w:trPr>")
        for width, cell in zip(widths, row, strict=True):
            shade = '<w:shd w:fill="EEF3F0" w:val="clear"/>' if number == 0 else ""
            text = f"**{cell}**" if number == 0 and cell and "**" not in cell else cell
            out.append(
                f'<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="{width}"/>{shade}{margins}</w:tcPr>'
                f'<w:p><w:pPr>{keep}<w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
                f"{inline(text, size)}</w:p></w:tc>"
            )
        out.append("</w:tr>")
    out.append("</w:tbl>" + SPACER + SPACER)
    return "".join(out)


def picture(path: Path, caption: str, scale: float, media: Media) -> str:
    """An inline picture and its caption. `scale` is a share of the text width."""
    number, width, height = media.add(path)
    cx = int(WIDTH * 635 * scale)
    cy = int(cx * height / width)
    graphic = (
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{number}" name="{path.name}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="rIdMedia{number}"/><a:stretch><a:fillRect/></a:stretch>'
        "</pic:blipFill><pic:spPr><a:xfrm>"
        f'<a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
        "</a:graphicData></a:graphic>"
    )
    description = escape(caption.replace("*", ""), {'"': "&quot;"})
    drawing = (
        f'<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" '
        f'cy="{cy}"/><wp:docPr id="{100 + number}" name="Figure {number}" '
        f'descr="{description}"/>{graphic}</wp:inline></w:drawing>'
    )
    centre = '<w:jc w:val="center"/>'
    image = (
        f'<w:p><w:pPr><w:keepNext/><w:spacing w:after="60"/>{centre}</w:pPr>'
        f"<w:r>{drawing}</w:r></w:p>"
    )
    note = (
        f'<w:p><w:pPr><w:spacing w:after="160" w:line="252" w:lineRule="auto"/>{centre}</w:pPr>'
        f"{inline(caption, SMALL, GREY)}</w:p>"
    )
    return image + note


def markdown(text: str, media: Media, level: int = 3) -> str:
    """The Markdown these chapters use, as Word paragraphs and tables."""
    out, lines, i = [], text.strip().splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip() == "---":
            i += 1
        elif image := re.fullmatch(r"!\[(.+)\]\(([^)|]+)(?:\|([\d.]+))?\)", line.strip()):
            scale = float(image.group(3) or 1)
            out.append(picture(HERE / image.group(2), image.group(1), scale, media))
            i += 1
        elif line.startswith("#"):
            out.append(heading(line.lstrip("# ").strip(), level))
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in re.split(r"(?<!\\)\|", lines[i].strip())[1:-1]]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append([c.replace("\\|", "|") for c in cells])
                i += 1
            out.append(table(rows))
        elif line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> ").strip())
                i += 1
            ind = '<w:ind w:left="360" w:right="360"/>'
            out.append(para(" ".join(quote), props=ind))
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
                i < len(lines) and lines[i].strip() and not re.match(r"[#|>!]|\d+\. |- ", lines[i])
            ):
                words.append(lines[i].strip())
                i += 1
            out.append(para(" ".join(words)))
    return "".join(out)


def sections(text: str) -> dict[str, str]:
    """A chapter split at its `## ` headings, keyed by heading."""
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    return {parts[n].strip(): parts[n + 1] for n in range(1, len(parts) - 1, 2)}


def body_of(text: str) -> str:
    """A chapter without its title, its note and its references."""
    text = text.split("### References used")[0]
    return text.split("\n---\n", 1)[1] if "\n---\n" in text else text


def references() -> list[str]:
    """Every entry the chapters hold, sorted, each once."""
    found = set()
    for name in REFERENCE_FILES:
        text = (HERE / name).read_text()
        if name != "references-verified.md":
            text = text.split("### References used in this section")[1]
        found |= {" ".join(entry.split()) for entry in text.strip().split("\n\n") if entry.strip()}
    return sorted(found, key=lambda entry: entry.lstrip('*"').lower())


def contents(body: list[str], pages: dict[str, int]) -> str:
    """The contents field, filled in so it reads before Word has refreshed it."""
    entries = []
    for element in body:
        style = re.search(r'<w:pStyle w:val="Heading([12])"/>', element[:200])
        if style:
            name = "".join(re.findall(r"<w:t[^>]*>([^<]*)", element)).replace("&amp;", "&")
            if name != "Contents":
                entries.append((int(style.group(1)), name))
    out, instruction = [], 'TOC \\h \\o "1-2"'
    for number, (level, name) in enumerate(entries):
        props = (
            f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{WIDTH}"/></w:tabs>'
            f'<w:spacing w:after="10" w:before="{50 if level == 1 else 0}" w:line="240" '
            f'w:lineRule="auto"/><w:ind w:left="{0 if level == 1 else 240}"/>'
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


def chapter(title: str, name: str, owner: str, clean: bool, media: Media) -> list[str]:
    text = (HERE / name).read_text()
    out = [heading(title, 1, new_page=title == "Abstract")]
    if owner and not clean:
        note = "Not yet rewritten in the owner's own words."
        out.append(callout(f"Draft · for {owner}", note))
    body = body_of(text)
    parts = sections(body)
    lead = body.split("## ", 1)[0].strip()
    if lead:
        out.append(markdown(lead, media))
    if name == "03-design.md":
        selection = body_of((HERE / SELECTION).read_text())
        ordered = {}
        for key, value in parts.items():
            if key.startswith("3.5"):
                ordered["3.4 Technology selection, and the reasoning behind it"] = selection
            ordered[key] = value
        parts = ordered
    for key, value in parts.items():
        out.append(heading(key, 2))
        out.append(markdown(value, media))
    return out


def main() -> None:
    args = sys.argv[1:]
    clean = "--clean" in args
    paths = [a for a in args if a != "--clean"]
    pages = json.loads(Path(paths[0]).read_text()) if paths else {}
    package = zipfile.ZipFile(SKELETON)
    document = package.read("word/document.xml").decode()
    start, end = document.index("<w:body>") + 8, document.index("</w:body>")
    old = elements(document[start:end])
    media = Media()

    title_page = [e for n, e in enumerate(old[:7]) if n != 5]
    title_page = [
        e.replace('w:w="9360"', f'w:w="{WIDTH}"').replace('w:w="6960"', f'w:w="{WIDTH - 2400}"')
        for e in title_page
    ]
    body = [*title_page, heading("Contents", 1, new_page=True), "CONTENTS"]
    for title, name, owner in CHAPTERS:
        body += chapter(title, name, owner, clean, media)

    body.append(heading("References", 1, new_page=True))
    hang = '<w:ind w:left="480" w:hanging="480"/>'
    body += [para(e, after=16, props=hang, line=240, jc="") for e in references()]

    body.append(heading("Appendices", 1, new_page=True))
    body.append(para("Excluded from the twenty-page body. Appendices C and D follow."))
    listing = next(e for e in old if e.startswith("<w:tbl") and "Team contribution" in e)
    narrower = f'w:w="{4100 - (9360 - WIDTH)}"'
    body.append(listing.replace('w:w="9360"', f'w:w="{WIDTH}"').replace('w:w="4100"', narrower))
    appendix = (HERE / "appendix-c-evaluation-results.md").read_text()
    body.append(heading("Appendix C · Full evaluation results", 2, new_page=True))
    body.append(para("The raw runs are in `eval/results/`."))
    body.append(markdown(appendix[appendix.index("## C.1") :], media))
    sample = (HERE / "appendix-d-golden-set-sample.md").read_text()
    body.append(heading("Appendix D · Golden set: sample questions", 2, new_page=True))
    body.append(markdown(sample[sample.index("The sample is chosen") :], media))

    joined = [contents(body, pages) if part == "CONTENTS" else part for part in body]
    tail = next(e for e in old if e.startswith("<w:sectPr"))
    tail = tail.replace('w:right="1512"', 'w:right="1440"').replace(
        'w:left="1512"', 'w:left="1440"'
    )
    document = document[:start] + "".join(joined) + tail + document[end:]
    document = document.replace("Aptos Display", "Arial").replace("Aptos", "Arial")

    declared = package.read("[Content_Types].xml").decode()
    types = "".join(  # Word refuses a file that declares an extension twice; the skeleton has some
        f'<Default Extension="{ext}" ContentType="image/{kind}"/>'
        for ext, kind in (("png", "png"), ("jpg", "jpeg"))
        if f'Extension="{ext}"' not in declared
    )
    relations = "".join(
        f'<Relationship Id="rIdMedia{n}" Target="media/image{n}{p.suffix}" Type="http://schemas.'
        'openxmlformats.org/officeDocument/2006/relationships/image"/>'
        for n, p in enumerate(media.files, 1)
    )
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as out:
        for item in package.infolist():
            if item.filename.endswith("/"):
                continue
            data = package.read(item.filename)
            if item.filename == "word/document.xml":
                data = document.encode()
            elif item.filename == "[Content_Types].xml":
                data = data.replace(b"</Types>", types.encode() + b"</Types>")
            elif item.filename == "word/_rels/document.xml.rels":
                data = data.replace(b"</Relationships>", relations.encode() + b"</Relationships>")
            elif item.filename == "word/header1.xml":
                label = b"clean" if clean else b"draft"
                data = data.replace(b"skeleton", label).replace(b"Aptos", b"Arial")
            elif item.filename == "word/styles.xml":
                data = data.replace(b"</w:styles>", CONTENTS_STYLES.encode() + b"</w:styles>")
                data = re.sub(  # a refreshed contents list uses this style
                    rb'(w:styleId="Hyperlink">.*?<w:rPr>)',
                    rb"\1" + FONT.encode(),
                    data,
                    count=1,
                    flags=re.S,
                )
            elif item.filename == "docProps/core.xml":
                data = data.replace(
                    "ILP Project Report — skeleton".encode(), b"Project Parrot: final report"
                ).replace(b"Report skeleton for", b"Report for")
            if item.filename.endswith(".xml"):  # the brief sets one font, numbering included
                data = data.replace(b"Aptos Display", b"Arial").replace(b"Aptos", b"Arial")
            out.writestr(item.filename, data)
        for number, path in enumerate(media.files, 1):
            out.write(path, f"word/media/image{number}{path.suffix}")
    print(OUTPUT)


if __name__ == "__main__":
    main()
