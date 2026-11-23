// Společné pro snímky: kde leží, jak se jmenují a jak se z PNG přečte rozměr.
import fs from 'node:fs';
import path from 'node:path';
export const SHOTS_DIR = process.env.TAPKASA_SHOTS || '/Volumes/T7 4TB/ClaudeDev/tapkasa-shots-2026-11';
/** Sady App Store: složka → typ v App Store Connect a přesný rozměr. */
export const AS_SETS = {
  iphone69: { type: 'APP_IPHONE_67', w: 1320, h: 2868 },
  iphone65: { type: 'APP_IPHONE_65', w: 1284, h: 2778 },
  ipad13: { type: 'APP_IPAD_PRO_3GEN_129', w: 2064, h: 2752 },
};
export const PLAY_PHONE = { w: 1080, h: 1920 };
export function pngSize(file) {
  const b = Buffer.alloc(24); const fd = fs.openSync(file, 'r'); fs.readSync(fd, b, 0, 24, 0); fs.closeSync(fd);
  if (b.toString('ascii', 1, 4) !== 'PNG') throw new Error('není PNG: ' + file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}
/** Seřazené PNG ve složce (01-…, 02-…), prázdné pole, když složka není. */
export function listShots(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((f) => /^\d\d-.*\.png$/.test(f)).sort().map((f) => path.join(dir, f));
}
