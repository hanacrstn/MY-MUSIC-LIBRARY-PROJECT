
def total_duration(data, key=None):
    counter = 0
    for track in data[key]:
        total_sec = int(track["duration"])
        counter = counter +  total_sec

    minutes = counter // 60
    seconds = counter % 60
    hours = minutes//60

    minutes = minutes % 60

    if hours > 0:
        return f"{hours} hr/s {minutes} mins and {seconds}s"
    elif minutes > 0:
        return f"{minutes} mins and {seconds}s"
    else:
        return f"{seconds}s"
    
def sec_to_min(duration):
    if ":" not in duration:
        minutes = int(duration) // 60
        seconds = int(duration) % 60

        return f"{minutes:02}:{seconds:02}"
    
def checkformat(duration):
    if ":" in duration:
        parts = duration.split(":")
        try:
            if len(parts) == 2:
                minutes = int(parts[0]) * 60
                seconds = int(parts[1]) 
                return str(minutes + seconds)
        except ValueError:
            return "invalid"
    else:
        try:
            return str(int(duration))
        except ValueError:
            return "invalid"
