def total_duration(data,key=None):
    if key and isinstance(data,dict):
        tracks = data.get(key, [])
    else:
        tracks = data if isinstance(data,list) else []
    
    total_seconds = sum(int(track.get("duration",0)) for track in tracks)
    return format_duration(total_seconds)
def format_duration(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds %3600) // 60 
    seconds = total_seconds % 60
    parts = []
    if hours > 0:
        parts.append(f"{hours} hr{"s" if hours != 1 else ""}")
    if minutes > 0:
        parts.append(f"{minutes} min{"s" if minutes != 1 else ""}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}")
        return "".join(parts)
def sec_to_min(duration):
    if isinstance(duration,str) and ":" in duration:
        return duration
    
    try:
        total_seconds= int(duration)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    except (ValueError,TypeError):
        return "00:00"
def checkformat(duration):
    if not duration:
        return "invalid"
    duration = str(duration).strip()
    if ":" in duration:
        parts = duration.strip(":")
        if len(parts) != 2:
            return "invalid"
    try:
        minutes = int(parts[0])
        seconds = int(parts[1])
        if minutes < 0 or seconds < 0 or seconds >= 60:
            return "invalid"
        total_seconds = minutes * 60 + seconds
        return str(total_seconds)
    except (ValueError):
        return "invalid"
    else: 
        try:
            seconds = int(duration)
            if seconds < 0:
                return "invalid"
            return str(seconds)
        except (ValueError):
            return "invalid"
def min_to_sec(duration_str):
    if ":" not in duration_str:
        try:
            return int(duration_str)
        except(ValueError):
            return 0
        parts = duration_str.split(":")
        if len(parts) != 2:
            return 0 
        try:
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes * 60 + seconds
        except(ValueError):
            return 0
