import flet as ft

from permutationСiphers.blockPermutation import encrypt_block, decrypt_block
from permutationСiphers.routeRearrangement import encrypt_route, decrypt_route
from permutationСiphers.verticalPermutation import encrypt_vertical, decrypt_vertical

from baseFunctionForCryptography.baseFunction import (
    normalize_encrypt,
    normalize_decrypt,
    output_encrypt,
    output_decrypt,
)


"""
Графический интерфейс для работы с перестановочными шифрами:
- вертикальная перестановка;
- маршрутная перестановка;
- блочная перестановка.
Реализованы шифрование, расшифровка и вывод отладочной информации.
"""


# ---------------- НАСТРОЙКИ ОФОРМЛЕНИЯ ----------------

BG_GRAD = ft.LinearGradient(
    begin=ft.alignment.top_left,
    end=ft.alignment.bottom_right,
    colors=["#200022", "#050007"],
)

ACCENT = "#A84DFF"
TEXT_LIGHT = "#F3E9FF"
BLOCK_BG = "#130017"
FIELD_BG = "#1D0023"

ROUTE_CHOICES = [
    ("snake_lr_rl", "Змейка: слева-направо, затем справа-налево"),
    ("snake_rl_lr", "Змейка: справа-налево, затем слева-направо"),
    ("spiral_cw",   "Спираль по часовой стрелке"),
    ("spiral_ccw",  "Спираль против часовой"),
    ("bottom_up",   "Снизу-вверх по столбцам"),
    ("top_down",    "Сверху-вниз по столбцам"),
]

ROUTE_TO_INT = {
    "snake_lr_rl": 1,
    "snake_rl_lr": 2,
    "spiral_cw":   3,
    "spiral_ccw":  4,
    "bottom_up":   5,
    "top_down":    6,
}


def main(page: ft.Page):
    """
    Точка входа Flet-приложения.
    Строит интерфейс и подключает обработчики событий.
    """
    page.title = "CryptoLab — Перестановочные шифры"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_maximized = True
    page.bgcolor = None
    page.gradient = BG_GRAD
    page.horizontal_alignment = "stretch"
    page.vertical_alignment = "stretch"

    # ---------- левая часть: параметры шифрования ----------

    cipher_select = ft.Dropdown(
        label="Выберите шифр",
        options=[
            ft.dropdown.Option("vertical", "Вертикальная перестановка"),
            ft.dropdown.Option("route", "Маршрутная перестановка"),
            ft.dropdown.Option("block", "Блочная перестановка"),
        ],
        value="vertical",
        bgcolor=FIELD_BG,
        color=TEXT_LIGHT,
        border_color=ACCENT,
        text_style=ft.TextStyle(size=18),
    )

    mode_select = ft.Dropdown(
        label="Режим работы",
        options=[
            ft.dropdown.Option("encrypt", "Шифрование"),
            ft.dropdown.Option("decrypt", "Расшифровка"),
        ],
        value="encrypt",
        bgcolor=FIELD_BG,
        color=TEXT_LIGHT,
        border_color=ACCENT,
        text_style=ft.TextStyle(size=18),
    )

    input_text = ft.TextField(
        label="Входной текст",
        multiline=True,
        min_lines=4,
        bgcolor=FIELD_BG,
        color=TEXT_LIGHT,
        border_color=ACCENT,
        text_style=ft.TextStyle(size=18),
    )

    key_field = ft.TextField(
        label="Ключ (вертикальная перестановка)",
        bgcolor=FIELD_BG,
        color=TEXT_LIGHT,
        border_color=ACCENT,
        text_style=ft.TextStyle(size=18),
    )

    # параметры маршрутной перестановки
    route_dim_mode = ft.Dropdown(
        label="Что задаём",
        options=[
            ft.dropdown.Option("rows", "Число строк"),
            ft.dropdown.Option("cols", "Число столбцов"),
        ],
        value="rows",
        bgcolor=FIELD_BG,
        color=TEXT_LIGHT,
        border_color=ACCENT,
        text_style=ft.TextStyle(size=18),
    )

    route_rows = ft.TextField(
        label="Число строк",
        bgcolor=FIELD_BG,
        color=TEXT_LIGHT,
        border_color=ACCENT,
        text_style=ft.TextStyle(size=18),
    )

    route_cols = ft.TextField(
        label="Число столбцов",
        bgcolor=FIELD_BG,
        color=TEXT_LIGHT,
        border_color=ACCENT,
        text_style=ft.TextStyle(size=18),
    )

    route_mode = ft.Dropdown(
        label="Маршрут",
        options=[ft.dropdown.Option(v, title) for v, title in ROUTE_CHOICES],
        value="snake_lr_rl",
        bgcolor=FIELD_BG,
        color=TEXT_LIGHT,
        border_color=ACCENT,
        text_style=ft.TextStyle(size=18),
    )

    # параметры блочной перестановки
    block_size = ft.TextField(
        label="Размер блока",
        bgcolor=FIELD_BG,
        color=TEXT_LIGHT,
        border_color=ACCENT,
        text_style=ft.TextStyle(size=18),
    )

    block_perm = ft.TextField(
        label="Перестановка (например: 3 1 4 2, пусто — обратный порядок)",
        bgcolor=FIELD_BG,
        color=TEXT_LIGHT,
        border_color=ACCENT,
        text_style=ft.TextStyle(size=18),
    )

    status_text = ft.Text("", color="#FF6B8B", size=17)

    # ---------- правая часть: отладка и результат ----------

    debug_list = ft.ListView(
        expand=True,
        spacing=2,
        padding=ft.Padding(4, 4, 4, 4),
        auto_scroll=True,
    )

    debug_container = ft.Container(
        bgcolor=BLOCK_BG,
        border_radius=12,
        padding=10,
        expand=True,
        content=ft.Column(
            [
                ft.Text("Отладочная информация", color=TEXT_LIGHT, size=20),
                ft.Divider(color="#3A124F", height=1),
                debug_list,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    result_output = ft.TextField(
        label="Результат (шифртекст / расшифровка)",
        multiline=True,
        min_lines=3,
        read_only=True,
        bgcolor=BLOCK_BG,
        color="#FFFFFF",
        border_color="#5F1F82",
        text_style=ft.TextStyle(size=18),
    )

    result_container = ft.Container(
        bgcolor=BLOCK_BG,
        border_radius=12,
        padding=10,
        expand=True,
        content=ft.Column(
            [
                ft.Text("Результат", color=TEXT_LIGHT, size=20),
                ft.Divider(color="#3A124F", height=1),
                result_output,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    # ---------- служебные функции ----------

    def refresh_fields(e=None):
        """
        Управляет видимостью полей ввода в зависимости от выбранного шифра.
        """
        c = cipher_select.value

        key_field.visible = (c == "vertical")

        is_route = (c == "route")
        route_dim_mode.visible = is_route
        route_rows.visible = is_route
        route_cols.visible = is_route
        route_mode.visible = is_route

        is_block = (c == "block")
        block_size.visible = is_block
        block_perm.visible = is_block

        page.update()

    cipher_select.on_change = refresh_fields
    refresh_fields()

    def render_debug(text: str, is_error: bool = False):
        """
        Выводит отладочную информацию или сообщение об ошибке в правой панели.
        """
        debug_list.controls.clear()

        if is_error:
            debug_list.controls.append(
                ft.Text(
                    text,
                    color="#FF4B5C",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    font_family="Consolas",
                )
            )
            return

        for line in text.splitlines():
            stripped = line.strip()

            if any(
                stripped.startswith(pref)
                for pref in (
                    "Матрица",
                    "Исходные блоки",
                    "Блоки после",
                    "Блоки шифртекста",
                    "Маршрут:",
                    "Размер блока",
                    "Заданный ключ",
                    "Использованный ключ",
                    "Номера букв в ключе",
                )
            ):
                color = "#FFD86A"
                weight = ft.FontWeight.BOLD
                size = 18
            elif stripped == "":
                color = "#7A6A90"
                weight = ft.FontWeight.NORMAL
                size = 17
            elif all((ch.isalpha() or ch.isspace() or ch in "-ф") for ch in stripped):
                color = "#F8F8FF"
                weight = ft.FontWeight.NORMAL
                size = 17
            else:
                color = "#B9A0FF"
                weight = ft.FontWeight.NORMAL
                size = 17

            debug_list.controls.append(
                ft.Text(
                    line,
                    color=color,
                    size=size,
                    weight=weight,
                    font_family="Consolas",
                )
            )

    # ---------- обработчик кнопки ----------

    def run_cipher(e):
        """
        Основной обработчик: запускает шифрование или расшифровку
        в зависимости от выбранного шифра и режима работы.
        """
        result_output.value = ""
        status_text.value = ""

        cipher = cipher_select.value
        mode = mode_select.value
        raw_txt = input_text.value

        # нормализация входного текста
        if mode == "encrypt":
            working_txt = normalize_encrypt(raw_txt)
        else:
            working_txt = normalize_decrypt(raw_txt)

        try:
            # вертикальная перестановка
            if cipher == "vertical":
                key = key_field.value
                if mode == "encrypt":
                    dbg, res = encrypt_vertical(working_txt, key)
                else:
                    dbg, res = decrypt_vertical(working_txt, key)

            # маршрутная перестановка
            elif cipher == "route":
                norm_len = len(working_txt)
                if norm_len == 0:
                    raise ValueError("Текст после нормализации пуст.")

                dim_mode = route_dim_mode.value
                rows = cols = None

                if dim_mode == "rows":
                    if not route_rows.value:
                        raise ValueError("Укажите число строк.")
                    rows = int(route_rows.value)
                    if rows <= 0:
                        raise ValueError("Число строк должно быть > 0.")
                    cols = norm_len // rows + (1 if norm_len % rows != 0 else 0)
                    route_cols.value = str(cols)
                else:
                    if not route_cols.value:
                        raise ValueError("Укажите число столбцов.")
                    cols = int(route_cols.value)
                    if cols <= 0:
                        raise ValueError("Число столбцов должно быть > 0.")
                    rows = norm_len // cols + (1 if norm_len % cols != 0 else 0)
                    route_rows.value = str(rows)

                if rows * cols < norm_len:
                    raise ValueError("Размер матрицы меньше длины текста.")

                rmode = ROUTE_TO_INT[route_mode.value]

                if mode == "encrypt":
                    dbg, res = encrypt_route(working_txt, rows, cols, rmode)
                else:
                    dbg, res = decrypt_route(working_txt, rows, cols, rmode)

            # блочная перестановка
            elif cipher == "block":
                if not block_size.value:
                    raise ValueError("Укажите размер блока.")
                size = int(block_size.value)
                if size <= 1:
                    raise ValueError("Размер блока должен быть > 1.")
                perm = block_perm.value or ""
                if mode == "encrypt":
                    dbg, res = encrypt_block(working_txt, size, perm)
                else:
                    dbg, res = decrypt_block(working_txt, size, perm)
            else:
                raise ValueError("Неизвестный шифр.")

            render_debug(dbg, is_error=False)

            # вывод результата в удобном виде
            if mode == "encrypt":
                result_output.value = output_encrypt(res, not_print=True)
            else:
                result_output.value = output_decrypt(res, not_print=True)

            status_text.value = "Готово."

        except Exception as ex:
            render_debug(f"ОШИБКА:\n{ex}", is_error=True)
            result_output.value = ""
            status_text.value = "Произошла ошибка."

        page.update()

    run_button = ft.ElevatedButton(
        text="Выполнить",
        bgcolor=ACCENT,
        color="white",
        on_click=run_cipher,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.Padding(16, 10, 16, 10),
        ),
    )

    # ---------- сборка панелей ----------

    left_panel = ft.Container(
        width=420,
        bgcolor=BLOCK_BG,
        border_radius=16,
        padding=16,
        content=ft.Column(
            [
                ft.Text(
                    "Параметры шифрования",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_LIGHT,
                ),
                cipher_select,
                mode_select,
                input_text,
                key_field,
                route_dim_mode,
                route_rows,
                route_cols,
                route_mode,
                block_size,
                block_perm,
                run_button,
                status_text,
            ],
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    right_panel = ft.Container(
        bgcolor=BLOCK_BG,
        border_radius=16,
        padding=16,
        expand=True,
        content=ft.Column(
            [
                debug_container,
                result_container,
            ],
            spacing=12,
            expand=True,
        ),
    )

    page.add(
        ft.Row(
            [left_panel, right_panel],
            expand=True,
            spacing=20,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
