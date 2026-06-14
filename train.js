// TinyLM — Node.js training script
// Mirrors the NgramLM logic in Index.html exactly.
// Usage: node train.js [--n 4] [--epochs 5] [--smoothing 0.5] [--temp 0.8]

const fs = require('fs');
const path = require('path');

// ── Parse CLI args ─────────────────────────────────────────────────────────
const args = process.argv.slice(2);
function getArg(name, def) {
  const i = args.indexOf('--' + name);
  return i !== -1 ? parseFloat(args[i + 1]) : def;
}

const N         = Math.round(getArg('n',        4));
const EPOCHS    = Math.round(getArg('epochs',   5));
const SMOOTHING =            getArg('smoothing', 0.5);
const TEMP      =            getArg('temp',      0.8);

// ── Training corpus (same Shakespeare default as Index.html) ───────────────
const TEXT = `To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles
And by opposing end them. To die—to sleep,
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to: 'tis a consummation
Devoutly to be wish'd. To die, to sleep;
To sleep, perchance to dream—ay, there's the rub:
For in that sleep of death what dreams may come
When we have shuffled off this mortal coil
Must give us pause. There's the respect
That makes calamity of so long life.
For who would bear the whips and scorns of time,
The oppressor's wrong, the proud man's contumely,
The pangs of despised love, the law's delay,
The insolence of office, and the spurns
That patient merit of the unworthy takes,
When he himself might his quietus make
With a bare bodkin? Who would fardels bear,
To grunt and sweat under a weary life,
But that the dread of something after death,
The undiscover'd country, from whose bourn
No traveller returns, puzzles the will,
And makes us rather bear those ills we have
Than fly to others that we know not of?
Thus conscience does make cowards of us all,
And thus the native hue of resolution
Is sicklied o'er with the pale cast of thought,
And enterprises of great pitch and moment,
With this regard their currents turn awry,
And lose the name of action.`;

// ── N-gram model (identical to Index.html NgramLM class) ───────────────────
class NgramLM {
  constructor(n, smoothing) {
    this.n = n;
    this.smoothing = smoothing;
    this.counts = {};
    this.vocab = [];
    this.charToIdx = {};
  }

  train(text) {
    this.vocab = [...new Set(text.split(''))].sort();
    this.vocab.forEach((c, i) => (this.charToIdx[c] = i));
    for (let i = 0; i < text.length - this.n; i++) {
      const ctx  = text.slice(i, i + this.n - 1);
      const next = text[i + this.n - 1];
      if (!this.counts[ctx]) this.counts[ctx] = {};
      this.counts[ctx][next] = (this.counts[ctx][next] || 0) + 1;
    }
    return this;
  }

  logProb(ctx, char) {
    const dist  = this.counts[ctx] || {};
    const num   = (dist[char] || 0) + this.smoothing;
    const denom = Object.values(dist).reduce((a, b) => a + b, 0)
                  + this.smoothing * this.vocab.length;
    return Math.log(num / denom);
  }

  perplexity(text) {
    let logSum = 0, count = 0;
    for (let i = this.n - 1; i < text.length; i++) {
      const ctx  = text.slice(i - (this.n - 1), i);
      const char = text[i];
      logSum += this.logProb(ctx, char);
      count++;
    }
    return Math.exp(-logSum / count);
  }

  sample(ctx, temperature) {
    const dist   = this.counts[ctx] || {};
    const logits = this.vocab.map(c => {
      const cnt   = (dist[c] || 0) + this.smoothing;
      const total = Object.values(dist).reduce((a, b) => a + b, 0)
                    + this.smoothing * this.vocab.length;
      return Math.log(cnt / total) / temperature;
    });
    const maxL = Math.max(...logits);
    const exps = logits.map(l => Math.exp(l - maxL));
    const sum  = exps.reduce((a, b) => a + b, 0);
    const probs = exps.map(e => e / sum);
    let r = Math.random(), cumul = 0;
    for (let i = 0; i < this.vocab.length; i++) {
      cumul += probs[i];
      if (r <= cumul) return this.vocab[i];
    }
    return this.vocab[this.vocab.length - 1];
  }

  generate(seed, length, temperature) {
    let result = seed;
    const n1 = this.n - 1;
    for (let i = 0; i < length; i++) {
      const ctx = result.slice(-n1).padStart(n1, result[0] || ' ');
      result += this.sample(ctx, temperature);
    }
    return result;
  }

  get ngramCount() {
    return Object.values(this.counts).reduce(
      (a, b) => a + Object.keys(b).length, 0
    );
  }
}

// ── Training loop ──────────────────────────────────────────────────────────
console.log('TinyLM — N-gram Language Model Training');
console.log('========================================');
console.log(`Config  n=${N}  epochs=${EPOCHS}  smoothing=${SMOOTHING}  temp=${TEMP}`);
console.log(`Corpus  ${TEXT.length} chars`);
console.log('');

const model       = new NgramLM(N, SMOOTHING);
const lossHistory = [];

console.log('Building vocabulary...');
// Prime vocab on full text
model.train(TEXT);

for (let e = 1; e <= EPOCHS; e++) {
  // Augment with random offset (matches browser training exactly)
  const offset = Math.floor(Math.random() * Math.min(10, TEXT.length));
  model.train(TEXT.slice(offset));
  model.train(TEXT);

  const ppl  = model.perplexity(TEXT);
  const loss = Math.log(ppl);
  lossHistory.push({ epoch: e, loss: +loss.toFixed(4), ppl: +ppl.toFixed(2) });

  // Progress bar
  const filled = Math.round((e / EPOCHS) * 20);
  const bar    = '[' + '█'.repeat(filled) + '░'.repeat(20 - filled) + ']';
  process.stdout.write(`\rEpoch ${e}/${EPOCHS} ${bar}  loss=${loss.toFixed(4)}  ppl=${ppl.toFixed(2)}  `);
}
console.log('\n');

const finalPpl  = model.perplexity(TEXT);
const finalLoss = Math.log(finalPpl);

console.log('Training complete!');
console.log('------------------');
console.log(`Final perplexity : ${finalPpl.toFixed(2)}`);
console.log(`Final loss       : ${finalLoss.toFixed(4)}`);
console.log(`Vocab size       : ${model.vocab.length}`);
console.log(`N-grams learned  : ${model.ngramCount.toLocaleString()}`);
console.log('');

// ── Sample generation ──────────────────────────────────────────────────────
const seeds = ['To', 'Wh', 'An', 'Th'];
console.log('Sample generations (seed → 120 chars):');
console.log('---------------------------------------');
seeds.forEach(seed => {
  const out = model.generate(seed, 120, TEMP);
  console.log(`[${seed}] ${out}`);
});
console.log('');

// ── Save checkpoint ────────────────────────────────────────────────────────
const checkpoint = {
  version     : '1.0',
  trainedAt   : new Date().toISOString(),
  config      : { n: N, epochs: EPOCHS, smoothing: SMOOTHING, temperature: TEMP },
  corpusLength: TEXT.length,
  vocab       : model.vocab,
  counts      : model.counts,
  metrics     : {
    finalPerplexity : +finalPpl.toFixed(4),
    finalLoss       : +finalLoss.toFixed(6),
    vocabSize       : model.vocab.length,
    ngramCount      : model.ngramCount,
    lossHistory,
  },
};

const outPath = path.join(__dirname, 'model_checkpoint.json');
fs.writeFileSync(outPath, JSON.stringify(checkpoint, null, 2));
console.log(`Checkpoint saved → ${outPath}`);
