# Using a Font Package

## Install

```bash
npm install @devraj-labs/rn-font-inter
```

Then add (or update) `react-native.config.js` in your app root to tell `react-native-asset` where the font files are:

```js
// react-native.config.js
module.exports = {
  assets: [
    './node_modules/@devraj-labs/rn-font-inter/assets/fonts',
    // add one entry per font package you install
  ],
};
```

Then link the fonts into your native projects:

```bash
npx react-native-asset
```

Re-run `npx react-native-asset` and rebuild your app whenever you add or update a font package. Metro reload alone is not enough — the `.ttf` files must be copied into the native iOS/Android projects first.

---

## With Vajra UI

Register the fonts in your theme:

```ts
import { interFonts } from '@devraj-labs/rn-font-inter';
import { newsreaderFonts } from '@devraj-labs/rn-font-newsreader';

createVajraTheme({
  typography: {
    fonts: {
      families: {
        ...interFonts,
        ...newsreaderFonts,
      },
    },
  },
});
```

Use in components via the `font` prop — the key is the family alias from the package:

```tsx
<Text font="inter" fontWeight="400">Body text</Text>
<Text font="newsreader14pt" fontWeight="700">Article heading</Text>
<Text font="newsreader36pt" fontWeight="600">Display</Text>
```

---

## Without Vajra UI

The export is a plain object — use it however your app resolves fonts:

```ts
import { interFonts } from '@devraj-labs/rn-font-inter';

// interFonts.inter['700'] → 'Inter-Bold'

const styles = StyleSheet.create({
  heading: {
    fontFamily: interFonts.inter['700'],
    fontSize: 24,
  },
  body: {
    fontFamily: interFonts.inter['400'],
    fontSize: 16,
  },
});
```

For fonts with optical sizes, pick the right size for the context:

```ts
import { newsreaderFonts } from '@devraj-labs/rn-font-newsreader';

const styles = StyleSheet.create({
  display: {
    fontFamily: newsreaderFonts.newsreader60pt['700'],
    fontSize: 56,
  },
  body: {
    fontFamily: newsreaderFonts.newsreader14pt['400'],
    fontSize: 16,
  },
});
```

---

## Why PostScript names?

iOS requires the internal PostScript name (not the filename) when setting `fontFamily` — using the filename silently fails. Android uses the filename without extension, which matches the PostScript name when fonts follow the `Family-Weight` convention. These packages export PostScript names so both platforms work without any branching.
