# Understanding Modern LLMs - coursebook

An evolving Quarto website built from completed learning units, with typeset mathematics, expandable worked solutions, executable Python examples, and interactive figures.

No Quarto account is required. Install the open-source Quarto CLI locally, or let the GitHub Actions workflow render the source.

## Local use

Requirements: Quarto 1.11.9 or a compatible later release. The publishing build renders HTML only.

~~~sh
quarto render --to html
quarto preview
~~~

The rendered website is written to the _book directory. The entry point is _book/index.html. If an older local build contains understanding-modern-llms.pdf, remove that generated file before serving or uploading the output directory.

Lesson sources live in units/. A .qmd file is Markdown with Quarto metadata and optional computational features. This book does not execute Python or R during rendering; check the Python worked examples separately.

## Updating the book

1. Update the chapter source and typeset worked solutions.
2. Check worked calculations and code, render HTML, and inspect equations, links, expandable solutions, and interactive figures at desktop and tablet widths.
3. Commit and push to main.

The GitHub Actions workflow builds HTML and deploys _book to GitHub Pages.

The learner currently uses the website only. Keep the PDF download and PDF rendering disabled; a PDF can be generated at the end of the project if requested. No PDF artifact should be included in the published output.

## Content boundaries

Only the edited coursebook and selected lesson assets belong here. The parent workspace's planning notes, learner profile, chat records, and account configuration are not part of this repository.

Publish the correct worked calculations without personal error or correction narratives. Handwritten-exercise photographs are excluded from the book and its current published assets.

## Hosting

Public URL: https://dragos-fotache.github.io/llm-coursebook/

Open the website in Safari on an iPad. Use Share > Add to Home Screen for a shortcut.

The interactive loss plot is a standalone export of the graph used during unit 1. Its browser-local saved state does not change the coursebook source or send information to the learning chat.

The editable plot fragment is assets/loss-surface-source.html; assets/loss-surface.html is its standalone export. The optional scripts/generate_figures.py regenerates the static SVG figures with NumPy and Matplotlib. These figures are checked in, so the publishing build needs neither Python package.

The optional scripts/generate_graphs.py regenerates unit 2's SVG computational graphs with Graphviz. These assets are also checked in; publishing does not require Graphviz.

Unit 3's assets/scalar_autodiff.py is the standalone worked implementation. Keep it consistent with the complete code listing in the chapter. assets/backward-trace.html is a standalone interactive trace of the shared graph; it runs entirely in the browser and includes an intentionally early-callback order for comparison.
