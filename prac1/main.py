"""Спецификации модуля аварийной диагностики скважины (Вариант Б)"""

#Константы
W_CRITICAL: float = 85.0 
DP_MIN_ACTIVE: float = 0.5 
J_NORM_DEFAULT: float = 4.75

def validate_telemetry(q_liq: float, w_pct: float, p_res: float, p_bhp: float) -> bool: 
    """Проверяет допустимые значения четырёх датчиков""" 
    if 0 <= q_liq <= 1000: 
        if 0 <= w_pct <= 100: 
            if 5 <= p_res <= 60: 
                if 1 <= p_bhp <= 60: 
                    return True
    return False

def calc_hydraulics(q_liq: float, p_res: float, p_bhp: float) -> tuple[float, float]: 
    """Рассчитывает депрессию и коэффициент продуктивности""" 
    drawdown = p_res - p_bhp
    if drawdown > 0:
        prod_index = q_liq / drawdown
    else:
        prod_index = 0.0

    return drawdown, prod_index

def determine_status_code(drawdown: float, w_pct: float, prod_index: float, j_norm: float = J_NORM_DEFAULT) -> str: 
    """Определяет состояние скважины на основе депрессии, обводненности и продуктивности"""
    if drawdown < 0.0:
        return "BLOWOUT"
    elif drawdown <= DP_MIN_ACTIVE:
        return "IDLE"
    elif w_pct >= W_CRITICAL:
        return "WATERED"
    elif prod_index < j_norm:
        return "CLOGGED"
    else:
        return "NORMAL"

def route_dispatcher_action(status_code: str) -> str: 
    """Выбирает команду диспетчеру через match-case"""
    match status_code:
        case "BLOWOUT":
            return "АВАРИЯ! Срочно остановить скважину!"
        case "IDLE":
            return "Скважина не работает. Проверить оборудование."
        case "WATERED":
            return "Высокая обводнённость! Проверить водоприток."
        case "CLOGGED":
            return "Низкая продуктивность! Проверить скважину на засорение."
        case "NORMAL":
            return "Скважина работает нормально."
        case _:
            return "Неизвестный код состояния!"
        
#Основная программа
if __name__ == "__main__":
    print("=== Аварийная диагностика скважины ===")
    print("Вариант Б")
    print("Номера студентов: 12 и 13")
    print("J_norm =", J_NORM_DEFAULT)

    #Ввод данных
    q_liq = float(input("Введите дебит жидкости Qж: "))
    w_pct = float(input("Введите обводнённость W: "))
    p_res = float(input("Введите пластовое давление Pпл: "))
    p_bhp = float(input("Введите забойное давление Pзаб: "))

    #Проверка датчиков
    if validate_telemetry(q_liq, w_pct, p_res, p_bhp):

        #Расчёт показателей
        drawdown, prod_index = calc_hydraulics(
            q_liq, p_res, p_bhp
        )

        #Определение состояния
        status_code = determine_status_code(
            drawdown, w_pct, prod_index
        )

        #Команда диспетчеру
        action = route_dispatcher_action(status_code)

        #Вывод результатов
        print("\n=== Результаты диагностики ===")
        print(f"Депрессия dP: {drawdown:.2f} МПа")
        print(f"Продуктивность J: {prod_index:.2f}")
        print(f"Норматив J_norm: {J_NORM_DEFAULT}")
        print(f"Код состояния: {status_code}")
        print(f"Команда диспетчеру: {action}")

    else:
        print("\nОШИБКА: данные датчиков выходят за допустимые пределы!")