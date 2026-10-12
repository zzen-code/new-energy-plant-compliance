#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 Agent Skill 仓库结构，尤其是 SKILL.md 的 frontmatter。

校验项对应技能加载器的真实行为（本项目踩过的坑都列在里面）：

  1. 目录 bundle 形式：<name>/SKILL.md 必须存在
  2. frontmatter 由首行 `---` 与后续 `---` 包裹，且结构可解析
  3. 必填 name（kebab-case，建议与目录名一致）与 description
  4. **无引号标量中不得出现 ": "** —— 会破坏 YAML 解析，导致技能被
     静默跳过（本项目真实踩过：description 里写了英文冒号加空格，
     skill 直接从会话目录消失）
  5. SKILL.md 字符数 < 8192 —— 渲染为工具结果时的裁剪阈值
  6. SKILL.md 中提到的 references/、templates/ 路径必须真实存在
  7. 每个 references/*.md 以一级标题开头，并标注"核验基线"

依赖：优先使用 PyYAML；若未安装则退化为内置极简解析（无第三方依赖）。
退出码：0 = 通过（可能有警告）；1 = 有错误。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_SKILL_CHARS = 8192
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PATH_REF = re.compile(r"`((?:references|templates)/[^`\s]+\.md)`")
BASELINE = re.compile(r"核验基线")

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)
    print(f"::error::{msg}")


def warn(msg: str) -> None:
    warnings.append(msg)
    print(f"::warning::{msg}")


def info(msg: str) -> None:
    print(f"  OK   {msg}")


def strip_scalar(value: str) -> str:
    """去掉行尾注释与包裹引号。"""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def parse_fallback(raw: str) -> dict:
    """无 PyYAML 时的极简解析：只取顶层 key: value，够做必填字段校验。"""
    fm: dict[str, str] = {}
    for line in raw.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1] in (" ", "\t"):
            continue  # 嵌套层忽略
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = strip_scalar(value)
    return fm


def load_frontmatter(raw: str) -> tuple[dict, str]:
    """返回 (解析结果, 解析器名称)。"""
    try:
        import yaml  # type: ignore
    except ImportError:
        return parse_fallback(raw), "内置极简解析（未安装 PyYAML）"

    try:
        data = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        err(f"frontmatter YAML 解析失败：{exc}")
        return {}, "PyYAML"
    if not isinstance(data, dict):
        err("frontmatter 不是键值映射（key: value 形式）")
        return {}, "PyYAML"
    return data, "PyYAML"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    skill_md = root / "SKILL.md"

    print(f"校验目录：{root}")
    print(f"技能名（目录）：{root.name}\n")

    if not skill_md.is_file():
        err("缺少 SKILL.md —— 目录 bundle 形式必须是 <name>/SKILL.md")
        return 1

    text = skill_md.read_text(encoding="utf-8")

    # ---- 5. 字符数阈值 -------------------------------------------------
    n = len(text)
    if n >= MAX_SKILL_CHARS:
        err(
            f"SKILL.md 共 {n} 字符，达到或超过 {MAX_SKILL_CHARS} 阈值；"
            "作为工具结果渲染时会被裁剪，请把长内容移到 references/"
        )
    else:
        info(f"SKILL.md {n} 字符（阈值 {MAX_SKILL_CHARS}）")

    # ---- 2. frontmatter 提取 ------------------------------------------
    if not text.startswith("---"):
        err("SKILL.md 未以 `---` 开头，缺少 frontmatter")
        return 1

    lines = text.split("\n")
    close = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            close = i
            break
    if close is None:
        err("frontmatter 缺少结束的 `---`")
        return 1

    fm_lines = lines[1:close]
    fm_raw = "\n".join(fm_lines)

    # ---- 4. 无引号标量中的 ": "（本项目真实踩过的坑）------------------
    for offset, line in enumerate(fm_lines, start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line[:1] in (" ", "\t"):
            continue  # 嵌套层交给解析器判断
        if stripped.count(":") <= 1:
            continue
        value = stripped.split(":", 1)[1].lstrip()
        if value.startswith(("'", '"', "|", ">")):
            continue  # 已加引号或块标量，安全
        err(
            f"frontmatter 第 {offset} 行的无引号标量含 ': '，会破坏 YAML 解析"
            "（技能将被静默跳过）。请把冒号改为句号，或给整个值加引号"
        )

    # ---- 2b. 解析 ------------------------------------------------------
    fm, parser = load_frontmatter(fm_raw)
    if not fm and errors:
        return 1
    info(f"frontmatter 解析通过（{parser}）")

    # ---- 3. 必填字段 ---------------------------------------------------
    name = fm.get("name")
    if not name:
        err("frontmatter 缺少必填字段 name")
    elif not KEBAB.fullmatch(str(name)):
        err(f"name 必须为 kebab-case（小写字母/数字/连字符），当前为 {name!r}")
    elif str(name) != root.name:
        warn(f"name（{name}）与目录名（{root.name}）不一致，建议保持一致")
    else:
        info(f"name = {name}（kebab-case，与目录名一致）")

    desc = fm.get("description")
    if not desc or not str(desc).strip():
        err("frontmatter 缺少必填字段 description —— 它决定技能何时被自动加载")
    else:
        info(f"description {len(str(desc))} 字符")

    # ---- 6. 引用路径存在性 ---------------------------------------------
    refs = sorted(set(PATH_REF.findall(text)))
    if not refs:
        warn("SKILL.md 未引用任何 references/ 或 templates/ 文件")
    for rel in refs:
        if (root / rel).is_file():
            info(f"引用存在：{rel}")
        else:
            err(f"SKILL.md 引用了不存在的文件：{rel}")

    # ---- 7. 反向检查 + 资源文件规范 ------------------------------------
    on_disk: set[str] = set()
    for sub in ("references", "templates"):
        d = root / sub
        if d.is_dir():
            for p in sorted(d.rglob("*.md")):
                on_disk.add(p.relative_to(root).as_posix())

    for rel in sorted(on_disk - set(refs)):
        warn(f"{rel} 存在于磁盘但未被 SKILL.md 引用")

    for rel in sorted(on_disk):
        body = (root / rel).read_text(encoding="utf-8", errors="replace")
        first = next((l for l in body.split("\n") if l.strip()), "")
        if not first.startswith("#"):
            warn(f"{rel} 未以 Markdown 一级标题开头")
        if not BASELINE.search(body):
            warn(f"{rel} 未标注「核验基线」—— 本项目的核心约定是标明数据快照日期")

    # ---- 汇总 ----------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"错误 {len(errors)} 项，警告 {len(warnings)} 项")
    if errors:
        print("校验未通过。")
        return 1
    print("校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
