import rc4
import hashlib
import time
import socket

# Reset the client to default values
def reset_client(client):
    server = client["server"]

    client["sequence_id_in"] = new_counter(0)
    client["sequence_id_out_manager"] = new_sequence_id_manager()
    client["incoming_packet_manager"] = new_packet_manager()

    if client["outgoing_resend_manager"] is not None:
        client["outgoing_resend_manager"].clear()

    client["outgoing_resend_manager"] = new_packet_resend_manager(
        server["resend_timeout"],
        server["resend_timeout_increment"],
        server["resend_max_iterations"]
    )

    client["signature_key"] = update_access_key(client, server["access_key"])
    if not update_rc4_key(client, b"CD&ML"):
        return "Failed to update client RC4 key."

    if server["prudp_version"] == 0:
        client["server_connection_signature"] = bytearray(4)
        client["client_connection_signature"] = bytearray(4)
    else:
        client["server_connection_signature"] = bytearray()
        client["client_connection_signature"] = bytearray()

    client["connected"] = False
    return None

# Update the client’s RC4 key
def update_rc4_key(client, key):
    try:
        client["cipher"] = rc4.new(key)
        client["decipher"] = rc4.new(key)
        return True
    except Exception as e:
        print(f"Failed to create RC4 cipher. {str(e)}")
        return False

# Update the client’s access key and signature base
def update_access_key(client, access_key):
    client["signature_base"] = sum(map(ord, access_key))
    client["signature_key"] = hashlib.md5(access_key.encode()).digest()

# Increase the ping timeout
def increase_ping_timeout(client, seconds):
    if client["ping_kick_timer"]:
        client["ping_kick_timer"].cancel()
    if client["ping_check_timer"]:
        client["ping_check_timer"].cancel()
    client["ping_check_timer"] = time.Timer(seconds, lambda: None)

# Start the packet timeout timer
def start_timeout_timer(client):
    def check_ping():
        client["server"]["send_ping"](client)
        client["ping_kick_timer"] = time.Timer(client["server"]["ping_timeout"], lambda: client["server"]["timeout_kick"](client))

    client["ping_check_timer"] = time.Timer(client["server"]["ping_timeout"], check_ping)

# Stop the packet timeout timer
def stop_timeout_timer(client):
    if client["ping_kick_timer"]:
        client["ping_kick_timer"].cancel()
    if client["ping_check_timer"]:
        client["ping_check_timer"].cancel()

# Create a new PRUDP client
def new_client(address, server):
    client = {
        "address": address,
        "server": server,
        "sequence_id_in": None,
        "sequence_id_out_manager": None,
        "incoming_packet_manager": None,
        "outgoing_resend_manager": None,
        "cipher": None,
        "decipher": None,
        "signature_key": None,
        "signature_base": None,
        "server_connection_signature": None,
        "client_connection_signature": None,
        "connected": False,
        "ping_check_timer": None,
        "ping_kick_timer": None
    }

    err = reset_client(client)
    if err:
        print(err)
        return None

    return client