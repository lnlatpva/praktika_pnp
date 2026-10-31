"""
Модуль аварийной диагностики скважины.
Практическая работа № 1. Вариант Б.
N1 = 12, N2 = 13, N = 25.
"""

W_CRITICAL: float = 85.0
W_EMERGENCY: float = 98.0
DP_MIN_ACTIVE: float = 0.5
J_NORM_DEFAULT: float = 4.75


def validate_telemetry(
    q_liq: float,
    w_pct: float,
    p_res: float,
    p_bhp: float
) -> bool:
    """
    Проверяет корректность показаний четырёх датчиков.

    Args:
        q_liq: Дебит жидкости (0..1000 м3/сут).
        w_pct: Обводнённость (0..100%).
        p_res: Пластовое давление (5..60 МПа).
        p_bhp: Забойное давление (1..60 МПа).

    Returns:
        bool: True, если все параметры находятся в допустимых пределах.
    """
    return (
        0 <= q_liq <= 1000
        and 0 <= w_pct <= 100
        and 5 <= p_res <= 60
        and 1 <= p_bhp <= 60
    )


def calc_hydraulics(
    q_liq: float,
    p_res: float,
    p_bhp: float
) -> tuple[float, float]:
    """
    Рассчитывает депрессию и коэффициент продуктивности.

    Формулы:
        dP = p_res - p_bhp
        J = q_liq / dP

    Если dP <= 0, коэффициент J равен 0.

    Args:
        q_liq: Дебит жидкости.
        p_res: Пластовое давление.
        p_bhp: Забойное давление.

    Returns:
        tuple: Депрессия и коэффициент продуктивности.
    """
    drawdown = p_res - p_bhp

    if drawdown <= 0:
        productivity_index = 0.0
    else:
        productivity_index = q_liq / drawdown

    return drawdown, productivity_index


def determine_status_code(
    drawdown: float,
    w_pct: float,
    prod_index: float,
    j_norm: float = J_NORM_DEFAULT
) -> str:
    """
    Определяет техническое состояние скважины.

    Бизнес-правила:
        1. dP < 0 -> BLOWOUT
        2. W >= 98 -> CRITICAL_WATER
        3. dP <= 0.5 -> IDLE
        4. W >= 85 -> WATERED
        5. J < J_norm -> CLOGGED
        6. Иначе -> NORMAL

    Args:
        drawdown: Депрессия.
        w_pct: Обводнённость.
        prod_index: Коэффициент продуктивности.
        j_norm: Норматив продуктивности.

    Returns:
        str: Код технического состояния.
    """
    if drawdown < 0.0:
        return "BLOWOUT"

    elif w_pct >= W_EMERGENCY:
        return "CRITICAL_WATER"

    elif drawdown <= DP_MIN_ACTIVE:
        return "IDLE"

    elif w_pct >= W_CRITICAL:
        return "WATERED"

    elif prod_index < j_norm:
        return "CLOGGED"

    elif w_pct >= 98.0:
        return "CRITTICAL_WATER"

    else:
        return "NORMAL"


def route_dispatcher_action(
    status_code: str
) -> tuple[str, int]:
    """
    Формирует команду диспетчеру через match-case.

    Args:
        status_code: Код технического состояния скважины.

    Returns:
        tuple: Текст команды и уровень критичности (0..3).
    """
    match status_code:

        case "BLOWOUT":
            return "Аварийная диагностика и проверка режима", 3

        case "CRITICAL_WATER":
            return "Критическая обводнённость. Срочная проверка", 3

        case "IDLE":
            return "Проверить рабочий режим скважины", 2

        case "WATERED":
            return "Провести анализ обводнённости", 2

        case "CLOGGED":
            return "Проверить состояние оборудования", 2

        case "NORMAL":
            return "Работа в штатном режиме", 0

        case _:
            return "Неизвестный код состояния", 1


if __name__ == "__main__":

    # Вариант Б
    q_liq = 60.0
    w_pct = 95.0
    p_res = 27.0
    p_bhp = 16.8

    # Проверка данных
    valid = validate_telemetry(
        q_liq, w_pct, p_res, p_bhp
    )

    print("ПРАКТИЧЕСКАЯ РАБОТА №1")
    print("Вариант Б")
    print("N1 = 12, N2 = 13, N = 25")
    print("-" * 45)

    print("Проверка телеметрии:", valid)

    if valid:

        # Расчёт гидравлики
        dp, j = calc_hydraulics(
            q_liq, p_res, p_bhp
        )

        # Определение состояния
        status = determine_status_code(
            dp, w_pct, j
        )

        # Маршрутизация
        action, criticality = route_dispatcher_action(
            status
        )

        print(f"Дебит жидкости Qж: {q_liq}")
        print(f"Обводнённость W: {w_pct}%")
        print(f"Пластовое давление: {p_res} МПа")
        print(f"Забойное давление: {p_bhp} МПа")

        print("-" * 45)

        print(f"Депрессия dP: {dp:.2f} МПа")
        print(f"Коэффициент J: {j:.2f}")
        print(f"Норматив J_norm: {J_NORM_DEFAULT}")

        print("-" * 45)

        print("Код состояния:", status)
        print("Команда диспетчеру:", action)
        print("Критичность:", criticality)

        print("-" * 45)

        # Проверка дополнительного условия
        emergency_status = determine_status_code(
            dp, 98.0, j
        )

        print(
            "Проверка CRITICAL_WATER:",
            emergency_status
        )

        # Проверка документации
        print("\nДОКУМЕНТАЦИЯ ФУНКЦИИ:")
        help(calc_hydraulics)

    else:
        print("Ошибка: некорректные входные данные.")