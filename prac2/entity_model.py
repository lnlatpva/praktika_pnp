
"""Практическая работа №2. Вариант Б. N1=12, N2=13."""

import json
from typing import Any


def build_telemetry_packet() -> dict[str, Any]:
    """Формирует пакет телеметрии с индивидуальными данными пары."""
    return {
        "pad_id": "PAD-15",
        "well_id": "W-225",
        "p_res_mpa": 24.5,
        "p_bhp_mpa": 14.0,
        "mode": "PUMPING",
        "is_online": True,
        "sensors": [
            {"code": "T-01", "value": 60.0, "unit": "C"},
            {"code": "Q-01", "value": 60.0, "unit": "m3/d"},
            {"code": "P-01", "value": 14.0, "unit": "MPa"},
        ],
    }


def save_to_json(
    data: dict[str, Any],
    filename: str = "data.json"
) -> None:
    """Сохраняет пакет телеметрии в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_from_json(
    filename: str = "data.json"
) -> dict[str, Any]:
    """Читает JSON-файл обратно в словарь Python."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def print_telemetry_summary(packet: dict[str, Any]) -> None:
    """Выводит сводку и рассчитывает депрессию на пласт."""
    drawdown = packet["p_res_mpa"] - packet["p_bhp_mpa"]

    print("=" * 58)
    print(
        f"ПАКЕТ ТЕЛЕМЕТРИИ: Куст {packet['pad_id']} | "
        f"Скважина {packet['well_id']}"
    )
    print("=" * 58)
    print(f"Режим работы: {packet['mode']}")
    print(f"Связь со станцией: {packet['is_online']}")
    print(
        f"Давления: Pпл = {packet['p_res_mpa']} МПа, "
        f"Pзаб = {packet['p_bhp_mpa']} МПа "
        f"(dP = {drawdown:.2f} МПа)"
    )

    print(f"Опрошено датчиков: {len(packet['sensors'])} шт.")

    for sensor in packet["sensors"]:
        print(
            f" -> Датчик {sensor['code']}: "
            f"{sensor['value']} {sensor['unit']}"
        )

    print("=" * 58)


if __name__ == "__main__":
    # 1. Формируем словарь
    pkt = build_telemetry_packet()

    # 2. Сохраняем в JSON
    save_to_json(pkt, "data.json")
    print("[OK] Файл 'data.json' успешно записан на диск!")

    # 3. Читаем JSON обратно
    loaded_pkt = load_from_json("data.json")

    # 4. Проверяем совпадение данных
    assert loaded_pkt == pkt, "Ошибка: данные при чтении JSON исказились!"
    print("[OK] Обратное чтение через json.load() прошло успешно!")

    # 5. Выводим сводку
    print_telemetry_summary(loaded_pkt)