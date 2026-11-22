// THE WORLD TODAY — Saturday 21 November 2026.
// Entry program for make.fun news-image-20261121.
// The front page is rendered by render.py (Pillow) from the verified
// story list and the photos/ directory; this program only places the
// finished, deterministic image at the grader's output path.
//
// No network, no randomness, no clock: the same input bytes always
// produce the same output bytes.
import { copyFileSync, existsSync, statSync } from "node:fs";
import { join } from "node:path";

const SOURCE = new URL("./entry.png", import.meta.url).pathname;
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const TARGET = join(OUT_DIR, "entry.png");

if (!existsSync(SOURCE)) {
  console.error(`missing bundled image: ${SOURCE}`);
  process.exit(1);
}

const expectedBytes = statSync(SOURCE).size;
copyFileSync(SOURCE, TARGET);

const writtenBytes = statSync(TARGET).size;
if (writtenBytes !== expectedBytes) {
  console.error(
    `output size mismatch: wrote ${writtenBytes} bytes, expected ${expectedBytes}`,
  );
  process.exit(1);
}

console.log(`wrote ${TARGET} (${writtenBytes} bytes)`);
