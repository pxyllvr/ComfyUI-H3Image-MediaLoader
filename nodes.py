"""MiniMax H3-Image Media Loader
Extension nodepack for the official MiniMax-H3-Image model (released 2026-11-10).
Supports up to 16 reference images with the full QoL of the original Fantastic H3 Media Loader
(drag-and-drop, crop, mirror, rotate, resize, enable/disable, previews, etc.).

Isolated from Adudeguyman's pack so changes here don't affect the video-focused nodes.
"""

import json
import os

from . import media_io

try:
    import folder_paths
except Exception:
    folder_paths = None

# Official H3-Image supports up to 16 reference images.
PICTURES = 16


class MiniMaxH3ImageMediaLoader:
    """Drag-and-drop / file-picker loader for H3-Image reference images (up to 16).

    Emits a single `references` bundle. Use the companion Reference Splitter
    when you need the individual picture_1 .. picture_16 IMAGE slots.
    Carries over crop / mirror / rotate / resize / enable from the original loader.
    """

    CATEGORY = "conditioning/image_models"
    DESCRIPTION = (
        "Load up to 16 reference images for MiniMax-H3-Image by drag-and-drop or file picker. "
        "Supports the same crop, mirror, rotate, resize, and enable/disable QoL as the original "
        "Fantastic H3 Media Loader. Outputs a single references bundle — use the "
        "Fantastic H3-Image Reference Splitter to get individual picture slots. "
        "Picture 1 is typically the image being edited."
    )

    RETURN_TYPES = ("H3_IMAGE_REFS",)
    RETURN_NAMES = ("references",)
    FUNCTION = "load"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "media_state": ("STRING", {"multiline": False, "default": "[]"}),
            },
            "hidden": {"prompt": "PROMPT", "unique_id": "UNIQUE_ID"},
        }

    @classmethod
    def IS_CHANGED(cls, media_state="[]", **kwargs):
        return media_state

    @classmethod
    def VALIDATE_INPUTS(cls, media_state="[]", **kwargs):
        try:
            items = json.loads(media_state or "[]")
        except Exception:
            return "Media Loader state is corrupt; clear the node and re-add media."
        if not isinstance(items, list):
            return "Media Loader state is corrupt; clear the node and re-add media."
        pics = sum(1 for i in items if isinstance(i, dict) and i.get("kind") == "picture" and i.get("enabled") is not False)
        if pics > PICTURES:
            return f"{pics} pictures loaded; H3-Image accepts {PICTURES}."
        return True

    @staticmethod
    def _partition(items):
        pictures = []
        for item in items:
            if not isinstance(item, dict) or item.get("enabled") is False:
                continue
            if item.get("kind") == "picture":
                pictures.append(item)
        return pictures

    def load(self, media_state="[]", prompt=None, unique_id=None):
        try:
            items = json.loads(media_state or "[]")
        except Exception:
            items = []

        pictures = self._partition(items)

        pic_t = []
        for i in pictures[:PICTURES]:
            try:
                img = media_io.load_image(
                    i["file"],
                    crop=i.get("crop"),
                    mirror=bool(i.get("mirror")),
                    rotate=i.get("rotate") or 0,
                    resize=i.get("resize") or 0,
                )
                pic_t.append(img)
            except Exception as e:
                print(f"[H3Image MediaLoader] failed to load {i.get('file')}: {e}")
                pic_t.append(None)

        # Pad to exactly PICTURES so the splitter always gets a full list
        while len(pic_t) < PICTURES:
            pic_t.append(None)

        bundle = {
            "pictures": pic_t,
            "items": items,
            "count": sum(1 for x in pic_t if x is not None),
        }

        print(f"[H3Image MediaLoader] {len(items)} item(s) -> {bundle['count']} picture(s) ready (max {PICTURES})")

        return (bundle,)


class MiniMaxH3ImageReferenceSplitter:
    """Fan image references into individual picture slots (1-16).

    Accepts either the Media Loader's references bundle, or a batch IMAGE
    tensor (e.g. from a Load Image Batch or similar node). When both are
    connected, the batch overrides the bundle.
    """

    CATEGORY = "conditioning/image_models"
    DESCRIPTION = (
        "Split references into individual picture_1 .. picture_16 IMAGE outputs "
        "for wiring into MiniMaxH3ImageConditioning. Accepts the Media Loader bundle "
        "or a batch IMAGE (batch overrides bundle when both are connected)."
    )

    RETURN_TYPES = ("IMAGE",) * PICTURES
    RETURN_NAMES = tuple(f"picture_{i}" for i in range(1, PICTURES + 1))
    FUNCTION = "split"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "references": ("H3_IMAGE_REFS",),
                "images": ("IMAGE",),
            }
        }

    def split(self, references=None, images=None):
        pics = []

        # Batch IMAGE overrides the bundle when connected.
        if images is not None:
            # images: [B, H, W, C] — each slice is one picture
            try:
                batch = images.shape[0] if hasattr(images, "shape") else len(images)
            except Exception:
                batch = 0
            for i in range(min(batch, PICTURES)):
                pics.append(images[i:i+1])
        elif isinstance(references, dict):
            pics = list(references.get("pictures") or [])

        pics = pics[:PICTURES] + [None] * (PICTURES - len(pics))
        return tuple(pics)


NODE_CLASS_MAPPINGS = {
    "MiniMaxH3ImageMediaLoader": MiniMaxH3ImageMediaLoader,
    "MiniMaxH3ImageReferenceSplitter": MiniMaxH3ImageReferenceSplitter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MiniMaxH3ImageMediaLoader": "Fantastic H3-Image Media Loader (16 refs)",
    "MiniMaxH3ImageReferenceSplitter": "Fantastic H3-Image Reference Splitter",
}
