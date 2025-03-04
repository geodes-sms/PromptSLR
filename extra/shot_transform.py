import pandas as pd

original_path = "~/Code/relis_analysis/icse2024/data/04-clean_datasets/mobilemde.csv"
result_path = "~/Code/relis_analysis/icse2024/results/gpt_turbo_p1/mobilemde_result.csv"
store_path = "data/mobilemde_golden.csv"

df_original = pd.read_csv(
    original_path, sep="\t", na_values=[None], keep_default_na=False
)

df_result = pd.read_csv(
    result_path, sep="\t", na_values=[None], keep_default_na=False, header=None
)

print("Original DF Shape", df_original.shape)
print("Result DF Shape", df_result.shape)

merged_df = df_original.merge(df_result, left_on="key", right_on=1)
merged_df["is_shot"] = merged_df[10].apply(lambda x: x in ["FN", "FP"])
merged_df = merged_df.drop(columns=df_result.columns.tolist())

print("Merged DF Shape", merged_df.shape)

merged_df.to_csv(store_path, sep="\t", index=False)
