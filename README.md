# ComfyUI-H3Image-MediaLoader

Media loader for the official **MiniMax-H3-Image** model in ComfyUI.

H3-Image accepts up to **16 reference images** (`Picture 1` … `Picture 16`). This pack provides a loader with the same quality-of-life features as the Fantastic H3 Media Loader, adapted for the image model and kept as a separate nodepack so it can be installed alongside the original.

## Features

- Drag-and-drop or file-picker loading for up to 16 images
- Crop, mirror, rotate, resize, and enable/disable per slot
- Live previews and reorderable slots
- Single `references` output on the loader (no cluttered node)
- Separate splitter that expands the bundle into individual `picture_1` … `picture_16` IMAGE outputs
- Preset save/load for media sets

## Nodes

| Node | Description |
|------|-------------|
| **Fantastic H3-Image Media Loader (16 refs)** | Loads and manages up to 16 reference images. Outputs a single `references` bundle. |
| **Fantastic H3-Image Reference Splitter** | Splits the bundle into individual `picture_1` … `picture_16` IMAGE slots for use with MiniMax H3 Image Conditioning. |

## Installation

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YOUR_USERNAME/ComfyUI-H3Image-MediaLoader.git
```

Restart ComfyUI. The nodes appear under the image models / conditioning category.

**Requirements:** ComfyUI with native MiniMax-H3-Image support, and PyAV (already required by ComfyUI).

## Usage

1. Add **Fantastic H3-Image Media Loader** to the graph.
2. Load images by dragging them onto the panel or using the file picker. Reorder, crop, rotate, or disable slots as needed.
3. Click **+ Image splitter** (or add the splitter node manually) and connect the loader’s `references` output to the splitter.
4. Connect the splitter’s `picture_1` … `picture_16` outputs to **MiniMax H3 Image Conditioning**.
5. Reference the images in the prompt as `Picture 1`, `Picture 2`, and so on.

`Picture 1` is conventionally the image being edited; the remaining slots are references (style, identity, products, etc.).

## Notes

- This pack is image-focused. The official H3-Image model does not support video references.
- It is designed to coexist with the original Fantastic H3 nodepack. Routes and the frontend extension are namespaced to avoid conflicts.
- Panel layout and slot sizing are tuned for a 4×4 grid of square previews.

## Credits

Quality-of-life features, media handling, and the frontend panel are adapted from [Adudeguyman/ComfyUI-Fantastic-MiniMaxH3-PromptBuilder](https://github.com/Adudeguyman/ComfyUI-Fantastic-MiniMaxH3-PromptBuilder) (MIT). This repository is a separate derivative focused on the H3-Image model.

## License

MIT
