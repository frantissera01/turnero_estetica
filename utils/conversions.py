# utils/conversions.py
from datetime import date, datetime, time
from typing import Any, Optional

def safe_date_str(x: Any) -> str:
    """YYYY-MM-DD si es date/datetime; str(x) en otros casos."""
    if isinstance(x, (date, datetime)):
        return x.date().isoformat() if isinstance(x, datetime) else x.isoformat()
    return str(x)

def safe_time_str(x: Any) -> str:
    """HH:MM:SS si es time/datetime; str(x) en otros casos."""
    if isinstance(x, datetime):
        return x.time().strftime("%H:%M:%S")
    if isinstance(x, time):
        return x.strftime("%H:%M:%S")
    # a veces MySQL devuelve '07:00:00' como str o Decimal->str
    s = str(x)
    # normalizamos '7:0:0' -> '07:00:00' si parece hora simple
    if s.count(":") == 2 and all(part.isdigit() for part in s.split(":")):
        h, m, sec = (f"{int(p):02d}" for p in s.split(":"))
        return f"{h}:{m}:{sec}"
    return s

def safe_int(x: Any, default: int = 0) -> int:
    if x is None:
        return default
    try:
        return int(x)
    except Exception:
        try:
            return int(str(x))
        except Exception:
            return default

def to_time(x: Any) -> Optional[time]:
    """Devuelve un time(HH:MM:SS) a partir de distintos tipos (time, datetime, str, Decimal, etc.)."""
    if x is None:
        return None
    if isinstance(x, time):
        return x
    if isinstance(x, datetime):
        return x.time()
    # Normalizamos todo lo demás a str y probamos varios formatos
    s = str(x).strip()
    # formatos comunes
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            dt = datetime.strptime(s, fmt)
            return time(dt.hour, dt.minute, dt.second)
        except Exception:
            pass
    # último intento: si viene como "7:0:0" o "7:0"
    parts = s.split(":")
    if 1 <= len(parts) <= 3 and all(p.replace(".", "", 1).isdigit() for p in parts):
        try:
            h = int(float(parts[0] or 0))
            m = int(float(parts[1] if len(parts) > 1 else 0))
            sec = int(float(parts[2] if len(parts) > 2 else 0))
            return time(max(0, min(h, 23)), max(0, min(m, 59)), max(0, min(sec, 59)))
        except Exception:
            return None
    return None