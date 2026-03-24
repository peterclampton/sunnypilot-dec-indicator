# sunnypilot DEC & Traffic Mode HUD Indicators

Adds small on-screen icons to the sunnypilot MICI HUD so you can tell at a glance when **Experimental Mode** or **Traffic Personality** is active.

![sunnypilot](https://img.shields.io/badge/sunnypilot-MICI_UI-blue)
![comma](https://img.shields.io/badge/comma-Comma_3%2F3X%2F4-green)

## What It Does

### 🔬 Experimental Mode Indicator
- Displays a small **atom icon** (28×28) in the top-right corner of the HUD
- Triggers when:
  - `selfdriveState.experimentalMode` is `True` (manual toggle via long-press gap button), **or**
  - DEC (Dynamic Experimental Control) switches to **blended** mode (`longitudinalPlanSP.dec.state == blended`)
- Uses the existing `icons_mici/experimental_mode.png` asset — no new images needed

### 🚦 Traffic Personality Indicator
- Displays a **traffic icon** in amber below the experimental mode icon
- Shows when the driving personality is set to **Traffic** (personality raw value `3`)
- Uses the existing `icons_mici/traffic_mode.png` asset

## Requirements

- **sunnypilot** with MICI UI layout (current default)
- **Comma 3, 3X, or 4** hardware
- DEC indicator uses `longitudinalPlanSP.dec` — requires sunnypilot builds with DEC support

## Installation

1. **SSH into your comma:**
   ```bash
   ssh comma@<your-comma-ip>
   ```

2. **Back up the original file:**
   ```bash
   cp /data/openpilot/selfdrive/ui/sunnypilot/mici/onroad/hud_renderer.py \
      /data/openpilot/selfdrive/ui/sunnypilot/mici/onroad/hud_renderer.py.bak
   ```

3. **Copy the modified file:**
   ```bash
   # From your computer:
   scp hud_renderer.py comma@<your-comma-ip>:/data/openpilot/selfdrive/ui/sunnypilot/mici/onroad/hud_renderer.py
   ```

4. **Recompile the bytecache** (critical — Python won't pick up changes without this):
   ```bash
   ssh comma@<your-comma-ip>
   cd /data/openpilot
   python3 -c "
   import py_compile
   src = 'selfdrive/ui/sunnypilot/mici/onroad/hud_renderer.py'
   pyc = 'selfdrive/ui/sunnypilot/mici/onroad/__pycache__/hud_renderer.cpython-312.pyc'
   py_compile.compile(src, pyc, doraise=True)
   print('Bytecache compiled successfully')
   "
   ```
   > ⚠️ Adjust `cpython-312` to match your Python version if different.

5. **Reboot** the comma (or restart the UI process).

## How It Works

The file extends sunnypilot's `HudRenderer` class (MICI layout) via `HudRendererSP`. The two indicator methods hook into the existing `_render()` pipeline:

- **`_draw_dec_indicator()`** — checks experimental mode state from `selfdriveState` and DEC blended state from `longitudinalPlanSP.dec`
- **`_draw_traffic_indicator()`** — checks driving personality from `selfdriveState.personality`

Both use existing icon textures already bundled with sunnypilot. No additional assets required.

## Notes

- **Survives reboots** but NOT sunnypilot updates (updates replace `/data/openpilot/`). Re-apply after updating.
- The icons are small and unobtrusive — won't block your driving view.
- All rendering errors are silently caught to avoid crashing the UI.
- Tested on **Comma 4 + 2017 Lexus RX350 (TSS-P)** with Smart DSU.

## License

MIT — same as sunnypilot.
