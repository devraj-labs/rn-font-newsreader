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
npx react-native-asset
```

`react-native-asset` reads `react-native.config.js` from the package and copies the `.ttf` files into your native iOS/Android project automatically. Re-run it whenever you add or update a font package.

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
```

### Without Vajra UI

The export is a plain object — use it however your app resolves fonts:

```ts
import { newsreaderFonts } from '@devraj-labs/rn-font-newsreader';

const styles = StyleSheet.create({
  // newsreaderFonts.newsreader14pt['200'] → 'Newsreader14pt-ExtraLight'
  heading: { fontFamily: newsreaderFonts.newsreader14pt['200'], fontSize: 24 },
  body:    { fontFamily: newsreaderFonts.newsreader14pt['800'], fontSize: 16 },
  // newsreaderFonts.newsreader24pt['200'] → 'Newsreader24pt-ExtraLight'
  heading: { fontFamily: newsreaderFonts.newsreader24pt['200'], fontSize: 24 },
  body:    { fontFamily: newsreaderFonts.newsreader24pt['800'], fontSize: 16 },
  // newsreaderFonts.newsreader36pt['200'] → 'Newsreader36pt-ExtraLight'
  heading: { fontFamily: newsreaderFonts.newsreader36pt['200'], fontSize: 24 },
  body:    { fontFamily: newsreaderFonts.newsreader36pt['800'], fontSize: 16 },
  // newsreaderFonts.newsreader60pt['200'] → 'Newsreader60pt-ExtraLight'
  heading: { fontFamily: newsreaderFonts.newsreader60pt['200'], fontSize: 24 },
  body:    { fontFamily: newsreaderFonts.newsreader60pt['800'], fontSize: 16 },
  // newsreaderFonts.newsreader9pt['200'] → 'Newsreader9pt-ExtraLight'
  heading: { fontFamily: newsreaderFonts.newsreader9pt['200'], fontSize: 24 },
  body:    { fontFamily: newsreaderFonts.newsreader9pt['800'], fontSize: 16 },
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
| `newsreader24pt` | `'200'` | `'Newsreader24pt-ExtraLight'` |
| `newsreader24pt` | `'300'` | `'Newsreader24pt-Light'` |
| `newsreader24pt` | `'400'` | `'Newsreader24pt-Regular'` |
| `newsreader24pt` | `'500'` | `'Newsreader24pt-Medium'` |
| `newsreader24pt` | `'600'` | `'Newsreader24pt-SemiBold'` |
| `newsreader24pt` | `'700'` | `'Newsreader24pt-Bold'` |
| `newsreader24pt` | `'800'` | `'Newsreader24pt-ExtraBold'` |
| `newsreader36pt` | `'200'` | `'Newsreader36pt-ExtraLight'` |
| `newsreader36pt` | `'300'` | `'Newsreader36pt-Light'` |
| `newsreader36pt` | `'400'` | `'Newsreader36pt-Regular'` |
| `newsreader36pt` | `'500'` | `'Newsreader36pt-Medium'` |
| `newsreader36pt` | `'600'` | `'Newsreader36pt-SemiBold'` |
| `newsreader36pt` | `'700'` | `'Newsreader36pt-Bold'` |
| `newsreader36pt` | `'800'` | `'Newsreader36pt-ExtraBold'` |
| `newsreader60pt` | `'200'` | `'Newsreader60pt-ExtraLight'` |
| `newsreader60pt` | `'300'` | `'Newsreader60pt-Light'` |
| `newsreader60pt` | `'400'` | `'Newsreader60pt-Regular'` |
| `newsreader60pt` | `'500'` | `'Newsreader60pt-Medium'` |
| `newsreader60pt` | `'600'` | `'Newsreader60pt-SemiBold'` |
| `newsreader60pt` | `'700'` | `'Newsreader60pt-Bold'` |
| `newsreader60pt` | `'800'` | `'Newsreader60pt-ExtraBold'` |
| `newsreader9pt` | `'200'` | `'Newsreader9pt-ExtraLight'` |
| `newsreader9pt` | `'300'` | `'Newsreader9pt-Light'` |
| `newsreader9pt` | `'400'` | `'Newsreader9pt-Regular'` |
| `newsreader9pt` | `'500'` | `'Newsreader9pt-Medium'` |
| `newsreader9pt` | `'600'` | `'Newsreader9pt-SemiBold'` |
| `newsreader9pt` | `'700'` | `'Newsreader9pt-Bold'` |
| `newsreader9pt` | `'800'` | `'Newsreader9pt-ExtraBold'` |

## Docs

- [Using a font package](https://github.com/devraj-labs/rn-font-template/blob/main/docs/using-a-package.md) — full usage guide including Vajra UI and standalone examples
- [Creating a font package](https://github.com/devraj-labs/rn-font-template/blob/main/docs/creating-a-package.md) — how this package was built from the template
- [README generation](https://github.com/devraj-labs/rn-font-template/blob/main/docs/readme-generation.md) — how this file is auto-generated

## License

MIT
