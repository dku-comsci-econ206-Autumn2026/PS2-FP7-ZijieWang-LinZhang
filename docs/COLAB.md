# Colab

[Open shared Colab](https://colab.research.google.com/drive/1E5NDNUU62rHPwp9UCG9oEHXplz3PG9EJ?usp=sharing). Live sharing settings were not independently verified. The fixed repository source is [`notebooks/dynamic_fee_choice.ipynb`](../notebooks/dynamic_fee_choice.ipynb); upload this file to Colab to run the exact packaged version.

Choose **Runtime → Run all** on CPU. The source has 26 cells, including 13 Python cells. It implements the stage best-response check, three-condition simulation, round-level comparison, signal-following sensitivity, and noisy-urgency experiment. No external data or API key is required.

The notebook exports `condition_summary.csv`, `round_summary.csv`, `signal_sensitivity.csv`, `noisy_urgency_summary.csv`, and `noisy_urgency_round_records.csv`. Download the files you need before the runtime ends. The large round-level file is generated on demand and excluded from Git.

For local verification, follow the root README and run `python scripts/reproduce.py`. It also exports `strategic_benchmark.csv`, sixteen PNGs, an executed notebook, and a run manifest. The comparison policy is not the stage equilibrium, and these simulations do not solve the full dynamic Bayesian game.
