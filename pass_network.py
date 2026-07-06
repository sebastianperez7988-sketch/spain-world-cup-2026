from statsbombpy import sb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from mplsoccer import Pitch
import numpy as np

events = sb.events(match_id=3857291)

# Completed Spain passes only
passes = events[
    (events['type'] == 'Pass') &
    (events['team'] == 'Spain') &
    (events['pass_outcome'].isna())
].copy()

# Extract coordinates
passes['x'] = passes['location'].apply(lambda l: l[0])
passes['y'] = passes['location'].apply(lambda l: l[1])
passes['end_x'] = passes['pass_end_location'].apply(lambda l: l[0])
passes['end_y'] = passes['pass_end_location'].apply(lambda l: l[1])

# Get starting 11 only (before first sub)
lineup = sb.lineups(match_id=3857291)['Spain']
starting_11 = lineup[lineup['jersey_number'] <= 11]['player_name'].tolist()

# Get substitution times to filter to starting XI passes
subs = events[
    (events['type'] == 'Substitution') &
    (events['team'] == 'Spain')
]

first_sub_minute = subs['minute'].min() if len(subs) > 0 else 90
passes_first = passes[passes['minute'] < first_sub_minute].copy()

# Average position per player
avg_pos = passes_first.groupby('player').agg(
    avg_x=('x', 'mean'),
    avg_y=('y', 'mean')
).reset_index()

# Count passes between pairs
pass_pairs = passes_first.groupby(
    ['player', 'pass_recipient']
).size().reset_index(name='count')

# Filter to players in avg_pos
players_with_pos = avg_pos['player'].tolist()
pass_pairs = pass_pairs[
    (pass_pairs['player'].isin(players_with_pos)) &
    (pass_pairs['pass_recipient'].isin(players_with_pos))
]

# Min passes threshold for drawing lines
min_passes = 5

# ── Draw ───────────────────────────────────────────────────────
pitch = Pitch(pitch_type='statsbomb', pitch_color='#0a1628',
              line_color='#4a6080')
fig, ax = pitch.draw(figsize=(14, 10))
fig.patch.set_facecolor('#0a1628')

# Draw pass lines
max_count = pass_pairs['count'].max()
for _, row in pass_pairs.iterrows():
    if row['count'] < min_passes:
        continue

    p1 = avg_pos[avg_pos['player'] == row['player']]
    p2 = avg_pos[avg_pos['player'] == row['pass_recipient']]

    if p1.empty or p2.empty:
        continue

    x1, y1 = p1['avg_x'].values[0], p1['avg_y'].values[0]
    x2, y2 = p2['avg_x'].values[0], p2['avg_y'].values[0]

    width = (row['count'] / max_count) * 8
    alpha = 0.3 + (row['count'] / max_count) * 0.5

    ax.plot([x1, x2], [y1, y2],
            color='#4a8fc4', linewidth=width,
            alpha=alpha, zorder=2, solid_capstyle='round')

# Draw player nodes
total_passes = passes_first.groupby('player').size().reset_index(name='total')
avg_pos = avg_pos.merge(total_passes, on='player', how='left')

max_total = avg_pos['total'].max()
for _, row in avg_pos.iterrows():
    size = 100 + (row['total'] / max_total) * 600
    color = '#AA151B' if row['total'] == max_total else '#ffffff'

    ax.scatter(row['avg_x'], row['avg_y'],
               s=size, c=color, edgecolors='#FFD700',
               linewidths=1.5, zorder=4)

    # Shorten name to last name
    last_name = row['player'].split()[-1]
    ax.annotate(last_name, (row['avg_x'], row['avg_y']),
                textcoords='offset points', xytext=(0, 12),
                ha='center', fontsize=7, color='white',
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2',
                          facecolor='#0a1628', edgecolor='none', alpha=0.7))

ax.set_title('Spain vs Costa Rica — Pass Network\n2022 FIFA World Cup | First Half Starting XI',
             color='white', fontsize=13, fontweight='bold', pad=15)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='#AA151B', edgecolor='#FFD700', label='Most passes'),
    mpatches.Patch(facecolor='white', edgecolor='#FFD700', label='Player node'),
    mpatches.Patch(facecolor='#4a8fc4', label='Pass connection'),
]
ax.legend(handles=legend_elements, loc='lower left',
          facecolor='#1a2040', labelcolor='white',
          fontsize=8, framealpha=0.8)

ax.text(0.5, -0.02,
        'Data: StatsBomb | Built with Python, mplsoccer & matplotlib',
        transform=ax.transAxes, ha='center', fontsize=7, color='#445566')

plt.tight_layout()
plt.savefig('spain_pass_network_wc2022.png', dpi=150,
            facecolor='#0a1628', bbox_inches='tight')
plt.show()
print("Pass network saved.")