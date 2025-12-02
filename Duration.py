def normalize_duration(duration):
    """
    Convert any duration format to seconds (int).
    Handles: int, "180", "3:00", etc.
    Returns 0 for invalid input.
    """
    if isinstance(duration, int):
        return duration
    
    if isinstance(duration, str):
        duration = duration.strip()
        
        # Handle mm:ss format
        if ":" in duration:
            parts = duration.split(":")
            if len(parts) == 2:
                try:
                    mins = int(parts[0])
                    secs = int(parts[1])
                    if mins >= 0 and secs >= 0 and secs < 60:
                        return mins * 60 + secs
                except ValueError:
                    return 0
        else:
            # Handle raw seconds as string
            try:
                secs = int(duration)
                return secs if secs >= 0 else 0
            except ValueError:
                return 0
    
    return 0


def total_duration(data, key=None):
    """
    Calculate total duration from tracks.
    Handles both dict with key and list of tracks.
    Works with any duration format (seconds or mm:ss).
    """
    if key and isinstance(data, dict):
        tracks = data.get(key, [])
    else:
        tracks = data if isinstance(data, list) else []
    
    total_seconds = sum(normalize_duration(track.get("duration", 0)) for track in tracks)
    return format_duration(total_seconds)


def format_duration(total_seconds):
    """
    Format seconds into human-readable duration.
    Examples: "3 hrs 45 mins 20 secs", "2 mins 30 secs", "45 secs"
    """
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60 
    seconds = total_seconds % 60
    parts = []
    
    if hours > 0:
        parts.append(f"{hours} hr{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} min{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} sec{'s' if seconds != 1 else ''}")
    
    return " ".join(parts)


def sec_to_min(duration):
    """
    Convert duration to mm:ss format for display.
    Accepts: int, "180", or "3:00"
    Returns: "03:00" format
    """
    # If already in mm:ss format, return as-is
    if isinstance(duration, str) and ":" in duration:
        return duration
    
    try:
        total_seconds = normalize_duration(duration)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    except (ValueError, TypeError):
        return "00:00"


def checkformat(duration):
    """
    Validate and convert duration to seconds (as string).
    Accepts: "3:00" or "180"
    Returns: "180" if valid, "invalid" if not
    """
    if not duration:
        return "invalid"
    
    duration = str(duration).strip()
    
    # Check if it's in mm:ss format
    if ":" in duration:
        parts = duration.split(":")
        if len(parts) != 2:
            return "invalid"
        
        try:
            minutes = int(parts[0])
            seconds = int(parts[1])
            if minutes < 0 or seconds < 0 or seconds >= 60:
                return "invalid"
            total_seconds = minutes * 60 + seconds
            return str(total_seconds)
        except ValueError:
            return "invalid"
    else:
        # It's in raw seconds format
        try:
            seconds = int(duration)
            if seconds < 0:
                return "invalid"
            return str(seconds)
        except ValueError:
            return "invalid"


def min_to_sec(duration_str):
    """
    Convert mm:ss string to total seconds (int).
    Accepts: "3:00" or "180"
    Returns: 180
    """
    if not duration_str:
        return 0
    
    duration_str = str(duration_str).strip()
    
    if ":" not in duration_str:
        try:
            return int(duration_str)
        except ValueError:
            return 0
    
    parts = duration_str.split(":")
    if len(parts) != 2:
        return 0
    
    try:
        minutes = int(parts[0])
        seconds = int(parts[1])
        return minutes * 60 + seconds
    except ValueError:
        return 0
