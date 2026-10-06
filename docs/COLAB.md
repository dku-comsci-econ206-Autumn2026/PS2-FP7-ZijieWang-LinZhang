# Updated Colab

[Open notebook](https://colab.research.google.com/drive/1E5NDNUU62rHPwp9UCG9oEHXplz3PG9EJ?usp=sharing). Live sharing settings were not independently verified.

Run all cells on CPU. The source has 22 cells, of which 10 contain Python code. It implements a three-round L/M/H game, a stage best-response check, three-condition simulation, round-level outputs, and signal-following sensitivity. No external dataset or API key is required.

The final cell exports `condition_summary.csv`, `round_summary.csv`, and `signal_sensitivity.csv`. Download those files before the runtime ends. For a fixed local run, follow the README and `scripts/reproduce.py`; it also exports `strategic_benchmark.csv`, eleven figures, and a manifest.

The comparison policy is not the stage equilibrium. Do not describe these Monte Carlo results as a solved full dynamic Bayesian equilibrium.
