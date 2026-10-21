# Reproducibility

The current source is [`notebooks/dynamic_fee_choice.ipynb`](../notebooks/dynamic_fee_choice.ipynb), copied byte-for-byte from the authors’ updated notebook. The README lists inputs, results, commands, and metric denominators. `results/run_manifest.json` records the current source hash, runtime, seeds, output hashes, and validation results; `results/baseline_run_manifest.json` preserves the earlier baseline test record.

Run `python scripts/reproduce.py` from the repository root after installing `requirements.txt`. All thirteen code cells execute in source order with their code unchanged. The runner captures final expressions and explicit display calls, exports Matplotlib figures, and sets the working directory to `results/` for the notebook’s relative CSV exports.

The full run contains 900,000 baseline rows, 990,000 signal-following sensitivity rows, and 900,000 noisy-urgency rows. Checks cover eighteen baseline and eighteen noisy-urgency aggregate values, exact zero-noise agreement with the signal baseline, six strict best responses, three-round session lengths, and sixteen figures. The fresh executed notebook is written to `results/dynamic_fee_choice.executed.ipynb`.

Six CSVs are generated, including the stage benchmark. The large `noisy_urgency_round_records.csv` is generated locally, excluded by `.gitignore`, and omitted from the upload package; the aggregate noise summary is included.

The historical baseline was tested at commit `726511c24480e1d95ed4a611672a214334679625`. The current local package has no Git commit, so its new run manifest records `tested_commit: null` and identifies the tested source by SHA-256. After uploading, rerun in the actual checkout and record that commit; a local source hash must not be presented as a GitHub commit.

The current poster’s baseline comparison maps to the full-precision baseline CSVs and generated figures. All observations are simulated; no participant dataset is used.
