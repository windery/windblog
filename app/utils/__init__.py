from .HighlighterRenderer import HighlightRenderer as hrenderer
import mistune

renderer = hrenderer()
markdown = mistune.Markdown(renderer=renderer)
