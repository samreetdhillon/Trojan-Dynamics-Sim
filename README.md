# Trojan Asteroids Animation 🔭

A compact script to animate Jupiter and Trojan asteroids (tadpole and horseshoe orbits) using Matplotlib.

## Quick start

1. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate # macOS / Linux
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the animation:

   ```bash
   python trojan.py
   ```

By default the script tries to save an MP4 named `trojan_tadpole_horseshoe.mp4` in the project folder. If saving fails it will display the plot instead.

## Note on ffmpeg

Matplotlib's `FFMpegWriter` requires `ffmpeg` on your PATH. The `imageio-ffmpeg` package included in `requirements.txt` can provide a bundled ffmpeg if you don't want to install it system-wide.

## Tuning

Edit constants at the top of `trojan.py` to change behavior (e.g., `RADIUS_JUPITER`, `NUM_ASTEROIDS`, `FPS`, `OUTPUT_FILE`).
