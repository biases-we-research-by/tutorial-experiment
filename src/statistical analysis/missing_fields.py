import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os


def run_wikidata_analysis(
        data_folder='/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Data/cleaned_data'):
    path_pattern = os.path.join(data_folder, "**", "*.csv")
    files = glob.glob(path_pattern, recursive=True)

    if not files:
        print(f"No CSV files found in {data_folder}")
        return

    print(f"Files found: {len(files)}")
    df_list = []
    for f in files:
        temp_df = pd.read_csv(f)
        temp_df['category'] = os.path.basename(f).replace('.csv', '')
        df_list.append(temp_df)

    df = pd.concat(df_list, ignore_index=True)

    # 2. Define attribute columns
    exclude = ['qid', 'label', 'pareto_claims', 'pareto_ext', 'total_claims', 'external_ids', 'citizenship_label',
               'birth_country_label', 'birth_hdi', 'birth_unm49', 'edu_country', 'type', 'educated_at_label',
               'edu_country_label', 'edu_hdi', 'edu_nm49', 'edu_mobility', 'category', 'generation']
    attribute_cols = [c for c in df.columns if c not in exclude]

    # Calculate missing percentages
    missing_pct = df.groupby('pareto_claims')[attribute_cols].apply(lambda x: x.isnull().mean() * 100)

    # Rename variables for the plot to be clean and in English
    rename_mapping = {
        'gender': 'Gender',
        'citizenship': 'Citizenship',
        'birth_country': 'Birth country',
        'educated_at': 'Education',
        'date_of_birth': 'Date of birth'
    }
    missing_pct = missing_pct.rename(columns=rename_mapping)

    # Calculate total missing fields per entity
    df['total_missing'] = df[attribute_cols].isnull().sum(axis=1)

    # Aggregate descriptive statistics
    stats_summary = df.groupby('pareto_claims')['total_missing'].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).rename(columns={'count': 'Entities_Count', 'mean': 'Missing_Mean', 'median': 'Missing_Median'})


    sns.set_theme(style="ticks", context="paper", font_scale=1.2)

    plt.figure(figsize=(12, 6))
    plot_data = missing_pct.stack().reset_index()
    plot_data.columns = ['Group', 'Attribute', 'Missing_Percentage']

    ax = sns.barplot(
        data=plot_data,
        x='Attribute',
        y='Missing_Percentage',
        hue='Group',
        palette='Set2',
        edgecolor=".2",
        linewidth=1.5
    )

    plt.title('Percentage of Missing Fields per Variable', fontsize=16, pad=15, fontweight='bold')
    plt.xticks(rotation=30, ha='right', fontsize=11)
    plt.ylabel('% Missing Fields', fontsize=12, fontweight='bold')
    plt.xlabel('')

    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=3, size=10)

    sns.despine(trim=True)  # Removes top and right borders for a clean look
    plt.legend(title='Pareto Claims', title_fontsize='11', fontsize='10', frameon=False)
    plt.tight_layout()
    plt.savefig('/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Results/missing_per_attribute.png',
                dpi=300)

    # --- Plot 2: Boxenplot (Advanced Boxplot) for missing fields ---
    plt.figure(figsize=(8, 6))

    # ---------------------------------------------------------
    # 6. Save results
    # ---------------------------------------------------------
    stats_summary.to_csv(
        '/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Results/missing_stats_comparison.csv')
    missing_pct.T.to_csv(
        '/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Results/missing_columns_detail.csv')

    print("\n--- Analysis Completed ---")
    print("\nStatistical Summary (Missing Fields):")
    print(stats_summary)
    print(
        "\nThe plots 'missing_per_attribute.png' and 'missing_distribution.png' have been saved in high resolution (300 dpi).")


# Execution
if __name__ == "__main__":
    run_wikidata_analysis()