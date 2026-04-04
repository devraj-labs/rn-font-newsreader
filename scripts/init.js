#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const ROOT = path.resolve(__dirname, '..');

function ask(rl, question) {
  return new Promise((resolve) => rl.question(question, resolve));
}

function toCamelCaseExport(str) {
  const parts = str.split(/[-_\s]+/);
  return (
    parts[0].toLowerCase() +
    parts.slice(1).map((p) => p.charAt(0).toUpperCase() + p.slice(1)).join('') +
    'Fonts'
  );
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

async function main() {
  const pkgPath = path.join(ROOT, 'package.json');
  const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  const orgInput = await ask(rl, 'GitHub username/org [devraj-labs]: ');
  const githubOrg = orgInput.trim() || 'devraj-labs';

  const fontNameInput = await ask(rl, 'Font name (e.g. inter, jetbrains-mono): ');
  const fontName = fontNameInput.trim().toLowerCase();

  const defaultDesc = `${capitalize(fontName)} font package for React Native`;
  const descInput = await ask(rl, `Description [${defaultDesc}]: `);
  const description = descInput.trim() || defaultDesc;

  rl.close();

  const repoName = `rn-font-${fontName}`;
  const packageName = `@${githubOrg}/${repoName}`;
  const repoUrl = `https://github.com/${githubOrg}/${repoName}`;
  const exportName = toCamelCaseExport(fontName);

  // Update package.json
  pkg.name = packageName;
  pkg.description = description;
  pkg.repository = { type: 'git', url: repoUrl };
  fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2) + '\n');
  console.log('✓ package.json updated');

  // Write src/index.ts
  const indexTs = `export type TFontWeightToken = '100' | '200' | '300' | '400' | '500' | '600' | '700' | '800' | '900';
export type TFontFamilyMap = Record<TFontWeightToken, string>;
export type TFontPackage = Record<string, TFontFamilyMap>;

export const ${exportName}: TFontPackage = {};
`;
  fs.writeFileSync(path.join(ROOT, 'src', 'index.ts'), indexTs);
  console.log('✓ src/index.ts updated');

  console.log('\nNext steps:');
  console.log('  1. Add your .ttf files to assets/fonts/');
  console.log('  2. npm run generate');
  console.log('  3. npm run release');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
