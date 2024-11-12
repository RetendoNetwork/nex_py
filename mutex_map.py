import threading

# MutexMap data storage and lock
mutex_map_data = {}
mutex_map_lock = threading.RLock()

# Set a key to a given value
def mutex_map_set(key, value):
    with mutex_map_lock:
        mutex_map_data[key] = value

# Get a value by key, returning (value, found) like in Go
def mutex_map_get(key):
    with mutex_map_lock:
        return mutex_map_data.get(key), key in mutex_map_data

# Delete a key from the map
def mutex_map_delete(key):
    with mutex_map_lock:
        if key in mutex_map_data:
            del mutex_map_data[key]

# Get the size of the map
def mutex_map_size():
    with mutex_map_lock:
        return len(mutex_map_data)

# Iterate over each item in the map, calling a callback function
def mutex_map_each(callback):
    with mutex_map_lock:
        for key, value in mutex_map_data.items():
            callback(key, value)

# Clear all items from the map
# An optional callback is called on each item before deletion
def mutex_map_clear(callback=None):
    with mutex_map_lock:
        keys_to_clear = list(mutex_map_data.keys())
        for key in keys_to_clear:
            value = mutex_map_data[key]
            if callback:
                callback(key, value)
            del mutex_map_data[key]

# Initialize the map (Optional: can use this for custom initialization if needed)
def new_mutex_map():
    global mutex_map_data
    with mutex_map_lock:
        mutex_map_data = {}