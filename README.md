# praktika_pnp
# Практическая работа 1
## Вариант Б. Аварийная диагностика скважины

### 1. Индивидуальные данные

N1 = 12
N2 = 13
N = 12 + 13 = 25

| Показатель | Значение |
|---|---:|
| Дебит жидкости Qж | 60 м³/сут |
| Обводнённость W | 95% |
| Пластовое давление Pпл | 27.0 МПа |
| Забойное давление Pзаб | 16.8 МПа |
| Норматив J_norm | 4.75 |

### 2. Таблица требований

| Функция | Назначение |
|---|---|
| validate_telemetry() | Проверяет допустимые границы четырёх датчиков |
| calc_hydraulics() | Рассчитывает депрессию и продуктивность |
| determine_status_code() | Определяет состояние скважины |
| route_dispatcher_action() | Выдаёт команду диспетчеру через match-case |

### 3. Расчёты

dP = 27.0 - 16.8 = 10.2 МПа
J = 60 / 10.2 = 5.88

### 4. Блок-схема

```mermaid
flowchart TD
Start([Вход: Qж, W, Pпл, Pзаб]) --> CalcDP[Депрессия: dP = Pпл - Pзаб]
CalcDP --> CheckDP{dP > 0?}
CheckDP -- Нет --> SetJZero[J = 0.0]
CheckDP -- Да --> CalcJ[J = Qж / dP]
SetJZero --> Diag1{dP < 0?}
CalcJ --> Diag1
Diag1 -- Да --> CodeBlow[BLOWOUT]
Diag1 -- Нет --> Diag2{dP <= 0.5?}
Diag2 -- Да --> CodeIdle[IDLE]
Diag2 -- Нет --> Diag3{W >= 85%?}
Diag3 -- Да --> CodeWat[WATERED]
Diag3 -- Нет --> Diag4{J < J_norm?}
Diag4 -- Да --> CodeClog[CLOGGED]
Diag4 -- Нет --> CodeNorm[NORMAL]
CodeBlow --> End([Вывод кода и директивы])
CodeIdle --> End
CodeWat --> End
CodeClog --> End
CodeNorm --> End
```

### 5. Результат

Состояние скважины: WATERED.
Причина: обводнённость составляет 95%, что превышает критическое значение 85%.
Команда диспетчеру: проверить водоизоляцию.
