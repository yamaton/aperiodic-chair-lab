"""Render exact-profile comparisons; these figures exaggerate physical height."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np

HERE = Path(__file__).resolve().parent


def main():
    candidate = json.loads((HERE/'triangular_v1/candidate.json').read_text())
    assert candidate['port_profile']['normalized_vertices'] == [[-1,-1],[1,-1],[-1,0]]
    fig = plt.figure(figsize=(12, 7.2), facecolor='#fafaf8')
    old_axes = fig.add_subplot(221, projection='3d')
    new_axes = fig.add_subplot(222, projection='3d')
    u, v = np.meshgrid(np.linspace(-1, 1, 65), np.linspace(-1, 1, 65))
    old = (1-u*u)*(1-v*v)*(1+u/5+v/7)
    old_axes.plot_surface(u,v,old,cmap='Blues',linewidth=0,antialiased=True)
    n = 55
    bary = np.array([(i/n,j/n) for i in range(n+1) for j in range(n+1-i)])
    x,y = bary.T
    tu,tv = 2*x-1,y-1
    triangulation = mtri.Triangulation(tu,tv)
    new = 27*x*y*(1-x-y)
    new_axes.plot_trisurf(triangulation,new,cmap='YlGn',linewidth=0,antialiased=True)
    for ax, title in [(old_axes,'Existing square cap: degree 5'),(new_axes,'Candidate triangular cap: degree 3')]:
        ax.set_title(title,fontsize=13,pad=12)
        ax.set(xlim=(-1.1,1.1),ylim=(-1.1,1.1),zlim=(0,1.25),xlabel='u',ylabel='v')
        ax.set_zlabel('height / depth unit',labelpad=8)
        ax.set_box_aspect((1,1,.55));ax.view_init(elev=26,azim=-60)
        ax.set_facecolor('#fafaf8')
        ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1]);ax.set_zticks([0,1])
    square = fig.add_subplot(223)
    triangle = fig.add_subplot(224)
    square.plot([-1,1,1,-1,-1],[-1,-1,1,1,-1],color='#3974a4',lw=2.5)
    square.text(0,0,'Square: 8 symmetries.\nAn extra linear factor\nfixes its orientation.',ha='center',va='center',fontsize=11)
    triangle.fill([-1,1,-1],[-1,-1,0],color='#a9d694',alpha=.4)
    triangle.plot([-1,1,-1,-1],[-1,-1,0,-1],color='#347b42',lw=2.5)
    triangle.text(0,-1.18,'long leg: 2w',ha='center',fontsize=11)
    triangle.text(-1.1,-.5,'w',ha='right',va='center',fontsize=11)
    triangle.text(.08,-.33,r'$\sqrt{5}w$',fontsize=11,rotation=-27)
    triangle.plot([-1],[ -1],'o',color='#347b42')
    triangle.text(.1,.65,'Three unequal sides\nfix the ordered axes.\nNo extra tilt factor needed.',ha='center',va='center',fontsize=12)
    for ax in (square,triangle):
        ax.set_aspect('equal');ax.set(xlim=(-1.5,1.5),ylim=(-1.5,1.25));ax.axis('off')
    fig.suptitle('Move the orientation information into the footprint',fontsize=17,y=.995)
    fig.text(.5,.015,'Both surfaces shown at key +1. Heights greatly exaggerated; two-depth candidate uses keys ±1 and ±2.\nExact curved profiles are specified in JSON. This illustration is not a certified manufactured surface.',ha='center',fontsize=10,color='#444444')
    fig.tight_layout(rect=(0,.07,1,.98))
    output = HERE.parent/'artifacts/port-simplification.png'
    fig.savefig(output,dpi=160,facecolor=fig.get_facecolor())
    plt.close(fig)
    print(output)


if __name__ == '__main__':
    main()
