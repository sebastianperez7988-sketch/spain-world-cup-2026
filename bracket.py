import requests
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

API_KEY = "705a3bbaa05643979f0ea5ea3baf5dc2"
headers = {"X-Auth-Token": API_KEY}

url = "https://api.football-data.org/v4/competitions/WC/matches"
response = requests.get(url, headers=headers)
data = response.json()

CODES = {
    'Spain': 'ESP', 'Portugal': 'POR', 'France': 'FRA', 'Germany': 'GER',
    'Brazil': 'BRA', 'Argentina': 'ARG', 'England': 'ENG', 'Netherlands': 'NED',
    'Morocco': 'MAR', 'Japan': 'JPN', 'United States': 'USA', 'Mexico': 'MEX',
    'Canada': 'CAN', 'Belgium': 'BEL', 'Croatia': 'CRO', 'Switzerland': 'SUI',
    'Norway': 'NOR', 'Australia': 'AUS', 'Colombia': 'COL', 'Uruguay': 'URU',
    'South Africa': 'RSA', 'Senegal': 'SEN', 'Algeria': 'ALG', 'Ecuador': 'ECU',
    'Paraguay': 'PAR', 'Costa Rica': 'CRC', 'Panama': 'PAN', 'Egypt': 'EGY',
    'Ghana': 'GHA', 'Cape Verde Islands': 'CPV', 'Bosnia-Herzegovina': 'BIH',
    'Austria': 'AUT', 'Sweden': 'SWE', 'Congo DR': 'COD', 'Ivory Coast': 'CIV',
    'Saudi Arabia': 'KSA',
}

def get_stage(stage_key):
    matches = [m for m in data['matches'] if m['stage'] == stage_key]
    result = []
    for m in matches:
        home = m['homeTeam']['name'] or 'TBD'
        away = m['awayTeam']['name'] or 'TBD'
        status = m['status']
        if status == 'FINISHED':
            hs = m['score']['fullTime']['home']
            as_ = m['score']['fullTime']['away']
            winner = home if hs > as_ else (away if as_ > hs else None)
        else:
            hs = as_ = None
            winner = None
        result.append({
            'home': home, 'away': away,
            'status': status,
            'home_score': hs, 'away_score': as_,
            'winner': winner,
            'date': m['utcDate'][5:10]
        })
    return result

def pad(lst, n):
    while len(lst) < n:
        lst.append({'home': 'TBD', 'away': 'TBD', 'status': 'SCHEDULED',
                    'home_score': None, 'away_score': None,
                    'winner': None, 'date': ''})
    return lst

r32 = pad(get_stage('LAST_32'), 16)
r16 = pad(get_stage('LAST_16'), 8)
qf_all = pad(get_stage('QUARTER_FINALS'), 4)
sf  = pad(get_stage('SEMI_FINALS'), 2)
fi  = pad(get_stage('FINAL'), 1)

# Fix QF left/right ordering
# Left QF: indices 0 and 2 (France/Morocco, Norway/England)
# Right QF: indices 1 and 3 (Spain/TBD, TBD/TBD)
qf_left  = [qf_all[0], qf_all[2]]
qf_right = [qf_all[1], qf_all[3]]

fig, ax = plt.subplots(figsize=(34, 24))
ax.set_xlim(0, 32)
ax.set_ylim(4, 22)
ax.axis('off')
fig.patch.set_facecolor('#060d1a')
ax.set_facecolor('#060d1a')

ax.text(16, 21.3, '2026 FIFA WORLD CUP', ha='center', va='center',
        fontsize=18, fontweight='bold', color='#FFD700', fontfamily='monospace')
ax.text(16, 20.7, 'TOURNAMENT BRACKET', ha='center', va='center',
        fontsize=11, color='#8899aa', fontfamily='monospace')
ax.plot([4, 28], [20.4, 20.4], color='#FFD700', linewidth=0.5, alpha=0.4)

BOX_W = 3.6
BOX_H = 0.85

def get_code(name):
    return CODES.get(name, name[:3].upper())

def draw_box(ax, match, x, y, highlight='Spain'):
    home = match['home'] or 'TBD'
    away = match['away'] or 'TBD'
    status = match['status']
    winner = match['winner']
    is_tbd = home == 'TBD' and away == 'TBD'

    if is_tbd:
        bg, border = '#0a1525', '#1a2a3a'
    elif status == 'FINISHED':
        bg, border = '#0f1e33', '#1e3a5a'
    elif status == 'IN_PROGRESS':
        bg, border = '#0a2010', '#00cc44'
    else:
        bg, border = '#0d1830', '#1a2d4a'

    rect = FancyBboxPatch((x, y), BOX_W, BOX_H,
                          boxstyle="round,pad=0.06",
                          facecolor=bg, edgecolor=border,
                          linewidth=1.0, zorder=2)
    ax.add_patch(rect)

    ax.plot([x + 0.1, x + BOX_W - 0.1], [y + BOX_H/2, y + BOX_H/2],
            color=border, linewidth=0.4, alpha=0.5, zorder=3)

    if is_tbd:
        ax.text(x + BOX_W/2, y + BOX_H/2, 'TBD',
                ha='center', va='center', fontsize=7,
                color='#2a4a6a', zorder=3)
        return

    if status == 'FINISHED':
        hw = winner == home
        aw = winner == away

        if hw:
            bar = FancyBboxPatch((x, y + BOX_H/2), 0.06, BOX_H/2,
                                 boxstyle="round,pad=0.01",
                                 facecolor='#FFD700', edgecolor='none', zorder=3)
            ax.add_patch(bar)
        if aw:
            bar = FancyBboxPatch((x, y), 0.06, BOX_H/2,
                                 boxstyle="round,pad=0.01",
                                 facecolor='#FFD700', edgecolor='none', zorder=3)
            ax.add_patch(bar)

        hc = '#ffffff' if hw else '#556677'
        ac = '#ffffff' if aw else '#556677'
        if home == highlight: hc = '#AA151B'
        if away == highlight: ac = '#AA151B'

        code_bg_h = '#FFD700' if hw else '#1a2d4a'
        code_tc_h = '#000000' if hw else '#556677'
        code_rect_h = FancyBboxPatch((x + 0.08, y + BOX_H*0.55), 0.38, 0.24,
                                     boxstyle="round,pad=0.02",
                                     facecolor=code_bg_h, edgecolor='none', zorder=4)
        ax.add_patch(code_rect_h)
        ax.text(x + 0.27, y + BOX_H*0.67, get_code(home),
                fontsize=5.5, color=code_tc_h, va='center',
                ha='center', fontweight='bold', zorder=5)
        ax.text(x + 0.56, y + BOX_H*0.75, home[:13],
                fontsize=6.5, color=hc, va='center',
                fontweight='bold' if hw else 'normal', zorder=3)

        s_bg_h = '#FFD700' if hw else '#1a2d4a'
        s_tc_h = '#000000' if hw else '#778899'
        s_rect_h = FancyBboxPatch((x + BOX_W - 0.42, y + BOX_H*0.55), 0.32, 0.28,
                                  boxstyle="round,pad=0.02",
                                  facecolor=s_bg_h, edgecolor='none', zorder=4)
        ax.add_patch(s_rect_h)
        ax.text(x + BOX_W - 0.26, y + BOX_H*0.69, str(match['home_score']),
                fontsize=7, color=s_tc_h, va='center',
                ha='center', fontweight='bold', zorder=5)

        code_bg_a = '#FFD700' if aw else '#1a2d4a'
        code_tc_a = '#000000' if aw else '#556677'
        code_rect_a = FancyBboxPatch((x + 0.08, y + BOX_H*0.21), 0.38, 0.24,
                                     boxstyle="round,pad=0.02",
                                     facecolor=code_bg_a, edgecolor='none', zorder=4)
        ax.add_patch(code_rect_a)
        ax.text(x + 0.27, y + BOX_H*0.33, get_code(away),
                fontsize=5.5, color=code_tc_a, va='center',
                ha='center', fontweight='bold', zorder=5)
        ax.text(x + 0.56, y + BOX_H*0.25, away[:13],
                fontsize=6.5, color=ac, va='center',
                fontweight='bold' if aw else 'normal', zorder=3)

        s_bg_a = '#FFD700' if aw else '#1a2d4a'
        s_tc_a = '#000000' if aw else '#778899'
        s_rect_a = FancyBboxPatch((x + BOX_W - 0.42, y + BOX_H*0.18), 0.32, 0.28,
                                  boxstyle="round,pad=0.02",
                                  facecolor=s_bg_a, edgecolor='none', zorder=4)
        ax.add_patch(s_rect_a)
        ax.text(x + BOX_W - 0.26, y + BOX_H*0.32, str(match['away_score']),
                fontsize=7, color=s_tc_a, va='center',
                ha='center', fontweight='bold', zorder=5)

    elif status == 'IN_PROGRESS':
        ax.text(x + 0.18, y + BOX_H*0.75, home[:15],
                fontsize=6.5, color='#00FF88', va='center', zorder=3)
        ax.text(x + 0.18, y + BOX_H*0.25, away[:15],
                fontsize=6.5, color='#00FF88', va='center', zorder=3)
        ax.text(x + BOX_W - 0.15, y + BOX_H/2, 'LIVE',
                fontsize=6, color='#00FF88', va='center',
                ha='right', fontweight='bold', zorder=3)
    else:
        hc = '#AA151B' if home == highlight else '#aabbcc'
        ac = '#AA151B' if away == highlight else '#667788'

        code_bg = '#1a2d4a'
        code_rect_h = FancyBboxPatch((x + 0.08, y + BOX_H*0.55), 0.38, 0.24,
                                     boxstyle="round,pad=0.02",
                                     facecolor=code_bg, edgecolor='none', zorder=4)
        ax.add_patch(code_rect_h)
        ax.text(x + 0.27, y + BOX_H*0.67, get_code(home),
                fontsize=5.5, color='#556677', va='center',
                ha='center', fontweight='bold', zorder=5)
        ax.text(x + 0.56, y + BOX_H*0.75, home[:13],
                fontsize=6.5, color=hc, va='center',
                fontweight='bold' if home == highlight else 'normal', zorder=3)

        code_rect_a = FancyBboxPatch((x + 0.08, y + BOX_H*0.21), 0.38, 0.24,
                                     boxstyle="round,pad=0.02",
                                     facecolor=code_bg, edgecolor='none', zorder=4)
        ax.add_patch(code_rect_a)
        ax.text(x + 0.27, y + BOX_H*0.33, get_code(away),
                fontsize=5.5, color='#556677', va='center',
                ha='center', fontweight='bold', zorder=5)
        ax.text(x + 0.56, y + BOX_H*0.25, away[:13],
                fontsize=6.5, color=ac, va='center',
                fontweight='bold' if away == highlight else 'normal', zorder=3)

        if match['date']:
            ax.text(x + BOX_W - 0.1, y + BOX_H/2, match['date'],
                    fontsize=5.5, color='#334455', va='center',
                    ha='right', zorder=3)

def draw_line(ax, x1, y1, x2, y2, finished=False):
    color = '#2a4a6a' if not finished else '#3a6a9a'
    ax.plot([x1, x2], [y1, y2], color=color,
            linewidth=0.9, zorder=1, solid_capstyle='round')

def connect(ax, x_from, y_top, y_bot, x_to, y_mid, finished=False):
    mid_x = (x_from + x_to) / 2
    draw_line(ax, x_from, y_top, mid_x, y_top, finished)
    draw_line(ax, x_from, y_bot, mid_x, y_bot, finished)
    draw_line(ax, mid_x, y_top, mid_x, y_bot, finished)
    draw_line(ax, mid_x, y_mid, x_to, y_mid, finished)

r32_y = [19.0, 17.4, 15.5, 13.9, 11.6, 10.0, 8.1, 6.5]
r16_y = [18.0, 14.9, 10.9, 7.5]
qf_y  = [16.6, 9.3]
sf_y  = [12.95]
fi_y  = 10.8

x_r32_l = 0.2
x_r16_l = 4.4
x_qf_l  = 8.4
x_sf_l  = 10.6
x_fi    = 13.7
x_sf_r  = 17.6
x_qf_r  = 19.8
x_r16_r = 23.4
x_r32_r = 27.6

for i, m in enumerate(r32[:8]):
    draw_box(ax, m, x_r32_l, r32_y[i])
for i, m in enumerate(r32[8:]):
    draw_box(ax, m, x_r32_r, r32_y[i])
for i, m in enumerate(r16[:4]):
    draw_box(ax, m, x_r16_l, r16_y[i])
for i, m in enumerate(r16[4:]):
    draw_box(ax, m, x_r16_r, r16_y[i])
for i, m in enumerate(qf_left):
    draw_box(ax, m, x_qf_l, qf_y[i])
for i, m in enumerate(qf_right):
    draw_box(ax, m, x_qf_r, qf_y[i])
draw_box(ax, sf[0], x_sf_l, sf_y[0])
draw_box(ax, sf[1], x_sf_r, sf_y[0])
draw_box(ax, fi[0], x_fi, fi_y)

for i in range(4):
    f = r32[i*2]['status'] == 'FINISHED' and r32[i*2+1]['status'] == 'FINISHED'
    connect(ax, x_r32_l + BOX_W,
            r32_y[i*2] + BOX_H/2,
            r32_y[i*2+1] + BOX_H/2,
            x_r16_l, r16_y[i] + BOX_H/2, f)

for i in range(2):
    f = r16[i*2]['status'] == 'FINISHED' and r16[i*2+1]['status'] == 'FINISHED'
    connect(ax, x_r16_l + BOX_W,
            r16_y[i*2] + BOX_H/2,
            r16_y[i*2+1] + BOX_H/2,
            x_qf_l, qf_y[i] + BOX_H/2, f)

f = qf_left[0]['status'] == 'FINISHED' and qf_left[1]['status'] == 'FINISHED'
connect(ax, x_qf_l + BOX_W,
        qf_y[0] + BOX_H/2,
        qf_y[1] + BOX_H/2,
        x_sf_l, sf_y[0] + BOX_H/2, f)

fi_cx = x_fi + BOX_W/2
fi_my = fi_y + BOX_H/2
sf_my = sf_y[0] + BOX_H/2
draw_line(ax, x_sf_l + BOX_W, sf_my, fi_cx, sf_my)
draw_line(ax, fi_cx, sf_my, fi_cx, fi_my)
draw_line(ax, fi_cx, fi_my, x_fi, fi_my)

for i in range(4):
    f = r32[8+i*2]['status'] == 'FINISHED' and r32[8+i*2+1]['status'] == 'FINISHED'
    connect(ax, x_r32_r,
            r32_y[i*2] + BOX_H/2,
            r32_y[i*2+1] + BOX_H/2,
            x_r16_r + BOX_W, r16_y[i] + BOX_H/2, f)

for i in range(2):
    f = r16[4+i*2]['status'] == 'FINISHED' and r16[4+i*2+1]['status'] == 'FINISHED'
    connect(ax, x_r16_r,
            r16_y[i*2] + BOX_H/2,
            r16_y[i*2+1] + BOX_H/2,
            x_qf_r + BOX_W, qf_y[i] + BOX_H/2, f)

f = qf_right[0]['status'] == 'FINISHED' and qf_right[1]['status'] == 'FINISHED'
connect(ax, x_qf_r,
        qf_y[0] + BOX_H/2,
        qf_y[1] + BOX_H/2,
        x_sf_r + BOX_W, sf_y[0] + BOX_H/2, f)

draw_line(ax, x_sf_r, sf_my, fi_cx, sf_my)
draw_line(ax, fi_cx, sf_my, fi_cx, fi_my)
draw_line(ax, fi_cx, fi_my, x_fi + BOX_W, fi_my)

round_labels = [
    ('ROUND OF 32', x_r32_l), ('ROUND OF 16', x_r16_l),
    ('QUARTER\nFINAL', x_qf_l), ('SEMI\nFINAL', x_sf_l),
    ('FINAL', x_fi), ('SEMI\nFINAL', x_sf_r),
    ('QUARTER\nFINAL', x_qf_r), ('ROUND OF 16', x_r16_r),
    ('ROUND OF 32', x_r32_r),
]
for label, x in round_labels:
    ax.text(x + BOX_W/2, 20.2, label, ha='center',
            fontsize=5.5, color='#3a5a7a', fontweight='bold',
            linespacing=1.3)

ax.text(16, 4.2,
        'Data: football-data.org  |  Built with Python + Matplotlib  |  github.com/sebastianperez7988-sketch',
        ha='center', fontsize=6, color='#2a4a6a')

plt.tight_layout()
plt.savefig('bracket_full.png', dpi=150, facecolor='#060d1a',
            bbox_inches='tight')
plt.show()
print("Bracket saved.")