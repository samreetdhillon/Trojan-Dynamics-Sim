import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# --- Constants ---
RADIUS_JUPITER = 7.0
NUM_ASTEROIDS = 12
TRAIL_LENGTH = 60
FPS = 30
ORBIT_DURATION = 30  # Seconds for one full Jupiter loop
TOTAL_FRAMES = ORBIT_DURATION * FPS
OUTPUT_FILE = 'trojan_tadpole_horseshoe.mp4'

# --- Physics Tweaks ---
LIB_AMP_ANG = np.radians(12) # How wide the tadpole is
LIB_AMP_RAD = 0.35           # How thick the tadpole is
LIB_FREQ = 0.05              # Speed of the "dance"

# --- Setup Figure ---
fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')
ax.set_facecolor('black')
ax.axis('off')

# Elements
sun = plt.Circle((0, 0), 0.6, color='#FFD700', zorder=5)
ax.add_patch(sun)

# Jupiter
jupiter_dot, = ax.plot([], [], 'o', color='Orange', markersize=14, zorder=10)
jupiter_positions = deque(maxlen=TRAIL_LENGTH)
jupiter_trail, = ax.plot([], [], '-', color='Orange', linewidth=1, alpha=0.5)

# Asteroid Setup
asteroid_dots = []
asteroid_trails = []
asteroid_data = [] # Stores (base_angle, radius, phase, is_horseshoe)
asteroid_positions = [deque(maxlen=TRAIL_LENGTH) for _ in range(NUM_ASTEROIDS + 1)]

# Create Tadpole Asteroids
for i in range(NUM_ASTEROIDS):
    base = 60 if i < NUM_ASTEROIDS // 2 else -60
    angle_offset = np.random.uniform(-10, 10)
    radius_offset = np.random.uniform(-0.2, 0.2)
    phase = np.random.uniform(0, 2 * np.pi)
    
    dot, = ax.plot([], [], 'o', color='lime', markersize=3, alpha=0.8)
    trail, = ax.plot([], [], '-', color='lime', linewidth=0.5, alpha=0.3)
    
    asteroid_dots.append(dot)
    asteroid_trails.append(trail)
    asteroid_data.append((np.radians(base + angle_offset), RADIUS_JUPITER + radius_offset, phase, False))

# Create ONE Horseshoe Asteroid
hs_dot, = ax.plot([], [], 'o', color='cyan', markersize=4, label="Horseshoe")
hs_trail, = ax.plot([], [], '-', color='cyan', linewidth=0.8, alpha=0.4)
asteroid_dots.append(hs_dot)
asteroid_trails.append(hs_trail)
# Horseshoe: starts near L3 (180 deg), much wider oscillation
asteroid_data.append((np.pi, RADIUS_JUPITER, 0, True))

# Labels
camp_labels = ['Greek Camp (L4)', 'Trojan Camp (L5)']
camp_angles = [60, -60]
camp_texts = [ax.text(0, 0, txt, color='white', ha='center', fontsize=9, alpha=0.7) for txt in camp_labels]

def update(frame):
    # System Rotation
    angle_j = 2 * np.pi * (frame / TOTAL_FRAMES)
    
    # 1. Jupiter Position
    xj, yj = RADIUS_JUPITER * np.cos(angle_j), RADIUS_JUPITER * np.sin(angle_j)
    jupiter_dot.set_data([xj], [yj])
    jupiter_positions.append((xj, yj))
    jupiter_trail.set_data(*zip(*jupiter_positions))

    # 2. Asteroids
    for i, (angle0, r0, phase, is_hs) in enumerate(asteroid_data):
        if not is_hs:
            # Tadpole Math
            a_osc = LIB_AMP_ANG * np.sin(frame * LIB_FREQ + phase)
            r_osc = LIB_AMP_RAD * np.cos(frame * LIB_FREQ + phase)
        else:
            # Horseshoe Math (Huge angular swing, small radial dip)
            a_osc = np.radians(140) * np.sin(frame * (LIB_FREQ * 0.4))
            r_osc = 0.2 * np.cos(frame * (LIB_FREQ * 0.4))

        curr_a = angle_j + angle0 + a_osc
        curr_r = r0 + r_osc
        
        xa, ya = curr_r * np.cos(curr_a), curr_r * np.sin(curr_a)
        asteroid_dots[i].set_data([xa], [ya])
        asteroid_positions[i].append((xa, ya))
        asteroid_trails[i].set_data(*zip(*asteroid_positions[i]))

    # 3. Labels
    for text, b_angle in zip(camp_texts, camp_angles):
        la = angle_j + np.radians(b_angle)
        text.set_position(((RADIUS_JUPITER + 1.5) * np.cos(la), (RADIUS_JUPITER + 1.5) * np.sin(la)))

    return [jupiter_dot, jupiter_trail] + asteroid_dots + asteroid_trails + camp_texts

ani = animation.FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=1000/FPS, blit=True)

# Save logic
try:
    writer = animation.FFMpegWriter(fps=FPS, bitrate=2000)
    ani.save(OUTPUT_FILE, writer=writer)
    print(f"Success! Saved as {OUTPUT_FILE}")
except Exception as e:
    print(f"Error saving: {e}. Showing plot instead...")
    plt.show()