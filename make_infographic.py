"""Build the project infographic (infographic.png and infographic.pdf).

Takeaway: the genres audiences rate highest are not the ones that make the most money.
Run:  python make_infographic.py
"""
import textwrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd

# ------------------------------------------------------------------ style
SURFACE, INK, INK2, MUTED = '#fcfcfb', '#0b0b0b', '#52514e', '#898781'
GRID, AXIS, GRAY_MARK = '#e1e0d9', '#c3c2b7', '#c9c8c1'
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'   # validated categorical slots 1-3

available = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in ['Helvetica Neue', 'Helvetica', 'Arial'] if f in available), 'DejaVu Sans')
plt.rcParams.update({'font.family': [FONT, 'DejaVu Sans'], 'text.color': INK, 'axes.labelcolor': INK2,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.edgecolor': AXIS})

# ------------------------------------------------------------------ data
movies = pd.read_csv('tmdb-movies.csv').drop_duplicates()
for col in ['budget_adj', 'revenue_adj']:
    movies[col] = movies[col].replace(0, np.nan).where(lambda s: s >= 1e4)
movies['profit'] = movies['revenue_adj'] - movies['budget_adj']

genres = (movies.dropna(subset=['genres'])
          .assign(genre=lambda d: d['genres'].str.split('|'))
          .explode('genre'))
genres = genres[genres['genre'] != 'TV Movie']

g = genres.dropna(subset=['profit']).groupby('genre').agg(profit=('profit', 'median'), n=('id', 'count'))
g['rating'] = genres[genres['vote_count'] >= 50].groupby('genre')['vote_average'].mean()
g = g[g['n'] >= 30].dropna()
g['rank_rating'] = g['rating'].rank(ascending=False, method='first').astype(int)
g['rank_profit'] = g['profit'].rank(ascending=False, method='first').astype(int)
g['shift'] = g['rank_rating'] - g['rank_profit']          # + means it earns better than it rates
N_GENRES = len(g)

films = movies.dropna(subset=['revenue_adj']).copy()
films['log_rev'] = np.log10(films['revenue_adj'])
r = films['vote_average'].corr(films['log_rev'])
slope, intercept = np.polyfit(films['vote_average'], films['log_rev'], 1)

def film(title):
    return films.loc[films['original_title'] == title].iloc[0]

shawshank, spiderman = film('The Shawshank Redemption'), film('Spider-Man 3')
times = spiderman['revenue_adj'] / shawshank['revenue_adj']
doc = g.loc['Documentary']

def money(x):
    if x >= 1e9:
        return f'${x / 1e9:.1f}B'
    return f'${x / 1e6:.0f}M'

# ------------------------------------------------------------------ canvas
# Layout is written in inches from the top of the page so sections can be moved independently.
W, H = 11, 18.4
fig = plt.figure(figsize=(W, H), facecolor=SURFACE)
L, R = 0.07, 0.93                     # page margins (figure fraction)

def Y(inches):
    return 1 - inches / H

def text(x, y_in, s, size, width=None, **kw):
    if width:
        s = '\n'.join(textwrap.fill(p, width, break_on_hyphens=False) for p in s.split('\n'))
    return fig.text(x, Y(y_in), s, fontsize=size, va='top', **kw)

def rule(y_in, x0=L, x1=R):
    fig.add_artist(plt.Line2D([x0, x1], [Y(y_in)] * 2, color=GRID, lw=1, transform=fig.transFigure))

def axes_at(x, top_in, w, height_in):
    return fig.add_axes([x, Y(top_in + height_in), w, height_in / H])

# ---- header
text(L, 0.48, 'TMDb MOVIES  ·  10,865 FILMS  ·  1960–2015', 11, color=MUTED, fontweight='bold')
text(L, 0.77, "The movies audiences love most\naren’t the ones that make the most money",
     31, fontweight='bold', linespacing=1.1)
text(L, 1.96,
     'We compared audience ratings with inflation-adjusted profit across 18 genres. The best-rated '
     'genres are among the least profitable. The biggest earners sit in the middle or bottom of the '
     'ratings, with one exception.',
     13.5, width=88, color=INK2, linespacing=1.4)

# ---- stat tiles
rule(2.86)
tiles = [
    ('1st → last', f'Documentaries are the best-rated genre (avg {doc["rating"]:.1f}/10) '
                   f'and the least profitable ({money(doc["profit"])} median profit)'),
    (f'{times:.0f}×', f'Spider-Man 3 (rated {spiderman["vote_average"]:.1f}) earned {times:.0f} times as much as '
                      f'The Shawshank Redemption (rated {shawshank["vote_average"]:.1f})'),
    (f'{r * r * 100:.0f}%', 'of the difference in box office between films is explained by their rating'),
]
tile_w = (R - L) / 3
for i, (big, small) in enumerate(tiles):
    x = L + i * tile_w
    text(x, 3.03, big, 40, fontweight='bold')
    text(x, 3.67, small, 11.5, width=34, color=INK2, linespacing=1.35)
    if i:
        fig.add_artist(plt.Line2D([x - 0.015] * 2, [Y(4.39), Y(3.03)], color=GRID, lw=1,
                                  transform=fig.transFigure))
rule(4.56)

# ---- chart 1: rank slope chart
text(L, 4.83, 'Rated highest ≠ earns most', 19, fontweight='bold')
text(L, 5.14, 'Each line follows one genre from its rank by average audience rating (left) '
              'to its rank by median profit per film (right). Genres that move 9 or more places are '
              'highlighted.', 12, width=105, color=INK2, linespacing=1.35)

def classify(row):
    if row.name == 'Animation':
        return AQUA
    if row['shift'] <= -9:
        return BLUE
    if row['shift'] >= 9:
        return ORANGE
    return ''
g['color'] = g.apply(classify, axis=1)

# legend row (marks beside ink-colored text)
legend = [(BLUE, 'Rated much higher than it earns'),
          (ORANGE, 'Earns much more than it is rated'),
          (AQUA, 'Animation: top 4 on both')]
for (c, label), x in zip(legend, [L, L + 0.30, L + 0.60]):
    fig.add_artist(plt.Line2D([x, x + 0.028], [Y(5.80)] * 2, color=c, lw=3, solid_capstyle='round',
                              transform=fig.transFigure))
    text(x + 0.036, 5.71, label, 11, color=INK2)

ax = axes_at(L, 6.39, R - L, 4.45)
ax.set_facecolor(SURFACE)
ax.set_xlim(-0.95, 1.95)
ax.set_ylim(N_GENRES + 0.6, 0.4)
ax.axis('off')

for name, row in sorted(g.iterrows(), key=lambda kv: kv[1]['color'] != ''):
    c = row['color']
    y0, y1 = row['rank_rating'], row['rank_profit']
    ax.plot([0, 1], [y0, y1], color=c or GRAY_MARK, lw=3 if c else 1.4, solid_capstyle='round',
            zorder=3 if c else 1)
    for x, y in [(0, y0), (1, y1)]:
        ax.scatter(x, y, s=70 if c else 28, color=c or GRAY_MARK, edgecolor=SURFACE, linewidth=2,
                   zorder=4 if c else 2)

for name, row in g.iterrows():
    hl = row['color'] != ''
    style = dict(fontsize=12 if hl else 11, color=INK if hl else INK2,
                 fontweight='bold' if hl else 'normal', va='center')
    ax.text(-0.05, row['rank_rating'], f'{row["rating"]:.1f}', ha='right', **style)
    ax.text(-0.22, row['rank_rating'], name, ha='right', **style)
    ax.text(1.05, row['rank_profit'], money(row['profit']), ha='left', **style)
    ax.text(1.27, row['rank_profit'], name, ha='left', **style)

for k in range(1, N_GENRES + 1):
    ax.text(-0.93, k, str(k), ha='left', va='center', fontsize=9.5, color=MUTED)
    ax.text(1.93, k, str(k), ha='right', va='center', fontsize=9.5, color=MUTED)

head_style = dict(va='bottom', fontsize=10, color=MUTED, fontweight='bold')
ax.text(-0.05, -0.15, 'AVG RATING (0–10)', ha='right', **head_style)
ax.text(1.05, -0.15, 'MEDIAN PROFIT', ha='left', **head_style)
ax.text(-0.93, -0.15, 'RANK', ha='left', **head_style)
ax.text(1.93, -0.15, 'RANK', ha='right', **head_style)

# ---- chart 2: film-level scatter
rule(11.17)
text(L, 11.42, 'Film by film, a rating says little about the box office', 19, fontweight='bold')
text(L, 11.73, f'Each dot is one of {len(films):,} films with reported revenue. Better-rated films earn '
               f'slightly more on average (the line), but the spread swamps the trend.',
     12, width=105, color=INK2, linespacing=1.35)

ax2 = axes_at(L + 0.07, 12.45, R - L - 0.07, 3.0)
ax2.set_facecolor(SURFACE)
ax2.scatter(films['vote_average'], films['revenue_adj'], s=8, color=GRAY_MARK, alpha=0.55,
            linewidth=0, zorder=1)
xs = np.linspace(2, 8.6, 50)
ax2.plot(xs, 10 ** (slope * xs + intercept), color=INK2, lw=2, zorder=2)
ax2.set_yscale('log')
ax2.set_ylim(3e4, 1e10)
ax2.set_xlim(1.8, 10.9)
ax2.set_yticks([1e5, 1e6, 1e7, 1e8, 1e9, 1e10], ['$100K', '$1M', '$10M', '$100M', '$1B', '$10B'])
ax2.set_xticks(range(2, 11))
ax2.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
ax2.set_xlabel('Average audience rating (0–10)', fontsize=11)
ax2.set_ylabel('Revenue (2010 $)', fontsize=11)
ax2.tick_params(length=0, labelsize=10)
ax2.grid(axis='y', color=GRID, lw=0.8)
ax2.set_axisbelow(True)
for side in ['top', 'right', 'left']:
    ax2.spines[side].set_visible(False)

callouts = [  # title, color, label position (rating, revenue)
    ('Spider-Man 3', ORANGE, (3.0, 3.5e9)),
    ('The Smurfs', ORANGE, (3.0, 1.3e8)),
    ('The Shawshank Redemption', BLUE, (8.85, 1.5e8)),
    ('Whiplash', BLUE, (8.85, 2.5e6)),
]
for title, c, (lx_, ly_) in callouts:
    f = film(title)
    ax2.scatter(f['vote_average'], f['revenue_adj'], s=80, color=c, edgecolor=SURFACE, linewidth=2, zorder=4)
    ax2.annotate(f'{title}\n{f["vote_average"]:.1f} rating · {money(f["revenue_adj"])}',
                 xy=(f['vote_average'], f['revenue_adj']), xytext=(lx_, ly_), ha='left', va='center',
                 fontsize=10.5, color=INK, linespacing=1.3,
                 arrowprops=dict(arrowstyle='-', color=MUTED, lw=1, shrinkA=4, shrinkB=6))
ax2.text(2.05, 10 ** (slope * 2.05 + intercept) * 2.2, 'average trend', fontsize=9.5, color=INK2,
         va='bottom', ha='left')

# ---- closing takeaway
rule(16.2)
text(L, 16.38, 'So what?', 13, fontweight='bold')
text(L + 0.105, 16.38,
     'Acclaim and profit reward different kinds of films. The most dependable money comes from broad, '
     'family-friendly spectacle (animation, adventure, fantasy, action), while the films audiences rate '
     'highest are often modest earners. Animation is the one genre near the top of both lists.',
     12, width=100, color=INK2, linespacing=1.4)

# ---- footer
rule(17.3)
text(L, 17.45,
     'Data: TMDb movie dataset, 10,865 films released 1960–2015. Money is inflation-adjusted to 2010 dollars; '
     f'profit = revenue − budget, for the {movies["profit"].notna().sum():,} films that report both. '
     'Ratings are TMDb user averages; genre averages use films with 50+ votes. '
     'Genres need 30+ films with profit data, and a film counts toward every genre it is tagged with. '
     'These are associations, not causes.',
     9.5, width=150, color=MUTED, linespacing=1.4)

fig.savefig('infographic.png', dpi=200, facecolor=SURFACE)
fig.savefig('infographic.pdf', facecolor=SURFACE)
print('saved infographic.png and infographic.pdf | font:', FONT, '| r =', round(r, 3))
