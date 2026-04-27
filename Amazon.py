
 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
 
# ── Style global ────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0f1117',
    'axes.facecolor':   '#1a1d2e',
    'axes.edgecolor':   '#2e3250',
    'axes.labelcolor':  '#c9d1f0',
    'xtick.color':      '#8891b5',
    'ytick.color':      '#8891b5',
    'text.color':       '#c9d1f0',
    'grid.color':       '#2e3250',
    'grid.linestyle':   '--',
    'grid.alpha':       0.5,
    'font.family':      'DejaVu Sans',
})
PALETTE = ['#4f8ef7', '#f76f4f', '#4fdb9a', '#f7c44f', '#c44ff7',
           '#4ff7e8', '#f74f7e', '#a4f74f', '#f7a44f', '#4f6af7']
#import de la dataset
df = pd.read_csv('amazon.csv')
print("  ÉTAPE 1 — Exploration initiale")
print(f"taille : {df.shape}")
print("\nTypes de colonnes :")
print(df.dtypes)
print("\nValeurs manquantes :")
print(df.isnull().sum())
print("\nAperçu :")
print(df.head(3))
print(" \n ÉTAPE 2 — Nettoyage")
df = df.drop_duplicates()
 
def clean_price(series):
    """Retire ₹, virgules et espaces, convertit en float."""
    return (
        series.astype(str)
              .str.replace(r'[₹,\s]', '', regex=True)
              .replace('nan', np.nan)
              .astype(float)
    )
 
def clean_pct(series):
    """Retire le % et convertit en float."""
    return (
        series.astype(str)
              .str.replace('%', '', regex=False)
              .replace('nan', np.nan)
              .astype(float)
    )
 
def clean_count(series):
    """Retire les virgules du rating_count et convertit en float."""
    return (
        series.astype(str)
              .str.replace(',', '', regex=False)
              .replace('nan', np.nan)
              .astype(float)
    )

df['discounted_price']   = clean_price(df['discounted_price'])
df['actual_price']       = clean_price(df['actual_price'])
df['discount_percentage']= clean_pct(df['discount_percentage'])
df['rating']             = pd.to_numeric(df['rating'], errors='coerce')
df['rating_count']       = clean_count(df['rating_count'])
df['main_category'] = df['category'].astype(str).str.split('|').str[0].str.strip()
df['saving']= df['actual_price'] - df['discounted_price']
df['saving_pct_calc']= (df['saving'] / df['actual_price'].replace(0, np.nan) * 100).round(1)
df['popularity_score'] = (
    df['rating'] * np.log1p(df['rating_count'].fillna(0))
).round(2)
df_clean = df.dropna(subset=['discounted_price', 'actual_price']).copy()
df_clean = df.dropna(subset=['discounted_price', 'actual_price']).copy()
 
print(f"Lignes après nettoyage : {len(df_clean)}")
print(f"Catégories principales : {df_clean['main_category'].nunique()}")
print(df_clean[['discounted_price','actual_price','rating','rating_count']].describe().round(2))

print("  ÉTAPE 3 — CA / Produits par catégorie")

ca_cat = (
    df_clean
    .groupby('main_category')
    .agg(
        nb_produits       = ('product_id', 'nunique'),
        prix_moyen_reduit = ('discounted_price', 'mean'),
        prix_moyen_reel   = ('actual_price', 'mean'),
        remise_moy_pct    = ('discount_percentage', 'mean'),
        note_moy          = ('rating', 'mean'),
        avis_total        = ('rating_count', 'sum'),
        popularite_moy    = ('popularity_score', 'mean'),
    )
    .sort_values('nb_produits', ascending=False)
    .reset_index()
)
ca_cat['prix_moyen_reduit'] = ca_cat['prix_moyen_reduit'].round(2)
ca_cat['prix_moyen_reel']   = ca_cat['prix_moyen_reel'].round(2)
ca_cat['remise_moy_pct']    = ca_cat['remise_moy_pct'].round(1)
ca_cat['note_moy']          = ca_cat['note_moy'].round(2)
ca_cat['pct_produits']      = (ca_cat['nb_produits'] / ca_cat['nb_produits'].sum() * 100).round(1)
 
ca_cat.to_csv('resultats_categories.csv', index=False)
print(ca_cat.head(10).to_string())




top10 = (
    df_clean
    .groupby('product_name')
    .agg(
        prix_remise     = ('discounted_price', 'mean'),
        prix_reel       = ('actual_price', 'mean'),
        remise_pct      = ('discount_percentage', 'mean'),
        note_moy        = ('rating', 'mean'),
        nb_avis         = ('rating_count', 'sum'),
        score_pop       = ('popularity_score', 'mean'),
        main_category   = ('main_category', 'first'),
    )
    .sort_values('score_pop', ascending=False)
    .head(10)
    .round(2)
    .reset_index()
)
 
top10.to_csv('top10_produits.csv', index=False)
print(top10[['product_name','note_moy','nb_avis','score_pop','main_category']].to_string())
 
 
# ════════════════════════════════════════════════════════════
# GRAPHIQUE 1 — Répartition des produits par catégorie (bar h)
# ════════════════════════════════════════════════════════════
 
top_n = ca_cat.head(12)
fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#1a1d2e')
 
bars = ax.barh(
    top_n['main_category'][::-1],
    top_n['nb_produits'][::-1],
    color=PALETTE[:len(top_n)],
    edgecolor='none',
    height=0.65
)
for bar, val in zip(bars, top_n['nb_produits'][::-1]):
    ax.text(val + 2, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', fontsize=9, color='#c9d1f0')
 
ax.set_xlabel('Nombre de produits', fontsize=11, labelpad=8)
ax.set_title('📦  Répartition des produits par catégorie principale',
             fontsize=14, fontweight='bold', pad=15, color='#e8ecff')
ax.xaxis.grid(True, alpha=0.3)
ax.set_axisbelow(True)
ax.spines[:].set_visible(False)
plt.tight_layout()
plt.savefig('graphique_categories.png', dpi=150, bbox_inches='tight',
            facecolor='#0f1117')
plt.show()
print("✅  graphique_categories.png sauvegardé")
 
 
# ════════════════════════════════════════════════════════════
# GRAPHIQUE 2 — Distribution des notes & remises (double violin)
# ════════════════════════════════════════════════════════════
 
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('#0f1117')
fig.suptitle('📊  Distribution : Notes & Remises', fontsize=15,
             fontweight='bold', color='#e8ecff', y=1.01)
 
# --- Panel gauche : notes par catégorie top 6 ---
top6_cats = ca_cat.head(6)['main_category'].tolist()
df_top6 = df_clean[df_clean['main_category'].isin(top6_cats)].dropna(subset=['rating'])
 
ax = axes[0]
ax.set_facecolor('#1a1d2e')
for i, cat in enumerate(top6_cats):
    data = df_top6[df_top6['main_category'] == cat]['rating']
    parts = ax.violinplot(data, positions=[i], widths=0.6,
                          showmedians=True, showextrema=False)
    for pc in parts['bodies']:
        pc.set_facecolor(PALETTE[i])
        pc.set_alpha(0.75)
    parts['cmedians'].set_color('#ffffff')
    parts['cmedians'].set_linewidth(2)
 
ax.set_xticks(range(len(top6_cats)))
ax.set_xticklabels([c[:15] for c in top6_cats], rotation=30, ha='right', fontsize=8)
ax.set_ylabel('Note (/5)', fontsize=10)
ax.set_title('Notes par catégorie (top 6)', fontsize=11, color='#c9d1f0')
ax.spines[:].set_visible(False)
ax.yaxis.grid(True, alpha=0.3); ax.set_axisbelow(True)
 
# --- Panel droit : distribution remises ---
ax2 = axes[1]
ax2.set_facecolor('#1a1d2e')
disc = df_clean['discount_percentage'].dropna()
ax2.hist(disc, bins=30, color='#4f8ef7', edgecolor='#0f1117', alpha=0.85)
ax2.axvline(disc.mean(), color='#f76f4f', linewidth=2,
            label=f'Moyenne : {disc.mean():.1f}%')
ax2.axvline(disc.median(), color='#4fdb9a', linewidth=2, linestyle='--',
            label=f'Médiane : {disc.median():.1f}%')
ax2.set_xlabel('Remise (%)', fontsize=10)
ax2.set_ylabel('Nombre de produits', fontsize=10)
ax2.set_title('Distribution des remises', fontsize=11, color='#c9d1f0')
ax2.legend(fontsize=9, framealpha=0.3)
ax2.spines[:].set_visible(False)
ax2.yaxis.grid(True, alpha=0.3); ax2.set_axisbelow(True)
 
plt.tight_layout()
plt.savefig('graphique_notes_remises.png', dpi=150, bbox_inches='tight',
            facecolor='#0f1117')
plt.show()
print("✅  graphique_notes_remises.png sauvegardé")
 
 
# ════════════════════════════════════════════════════════════
# GRAPHIQUE 3 — Top 10 produits (score popularité)
# ════════════════════════════════════════════════════════════
 
fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#1a1d2e')
 
labels = [name[:40] + '…' if len(name) > 40 else name
          for name in top10['product_name']]
colors = [PALETTE[i % len(PALETTE)] for i in range(len(top10))]
 
bars = ax.barh(labels[::-1], top10['score_pop'][::-1],
               color=colors[::-1], edgecolor='none', height=0.6)
 
for bar, score, note, avis in zip(
        bars, top10['score_pop'][::-1],
        top10['note_moy'][::-1], top10['nb_avis'][::-1]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f'⭐ {note:.1f}  |  {int(avis):,} avis',
            va='center', fontsize=8.5, color='#8891b5')
 
ax.set_xlabel('Score de popularité  (note × log(nb avis))', fontsize=10, labelpad=8)
ax.set_title('🏆  Top 10 produits les plus populaires',
             fontsize=14, fontweight='bold', pad=15, color='#e8ecff')
ax.xaxis.grid(True, alpha=0.3); ax.set_axisbelow(True)
ax.spines[:].set_visible(False)
plt.tight_layout()
plt.savefig('graphique_top10.png', dpi=150, bbox_inches='tight',
            facecolor='#0f1117')
plt.show()
print("✅  graphique_top10.png sauvegardé")
 
 
# ════════════════════════════════════════════════════════════
# RÉCAP FINAL
# ════════════════════════════════════════════════════════════
 
print("\n" + "=" * 55)
print("  INSIGHTS BUSINESS CLÉS")
print("=" * 55)
print(f"📦 Produits analysés        : {len(df_clean):,}")
print(f"🗂️  Catégories principales   : {df_clean['main_category'].nunique()}")
print(f"⭐ Note moyenne globale     : {df_clean['rating'].mean():.2f} / 5")
print(f"💸 Remise moyenne           : {df_clean['discount_percentage'].mean():.1f}%")
print(f"💰 Prix moyen remisé        : ₹{df_clean['discounted_price'].mean():.0f}")
print(f"🔝 Catégorie #1 (produits)  : {ca_cat.iloc[0]['main_category']} "
      f"({ca_cat.iloc[0]['nb_produits']} produits)")
print(f"🏆 Produit le + populaire   : {top10.iloc[0]['product_name'][:50]}")
print("\nFichiers générés :")
print("  • resultats_categories.csv")
print("  • top10_produits.csv")
print("  • graphique_categories.png")
print("  • graphique_notes_remises.png")
print("  • graphique_top10.png")