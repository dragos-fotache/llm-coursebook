# Understanding Modern LLMs - coursebook

An evolving Quarto book built from completed learning units. The HTML version includes interactive figures; the PDF version includes static figures and the handwritten workbook.

No Quarto account is required. Install the open-source Quarto CLI locally, or let the GitHub Actions workflow render the source.

## Local use

Requirements: Quarto 1.11.9 or a compatible later release. Typst is bundled with Quarto; a separate LaTeX installation is not required for this book.

~~~sh
quarto render --to all
quarto preview
~~~

The rendered website and PDF are written to the _book directory. The entry point is _book/index.html.

The lesson source is units/01-local-change.qmd. A .qmd file is Markdown with Quarto metadata and optional computational features. This book does not execute Python or R during rendering.

## Updating the book

1. Update the chapter source and reviewed working.
2. Render locally and inspect equations, links, figures, and the PDF.
3. Commit and push to main.

The GitHub Actions workflow builds the HTML and PDF and deploys _book to GitHub Pages.

## Content boundaries

Only the edited coursebook and selected lesson assets belong here. The parent workspace's planning notes, learner profile, chat records, and account configuration are not part of this repository.

## Hosting

Public URL: https://dragos-fotache.github.io/llm-coursebook/

Open the website in Safari on an iPad. Use Share > Add to Home Screen for a shortcut, or download the PDF from the book's navigation to read it in Books or a note-taking app.

The interactive loss plot is a standalone export of the graph used during unit 1. Its browser-local saved state does not change the coursebook source or send information to the learning chat.

The editable plot fragment is assets/loss-surface-source.html; assets/loss-surface.html is its standalone export. The optional scripts/generate_figures.py regenerates the static SVG figures with NumPy and Matplotlib. These figures are checked in, so the publishing build needs neither Python package.
