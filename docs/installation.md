# Installation

## Requirements

- Python 3.7 or higher
- MkDocs 1.4.0 or higher
- Material for MkDocs (recommended)

## Installing the Plugin

Install using pip:

```bash
pip install mkdocs-slides
```

## Configuration

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - slides
```

### Optional Configuration

```yaml
plugins:
  - slides:
      auto_play: false  # Enable automatic slide advancement
      slide_delay: 5    # Seconds between slides in auto-play mode
      theme: default    # Slide theme (default, dark, light)
``` 