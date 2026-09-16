"""Draw face arrows and the local parent rule from checked motif data."""

import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np


HERE = Path(__file__).resolve().parent
BG, FG, MUTED = '#101c29', '#eff5fb', '#adbfce'
COLORS = {'A': '#e9b875', 'B': '#ac9ddd', 'C': '#63c7ad'}


def run():
    data = json.loads((HERE / 'motif_grouping_certificate.json').read_text())
    checked = json.loads((HERE / 'motif_grouping_verification.json').read_text())
    assert checked['status'] == 'passed' and data['candidate_sha256'] == checked['candidate_sha256']
    fig, axes = plt.subplots(3, 3, figsize=(12, 10), facecolor=BG)
    for ax in axes.flat:
        ax.set(facecolor=BG, xlim=(-1.18, 1.18), ylim=(-1.3, 1.2), aspect='equal')
        ax.axis('off')
    for index in range(9):
        ax = axes.flat[index]
        axis = index % 3
        sign = -1 if index < 3 else 1
        plane = -2 if index < 3 else 2 if index < 6 else 0
        n = np.eye(3, dtype=int)[axis]*sign
        u = np.eye(3, dtype=int)[(axis+1) % 3]
        v = np.cross(n, u)
        for f in data['face_table']:
            if tuple(f['normal']) != tuple(n) or f['center_times_2'][axis] != plane:
                continue
            center = np.array(f['center_times_2'])/2
            x, y = center @ u, center @ v
            color = COLORS[f['motif']]
            ax.add_patch(Rectangle((x-.5, y-.5), 1, 1, facecolor=color, edgecolor=BG, linewidth=2))
            ax.text(x-.31, y+.23, f['motif'], fontsize=20, color=BG, fontweight='bold', ha='center')
            arrow = np.array(f['arrow'])
            dx, dy = .52*(arrow @ u), .52*(arrow @ v)
            ax.annotate('', (x+dx/2, y+dy/2-.08), (x-dx/2, y-dy/2-.08),
                        arrowprops={'arrowstyle': '-|>', 'color': BG, 'lw': 2})
            ax.text(x+.34, y+.33, str(f['id']), fontsize=8, color=BG, ha='center')
        label = f"{'xyz'[axis]} = {plane/2:g}" if index < 6 else f"Notch: {'xyz'[axis]} = 0"
        ax.set_title(label, color=FG, fontsize=15)
        vlabel = ('+' if v[(axis+2) % 3] > 0 else '-')+'xyz'[(axis+2) % 3]
        ax.text(0, -1.23, f"Screen right: +{'xyz'[(axis+1) % 3]}    up: {vlabel}", ha='center', color=MUTED, fontsize=9)
    fig.suptitle('The entire matching rule: 24 faces, three patterns, and arrows', color=FG, fontsize=18, y=.98)
    fig.text(.5, .935, 'A meets A with U₂ = V₁; B meets C with U₂ = −U₁. Opposing normals; V = n × U.',
             color=MUTED, ha='center', fontsize=11)
    fig.text(.5, .025, 'Each square is one exposed unit face. Tiny numbers link to the proof tables. Blank positions are absent faces.',
             color=MUTED, ha='center', fontsize=10)
    fig.subplots_adjust(left=.06, right=.94, bottom=.08, top=.88, hspace=.38, wspace=.25)
    fig.savefig(HERE.parent / 'artifacts/motif-face-layout.png', dpi=170, facecolor=BG)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(13, 6), facecolor=BG)
    ax.set(xlim=(0, 13), ylim=(0, 6)); ax.axis('off')
    def box(x, y, w, h, title, body, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.12', facecolor=color, edgecolor='none'))
        ax.text(x+w/2, y+h-.27, title, ha='center', va='top', color=BG, fontsize=14, fontweight='bold')
        ax.text(x+w/2, y+h/2-.12, body, ha='center', va='center', color=BG, fontsize=11, linespacing=1.5)
    def link(a, b, text='', offset=(0, 0)):
        ax.annotate('', b, a, arrowprops={'arrowstyle': '-|>', 'color': FG, 'lw': 1.7})
        ax.text((a[0]+b[0])/2+offset[0], (a[1]+b[1])/2+offset[1], text, color=FG, ha='center', fontsize=10)
    ax.text(6.5, 5.78, 'Find a chair’s parent from its immediate neighbors', ha='center', color=FG, fontsize=20)
    box(.35, 2.1, 3.1, 2, 'Inspect chair Q', 'One of six specified\nmixed-sign diagonal\ncontacts present?', COLORS['A'])
    box(4.5, 3.7, 3.35, 1.35, 'Yes: Q is a center', 'Face coverage forces the\nseven outer children.', COLORS['C'])
    box(4.5, .8, 3.35, 1.8, 'No: inspect notch owner P', 'Six orientations: Q itself\ntriggers a center at P.\nSame orientation: use S.', COLORS['B'])
    box(9, 2.1, 3.55, 2, 'Parent of Q is determined', 'Center case: Q itself.\nOtherwise: notch owner P.\nAll seven children agree.', '#d4e4ef')
    link((3.6, 3.7), (4.34, 4.3), 'yes', (0, .2))
    link((3.6, 2.55), (4.34, 1.9), 'no', (0, -.3))
    link((8.02, 4.3), (8.85, 3.7))
    link((8.02, 1.85), (8.85, 2.6))
    ax.text(6.5, .28, 'Same-orientation case: P=(1,1,1), S=(2,0,0). From P, S is the diagonal trigger (1,−1,−1).',
            ha='center', color=MUTED, fontsize=10)
    fig.tight_layout()
    fig.savefig(HERE.parent / 'artifacts/motif-parent-rule.png', dpi=170, facecolor=BG)
    plt.close(fig)
    print('Wrote motif-face-layout.png and motif-parent-rule.png')


if __name__ == '__main__':
    run()
