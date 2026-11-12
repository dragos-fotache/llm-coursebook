from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

out = Path(__file__).resolve().parents[1] / "assets"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.labelsize": 10,
    "svg.fonttype": "none", "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#9aa7b2", "axes.linewidth": 0.6,
    "xtick.color": "#46515b", "ytick.color": "#46515b"
})
blue = "#216b9c"
fig, ax = plt.subplots(figsize=(4.6, 3.05), layout="constrained")
w = np.linspace(0.5, 2.15, 400)
ax.plot(w, (2*w-4)**2, color=blue, lw=1.8, label="Squared loss")
ax.plot(w, 4-8*(w-1), color="#6b7280", lw=1.25, ls="--", label="Tangent at w = 1")
ax.scatter([1], [4], color=blue, s=22, zorder=4)
ax.annotate("(1, 4)", (1, 4), xytext=(6, 7), textcoords="offset points")
ax.axhline(0, color="#cdd4da", lw=0.6, zorder=0)
ax.set(xlabel="Weight w", ylabel="Loss L", xlim=(0.5, 2.15), ylim=(-2, 10))
ax.set_xticks([0.5, 1, 1.5, 2])
ax.set_yticks([0, 4, 8])
ax.legend(loc="upper right", frameon=False, fontsize=8)
fig.savefig(out / "local-linearization.svg")
plt.close(fig)

fig, ax = plt.subplots(figsize=(4.6, 3.3), layout="constrained")
wv = np.linspace(0.6, 3.6, 300)
bv = np.linspace(0.5, 2.5, 230)
W, B = np.meshgrid(wv, bv)
Z = (2*W+B-5)**2
contours = ax.contour(W, B, Z, levels=[1, 4, 9, 16], colors=["#bac6d0"], linewidths=0.7)
ax.clabel(contours, fmt=lambda value: "L=" + str(int(value)), fontsize=8, inline=True)
ax.plot([1.25, 2.25], [2.5, 0.5], color="#26323b", lw=1.15)
ax.text(1.3, 2.35, "L=0", fontsize=8, bbox={"facecolor": "white", "edgecolor": "none", "pad": 1})
ax.plot([1, 3.4], [1, 2.2], color="#9aa7b2", lw=0.8, ls="--")
ax.annotate("", xy=(1.8, 1.4), xytext=(1, 1), arrowprops={"arrowstyle": "-|>", "color": blue, "lw": 1.6})
ax.scatter([1], [1], s=15, color="#26323b", zorder=5)
ax.scatter([1.8], [1.4], s=28, color=blue, zorder=5)
ax.annotate("start", (1, 1), xytext=(-7, -12), textcoords="offset points", ha="right", fontsize=8)
ax.annotate("new", (1.8, 1.4), xytext=(7, 5), textcoords="offset points", fontsize=8)
ax.set(xlabel="Weight w", ylabel="Bias b", xlim=(0.6, 3.6), ylim=(0.5, 2.5), aspect="equal")
ax.set_xticks([1, 2, 3])
ax.set_yticks([0.5, 1, 1.5, 2, 2.5])
fig.savefig(out / "loss-contours.svg")
plt.close(fig)
print("Created both vector figures.")
