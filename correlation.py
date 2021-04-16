#Mesurer la corrélation des cours de cloture
'''Nous calculons la corrélation de Pearson entre les cours de clôture de BCH, ETH, LTC, BTC, XMR, ETC et USD. La corrélation de Pearson est une mesure de la corrélation linéaire
entre deux variables X et Y. Elle a une valeur comprise entre +1 et −1, où 1 est la corrélation linéaire positive totale, 0 est aucune corrélation linéaire et −1 est la linéaire négative totale corrélation. 
La matrice de corrélation est symétrique, nous ne montrons donc que la moitié inférieure.
Sifr Data met à jour quotidiennement les corrélations Pearson pour de nombreuses crypto-monnaies.'''


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# Compute the correlation matrix
corr = df.corr()
# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(10, 10))
# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, annot=True, fmt = '.4f', mask=mask, center=0, square=True, linewidths=.5)
