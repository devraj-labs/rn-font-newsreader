# README Generation

This template manages two README files across the package lifecycle.

## How it works

### `npm run init`

The init script renames `README.md` → `README-TEMPLATE.md`.

This moves the template's contributor-facing documentation out of the way so the font package gets its own README after generate runs. The rename only happens once — if `README-TEMPLATE.md` already exists, the file is left as-is.

### `npm run generate`

After writing `src/index.ts`, the generate script (`generate-font-package.py`) reads the resolved `family_map` and `package.json` name and writes a new `README.md` at the repo root.

This README is consumer-facing — it describes the published package, not the template. It includes:

- Package name and description
- Install command (`npm install <package-name>` + `npx react-native-asset`)
- Usage example with the real export name and actual PostScript names
- Font map table — every family alias, weight token, and PostScript name
- License

The file is always overwritten on each `generate` run, so it stays in sync with whatever fonts are in `assets/fonts/`.

## File states by stage

| Stage | `README.md` | `README-TEMPLATE.md` |
|-------|-------------|----------------------|
| Fresh clone | template README (this repo's docs) | does not exist |
| After `npm run init` | does not exist | template README (archived) |
| After `npm run generate` | generated consumer README | template README (archived) |

## What the generated README looks like

Given a package `@devraj-labs/rn-font-inter` with Inter Regular and Bold, the generated README includes:

**Header** — `# Inter for React Native` with the package name and a one-line description, plus a compatibility table (RN 0.60+, iOS, Android).

**Install** — `npm install` command + `npx react-native-asset`.

**Usage — With Vajra UI** — `createVajraTheme` snippet spreading the export into `typography.fonts.families`, followed by `<Text font="..." fontWeight="...">` examples for each family and weight.

**Usage — Without Vajra UI** — `StyleSheet.create` snippet with real PostScript names as inline comments.

**Font map** — full table of every family alias, weight token, and PostScript name.

**Docs** — links to `using-a-package.md`, `creating-a-package.md`, and `readme-generation.md` on GitHub.

## Customising

The generated README is a starting point. After running `generate`, edit `README.md` freely — it will be overwritten the next time `npm run generate` runs, so commit your edits or add extra sections after publishing.

If you need permanent additions (e.g. a design system usage section), add them to `README-TEMPLATE.md` and update `build_readme()` in `scripts/generate-font-package/generate-font-package.py` to include them.
