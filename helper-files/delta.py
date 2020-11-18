prev_value= {}
def delta(key, value, **kwargs):
    key = key
    # Get previous values
    global prev_value
    cur_value = value
    # Calculare delta
    try:
        delta = cur_value - prev_value.get(key, 0)
    except Exception:
        print("Hit Exception", file=sys.stderr)
        delta = prev_value.get(key, 0)
    #update global values
    prev_value[key] = cur_value
    return delta
