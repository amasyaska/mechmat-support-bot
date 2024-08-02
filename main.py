import threading
import time

import MechmatSupportBot

import MechmatSupportAdministratorBot

MechmatSupportAdministratorBot.bot_sender = MechmatSupportBot.bot

mechmatsupportbot_thread = threading.Thread(target=MechmatSupportBot.main, daemon=True)
mechmatsupportadminbot_thread = threading.Thread(target=MechmatSupportAdministratorBot.main, daemon=True)

if __name__ == "__main__":
    mechmatsupportadminbot_thread.start()
    print(f'MechmatSupportAdministratorBot.main has been started')
    mechmatsupportbot_thread.start()
    print(f'MechmatSupportBot.main has been started')

    while (mechmatsupportbot_thread.is_alive() and mechmatsupportadminbot_thread.is_alive()):
        time.sleep(0)
