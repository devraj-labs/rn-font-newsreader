/**
 * Font Package Template for Vajra UI (@devraj-labs)
 *
 * Replace the placeholder filenames below with your actual .ttf font files.
 * Place the actual .ttf files in assets/fonts/.
 *
 * This template uses static multi-file fonts — one .ttf file per weight.
 * See README for why static fonts are the right choice for cross-platform support.
 */

/**
 * Supported font weight tokens.
 * Maps to CSS/React Native fontWeight values.
 */
export type TFontWeightToken = '400' | '500' | '600' | '700';

/**
 * Maps each weight token to a .ttf filename (not a full path — just the filename).
 * The filename must match the file placed in assets/fonts/.
 */
export type TFontFamilyMap = Record<TFontWeightToken, string>;

/**
 * The full font package shape.
 * Keys are font family aliases (e.g. 'sans', 'mono', 'serif').
 * Values map each weight token to the corresponding .ttf filename.
 */
export type TFontPackage = Record<string, TFontFamilyMap>;

/**
 * Main font mapping for this package.
 *
 * Replace the placeholder filenames with your actual .ttf filenames.
 * The filenames must exactly match the files in assets/fonts/.
 *
 * e.g.
 *   '<Font-Regular>.ttf'  → 'Inter-Regular.ttf'
 *   '<Font-Medium>.ttf'   → 'Inter-Medium.ttf'
 *   '<Font-SemiBold>.ttf' → 'Inter-SemiBold.ttf'
 *   '<Font-Bold>.ttf'     → 'Inter-Bold.ttf'
 */
export const fontTemplate: TFontPackage = {
  sans: {
    '400': '<Font-Regular>.ttf',   // Replace with e.g. 'Inter-Regular.ttf'
    '500': '<Font-Medium>.ttf',    // Replace with e.g. 'Inter-Medium.ttf'
    '600': '<Font-SemiBold>.ttf',  // Replace with e.g. 'Inter-SemiBold.ttf'
    '700': '<Font-Bold>.ttf',      // Replace with e.g. 'Inter-Bold.ttf'
  },
};
