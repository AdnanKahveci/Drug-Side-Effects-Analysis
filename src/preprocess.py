import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
import os

# Veriyi yükle
data_path = os.path.join('data', 'side_effect_data.xlsx')
veriler = pd.read_excel(data_path)

# Genel bilgi ve eksik değer kontrolü
print("Genel Bilgi ve Eksik Değer Kontrolü:")
print(veriler.info())
print(veriler.isnull().sum())

# Eksik değerleri doldur
veriler['Cinsiyet'].fillna('Unknown', inplace=True)
veriler['Kan Grubu'].fillna(veriler['Kan Grubu'].mode()[0], inplace=True)
veriler['Kilo'].fillna(veriler['Kilo'].mean(), inplace=True)
veriler['Boy'].fillna(veriler['Boy'].mean(), inplace=True)

# Tarih sütunlarını işle
veriler['Ilac_Baslangic_Yil'] = veriler['Ilac_Baslangic_Tarihi'].dt.year
veriler['Ilac_Baslangic_Ay'] = veriler['Ilac_Baslangic_Tarihi'].dt.month
veriler['Ilac_Baslangic_Gun'] = veriler['Ilac_Baslangic_Tarihi'].dt.day

veriler['Ilac_Bitis_Yil'] = veriler['Ilac_Bitis_Tarihi'].dt.year
veriler['Ilac_Bitis_Ay'] = veriler['Ilac_Bitis_Tarihi'].dt.month
veriler['Ilac_Bitis_Gun'] = veriler['Ilac_Bitis_Tarihi'].dt.day

# Kategorik ve sayısal sütunları ayır
kategorik_sutunlar = veriler.select_dtypes(include=['object']).columns
sayisal_sutunlar = veriler.select_dtypes(include=['float64', 'int64']).columns

print("\nKategorik Sütunlar:", kategorik_sutunlar)
print("Sayısal Sütunlar:", sayisal_sutunlar)

# Kategorik verilerin kodlanması
encoder = OneHotEncoder(sparse=False, drop='first')
encoded_cols = pd.DataFrame(encoder.fit_transform(veriler[['Cinsiyet', 'Kan Grubu']]), columns=encoder.get_feature_names_out())
veriler = pd.concat([veriler, encoded_cols], axis=1)
veriler.drop(['Cinsiyet', 'Kan Grubu'], axis=1, inplace=True)

# Sayısal verilerin standartlaştırılması
scaler = StandardScaler()
veriler[['Kilo', 'Boy']] = scaler.fit_transform(veriler[['Kilo', 'Boy']])

# Veriyi yeniden kontrol et
print("\nTemizlenmiş Verinin İlk 5 Satırı:")
print(veriler.head())

# Temizlenmiş veriyi kaydet
processed_data_path = os.path.join('results', 'processed_data.csv')
veriler.to_csv(processed_data_path, index=False)

print(f"\nData preprocessing completed. Cleaned data saved to {processed_data_path}")
