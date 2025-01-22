# MkDocs Slides Plugin

A plugin for MkDocs that enables beautiful slide presentations within your documentation.

## Installation

```bash
pip install mkdocs-slides
```

## Usage

1. Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - slides
```

2. Create a slide deck in your markdown:

```yaml
```slides
title: My Presentation
url_stub: my-pres
nav:
    - slides/presentation/*.md
```

## Configuration

You can customize the plugin behavior in your `mkdocs.yml`:

```yaml
plugins:
  - slides:
      font_size: "28px"  # Default font size for slides
      template: "layouts/slide_template.html"  # Custom slide template
```

### Custom Templates

To use a custom template:

1. Create a `layouts` directory in your docs root
2. Copy the default template as a starting point:
```bash
mkdir -p layouts
cp $(python -c "import mkdocs_slides; import os; print(os.path.join(os.path.dirname(mkdocs_slides.__file__), 'templates', 'slide_template.html'))") layouts/slide_template.html
```

3. Modify the template to suit your needs
4. Reference it in your `mkdocs.yml`

For full documentation, visit [the plugin documentation](https://ianderrington.github.io/mkdocs_slides/).

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
