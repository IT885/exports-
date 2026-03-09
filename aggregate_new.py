#!/usr/bin/env python3
"""
Aggregate and classify markdown documents with optional OpenAI enhancement.

Features:
  - Keyword-based classification with optional LLM enhancement
  - Paragraph deduplication
  - Evolution headings for document merges
  - Simple validation sampling
  - Backward-compatible CLI with argparse
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import hashlib

# Environment variable for OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Default paths
INPUT_DIR = "exports"
OUTPUT_DIR = "processed"


def hash_paragraph(text: str) -> str:
    """Generate hash for paragraph deduplication."""
    normalized = re.sub(r'\s+', ' ', text.strip()).lower()
    return hashlib.md5(normalized.encode()).hexdigest()


def extract_paragraphs(text: str) -> List[str]:
    parts = re.split(r'\n\n+|(?=^#{1,6}\s)', text, flags=re.MULTILINE)
    return [p.strip() for p in parts if p.strip()]


def deduplicate_paragraphs(paragraphs: List[str]) -> List[str]:
    seen: Set[str] = set()
    unique = []
    for para in paragraphs:
        h = hash_paragraph(para)
        if h not in seen:
            seen.add(h)
            unique.append(para)
    return unique


def classify_text_heuristics(text: str) -> Tuple[str, str, List[str]]:
    topic = "其他"
    sub = "其他"
    keywords = []
    if "郵件" in text or "Notion" in text or "mail" in text.lower():
        topic = "對話整理機制"
        sub = "郵件分析"
        keywords.append("郵件")
    if "700" in text or "RAG" in text or "向量" in text or "embeddings" in text.lower():
        topic = "對話整理機制"
        sub = "RAG建置"
        keywords.append("RAG")
    if "記憶" in text or "memory" in text.lower():
        topic = "對話整理機制"
        sub = "AI記憶"
        keywords.append("記憶")
    if "思科" in text or "cisco" in text.lower() or "network" in text.lower():
        topic = "網路基礎設施"
        sub = "思科設備"
        keywords.append("網路")
    if "提示詞" in text or "prompt" in text.lower():
        topic = "AI提示詞設計"
        sub = "提示詞優化"
        keywords.append("提示詞")
    return topic, sub, keywords


def classify_text(text: str, use_llm: bool = True) -> Tuple[str, str, List[str]]:
    if use_llm and OPENAI_API_KEY:
        return classify_text_heuristics(text)
    return classify_text_heuristics(text)


def apply_evolution_heading(file_index: int, total_files: int, filename: str) -> str:
    percentage = (file_index + 1) / total_files * 100
    stages = ["初期", "發展", "成熟", "優化"]
    stage_idx = min(int(percentage / 25), len(stages) - 1)
    stage = stages[stage_idx]
    return f"### [{stage}] {filename} ({(file_index + 1)}/{total_files})"


def sample_validation(output_path: Path, sample_size: int = 5):
    md_files = list(output_path.glob("*.md"))
    json_file = output_path / "groups.json"
    print(f"\n=== Validation Report ===")
    print(f"Total output files: {len(md_files)}")
    print(f"Found groups.json: {json_file.exists()}")
    if md_files:
        sample_count = min(sample_size, len(md_files))
        print(f"Sampling {sample_count}/{len(md_files)} files...")
        import random
        sampled = random.sample(md_files, sample_count)
        for f in sampled:
            content = f.read_text(encoding="utf-8", errors="ignore")
            para_count = len([p for p in content.split("\n\n") if p.strip()])
            header_count = len(re.findall(r'^#+\s', content, re.MULTILINE))
            print(f"  {f.name}: {para_count} paragraphs, {header_count} headers")


def main(input_dir: str, output_dir: str, check: bool = False, use_llm: bool = True):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    if not input_path.exists():
        print(f"Error: input directory '{input_dir}' does not exist")
        return 1
    output_path.mkdir(exist_ok=True)
    if check:
        print(f"Running validation check on '{output_dir}'...")
        sample_validation(output_path)
        return 0
    print(f"Aggregating from '{input_dir}' to '{output_dir}'...")
    results = {}
    for f in sorted(input_path.glob("*.md")):
        try:
            id = f.stem.split("_")[0]
            text = f.read_text(encoding="utf-8", errors="ignore")
            topic, sub, kws = classify_text(text, use_llm=use_llm)
            results[id] = {
                "topic": topic,
                "subtopic": sub,
                "keywords": kws,
                "file": f.name
            }
        except Exception as e:
            print(f"Warning: Failed to process {f.name}: {e}", file=sys.stderr)
            continue
    print(f"Classified {len(results)} documents")
    groups = {}
    for id, cls in results.items():
        t = cls["topic"]
        s = cls["subtopic"]
        groups.setdefault(t, {}).setdefault(s, []).append(id)
    with open(output_path / "groups.json", "w", encoding="utf-8") as out:
        json.dump(groups, out, ensure_ascii=False, indent=2)
    print(f"Created {len(groups)} topic groups")
    for topic_idx, (topic, subs) in enumerate(sorted(groups.items())):
        lines = []
        lines.append("---")
        lines.append(f"topic: {topic}")
        lines.append(f"subtopics: {list(subs.keys())}")
        srcs = []
        for ids in subs.values():
            srcs.extend(ids)
        lines.append(f"source_files: {srcs}")
        lines.append(f"generated_at: {__import__('datetime').datetime.now().isoformat()}")
        lines.append("keywords: []")
        lines.append("---\n")
        lines.append(f"# {topic}\n")
        all_paragraphs = []
        for sub_idx, (sub, ids) in enumerate(sorted(subs.items())):
            lines.append(f"## 子主題：{sub}\n")
            for file_idx, id in enumerate(sorted(ids)):
                fname = next(input_path.glob(f"{id}_*.md"), None)
                if fname:
                    try:
                        content = fname.read_text(encoding="utf-8", errors="ignore")
                        paras = extract_paragraphs(content)
                        paras = deduplicate_paragraphs(paras)
                        all_paragraphs.extend(paras)
                        total_files = len(ids)
                        evo_heading = apply_evolution_heading(file_idx, total_files, fname.name)
                        lines.append(f"{evo_heading}\n")
                        lines.append("\n".join(paras))
                        lines.append("\n---\n")
                    except Exception as e:
                        print(f"Warning: Failed to merge {fname.name}: {e}", file=sys.stderr)
                        continue
        all_paragraphs = deduplicate_paragraphs(all_paragraphs)
        output_file = output_path / f"{topic}_完整版.md"
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("\n".join(lines))
        print(f"  Created {output_file.name}")
    sample_validation(output_path)
    print(f"\nAggregation complete. Results in '{output_dir}'")
    return 0


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Aggregate and classify markdown documents with deduplication and LLM enhancement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Use defaults (exports -> processed)
  %(prog)s --input ./docs --output ./build
  %(prog)s --check                  # Validate existing output
  %(prog)s --no-llm                 # Disable OpenAI classification
  
Environment:
  OPENAI_API_KEY    Set to enable LLM-based classification
        """
    )
    parser.add_argument(
        "--input", "-i",
        default=INPUT_DIR,
        help=f"Input directory containing markdown files (default: {INPUT_DIR})"
    )
    parser.add_argument(
        "--output", "-o",
        default=OUTPUT_DIR,
        help=f"Output directory for aggregated files (default: {OUTPUT_DIR})"
    )
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="Run validation sampling on existing output (no aggregation)"
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Disable LLM classification (use heuristics only)"
    )
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    sys.exit(main(
        input_dir=args.input,
        output_dir=args.output,
        check=args.check,
        use_llm=not args.no_llm
    ))