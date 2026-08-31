# Tapkasa — brand assets

Motif: a 2×2 grid of rounded product cards — the app's signature look — in four
palette colours on paper. No text in the icon; flat, bold, readable at 60 px.

| Token     | Hex       | Use in icon        |
|-----------|-----------|--------------------|
| paper     | `#FBFAF7` | background         |
| vermilion | `#D6402A` | top-left card      |
| žlutá     | `#F5CE3E` | top-right card     |
| modrá     | `#2158C4` | bottom-left card   |
| zelená    | `#127A4E` | bottom-right card  |

Ink `#15120E` and ink-2 `#5F5749` appear only in the feature graphic
(wordmark + tagline). Wordmark face: Archivo ExtraBold (the SVG falls back to
the system bold sans when Archivo is not installed — acceptable at this size).

## Source files (SVG — edit these, re-render PNGs)

| File | What it is |
|------|------------|
| `icon.svg` | 1024×1024 master icon. Full-bleed square — **iOS masks its own corners**, so no pre-rounding of the canvas. Grid: 376 px tiles, 48 px gap, 112 px margin, 88 px radius. |
| `icon-maskable.svg` | Android adaptive / PWA-maskable variant. Same motif scaled into the central 66 % safe zone (500 px span; farthest painted point 330 px from center, inside the 338 px guaranteed-visible circle), so circle/squircle masks never clip it. |
| `splash.svg` | 2732×2732 launch screen. Motif small (360 px span) and centered on paper; center-crops cleanly to any device size. |
| `feature-graphic.svg` | 1024×500 Google Play feature graphic: motif + "Tapkasa" wordmark + tagline "Pokladna do kapsy". |

## Rendered PNGs (`png/`) and where each one goes

All rendered at exactly the stated pixel size, `deviceScaleFactor: 1`
(verified after render — see "Re-rendering" below).

### iOS — Xcode asset catalog (`Assets.xcassets/AppIcon.appiconset`)

The ios/ project has no asset catalog yet; when it is added, either use the
modern **single-size** option (Xcode 14+: set the appiconset to
"Single Size" and drop in `icon-1024.png` — Xcode generates the rest), or
fill the classic slots:

| PNG | Slot |
|-----|------|
| `icon-1024.png` | App Store (iOS marketing), 1024 pt @1x — **no alpha**; ours is opaque paper, OK |
| `icon-180.png` | iPhone App 60 pt @3x |
| `icon-120.png` | iPhone App 60 pt @2x (also iPhone Spotlight 40 pt @3x) |
| `icon-167.png` | iPad Pro App 83.5 pt @2x |
| `icon-152.png` | iPad App 76 pt @2x |
| `splash-2732.png` | Launch screen image (full-screen image view, `scaleAspectFill`, background `#FBFAF7`) — or rebuild the motif natively in the launch storyboard |

### Android / Google Play

| PNG | Where |
|-----|-------|
| `icon-512.png` | Play Console → Store listing → **App icon** (512×512, 32-bit PNG) |
| `feature-graphic-1024x500.png` | Play Console → Store listing → **Feature graphic** (1024×500) |
| `maskable-512.png` | Basis for the adaptive-icon **foreground layer** (`ic_launcher_foreground`); pair with a plain `#FBFAF7` background layer. For exact `res/` densities, re-render `icon-maskable.svg` at 432, 324, 216, 162, 108 px (xxxhdpi → mdpi). |
| `splash-2732.png` | Splash source (e.g. Capacitor `@capacitor/splash-screen` / Android 12 SplashScreen API — for API 31+ use the motif as the windowed splash icon on a `#FBFAF7` window background) |

### Web manifest (`site.webmanifest`)

```json
"icons": [
  { "src": "design/png/icon-192.png",     "sizes": "192x192", "type": "image/png", "purpose": "any" },
  { "src": "design/png/icon-512.png",     "sizes": "512x512", "type": "image/png", "purpose": "any" },
  { "src": "design/png/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
]
```

Plus in the page `<head>`:

- `icon-180.png` → `<link rel="apple-touch-icon" href="…/icon-180.png">`
- `splash-2732.png` → source for `apple-touch-startup-image` variants if PWA
  splash screens are wanted (generate per-device crops from it)
- theme colour: `<meta name="theme-color" content="#FBFAF7">`

## Re-rendering

PNGs are produced by screenshotting each SVG at the exact viewport size with
the preinstalled Playwright Chromium (`deviceScaleFactor: 1`), then verified
by loading every PNG back and reading `naturalWidth`/`naturalHeight`.
If you edit an SVG, re-render with a script along these lines:

```js
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
// wrap the SVG in <img style="width:100vw;height:100vh"> on a margin-less page,
// page.setViewportSize({width, height}); page.screenshot({path});
```

Sizes to produce: icon at 1024/512/192/180/167/152/120, maskable at 512,
splash at 2732, feature graphic at 1024×500.
