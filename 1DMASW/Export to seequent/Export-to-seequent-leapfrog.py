import pandas as pd

# Exemple d’export CSV pour Leapfrog
df = pd.DataFrame(seismic_model_data)
df.to_csv(exportleapfrog_input.csv, index=False)
