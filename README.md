# Newsreader Font for React Native

Newsreader font, packaged for React Native. Exports a typed weight map (PostScript names) that resolves correctly on both iOS and Android — no `Platform.select`, no manual `fontFamily` string guessing.

| | |
|---|---|
| React Native | 0.60+ |
| iOS | ✓ |
| Android | ✓ |

## Install

```bash
npm install @devraj-labs/rn-font-newsreader
```

Then add (or update) `react-native.config.js` in your app root to include the font assets:

```js
module.exports = {
  assets: [
    './node_modules/@devraj-labs/rn-font-newsreader/assets/fonts',
    // ...other font packages
  ],
};
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
import { newsreaderFonts } from '@devraj-labs/rn-font-newsreader';

createVajraTheme({
  typography: {
    fonts: {
      families: {
        ...newsreaderFonts,
      },
    },
  },
});
```

```tsx
<Text font="newsreader14pt" fontWeight="200">Sample text</Text>
<Text font="newsreader14pt" fontWeight="300">Sample text</Text>
<Text font="newsreader24pt" fontWeight="200">Sample text</Text>
<Text font="newsreader24pt" fontWeight="300">Sample text</Text>
<Text font="newsreader36pt" fontWeight="200">Sample text</Text>
<Text font="newsreader36pt" fontWeight="300">Sample text</Text>
<Text font="newsreader60pt" fontWeight="200">Sample text</Text>
<Text font="newsreader60pt" fontWeight="300">Sample text</Text>
<Text font="newsreader9pt" fontWeight="200">Sample text</Text>
<Text font="newsreader9pt" fontWeight="300">Sample text</Text>
<Text font="newsreader14pt" fontStyle="italic">Italic text</Text>
```

### Italic

When using Vajra UI, pass `fontStyle="italic"` — the DS resolves the correct italic font file automatically:

```tsx
<Text font="newsreader9pt" fontStyle="italic">Good morning.</Text>
```


### Without Vajra UI

The export is a plain object — use it however your app resolves fonts:

```ts
import { newsreaderFonts } from '@devraj-labs/rn-font-newsreader';

const styles = StyleSheet.create({
  // newsreaderFonts.newsreader14pt['200'] → 'Newsreader14pt-ExtraLight'
  heading: { fontFamily: newsreaderFonts.newsreader14pt['200'], fontSize: 24 },
  body:    { fontFamily: newsreaderFonts.newsreader14pt['800'], fontSize: 16 },
  italic:  { fontFamily: newsreaderFonts.newsreader14pt['200i'], fontSize: 16 },
  // newsreaderFonts.newsreader24pt['200'] → 'Newsreader24pt-ExtraLight'
  heading: { fontFamily: newsreaderFonts.newsreader24pt['200'], fontSize: 24 },
  body:    { fontFamily: newsreaderFonts.newsreader24pt['800'], fontSize: 16 },
  italic:  { fontFamily: newsreaderFonts.newsreader24pt['200i'], fontSize: 16 },
  // newsreaderFonts.newsreader36pt['200'] → 'Newsreader36pt-ExtraLight'
  heading: { fontFamily: newsreaderFonts.newsreader36pt['200'], fontSize: 24 },
  body:    { fontFamily: newsreaderFonts.newsreader36pt['800'], fontSize: 16 },
  italic:  { fontFamily: newsreaderFonts.newsreader36pt['200i'], fontSize: 16 },
  // newsreaderFonts.newsreader60pt['200'] → 'Newsreader60pt-ExtraLight'
  heading: { fontFamily: newsreaderFonts.newsreader60pt['200'], fontSize: 24 },
  body:    { fontFamily: newsreaderFonts.newsreader60pt['800'], fontSize: 16 },
  italic:  { fontFamily: newsreaderFonts.newsreader60pt['200i'], fontSize: 16 },
  // newsreaderFonts.newsreader9pt['200'] → 'Newsreader9pt-ExtraLight'
  heading: { fontFamily: newsreaderFonts.newsreader9pt['200'], fontSize: 24 },
  body:    { fontFamily: newsreaderFonts.newsreader9pt['800'], fontSize: 16 },
  italic:  { fontFamily: newsreaderFonts.newsreader9pt['200i'], fontSize: 16 },
});
```

## Font map

| Family | Weight | PostScript name |
|--------|--------|-----------------|
| `newsreader14pt` | `'200'` | `'Newsreader14pt-ExtraLight'` |
| `newsreader14pt` | `'300'` | `'Newsreader14pt-Light'` |
| `newsreader14pt` | `'400'` | `'Newsreader14pt-Regular'` |
| `newsreader14pt` | `'500'` | `'Newsreader14pt-Medium'` |
| `newsreader14pt` | `'600'` | `'Newsreader14pt-SemiBold'` |
| `newsreader14pt` | `'700'` | `'Newsreader14pt-Bold'` |
| `newsreader14pt` | `'800'` | `'Newsreader14pt-ExtraBold'` |
| `newsreader14pt` | `'200i'` | `'Newsreader14pt-ExtraLightItalic'` |
| `newsreader14pt` | `'300i'` | `'Newsreader14pt-LightItalic'` |
| `newsreader14pt` | `'400i'` | `'Newsreader14pt-Italic'` |
| `newsreader14pt` | `'500i'` | `'Newsreader14pt-MediumItalic'` |
| `newsreader14pt` | `'600i'` | `'Newsreader14pt-SemiBoldItalic'` |
| `newsreader14pt` | `'700i'` | `'Newsreader14pt-BoldItalic'` |
| `newsreader14pt` | `'800i'` | `'Newsreader14pt-ExtraBoldItalic'` |
| `newsreader24pt` | `'200'` | `'Newsreader24pt-ExtraLight'` |
| `newsreader24pt` | `'300'` | `'Newsreader24pt-Light'` |
| `newsreader24pt` | `'400'` | `'Newsreader24pt-Regular'` |
| `newsreader24pt` | `'500'` | `'Newsreader24pt-Medium'` |
| `newsreader24pt` | `'600'` | `'Newsreader24pt-SemiBold'` |
| `newsreader24pt` | `'700'` | `'Newsreader24pt-Bold'` |
| `newsreader24pt` | `'800'` | `'Newsreader24pt-ExtraBold'` |
| `newsreader24pt` | `'200i'` | `'Newsreader24pt-ExtraLightItalic'` |
| `newsreader24pt` | `'300i'` | `'Newsreader24pt-LightItalic'` |
| `newsreader24pt` | `'400i'` | `'Newsreader24pt-Italic'` |
| `newsreader24pt` | `'500i'` | `'Newsreader24pt-MediumItalic'` |
| `newsreader24pt` | `'600i'` | `'Newsreader24pt-SemiBoldItalic'` |
| `newsreader24pt` | `'700i'` | `'Newsreader24pt-BoldItalic'` |
| `newsreader24pt` | `'800i'` | `'Newsreader24pt-ExtraBoldItalic'` |
| `newsreader36pt` | `'200'` | `'Newsreader36pt-ExtraLight'` |
| `newsreader36pt` | `'300'` | `'Newsreader36pt-Light'` |
| `newsreader36pt` | `'400'` | `'Newsreader36pt-Regular'` |
| `newsreader36pt` | `'500'` | `'Newsreader36pt-Medium'` |
| `newsreader36pt` | `'600'` | `'Newsreader36pt-SemiBold'` |
| `newsreader36pt` | `'700'` | `'Newsreader36pt-Bold'` |
| `newsreader36pt` | `'800'` | `'Newsreader36pt-ExtraBold'` |
| `newsreader36pt` | `'200i'` | `'Newsreader36pt-ExtraLightItalic'` |
| `newsreader36pt` | `'300i'` | `'Newsreader36pt-LightItalic'` |
| `newsreader36pt` | `'400i'` | `'Newsreader36pt-Italic'` |
| `newsreader36pt` | `'500i'` | `'Newsreader36pt-MediumItalic'` |
| `newsreader36pt` | `'600i'` | `'Newsreader36pt-SemiBoldItalic'` |
| `newsreader36pt` | `'700i'` | `'Newsreader36pt-BoldItalic'` |
| `newsreader36pt` | `'800i'` | `'Newsreader36pt-ExtraBoldItalic'` |
| `newsreader60pt` | `'200'` | `'Newsreader60pt-ExtraLight'` |
| `newsreader60pt` | `'300'` | `'Newsreader60pt-Light'` |
| `newsreader60pt` | `'400'` | `'Newsreader60pt-Regular'` |
| `newsreader60pt` | `'500'` | `'Newsreader60pt-Medium'` |
| `newsreader60pt` | `'600'` | `'Newsreader60pt-SemiBold'` |
| `newsreader60pt` | `'700'` | `'Newsreader60pt-Bold'` |
| `newsreader60pt` | `'800'` | `'Newsreader60pt-ExtraBold'` |
| `newsreader60pt` | `'200i'` | `'Newsreader60pt-ExtraLightItalic'` |
| `newsreader60pt` | `'300i'` | `'Newsreader60pt-LightItalic'` |
| `newsreader60pt` | `'400i'` | `'Newsreader60pt-Italic'` |
| `newsreader60pt` | `'500i'` | `'Newsreader60pt-MediumItalic'` |
| `newsreader60pt` | `'600i'` | `'Newsreader60pt-SemiBoldItalic'` |
| `newsreader60pt` | `'700i'` | `'Newsreader60pt-BoldItalic'` |
| `newsreader60pt` | `'800i'` | `'Newsreader60pt-ExtraBoldItalic'` |
| `newsreader9pt` | `'200'` | `'Newsreader9pt-ExtraLight'` |
| `newsreader9pt` | `'300'` | `'Newsreader9pt-Light'` |
| `newsreader9pt` | `'400'` | `'Newsreader9pt-Regular'` |
| `newsreader9pt` | `'500'` | `'Newsreader9pt-Medium'` |
| `newsreader9pt` | `'600'` | `'Newsreader9pt-SemiBold'` |
| `newsreader9pt` | `'700'` | `'Newsreader9pt-Bold'` |
| `newsreader9pt` | `'800'` | `'Newsreader9pt-ExtraBold'` |
| `newsreader9pt` | `'200i'` | `'Newsreader9pt-ExtraLightItalic'` |
| `newsreader9pt` | `'300i'` | `'Newsreader9pt-LightItalic'` |
| `newsreader9pt` | `'400i'` | `'Newsreader9pt-Italic'` |
| `newsreader9pt` | `'500i'` | `'Newsreader9pt-MediumItalic'` |
| `newsreader9pt` | `'600i'` | `'Newsreader9pt-SemiBoldItalic'` |
| `newsreader9pt` | `'700i'` | `'Newsreader9pt-BoldItalic'` |
| `newsreader9pt` | `'800i'` | `'Newsreader9pt-ExtraBoldItalic'` |

## Docs

- [Using a font package](https://github.com/devraj-labs/rn-font-template/blob/main/docs/using-a-package.md) — full usage guide including Vajra UI and standalone examples
- [Creating a font package](https://github.com/devraj-labs/rn-font-template/blob/main/docs/creating-a-package.md) — how this package was built from the template
- [README generation](https://github.com/devraj-labs/rn-font-template/blob/main/docs/readme-generation.md) — how this file is auto-generated

## License

MIT
