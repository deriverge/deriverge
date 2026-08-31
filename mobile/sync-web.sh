#!/bin/sh
# Zkopíruje webovou aplikaci (kava/index.html) do www/, odkud si ji bere
# Capacitor, a do kopie přidá adaptéry nativního mostu (bridge.js) a
# fakturace (billing.js). Zdrojový kava/index.html se nemění.
#
# Spouštět z adresáře mobile/ před každým `npx cap sync`:
#
#   ./sync-web.sh && npx cap sync
set -eu

DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$DIR/../kava/index.html"
DST="$DIR/www"

if [ ! -f "$SRC" ]; then
  echo "sync-web.sh: nenalezen $SRC" >&2
  exit 1
fi

mkdir -p "$DST"

# Adaptéry se vkládají před </body> — v prohlížeči bez Capacitoru nedělají
# nic, takže kopie zůstává použitelná i jako obyčejná webová stránka.
awk '
  /<\/body>/ {
    print "<script src=\"bridge.js\"></script>"
    print "<script src=\"billing.js\"></script>"
  }
  { print }
' "$SRC" > "$DST/index.html"

cp "$DIR/bridge.js" "$DST/bridge.js"
cp "$DIR/billing.js" "$DST/billing.js"

# Ikony a manifest — hlavička aplikace na ně odkazuje; v nativním obalu
# nejsou nutné, ale kopie ve www/ pak funguje beze zbytku i jako web.
for f in manifest.webmanifest icon-192.png icon-512.png icon-maskable-512.png apple-touch-icon.png; do
  [ -f "$DIR/../kava/$f" ] && cp "$DIR/../kava/$f" "$DST/$f"
done

echo "sync-web.sh: www/ aktualizováno ($(wc -c < "$DST/index.html") B index.html)"
