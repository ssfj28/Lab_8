"""Анимация сортировки вставками: выбранный элемент опускается вниз красным."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from insertion_sort import insertion_sort


DEFAULT_ARRAY = [3, 44, 38, 5, 47, 15, 36, 26, 27, 2, 46, 4, 19, 50, 48]
OUTPUT_FILE = Path(__file__).with_name("insertion_sort.gif")

# Цвета подобраны близко к приложенному примеру.
COLOR_UNSORTED = "#63BCE4"  # ещё не обработанные элементы
COLOR_SORTED = "#63BCE4"    # отсортированная часть — голубые столбцы
COLOR_KEY = "#E53935"       # выбранный элемент (key), опущенный вниз
COLOR_COMPARE = "#F5A623"   # элемент, с которым сравнивается key
COLOR_SHIFTED = "#8BC7E8"   # элемент после сдвига вправо
BACKGROUND = "#F8FAFC"


def read_array() -> list[int]:
    """Читает числа из консоли или берёт исходный пример задания."""
    print("СОРТИРОВКА ВСТАВКАМИ")
    print("Введите целые числа через пробел.")
    print("Нажмите Enter, чтобы использовать пример из задания.\n")
    raw = input("Массив: ").strip()

    if not raw:
        return DEFAULT_ARRAY.copy()

    try:
        values = [int(item) for item in raw.split()]
    except ValueError as error:
        raise ValueError("Вводите только целые числа, разделённые пробелами.") from error

    if not values:
        raise ValueError("Массив должен содержать хотя бы одно число.")

    return values


def create_animation(numbers: list[int]) -> list[int]:
    """Создаёт минималистичную GIF-анимацию сортировки вставками."""
    steps: list[dict] = []
    sorted_array = insertion_sort(numbers, on_step=steps.append)

    figure, axis = plt.subplots(figsize=(13, 7))
    figure.patch.set_facecolor(BACKGROUND)
    axis.set_facecolor(BACKGROUND)

    min_value = min(min(numbers), 0)
    max_value = max(max(numbers), 0)
    value_range = max(max_value - min_value, abs(max_value), 1)
    key_drop = value_range * 0.24
    lower_limit = min_value - key_drop * 1.65
    upper_limit = max_value + value_range * 0.17
    label_offset = value_range * 0.025

    def draw_frame(frame_number: int):
        axis.clear()
        axis.set_facecolor(BACKGROUND)
        step = steps[frame_number]
        values = step["array"]
        sorted_count = step["sorted_count"]
        step_type = step["type"]

        # Показываем элементы, которые в данный момент находятся в массиве.
        visible_positions = [i for i, value in enumerate(values) if value is not None]
        visible_values = [values[i] for i in visible_positions]
        colors = [
            COLOR_SORTED if index < sorted_count else COLOR_UNSORTED
            for index in visible_positions
        ]

        # Небольшое цветовое выделение элемента, с которым идёт сравнение,
        # или элемента, который был сдвинут вправо.
        if step_type == "compare" and step["compare_index"] is not None:
            if step["compare_index"] in visible_positions:
                colors[visible_positions.index(step["compare_index"])] = COLOR_COMPARE
        elif step_type == "shift" and step["shifted_index"] is not None:
            if step["shifted_index"] in visible_positions:
                colors[visible_positions.index(step["shifted_index"])] = COLOR_SHIFTED

        bars = axis.bar(
            visible_positions,
            visible_values,
            color=colors,
            width=0.78,
            edgecolor="white",
            linewidth=0.8,
            zorder=3,
        )

        # Числовые значения остаются над столбцами — без подписей осей и шкал.
        for bar, value in zip(bars, visible_values):
            if value >= 0:
                text_y = value + label_offset
                vertical_alignment = "bottom"
            else:
                text_y = value - label_offset
                vertical_alignment = "top"
            axis.text(
                bar.get_x() + bar.get_width() / 2,
                text_y,
                str(value),
                ha="center",
                va=vertical_alignment,
                fontsize=10,
                color="#14202B",
                zorder=5,
            )

        # Выбранный элемент показывается отдельным красным столбцом ниже массива.
        # По мере сдвига больших элементов вправо красный столбец перемещается
        # к освободившейся позиции. На нём оставляем только числовое значение.
        key = step["key"]
        key_position = step["key_position"]
        if key is not None and key_position is not None:
            axis.bar(
                key_position,
                -key_drop,
                bottom=0,
                width=0.78,
                color=COLOR_KEY,
                edgecolor="white",
                linewidth=0.8,
                zorder=4,
            )
            axis.text(
                key_position,
                -key_drop - label_offset * 0.45,
                str(key),
                ha="center",
                va="top",
                fontsize=10,
                fontweight="bold",
                color=COLOR_KEY,
                zorder=6,
            )

        # После вставки выделяем размещённый элемент красным.
        if step_type == "insert" and key is not None:
            inserted_index = step["inserted_index"]
            if inserted_index is not None:
                axis.bar(
                    inserted_index,
                    key,
                    color=COLOR_KEY,
                    width=0.78,
                    edgecolor="white",
                    linewidth=0.8,
                    zorder=4,
                )
                axis.text(
                    inserted_index,
                    key + label_offset,
                    str(key),
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontweight="bold",
                    color=COLOR_KEY,
                    zorder=6,
                )

        # Оставляем только одну тонкую базовую линию, чтобы столбцы
        # визуально стояли на общей поверхности. Шкалы, сетки и подписи скрыты.
        axis.axhline(0, color="#D5DDE5", linewidth=0.9, zorder=2)
        axis.set_xlim(-0.65, len(numbers) - 0.35)
        axis.set_ylim(lower_limit, upper_limit)
        axis.set_xticks([])
        axis.set_yticks([])
        axis.grid(False)
        for spine in axis.spines.values():
            spine.set_visible(False)

        axis.set_title(
            "Сортировка вставками",
            fontsize=17,
            fontweight="bold",
            color="#203040",
            pad=18,
        )
        figure.subplots_adjust(left=0.035, right=0.985, top=0.88, bottom=0.08)
        return []

    animation = FuncAnimation(
        figure,
        draw_frame,
        frames=len(steps),
        interval=350,
        repeat=False,
        blit=False,
    )
    animation.save(OUTPUT_FILE, writer=PillowWriter(fps=4), dpi=90)

    print("\nИсходный массив:       ", numbers)
    print("Отсортированный массив:", sorted_array)
    print(f"Количество кадров: {len(steps)}")
    print(f"GIF сохранён: {OUTPUT_FILE}")

    plt.show()
    plt.close(figure)
    return sorted_array


def main() -> None:
    try:
        create_animation(read_array())
    except ValueError as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
