CONFIG_PATH="configs/algo_101.yaml"
declare -a optimizers=("RS" "FLS" "BLS" "SH" "REA" "REA+W")
declare -a zc_metrics=("synflow" "params" "flops")

for opt in "${optimizers[@]}"
do
    python main.py --ss nb101 --optimizer "$opt" --config_file "$CONFIG_PATH"
done
for metric in "${zc_metrics[@]}"
do
    python scripts/change_config_file.py --object MF-NAS --config_file "$CONFIG_PATH" --attribute metric_stage1 --new_value "$metric"
    python main.py --ss nb101 --optimizer MF-NAS --config_file "$CONFIG_PATH"
done
