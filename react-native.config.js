/**
 * React Native asset linking configuration.
 *
 * This tells the React Native CLI where to find font assets so they are
 * automatically linked into the native iOS/Android projects when a consumer
 * runs `npx react-native-asset` (or the legacy `react-native link`).
 *
 * Consumers of this package must run:
 *   npx react-native-asset
 * after installing to copy the fonts into their native project.
 */
module.exports = {
  assets: ['./assets/fonts'],
};
