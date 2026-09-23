import type { CapacitorConfig } from '@capacitor/cli';

// Tapkasa — nativní obal pokladní aplikace (tapkasa/index.html).
// Web se do www/ kopíruje skriptem ./sync-web.sh, poté `npx cap sync`.
const config: CapacitorConfig = {
  appId: 'com.deriverge.tapkasa',
  appName: 'Tapkasa',
  webDir: 'www',
  // Papírové pozadí designu — stejná barva jako --paper ve webu,
  // aby start aplikace nebliknul bílou/černou.
  backgroundColor: '#FBFAF7',
  ios: {
    contentInset: 'never',
    backgroundColor: '#FBFAF7',
  },
  android: {
    backgroundColor: '#FBFAF7',
  },
  plugins: {
    // Aplikace má jen světlý vzhled. Bez toho měl Android 15+ v tmavém
    // režimu bílé ikony stavového řádku na světlém papíru, nečitelné.
    SystemBars: {
      style: 'LIGHT',
    },
  },
};

export default config;
