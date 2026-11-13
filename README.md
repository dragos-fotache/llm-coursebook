# Understanding Modern LLMs - coursebook

An evolving Quarto book built from completed learning units. The HTML version includes interactive figures; the PDF version includes static figures. Exercises and worked solutions are typeset in both editions.

No Quarto account is required. Install the open-source Quarto CLI locally, or let the GitHub Actions workflow render the source.

## Local use

Requirements: Quarto 1.11.9 or a compatible later release. Typst is bundled with Quarto; a separate LaTeX installation is not required for this book.

~~~sh
quarto render --to all
quarto preview
~~~

The rendered website and PDF are written to the _book directory. The entry point is _book/index.html.

The lesson sources are units/01-local-change.qmd and units/02-computational-graphs.qmd. A .qmd file is Markdown with Quarto metadata and optional computational features. This book does not execute Python or R during rendering.

## Updating the book

1. Update the chapter source and typeset worked solutions.
2. Render locally and inspect equations, links, figures, and the PDF.
3. Commit and push to main.

The GitHub Actions workflow builds the HTML and PDF and deploys _book to GitHub Pages.

## Content boundaries

Only the edited coursebook and selected lesson assets belong here. The parent workspace's planning notes, learner profile, chat records, and account configuration are not part of this repository.

Publish the correct worked calculations without personal error or correction narratives. Handwritten-exercise photographs are excluded from the book and its current published assets.

## Hosting

Public URL: https://dragos-fotache.github.io/llm-coursebook/

Open the website in Safari on an iPad. Use Share > Add to Home Screen for a shortcut, or download the PDF from the book's navigation to read it in Books or a note-taking app.

The interactive loss plot is a standalone export of the graph used during unit 1. Its browser-local saved state does not change the coursebook source or send information to the learning chat.

The editable plot fragment is assets/loss-surface-source.html; assets/loss-surface.html is its standalone export. The optional scripts/generate_figures.py regenerates the static SVG figures with NumPy and Matplotlib. These figures are checked in, so the publishing build needs neither Python package.

The optional scripts/generate_graphs.py regenerates unit 2's SVG computational graphs with Graphviz. These assets are also checked in; publishing does not require Graphviz.
