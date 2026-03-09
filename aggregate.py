import os
import re
import sys
import json
from pathlib import Path

INPUT_DIR = "exports"
OUTPUT_DIR = "processed"

# naive classifier based on keywords

def classify_text(text):
    # default
    topic = "其他"
    sub = "其他"
    keywords = []
    if "郵件" in text or "Notion" in text:
        topic = "對話整理機制"
        sub = "郵件分析"
        keywords.append("郵件")
    if "700" in text or "RAG" in text or "向量" in text:
        topic = "對話整理機制"
        sub = "RAG建置"
        keywords.append("RAG")
    if "記憶" in text:
        topic = "對話整理機制"
        sub = "AI記憶"
        keywords.append("記憶")
    # more heuristics can be added
    return topic, sub, keywords


def main(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    results = {}
    for f in sorted(input_path.glob("*.md")):
        id = f.stem.split("_")[0]
        text = f.read_text(encoding="utf-8", errors="ignore")
        topic, sub, kws = classify_text(text)
        results[id] = {"topic": topic, "subtopic": sub, "keywords": kws}

    # grouping
    groups = {}
    for id, cls in results.items():
        t = cls["topic"]
        s = cls["subtopic"]
        groups.setdefault(t, {}).setdefault(s, []).append(id)

    # write json log
    with open(output_path / "groups.json", "w", encoding="utf-8") as out:
        json.dump(groups, out, ensure_ascii=False, indent=2)

    # merge documents per topic
    for topic, subs in groups.items():
        lines = []
        # header frontmatter
        lines.append("---")
        lines.append(f"topic: {topic}")
        lines.append(f"subtopics: {list(subs.keys())}")
        srcs = []
        for ids in subs.values():
            srcs.extend(ids)
        lines.append(f"source_files: {srcs}")
        lines.append("keywords: []")
        lines.append("---\n")
        lines.append(f"# {topic}\n")
        for sub, ids in subs.items():
            lines.append(f"## 子主題：{sub}\n")
            for id in sorted(ids):
                fname = next(input_path.glob(f"{id}_*.md"), None)
                if fname:
                    content = fname.read_text(encoding="utf-8", errors="ignore")
                    # simple include entire file
                    lines.append(f"### 檔案 {fname.name}\n")
                    lines.append(content)
                    lines.append("\n---\n")
        with open(output_path / f"{topic}_完整版.md", "w", encoding="utf-8") as out:
            out.write("\n".join(lines))

    print("Analysis complete. results in", output_dir)


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else INPUT_DIR
    outp = sys.argv[2] if len(sys.argv) > 2 else OUTPUT_DIR
    main(inp, outp)
