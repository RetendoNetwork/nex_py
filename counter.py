# Initialize a new counter with a starting value
def new_counter(start):
    return {"value": start}

# Retrieve the current value of the counter
def get_value(counter):
    return counter["value"]

# Increment the counter by 1 and return the new value
def increment(counter):
    counter["value"] += 1
    return get_value(counter)