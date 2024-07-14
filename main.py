import threading

import MechmatSupportBot

import MechmatSupportAdministratorBot

MechmatSupportAdministratorBot.bot_sender = MechmatSupportBot.bot

mechmatsupportbot_thread = threading.Thread(target=MechmatSupportBot.main)
delivery_thread = threading.Thread(target=MechmatSupportBot.send_delivery_for_all_users_interface)
mechmatsupportadminbot_thread = threading.Thread(target=MechmatSupportAdministratorBot.main)

if __name__ == "__main__":
    mechmatsupportadminbot_thread.start()
    mechmatsupportbot_thread.start()
    delivery_thread.start()

    mechmatsupportadminbot_thread.join()
    mechmatsupportbot_thread.join()
    delivery_thread.join()
