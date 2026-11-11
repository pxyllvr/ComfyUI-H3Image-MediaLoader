"""ComfyUI-H3Image-MediaLoader
Isolated extension for official MiniMax-H3-Image (16 reference images).
Based on the QoL of Adudeguyman's Fantastic H3 Media Loader but kept separate.
"""

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Register upload / probe routes used by the media loader frontend.
try:
    from . import web_api  # noqa: F401
except Exception as exc:
    print(f"[H3Image MediaLoader] media routes unavailable: {exc}")

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
