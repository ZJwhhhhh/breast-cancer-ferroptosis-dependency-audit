#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'figure_source_data'
OUT = ROOT / 'outputs' / 'figures'
OUT.mkdir(parents=True, exist_ok=True)

comp = pd.read_csv(DATA / 'Figure5_observed_composition.csv')
res = pd.read_csv(DATA / 'Figure5_standardized_residuals.csv')
stats = pd.read_csv(DATA / 'Figure5_global_tests.csv')

rows = [f"{r.keyword_cluster}  {r.cluster_label}" for r in comp.itertuples()]
cols = ['R1', 'R2', 'R3']
a = comp[['R1_percent','R2_percent','R3_percent']].to_numpy(float)
b = res[['R1_residual','R2_residual','R3_residual']].to_numpy(float)

fig, axes = plt.subplots(1, 2, figsize=(14.5, 7.4), gridspec_kw={'width_ratios':[1,1]})
fig.suptitle('Cross-layer relationships between research fronts and intellectual bases', fontsize=16, fontweight='bold', y=.98)
fig.text(.5,.945,'Observed composition and standardized residuals across 117 bridge documents',ha='center',fontsize=10)

im1 = axes[0].imshow(a, cmap=LinearSegmentedColormap.from_list('bluegray',['#f2f3f3','#173b5e']), aspect='auto', vmin=0, vmax=100)
axes[0].set_title('A  Observed cross-layer composition', loc='left', fontweight='bold')
axes[0].set_yticks(range(len(rows)), labels=rows, fontsize=8)
axes[0].set_xticks(range(3), labels=cols)
for i in range(a.shape[0]):
    for j in range(a.shape[1]):
        axes[0].text(j,i,f'{a[i,j]:.1f}%',ha='center',va='center',fontsize=8,color='white' if a[i,j] > 45 else '#111')

cmap = LinearSegmentedColormap.from_list('div',['#173b5e','#f4f4f1','#b04a3a'])
im2 = axes[1].imshow(b, cmap=cmap, norm=TwoSlopeNorm(vmin=-2,vcenter=0,vmax=2), aspect='auto')
axes[1].set_title('B  Departure from independence', loc='left', fontweight='bold')
axes[1].set_yticks(range(len(rows)), labels=[])
axes[1].set_xticks(range(3), labels=cols)
for i in range(b.shape[0]):
    for j in range(b.shape[1]):
        axes[1].text(j,i,f'{b[i,j]:+.2f}',ha='center',va='center',fontsize=8,color='#111')

for ax in axes:
    ax.set_xticks(np.arange(-.5,3,1), minor=True)
    ax.set_yticks(np.arange(-.5,10,1), minor=True)
    ax.grid(which='minor',color='white',linewidth=1.2)
    ax.tick_params(which='minor',bottom=False,left=False)
    for s in ax.spines.values(): s.set_visible(False)

cb1=fig.colorbar(im1,ax=axes[0],orientation='horizontal',fraction=.06,pad=.13)
cb1.set_label('Observed share (%)')
cb2=fig.colorbar(im2,ax=axes[1],orientation='horizontal',fraction=.06,pad=.13)
cb2.set_label('Standardized residual')
p=float(stats.loc[stats.analysis.str.startswith('Primary'),'empirical_p'].iloc[0])
v=float(stats.loc[stats.analysis.str.startswith('Primary'),'cramers_v'].iloc[0])
fig.text(.5,.015,f'Primary global permutation test: empirical P = {p:.3f}; descriptive Cramer V = {v:.3f}. No cell remained significant after BH correction.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.04,1,.93])
fig.savefig(OUT/'Figure_5_Cross_Layer_Relationships_REPRODUCED.png',dpi=600,bbox_inches='tight',facecolor='white')
fig.savefig(OUT/'Figure_5_Cross_Layer_Relationships_REPRODUCED.pdf',bbox_inches='tight',facecolor='white')
print('Wrote Figure 5 PNG and PDF to', OUT)

