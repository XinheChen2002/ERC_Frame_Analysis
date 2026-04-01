from src.typology_ml import run_typology_ml
from src.bar_chart import run_bar_chart
from src.sankey_plot import run_sankey

def main():
    predicted_path = run_typology_ml(
        input_file="data/raw/update_0223.xlsx",
        output_file="data/interim/predicted_typology.csv"
    )

    run_bar_chart(
        input_file=predicted_path,
        output_file="data/output/bar_chart_2024.svg"
    )

    run_sankey(
        input_file=predicted_path,
        output_file="data/output/sankey_2021.html"
    )

if __name__ == "__main__":
    main()
