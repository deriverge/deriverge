#!/bin/sh
#
# Xcode Cloud, krok po naklonování repozitáře.
#
# Xcode projekt v mobile/ios/App je jen nativní obal. Než se dá stavět,
# musí se nainstalovat závislosti, zkopírovat webová aplikace z tapkasa/
# do mobile/www/ a nechat Capacitor doplnit nativní část. Bez toho by
# se do buildu dostala prázdná nebo zastaralá www/.
#
# Xcode Cloud hledá tento adresář vedle .xcodeproj, proto je skript
# v mobile/ios/App/ci_scripts/.

set -e

echo "==> pracovní adresář: $CI_PRIMARY_REPOSITORY_PATH"
cd "$CI_PRIMARY_REPOSITORY_PATH/mobile"

# Node na runnerech Xcode Cloud není zaručený, doinstalovat přes Homebrew.
if ! command -v node > /dev/null 2>&1; then
  echo "==> node chybí, instaluji přes Homebrew"
  brew install node
fi

echo "==> node $(node -v), npm $(npm -v)"

echo "==> npm ci"
npm ci

echo "==> sync-web.sh"
chmod +x ./sync-web.sh
./sync-web.sh

echo "==> capacitor sync ios"
npx cap sync ios

echo "==> hotovo, obsah www/:"
ls -la www/ | head -10
