# React Native Font Package Template

A GitHub template for creating and distributing typed React Native font packages.

Each package exports a PostScript name map that works on both iOS and Android — no platform-specific handling needed. Drop in your `.ttf` files, run two commands, publish.

| | |
|---|---|
| React Native | 0.60+ |
| iOS | ✓ |
| Android | ✓ |

---

## Quick start

**Option A — GitHub template (recommended)**

Click **Use this template** on GitHub to create a new repo under your account, then clone your repo:

```bash
git clone https://github.com/<your-org>/rn-font-<fontname>.git
cd rn-font-<fontname>
```

**Option B — Clone directly**

```bash
git clone https://github.com/devraj-labs/rn-font-template.git rn-font-<fontname>
cd rn-font-<fontname>
git remote set-url origin https://github.com/<your-org>/rn-font-<fontname>.git
```

Then in both cases:

```bash
npm run init          # enter font name — renames package.json, cleans placeholders, archives this README
# drop your .ttf files into assets/fonts/
npm run generate      # reads fonts, writes src/index.ts, generates README.md for the package
npm run release       # build + publish to npm
```

> After `npm run init`, this file becomes `README-TEMPLATE.md`.
> After `npm run generate`, a new `README.md` is written with install and usage instructions specific to your font package.

## Scripts

| Script | Description |
|---|---|
| `npm run init` | One-time setup — renames the package, cleans placeholders, moves this README to `README-TEMPLATE.md` |
| `npm run generate` | Reads `.ttf` files, infers weight map, writes `src/index.ts` and generates `README.md` |
| `npm run build` | Compiles TypeScript to `dist/` |
| `npm run release` | Build + publish to npm |

## Docs

- [Creating a font package](docs/creating-a-package.md) — full walkthrough for publishing a new font
- [Using a font package](docs/using-a-package.md) — how to consume the package in your app or design system
- [README generation](docs/readme-generation.md) — how `README.md` is generated and what it contains

## License

MIT
