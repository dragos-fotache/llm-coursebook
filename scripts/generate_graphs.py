"""Regenerate the coursebook's computational graphs with Graphviz."""

from pathlib import Path
import subprocess


ASSETS = Path(__file__).resolve().parents[1] / "assets"
STYLE = '''
  graph [rankdir=LR, bgcolor="transparent", pad="0.15", nodesep="0.35", ranksep="0.35"];
  node [shape=box, style="rounded,filled", fillcolor="#f2f7fa", color="#9aa7b2",
        fontname="DejaVu Sans", fontsize=14, margin="0.12,0.08", penwidth=0.8];
  edge [color="#216b9c", arrowsize=0.65, penwidth=1.1];
'''

GRAPHS = {
    "computational-chain": '''
      w [label="w"]; b [label="b"];
      a [label="a = 2w"]; p [label="p = a + b"];
      e [label="e = p - 5"]; L [label="L = e²"];
      w -> a; a -> p; b -> p; p -> e; e -> L;
    ''',
    "shared-intermediate": '''
      a [label="a"]; b [label="b"]; u [label="u = ab"];
      q [label="q = u²"]; L [label="L = q + u"];
      a -> u; b -> u; u -> q; q -> L; u -> L;
    ''',
    "two-paths": '''
      a [label="a = 2"]; b [label="b = -1"];
      r [label="r = a + b\\n= 1"]; s [label="s = ab\\n= -2"];
      J [label="J = rs\\n= -2"];
      a -> r; b -> r; a -> s; b -> s; r -> J; s -> J;
    ''',
}


for name, graph in GRAPHS.items():
    source = "digraph {\n" + STYLE + graph + "\n}"
    subprocess.run(
        ["dot", "-Tsvg", "-o", str(ASSETS / f"{name}.svg")],
        input=source,
        text=True,
        check=True,
    )
    print(f"Created {name}.svg")
