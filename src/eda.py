import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Veriyi yükle
data_path = os.path.join('data', 'side_effect_data.xlsx')
veriler = pd.read_excel(data_path)

# Genel bilgi ve eksik değer kontrolü
print(veriler.info())
print(veriler.isnull().sum())

# Sayısal verilerin histogramı
veriler[['Kilo', 'Boy']].hist(bins=20, figsize=(10, 5))
plt.savefig(os.path.join('results', 'histograms.png'))

# Cinsiyet ve kilo kutu grafiği
plt.figure(figsize=(8, 6))
sns.boxplot(x='Cinsiyet', y='Kilo', data=veriler)
plt.savefig(os.path.join('results', 'boxplot_kilo_cinsiyet.png'))

#Kategorik Verilerin Dağılımı
plt.figure(figsize=(8, 6))
veriler['Cinsiyet'].value_counts().plot(kind='bar')
plt.title('Cinsiyet Dağılımı')
plt.savefig(os.path.join('results', 'barplot_cinsiyet.png'))

#Eksik Verilerin Analizi
plt.figure(figsize=(10, 6))
sns.heatmap(veriler.isnull(), cbar=False, cmap='viridis')
plt.title('Eksik Veri Görselleştirmesi')
plt.savefig(os.path.join('results', 'heatmap_missing_values.png'))

#İlaç ve Yan Etki Analizi
ilac_yan_etki = veriler.groupby('Ilac_Adi')['Yan_Etki'].value_counts().unstack().fillna(0)
ilac_yan_etki.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('İlaçlara Göre Yan Etkiler')
plt.savefig(os.path.join('results', 'barplot_ilac_yan_etki.png'))

#Kronik Hastalıklar Analizi
hastalik_verisi = veriler[['Kronik Hastaliklarim', 'Baba Kronik Hastaliklari', 'Anne Kronik Hastaliklari']].copy()
hastalik_verisi.fillna('Yok', inplace=True)
sns.heatmap(hastalik_verisi.apply(lambda x: x.str.contains('Yok').astype(int)), cbar=False, cmap='coolwarm')
plt.title('Kronik Hastalıklar Analizi')
plt.savefig(os.path.join('results', 'heatmap_kronik_hastaliklar.png'))

# Korelasyon matrisi
plt.figure(figsize=(8, 6))
sns.heatmap(veriler[['Kilo', 'Boy']].corr(), annot=True, cmap='coolwarm')
plt.savefig(os.path.join('results', 'heatmap_correlation.png'))

print("EDA completed. Check the 'results' folder for output plots.")
