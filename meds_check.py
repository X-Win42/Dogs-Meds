import streamlit as st
from datetime import date

# =====================
# Configuración básica
# =====================
st.set_page_config(page_title="Medicaciones perros", page_icon="🐶", layout="centered")
st.title("🐶 Daily Dog Meds")

# =====================
# Nombres de los perros (editables en la barra lateral)
# =====================
with st.sidebar:
    st.header("Ajustes")
    dog1 = st.text_input("Nombre perro 1", value="Loki")
    dog2 = st.text_input("Nombre perro 2", value="Logan")
    st.write(":information_source: La fecha se detecta automáticamente (hoy).")

DOGS = [dog1, dog2]

# ===============================================
# Reglas por pastilla (cada una con su fecha de inicio)
# ===============================================
# Estructura de cada regla:
#   {
#     "start_date": date(YYYY, M, D),
#     "every_n_days": N,        # (opcional) frecuencia en días
#     "every_n_months": M,      # (opcional) frecuencia en meses
#     "note": "texto opcional"  # ej. "media pastilla"
#   }

SCHEDULE = {
    dog1: {  # Loki
        "Manganese": {"start_date": date(2025, 10, 23), "every_n_days": 28},
        "Omega 3":   {"start_date": date(2025, 10, 23), "every_n_days": 5},
        "Potassium": {"start_date": date(2025, 10, 24), "every_n_days": 4},
        "VE":        {"start_date": date(2025, 10, 24), "every_n_days": 9},
        "Condrovet": {"start_date": date(2025, 10, 21), "every_n_days": 1, "note": "media pastilla"},
        "VB":        {"start_date": date(2025, 10, 24), "every_n_days": 5},
        "Pipeta":    {"start_date": date(2025, 10, 21), "every_n_days": 30},
        "Librela":   {"start_date": date(2025, 9, 26),  "every_n_days": 30},
    },
    dog2: {  # Logan
        "Manganese": {"start_date": date(2025, 10, 23), "every_n_days": 6},
        "Omega 3":   {"start_date": date(2025, 10, 23), "every_n_days": 1},  # diario
        "Potassium": {"start_date": date(2025, 10, 23), "every_n_days": 3},
        "VE":        {"start_date": date(2025, 10, 23), "every_n_days": 2},
        "VB":        {"start_date": date(2025, 10, 23), "every_n_days": 1},  # diario
        "Seresto":   {"start_date": date(2025, 7, 15),  "every_n_months": 8},
    },
}

# =====================
# Utilidades de fechas (sin librerías externas)
# =====================
def is_leap(y: int) -> bool:
    return (y % 400 == 0) or (y % 4 == 0 and y % 100 != 0)

def days_in_month(y: int, m: int) -> int:
    dim = [31, 29 if is_leap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return dim[m-1]

def add_months(d: date, months: int) -> date:
    y, m = d.year, d.month
    total = m - 1 + months
    y += total // 12
    m = total % 12 + 1
    day = min(d.day, days_in_month(y, m))
    return date(y, m, day)

def occurs_every_n_days(target: date, start: date, n: int) -> bool:
    if n <= 0:
        return False
    delta = (target - start).days
    return delta >= 0 and delta % n == 0

def occurs_every_n_months(target: date, start: date, n_months: int) -> bool:
    if n_months <= 0 or target < start:
        return False
    cur = start
    while cur < target:
        cur = add_months(cur, n_months)
    return cur == target

def meds_for_date(d: date, schedule_for_dog: dict):
    out = []
    for pill, rule in schedule_for_dog.items():
        start = rule.get("start_date")
        if not isinstance(start, date):
            continue
        give = False
        if "every_n_days" in rule and occurs_every_n_days(d, start, int(rule["every_n_days"])):
            give = True
        if "every_n_months" in rule and occurs_every_n_months(d, start, int(rule["every_n_months"])):
            give = True
        if give:
            note = rule.get("note", "")
            out.append((pill, note))
    out.sort(key=lambda x: x[0].lower())
    return out

# =====================
# Fecha de trabajo: SIEMPRE hoy
# =====================
computed_date = date.today()

# Encabezado con fecha (formato ISO más corto y claro)
st.subheader(f"📅 Hoy: {computed_date.isoformat()}")

# =====================
# Salida por perro (UI simple y legible en móvil)
# =====================
for dog in DOGS:
    st.markdown(f"### 🐾 {dog}")
    meds = meds_for_date(computed_date, SCHEDULE.get(dog, {}))
    if meds:
        for name, note in meds:
            if note:
                st.write(f"• **{name}** — {note}")
            else:
                st.write(f"• **{name}**")
    else:
        st.write("— Ninguna pastilla hoy —")

st.caption("Cada pastilla usa su propia fecha de inicio como día cero. La fecha se detecta automáticamente.")
