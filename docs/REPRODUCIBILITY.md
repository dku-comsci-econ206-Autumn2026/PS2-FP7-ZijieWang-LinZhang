# Reproducibility

The README gives the exact inputs, runtime, fixed commit record, commands, output table, and metric denominators. `results/run_manifest.json` records the tested notebook hash, environment, RNG seeds, output hashes, and verification result.

Run `python scripts/reproduce.py` from the repository root after installing `requirements.txt`. All ten code cells are executed in source order with their code unchanged. Only their final expression is evaluated separately to save its displayed value; Matplotlib show calls export figures. The runner sets the working directory to `results/` so the notebook's existing CSV export cell writes there.

The full run contains 900,000 main simulation rows and 990,000 additional sensitivity rows across eleven compliance settings. The runner checks all eighteen aggregate values against the supplied notebook's saved display, checks the six strict best responses, session lengths, and plot count. It generates a fresh executed notebook with outputs. It does not use participant data.

The tested commit identifies the local source snapshot. If files are uploaded through GitHub's web UI, GitHub creates a different commit: rerun at that actual commit and update the README and manifest accordingly. A local hash must not be presented as an existing GitHub commit.

The README maps the poster's numerical comparison to the full-precision baseline CSVs and generated plots, using the authors' confirmation of the intended poster contents. Retain those files with the poster and use the actual tested GitHub commit in its caption.
