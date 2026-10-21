"""Execute the supplied notebook's Python cells, export outputs, and check claims.
Run from the repository root: python scripts/reproduce.py
No Jupyter kernel is required. The code cells are executed unchanged, in order.
"""
import ast
import base64
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.mplconfig'))
os.environ['MPLBACKEND'] = 'Agg'
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import IPython
from IPython.utils.capture import capture_output

source = ROOT / 'notebooks/dynamic_fee_choice.ipynb'
nb = json.loads(source.read_text())
plot_count = 0
active_outputs = []
figure_names = [f'figure_{i:02d}.png' for i in range(1, 12)] + [
    'noisy_urgency_priority_alignment.png', 'noisy_urgency_same_fee_collision.png',
    'noisy_urgency_fee_expenditure.png', 'noisy_urgency_user_welfare.png',
    'noisy_urgency_mean_wait.png']

def display_values(*values):
    for value in values:
        data = {'text/plain': [repr(value)]}
        if hasattr(value, '_repr_html_'):
            data['text/html'] = [value._repr_html_()]
        active_outputs.append({'output_type': 'display_data', 'metadata': {}, 'data': data})

namespace = {'__name__': '__main__', 'display': display_values}

def save_figures(*args, **kwargs):
    global plot_count
    for number in plt.get_fignums():
        fig = plt.figure(number)
        plot_count += 1
        path = OUT / figure_names[plot_count - 1]
        fig.savefig(path, dpi=150)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        active_outputs.append({'output_type': 'display_data', 'metadata': {},
            'data': {'image/png': base64.b64encode(buf.getvalue()).decode(),
                     'text/plain': [f'<Figure exported as {path.name}>']}})
    plt.close('all')

plt.show = save_figures
os.chdir(OUT)  # Original notebook writes CSVs relative to its working directory.
count = 0
for idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    count += 1
    active_outputs = []
    tree = ast.parse(''.join(cell['source']), filename=f'cell-{idx}')
    last = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
    with capture_output() as captured:
        exec(compile(tree, f'cell-{idx}', 'exec'), namespace)
        value = eval(compile(ast.Expression(last.value), f'cell-{idx}', 'eval'), namespace) if last else None
    if captured.stdout:
        active_outputs.append({'output_type':'stream','name':'stdout','text':captured.stdout.splitlines(True)})
    if captured.stderr:
        active_outputs.append({'output_type':'stream','name':'stderr','text':captured.stderr.splitlines(True)})
    if value is not None:
        data = {'text/plain': [repr(value)]}
        if hasattr(value, '_repr_html_'):
            data['text/html'] = [value._repr_html_()]
        active_outputs.append({'output_type':'execute_result','execution_count':count,'metadata':{},'data':data})
    cell['execution_count'] = count
    cell['outputs'] = active_outputs
    print(f'Executed code cell {count}', flush=True)

summary = namespace['summary']
# Independently compare all six aggregate metrics against the supplied saved output.
columns = ['same_fee_rate','mean_fee_expenditure','mean_welfare_per_round',
           'mean_wait_after','priority_alignment','urgent_confirmation']
expected = np.array([[.0292,2.9051,2.5982,.6591,.984772,.827554],
                     [.3336,2.3521,3.0570,.5479,.871067,.663947],
                     [.0520,2.8123,2.6780,.6497,.979861,.812451]])
np.testing.assert_allclose(summary[columns].astype(float).to_numpy(), expected, rtol=0, atol=0.000051)
assert namespace['strategic_benchmark']['H_is_strict_best_response_to_H'].all()
assert len(namespace['simulation']) == 900_000
assert plot_count == 16
assert len(namespace['sensitivity']) == 11
assert all(namespace['simulation'].groupby(['condition','session']).size() == 3)
noisy = namespace['noisy_summary'].set_index('error_rate')
noise_columns = ['same_fee_rate', 'priority_alignment', 'urgent_confirmation',
                 'mean_fee_expenditure', 'mean_welfare_per_round', 'mean_wait_after']
noise_expected = np.array([
    [.051980, .97986083, .81245057, 2.8123, 2.6780, .6497],
    [.058717, .86361566, .75388824, 2.8038, 2.5383, .6499],
    [.065520, .77050036, .69745418, 2.7952, 2.4076, .6492]])
np.testing.assert_allclose(noisy.loc[[0., .1, .2], noise_columns].astype(float).to_numpy(),
                           noise_expected, rtol=0, atol=0.000051)
np.testing.assert_allclose(noisy.loc[0., columns].astype(float).to_numpy(),
                           summary.loc['signal', columns].astype(float).to_numpy(),
                           rtol=0, atol=1e-12)
assert len(namespace['noisy_simulation']) == 900_000
assert all(namespace['noisy_simulation'].groupby(['error_rate','session']).size() == 3)
namespace['strategic_benchmark'].to_csv(OUT / 'strategic_benchmark.csv', index=False)
nb['metadata'].setdefault('kernelspec',{'display_name':'Python 3','language':'python','name':'python3'})
(OUT/'dynamic_fee_choice.executed.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n')
try:
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip() if (ROOT/'.git').exists() else None
except subprocess.CalledProcessError:
    commit = None
manifest = {'tested_commit':commit, 'python':platform.python_version(),
    'versions':{m.__name__:m.__version__ for m in [np,pd,matplotlib,IPython]},
    'notebook_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'sessions_per_condition':100000,'rounds':3,'rows':900000,
    'base_seed':206,'condition_seeds':{'complete':206,'incomplete':1000206,'signal':2000206},
    'sensitivity_sessions_per_rho':30000,'sensitivity_seed_rule':'206 + int(rho * 10000) + 2000000',
    'noise_error_rates':[0.0,0.1,0.2], 'noise_sessions_per_rate':100000,
    'noise_rows':900000, 'noise_behavior_seed':2000206,'noise_type_error_seed':3000206,
    'executed_code_cells':count,'figures':plot_count,'aggregate_comparison':'PASS; atol=0.000051',
    'noise_aggregate_comparison':'PASS; 18 metrics; atol=0.000051',
    'zero_noise_baseline_comparison':'PASS; atol=1e-12',
    'poster_numbers_source':'condition_summary.csv; correspondence confirmed by authors',
    'generated_only_files':['noisy_urgency_round_records.csv'],
    'files_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*.csv')) if p.name != 'noisy_urgency_round_records.csv'}}
(OUT/'run_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(summary.to_string())
print('PASS: baseline and noisy-urgency aggregates reproduced; 900,000 baseline rows; 900,000 noisy-urgency rows; 16 figures.')
