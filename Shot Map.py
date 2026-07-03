from statsbombpy import sb
import matplotlib.pyplot as plt
from mplsoccer import Pitch

events = sb.events(match_id=3857291)
shots = events[events['type'] == 'Shot'].copy()

shots['x'] = shots['location'].apply(lambda loc: loc[0])
shots['y'] = shots['location'].apply(lambda loc: loc[1])

pitch = Pitch(pitch_type='statsbomb', pitch_color='#0a1628',
              line_color='#4a6080')
fig, ax = pitch.draw(figsize=(12, 8))
fig.patch.set_facecolor('#0a1628')

for _, shot in shots.iterrows():
    x = shot['x']
    y = shot['y']
    xg = shot['shot_statsbomb_xg']
    outcome = shot['shot_outcome']
    player = shot['player']

    color = '#AA151B' if outcome == 'Goal' else 'none'
    edge = '#FFD700' if outcome == 'Goal' else '#AAAAAA'
    zorder = 3 if outcome == 'Goal' else 2
    size = max(xg * 1500, 50)

    ax.scatter(x, y, s=size, c=color, edgecolors=edge,
               linewidths=1.5, zorder=zorder, alpha=0.85)

    if outcome == 'Goal':
        last_name = player.split()[-1]
        ax.annotate(last_name, (x, y),
                    textcoords='offset points', xytext=(0, 10),
                    ha='center', fontsize=7, color='#FFD700',
                    fontweight='bold')

ax.set_title('Spain vs Costa Rica — Shot Map\n2022 FIFA World Cup | 7-0',
             color='white', fontsize=14, fontweight='bold', pad=15)

legend_elements = [
    plt.scatter([], [], s=200, c='#AA151B', edgecolors='#FFD700',
                linewidths=1.5, label='Goal'),
    plt.scatter([], [], s=200, c='none', edgecolors='#AAAAAA',
                linewidths=1.5, label='No Goal'),
    plt.scatter([], [], s=50, c='white', label='Low xG'),
    plt.scatter([], [], s=400, c='white', label='High xG'),
]
ax.legend(handles=legend_elements, loc='lower left',
          facecolor='#1a2040', labelcolor='white',
          fontsize=8, framealpha=0.8)

ax.text(0.5, -0.02,
        'Data: StatsBomb | Built with Python, mplsoccer & matplotlib',
        transform=ax.transAxes, ha='center', fontsize=7, color='#445566')

plt.tight_layout()
plt.savefig('spain_shot_map_wc2022.png', dpi=150,
            facecolor='#0a1628', bbox_inches='tight')
plt.show()
print("Shot map saved.")