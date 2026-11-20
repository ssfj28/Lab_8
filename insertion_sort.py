"""Реализация сортировки вставками с записью этапов для визуализации."""

from typing import Callable, Optional


StepCallback = Callable[[dict], None]


def insertion_sort(numbers: list[int], on_step: Optional[StepCallback] = None) -> list[int]:
    """Сортирует числа по возрастанию методом вставок.

    Если передан on_step, функция передаёт сведения о каждом действии
    алгоритма для последующего построения анимации.
    """
    array: list[Optional[int]] = list(numbers)
    n = len(array)

    def save_step(
        step_type: str,
        message: str,
        key: Optional[int] = None,
        key_position: Optional[int] = None,
        compare_index: Optional[int] = None,
        shifted_index: Optional[int] = None,
        sorted_count: int = 0,
        inserted_index: Optional[int] = None,
    ) -> None:
        if on_step is not None:
            on_step({
                "array": array.copy(),
                "type": step_type,
                "message": message,
                "key": key,
                "key_position": key_position,
                "compare_index": compare_index,
                "shifted_index": shifted_index,
                "sorted_count": sorted_count,
                "inserted_index": inserted_index,
            })

    if n == 0:
        save_step("done", "Массив пуст — сортировать нечего.")
        return []

    save_step("start", "Первый элемент считается отсортированным.", sorted_count=1)

    # Начинаем со второго элемента: первый уже образует отсортированную часть.
    for i in range(1, n):
        key = array[i]
        assert key is not None

        # Освобождаем ячейку: выбранный элемент временно находится «внизу».
        array[i] = None
        hole = i
        save_step(
            "select",
            f"Выбираем элемент {key}. Он временно вынесен из массива.",
            key=key,
            key_position=hole,
            sorted_count=i,
        )

        j = i - 1
        while j >= 0:
            current = array[j]
            assert current is not None
            save_step(
                "compare",
                f"Сравниваем {key} с {current}.",
                key=key,
                key_position=hole,
                compare_index=j,
                sorted_count=i,
            )

            if current > key:
                # Сдвигаем больший элемент на освободившуюся позицию справа.
                array[j + 1] = current
                array[j] = None
                hole = j
                save_step(
                    "shift",
                    f"{current} больше {key}: сдвигаем {current} на одну позицию вправо.",
                    key=key,
                    key_position=hole,
                    shifted_index=j + 1,
                    sorted_count=i,
                )
                j -= 1
            else:
                break

        # Вставляем выбранный элемент в освободившуюся ячейку.
        insert_position = j + 1
        array[insert_position] = key
        save_step(
            "insert",
            f"Вставляем {key} на позицию {insert_position + 1}.",
            key=key,
            sorted_count=i + 1,
            inserted_index=insert_position,
        )

    result = [value for value in array if value is not None]
    save_step("done", "Готово! Все элементы расположены по возрастанию.", sorted_count=n)
    return result


def main() -> None:
    """Запускает сортировку в консоли без графической визуализации."""
    raw = input("Введите целые числа через пробел: ").strip()

    try:
        numbers = [int(value) for value in raw.split()]
    except ValueError:
        print("Ошибка: необходимо вводить только целые числа.")
        return

    if not numbers:
        print("Массив пуст. Добавьте хотя бы одно число.")
        return

    print("Исходный массив:       ", numbers)
    print("Отсортированный массив:", insertion_sort(numbers))


if __name__ == "__main__":
    main()
