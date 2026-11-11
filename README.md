# ComfyUI-H3Image-MediaLoader

Isolated extension nodepack for the **official MiniMax-H3-Image** model (released 2026-11-10).

H3-Image supports up to **16 reference images** (addressed as `Picture 1` … `Picture 16` in the prompt).  
This pack provides a high-quality Media Loader that carries over all the QoL features from [Adudeguyman's Fantastic H3 Media Loader](https://github.com/Adudeguyman/ComfyUI-Fantastic-MiniMaxH3-PromptBuilder) while keeping the code completely separate.

## Nodes

| Node | Purpose |
|------|---------|
| **Fantastic H3-Image Media Loader (16 refs)** | Drag-and-drop / file-picker loader for up to 16 images. Supports crop, mirror, rotate, resize, enable/disable, previews. Outputs a single `references` bundle (clean node — no 16 outputs cluttering the graph). |
| **Fantastic H3-Image Reference Splitter** | Fans the bundle out into individual `picture_1` … `picture_16` IMAGE slots for wiring into MiniMax H3 Image Conditioning. |

## Why a separate pack?

- Isolates our changes from the original video-focused nodepack.
- Tailored for the image model (no unnecessary video/audio complexity unless you later enable it).
- Official H3-Image is image-only; video references are not supported by the model.

## Install

1. Delete any previous copy of this pack from `ComfyUI/custom_nodes/`.
2. Extract the tar.gz so you end up with `ComfyUI/custom_nodes/ComfyUI-H3Image-MediaLoader/`.
3. Fully quit ComfyUI, then start it again.
4. In the browser, hard-refresh (Ctrl+Shift+R) so the old `medialoader.js` is not cached.

After that the Media Loader node should show only the `references` output plus the panel buttons ("Open loader…" and "+ Image splitter"). The 16 individual image slots live on the Splitter node.

## Usage

1. Add the **Fantastic H3-Image Media Loader** node.
2. Drag images onto it (or use the file picker). Reorder, crop, rotate, etc. as needed.
3. Click **+ Image splitter** (or add the splitter node manually) and wire the loader's `references` output to it.
4. Wire the splitter's `picture_1` … `picture_16` outputs into **MiniMax H3 Image Conditioning**.
5. Refer to them in your prompt as `Picture 1`, `Picture 2`, …

`Picture 1` is conventionally the image you are editing; the rest are references (products, style, identity, etc.).

## Video support

The official H3-Image model does not document video reference support (unlike the original H3 video model).  
This loader is image-focused. If you drop a video, the frontend may still accept it for frame extraction experiments, but it is not wired as a native video reference.

## Credits

QoL features, media decoding, and frontend panel adapted from  
[Adudeguyman/ComfyUI-Fantastic-MiniMaxH3-PromptBuilder](https://github.com/Adudeguyman/ComfyUI-Fantastic-MiniMaxH3-PromptBuilder)  
(MIT license). This pack is a separate derivative focused on the image model.
"# ComfyUI-H3Image-MediaLoader" 
