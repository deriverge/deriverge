# Obchodní snímky

Dva kroky, oba se pouštějí přes CDP klienta ve scratchpadu
(`node run.mjs <krok>`), a to proti **vlastní bezhlavé instanci Chrome**:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --remote-debugging-port=9333 \
  --user-data-dir=/tmp/render-profile --allow-file-access-from-files \
  --hide-scrollbars --force-device-scale-factor=1 --disable-gpu about:blank &

CDP_PORT=9333 node run.mjs capture.mjs   # nafotí obrazovky aplikace
CDP_PORT=9333 node run.mjs frame.mjs     # zasadí je do grafiky
```

Proti přihlášenému Chrome uživatele to nedělejte: `setDeviceMetricsOverride`
se tam neuchytí spolehlivě, část snímků pak vyjde v jiném měřítku. Kroky si
rozměry po načtení ověřují (`metrics.mjs`), ale bezhlavá instance je jistota.

`capture.mjs` nasazuje stav rovnou do localStorage a maže i IndexedDB,
protože aplikace si stav zrcadlí i tam a po vymazání localStorage by ho
odtud zase obnovila.

`framed.html` je šablona grafiky. Hodnota `sar` musí odpovídat poměru stran
**zdrojového snímku**, ne plátna. Když nesedí, obraz uvnitř rámu se ořízne
a obsah aplikace vyjede mimo displej.
