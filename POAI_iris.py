import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.linear_model import LinearRegression

def load_and_analyze_iris(file_path):
    df = pd.read_csv(file_path)
    le = LabelEncoder()
    df['Species'] = le.fit_transform(df['Species'])
    
    print(f"No. of data points: {len(df)}")
    print(f'Column Datatypes:\n{df.dtypes}')
    print(f"Column names: {df.columns.tolist()}")
    print(f"Total number of species of flower: {df['Species'].nunique()}")
    return df

def correct_iris_errors(df):
    df.loc[34] = [4.9, 3.1, 1.5, 0.2, 0]
    df.loc[37] = [4.9, 3.6, 1.4, 0.1, 0]
    print("\nCorrected Rows:")
    print(df.iloc[[34, 37]])
    return df

def add_features_and_save(df, output_file):
    df['PetalRatio'] = df['Petal.Length'] / df['Petal.Width']
    df['SepalRatio'] = df['Sepal.Length'] / df['Sepal.Width']
    df.to_csv(output_file, index=False)
    print(f"\nNew features added. Data written to '{output_file}'.")

def calculate_correlations(df):
    numeric_df = df.select_dtypes(include=[np.number])
    correlations = numeric_df.corr()
    corr_unstacked = correlations.unstack().sort_values(ascending=False)
    highest_positive = corr_unstacked[corr_unstacked < 1].nlargest(10).idxmax()
    highest_negative = corr_unstacked.nsmallest(10).idxmin()
    print("\nPairwise Correlations :")
    print(correlations)
    print(f"\nMax positive correlation: {highest_positive} = {corr_unstacked[highest_positive]}")
    print(f"Maximum Negative Correlation: {highest_negative} = {corr_unstacked[highest_negative]}")

def scatter_with_regression(df, output_file):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="SepalRatio", y="PetalRatio", hue="Species", palette="Set2")
    for species in df['Species'].unique():
        species_data = df[df.Species == species]
        X = species_data[['SepalRatio']].values.reshape(-1, 1)
        y = species_data['PetalRatio'].values
        reg = LinearRegression().fit(X, y)
        plt.plot(X, reg.predict(X))
    plt.legend()
    plt.title("Sepal Ratio vs Petal Ratio with Regression Line")
    plt.savefig(output_file)
    plt.close()
    print(f"\nScatter plot saved in '{output_file}'.")

def create_pair_plot(df):
    sns.pairplot(df, hue="Species", vars=["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"])
    plt.suptitle('Pair Plot of Iris Dataset', y=1.02)
    plt.show()

def main():
    iris_file = "iris.csv"
    corrected_file = "iris_corrected.csv"
    scatter_plot_file = "iris_scatter_with_regression.pdf"
    
    df = load_and_analyze_iris(iris_file)
    df = correct_iris_errors(df)
    add_features_and_save(df, corrected_file)
    calculate_correlations(df)
    scatter_with_regression(df, scatter_plot_file)
    create_pair_plot(df)

if __name__ == "__main__":
    main()
