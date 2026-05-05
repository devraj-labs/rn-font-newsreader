#!/usr/bin/env python3

"""
generate-font-package.py

Reads all .ttf files in assets/fonts/, infers weight token mappings from
font metadata, writes src/index.ts, and generates README.md.

Requires:
    pip3 install fonttools

Usage:
    python3 scripts/generate-font-package/generate-font-package.py
    python3 scripts/generate-font-package/generate-font-package.py --export manropeFonts
    python3 scripts/generate-font-package/generate-font-package.py --dry-run
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from fontTools.ttLib import TTFont
except ImportError:
    print("✗ fonttools not installed. Run: pip3 install fonttools")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent.parent
FONTS_DIR = ROOT / "assets" / "fonts"
INDEX_TS = ROOT / "src" / "index.ts"
README_MD = ROOT / "README.md"

# ─── Weight token inference ────────────────────────────────────────────────────

# Order matters: longer/more-specific keywords must come before shorter ones
# (e.g. 'extrabold' before 'bold', 'extralight' before 'light')
WEIGHT_MAP = [
    (["thin"],                                                "100"),
    (["extralight", "extra light", "ultralight"],             "200"),
    (["light"],                                               "300"),
    (["regular", "normal", "book"],                          "400"),
    (["medium"],                                              "500"),
    (["demibold", "demi bold", "semibold", "semi bold"],     "600"),
    (["extrabold", "extra bold", "ultrabold", "ultra bold"], "800"),
    (["bold"],                                                "700"),
    (["black", "heavy"],                                      "900"),
]

WEIGHT_ORDER = ["100", "200", "300", "400", "500", "600", "700", "800", "900"]


def infer_weight_token(name: str) -> str | None:
    normalised = name.lower().replace("-", " ").strip()
    # "Italic" or "Oblique" alone (no weight keyword) implies regular weight
    if normalised in ("italic", "oblique"):
        return "400"
    for keywords, token in WEIGHT_MAP:
        for kw in keywords:
            if kw in normalised:
                return token
    return None


def is_italic(name: str) -> bool:
    normalised = name.lower().replace("-", " ")
    return "italic" in normalised or "oblique" in normalised


# ─── Font inspection ───────────────────────────────────────────────────────────

def get_name(font, name_id: int) -> str:
    val = font["name"].getDebugName(name_id)
    return val if val else ""


def inspect_font(ttf_path: Path) -> dict:
    font = TTFont(ttf_path)
    info = {
        "path":        ttf_path,
        "family":      get_name(font, 1),
        "subfamily":   get_name(font, 2),
        "postscript":  get_name(font, 6),
        "typo_family": get_name(font, 16),
        "typo_sub":    get_name(font, 17),
        "is_variable": "fvar" in font,
        "axes":        {},
        "instances":   [],
    }

    if "fvar" in font:
        for axis in font["fvar"].axes:
            info["axes"][axis.axisTag] = {
                "min":     axis.minValue,
                "default": axis.defaultValue,
                "max":     axis.maxValue,
            }
        for inst in font["fvar"].instances:
            info["instances"].append({
                "name":   get_name(font, inst.subfamilyNameID),
                "coords": inst.coordinates,
            })

    return info


# ─── Print helpers ─────────────────────────────────────────────────────────────

def print_info(info: dict):
    tag = "[variable]" if info["is_variable"] else "[static]  "
    print(f"\n  {tag}  {info['path'].name}")
    print(f"    Family     : {info['typo_family'] or info['family']}")
    print(f"    PostScript : {info['postscript']}")

    if info["is_variable"]:
        w = info["axes"].get("wght")
        if w:
            print(f"    wght axis  : {w['min']}–{w['max']}  (default {w['default']})")
        if info["instances"]:
            print("    Instances  :")
            for inst in info["instances"]:
                wv = inst["coords"].get("wght", "?")
                token = infer_weight_token(inst["name"])
                print(f"      {str(wv).rjust(3)}  {inst['name']:<14} → token '{token or '?'}'")
    else:
        sub = info["typo_sub"] or info["subfamily"]
        token = infer_weight_token(sub or info["postscript"])
        italic = is_italic(sub or info["postscript"])
        key = f"'{token}i'" if italic else f"'{token}'"
        print(f"    Subfamily  : {sub}")
        print(f"    Token      : {key or '(could not infer)'}")


# ─── Build family → weight → PostScript map ───────────────────────────────────

def family_to_alias(family: str) -> str:
    """'Newsreader 14pt' → 'newsreader14pt', 'JetBrains Mono' → 'jetbrainsMono'"""
    parts = family.strip().split()
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def build_family_map(infos: list[dict]) -> dict:
    """
    Groups fonts by family name and returns { alias: { token: postscript } }.

    Normal weights use numeric keys ('400', '700', etc.).
    Italic weights use the same number suffixed with 'i' ('400i', '700i', etc.).

    Single-family fonts (e.g. Inter) produce one entry — same as before.
    Multi-family fonts (e.g. Newsreader 14pt / 24pt / 36pt) produce one
    entry per optical size / family variant — automatically, no flags needed.
    """
    families = {}  # alias → { token → postscript }
    skipped = []

    for info in infos:
        if info["is_variable"]:
            skipped.append(info["path"].name)
            continue

        raw_family = (info["typo_family"] or info["family"] or "font").strip()
        alias = family_to_alias(raw_family)

        sub = info["typo_sub"] or info["subfamily"]
        name_for_inference = sub or info["postscript"]
        token = infer_weight_token(name_for_inference)
        italic = is_italic(name_for_inference)

        if not token:
            print(f"  ⚠  Could not infer token for: {info['path'].name}  (subfamily: \"{sub}\")")
            continue

        key = f"{token}i" if italic else token

        if alias not in families:
            families[alias] = {}

        if key in families[alias]:
            print(f"  ⚠  Duplicate token '{key}' in '{alias}' — skipping {info['path'].name}")
            continue

        families[alias][key] = info["postscript"]

    if skipped:
        print("\n  ℹ  Variable font(s) skipped (this template is static-only):")
        for s in skipped:
            print(f"       {s}")

    return families


# ─── src/index.ts codegen ─────────────────────────────────────────────────────

def build_index_ts(export_name: str, family_map: dict) -> str:
    # Collect all normal weight tokens and italic tokens separately
    normal_tokens = set()
    italic_tokens = set()
    for wmap in family_map.values():
        for t in wmap:
            if t.endswith("i"):
                italic_tokens.add(t)
            else:
                normal_tokens.add(t)

    ordered_normal = [t for t in WEIGHT_ORDER if t in normal_tokens]
    ordered_italic = [f"{t}i" for t in WEIGHT_ORDER if f"{t}i" in italic_tokens]

    all_ordered = ordered_normal + ordered_italic
    union = " | ".join(f"'{t}'" for t in all_ordered)

    family_blocks = []
    for alias, wmap in family_map.items():
        # Normal weights first, then italic weights, both in WEIGHT_ORDER
        ordered_keys = (
            [t for t in WEIGHT_ORDER if t in wmap] +
            [f"{t}i" for t in WEIGHT_ORDER if f"{t}i" in wmap]
        )
        entries = "\n".join(f"    '{k}': '{wmap[k]}'," for k in ordered_keys)
        family_blocks.append(f"  {alias}: {{\n{entries}\n  }},")

    families_ts = "\n".join(family_blocks)

    has_italic = bool(italic_tokens)
    italic_note = "\n * Italic keys use the weight suffixed with 'i' (e.g. '400i', '700i')." if has_italic else ""

    return f"""\
/**
 * Font package: {export_name}
 * Generated by scripts/generate-font-package/generate-font-package.py — edit as needed.
 *
 * Values are PostScript names — works on both iOS and Android.{italic_note}
 */

export type TFontWeightToken = {union};
export type TFontFamilyMap = Partial<Record<TFontWeightToken, string>>;
export type TFontPackage = Record<string, TFontFamilyMap>;

export const {export_name}: TFontPackage = {{
{families_ts}
}};
"""


def infer_export_name(infos: list[dict]) -> str:
    first = next((i for i in infos if not i["is_variable"]), infos[0])
    # Use only the base name (first word) — e.g. "Newsreader 14pt" → "newsreaderFonts"
    family = (first["typo_family"] or first["family"] or "font").strip()
    base = family.split()[0]
    return base[0].lower() + base[1:] + "Fonts"


# ─── README generation ────────────────────────────────────────────────────────

def build_readme(pkg_name: str, export_name: str, font_display_name: str, family_map: dict) -> str:
    install_cmd = f"npm install {pkg_name}"
    import_line = f'import {{ {export_name} }} from \'{pkg_name}\';'

    # Pick the first alias + a regular/bold pair for examples
    first_alias = next(iter(family_map))
    first_wmap = family_map[first_alias]
    normal_tokens = [t for t in WEIGHT_ORDER if t in first_wmap]
    italic_tokens = [f"{t}i" for t in WEIGHT_ORDER if f"{t}i" in first_wmap]

    vajra_spread = f"        ...{export_name},"
    vajra_text_examples = "\n".join(
        f'<Text font="{alias}" fontWeight="{t}">Sample text</Text>'
        for alias, wmap in family_map.items()
        for t in [t for t in WEIGHT_ORDER if t in wmap][:2]
    )
    if italic_tokens:
        first_italic_alias = next(
            (alias for alias, wmap in family_map.items() if any(f"{t}i" in wmap for t in WEIGHT_ORDER)),
            None
        )
        if first_italic_alias:
            first_it = next(f"{t}i" for t in WEIGHT_ORDER if f"{t}i" in family_map[first_italic_alias])
            vajra_text_examples += f'\n<Text font="{first_italic_alias}" fontStyle="italic">Italic text</Text>'

    # Standalone StyleSheet usage
    standalone_lines = []
    for alias, wmap in family_map.items():
        tokens = [t for t in WEIGHT_ORDER if t in wmap]
        if tokens:
            t = tokens[0]
            standalone_lines.append(f"  // {export_name}.{alias}['{t}'] → '{wmap[t]}'")
            standalone_lines.append(f"  heading: {{ fontFamily: {export_name}.{alias}['{t}'], fontSize: 24 }},")
            if len(tokens) > 1:
                t2 = tokens[-1]
                standalone_lines.append(f"  body:    {{ fontFamily: {export_name}.{alias}['{t2}'], fontSize: 16 }},")
        it_tokens = [f"{t}i" for t in WEIGHT_ORDER if f"{t}i" in wmap]
        if it_tokens:
            it = it_tokens[0]
            standalone_lines.append(f"  italic:  {{ fontFamily: {export_name}.{alias}['{it}'], fontSize: 16 }},")
    standalone_block = "\n".join(standalone_lines)

    # Font map table
    table_rows = []
    for alias, wmap in family_map.items():
        for t in WEIGHT_ORDER:
            if t in wmap:
                table_rows.append(f"| `{alias}` | `'{t}'` | `'{wmap[t]}'` |")
        for t in WEIGHT_ORDER:
            it = f"{t}i"
            if it in wmap:
                table_rows.append(f"| `{alias}` | `'{it}'` | `'{wmap[it]}'` |")
    table = "\n".join(table_rows)

    italic_section = ""
    if any(f"{t}i" in wmap for wmap in family_map.values() for t in WEIGHT_ORDER):
        italic_section = """
### Italic

When using Vajra UI, pass `fontStyle="italic"` — the DS resolves the correct italic font file automatically:

```tsx
<Text font="newsreader9pt" fontStyle="italic">Good morning.</Text>
```

"""

    return f"""\
# {font_display_name} Font for React Native

{font_display_name} font, packaged for React Native. Exports a typed weight map (PostScript names) that resolves correctly on both iOS and Android — no `Platform.select`, no manual `fontFamily` string guessing.

| | |
|---|---|
| React Native | 0.60+ |
| iOS | ✓ |
| Android | ✓ |

## Install

```bash
{install_cmd}
```

Then add (or update) `react-native.config.js` in your app root to include the font assets:

```js
module.exports = {{
  assets: [
    './node_modules/{pkg_name}/assets/fonts',
    // ...other font packages
  ],
}};
```

Then link the fonts into your native projects:

```bash
npx react-native-asset
```

Re-run `npx react-native-asset` and rebuild your app whenever you add or update a font package.

## Usage

### With Vajra UI

Register the font in your theme and use it via the `font` prop:

```ts
import {{ {export_name} }} from '{pkg_name}';

createVajraTheme({{
  typography: {{
    fonts: {{
      families: {{
{vajra_spread}
      }},
    }},
  }},
}});
```

```tsx
{vajra_text_examples}
```
{italic_section}
### Without Vajra UI

The export is a plain object — use it however your app resolves fonts:

```ts
{import_line}

const styles = StyleSheet.create({{
{standalone_block}
}});
```

## Font map

| Family | Weight | PostScript name |
|--------|--------|-----------------|
{table}

## Docs

- [Using a font package](https://github.com/devraj-labs/rn-font-template/blob/main/docs/using-a-package.md) — full usage guide including Vajra UI and standalone examples
- [Creating a font package](https://github.com/devraj-labs/rn-font-template/blob/main/docs/creating-a-package.md) — how this package was built from the template
- [README generation](https://github.com/devraj-labs/rn-font-template/blob/main/docs/readme-generation.md) — how this file is auto-generated

## License

MIT
"""


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Inspect fonts and update src/index.ts")
    parser.add_argument("--export",  help="Export name (e.g. manropeFonts)")
    parser.add_argument("--alias",   help="Family alias in theme (e.g. manrope, jetbrainsMono) — inferred from font family name if not provided")
    parser.add_argument("--dry-run", action="store_true", help="Print output without writing")
    args = parser.parse_args()

    print("\n┌─────────────────────────────────────────┐")
    print("│   Vajra UI — Font Inspector             │")
    print("└─────────────────────────────────────────┘")

    # 1. Collect .ttf files (skip placeholder names starting with '<')
    ttf_files = sorted(
        f for f in FONTS_DIR.iterdir()
        if f.suffix.lower() == ".ttf" and not f.name.startswith("<")
    )

    if not ttf_files:
        print("\n✗ No .ttf files found in assets/fonts/")
        sys.exit(1)

    print(f"\nFound {len(ttf_files)} font file(s) in assets/fonts/")

    # 2. Inspect
    infos = [inspect_font(f) for f in ttf_files]

    # 3. Print metadata
    print("\n── Font Metadata ─────────────────────────────────────────────────")
    for info in infos:
        print_info(info)

    # 4. Build family map
    print("\n── Family / Weight Map ───────────────────────────────────────────")
    family_map = build_family_map(infos)

    if not family_map:
        print("\n✗ No weight tokens mapped. Aborting.")
        sys.exit(1)

    for alias, wmap in family_map.items():
        print(f"\n  [{alias}]")
        for t in WEIGHT_ORDER:
            if t in wmap:
                print(f"    '{t}'  → '{wmap[t]}'")
            it = f"{t}i"
            if it in wmap:
                print(f"    '{it}' → '{wmap[it]}'")

    # 5. Resolve export name
    export_name = args.export or infer_export_name(infos)

    print(f"\n  export : {export_name}")
    if args.alias:
        print(f"  ℹ  --alias ignored when multiple families are detected")

    # 6. Write or dry-run
    index_ts = build_index_ts(export_name, family_map)

    # 7. Read package name for README
    pkg_json_path = ROOT / "package.json"
    pkg_name = json.loads(pkg_json_path.read_text())["name"] if pkg_json_path.exists() else export_name

    # Derive human-readable font display name from the first family
    first_family = (infos[0]["typo_family"] or infos[0]["family"] or "Font").strip()
    font_display_name = first_family.split()[0]

    readme = build_readme(pkg_name, export_name, font_display_name, family_map)

    if args.dry_run:
        print("\n── Dry run — src/index.ts output ─────────────────────────────────\n")
        print(index_ts)
        print("\n── Dry run — README.md output ────────────────────────────────────\n")
        print(readme)
    else:
        INDEX_TS.write_text(index_ts)
        print("\n✓ src/index.ts updated")

        # Safety net: if init was skipped, archive template README before overwriting
        readme_template = ROOT / "README-TEMPLATE.md"
        if README_MD.exists() and not readme_template.exists():
            README_MD.rename(readme_template)
            print("✓ README.md → README-TEMPLATE.md (archived)")

        README_MD.write_text(readme)
        print("✓ README.md generated")


if __name__ == "__main__":
    main()
