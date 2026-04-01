import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["svg.fonttype"] = "none"

df = pd.read_csv("long_format_data.csv")

year = 2024

categories = [
    "Time Dimension",
    "Scale",
    "Specialization",
    "Interdisciplinary",
    "Type"
]

colors = [
    "#F58111",
    "#FFA34A",
    "#FFC080",
    "#FFDCBD"
]

fig, ax = plt.subplots(figsize=(12, 5), dpi=300)

total_width = 10
bar_height = 0.6

for i, cat in enumerate(categories):

    data = df[(df.year == year) & (df.category == cat)]
    data = data.sort_values("percentage", ascending=False)

    start_x = 0
    y_pos = 4 - i

    for j, row in enumerate(data.itertuples()):

        total_percent = data["percentage"].sum()
        width = row.percentage / total_percent * total_width

        ax.barh(
            y=y_pos,
            width=width,
            left=start_x,
            height=bar_height,
            color=colors[j],
            edgecolor="none"
        )

        # if width > 1.2:   # ⭐ 关键阈值（可调）
        ax.text(
                    start_x + width/2,
                    y_pos,
                    f"{row.subcategory}\n{row.percentage}%",
                    ha="center",
                    va="center",
                    fontsize=9,
                    color="white"
                )

        start_x += width

ax.set_xlim(0, total_width)
ax.set_xticks([])
ax.set_yticks([])
ax.spines[:].set_visible(False)

plt.tight_layout()
plt.savefig("five_equal_bars.svg", transparent=True)
plt.show()
