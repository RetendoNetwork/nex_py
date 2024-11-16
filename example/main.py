import threading
import error, result_codes, account
from account import Account
from result_codes import ResultCodes, init_result_codes


authentication_server_account = Account
secure_server_account = Account
test_user_account = Account

async def account_details_by_pid(pid):
    if pid == authentication_server_account.pid:
        return authentication_server_account, None

    if pid == secure_server_account.pid:
        return secure_server_account, None

    if pid == test_user_account.pid:
        return test_user_account, None

    return None, error.new_error(ResultCodes.RendezVous.InvalidPID, "Invalid PID")

async def account_details_by_username(username):
    if username == authentication_server_account.username:
        return authentication_server_account, None

    if username == secure_server_account.username:
        return secure_server_account, None

    if username == test_user_account.username:
        return test_user_account, None

    return None, error.new_error(ResultCodes.RendezVous.InvalidUsername, "Invalid username")

async def main():
    global authentication_server_account, secure_server_account, test_user_account

    authentication_server_account = Account.new_account(1, "Quazal Authentication", "authpassword")
    secure_server_account = Account.new_account(2, "Quazal Rendez-Vous", "securepassword")
    test_user_account = Account.new_account(1800000000, "1800000000", "nexuserpassword")

    threads = []

    # Create and start threads (like goroutines in Go)
    threads.append(threading.Thread(target=start_authentication_server))
    threads.append(threading.Thread(target=start_secure_server))
    threads.append(threading.Thread(target=start_hpp_server))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()