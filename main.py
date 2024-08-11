from telethon import TelegramClient, events, Button
import time
from dotenv import load_dotenv
import os


async def click_button(bot_name, current_amount=0):
    # global current_amount
    async for dialog in client.iter_dialogs():
        if dialog.name == bot_name:
            print(f"Found bot: {dialog.name}")
            async for message in client.iter_messages(dialog):
                if message.buttons:
                    for row in message.buttons:
                        for button in row:
                            # print(button.text)
                            if button.text == '⛏ Clic':  # Check for the button text
                                while current_amount <= 1200:
                                    try:
                                        await button.click()
                                        current_amount += 1
                                        print(
                                            f"Clicked button! Current amount: {current_amount}")

                                    # async for new_message in client.iter_messages(dialog, limit=1):
                                    #     # print(new_message)
                                    #     print(new_message.message)
                                        # if "+1⛏" in new_message.message:
                                        #     print("Detected +1⛏ notification!")
                                        #     break  # Exit the loop when notification is found
                                    
                                    # while True:
                                    #     async for new_message in client.iter_messages(dialog, limit=1):
                                    #         if "+1⛏" in new_message.message:
                                    #             print("Detected +1⛏ notification!")
                                    #             break  # Exit the loop when notification is found
                                    #     time.sleep(0.5) 
                                    except Exception as e:
                                        print(f"Error clicking button: {e}")
                                    time.sleep(1.5)

                            else:
                                print("Button text not found")


async def main(bot_name: str, current_amount=0, target_amount=1200):
    while current_amount < target_amount:
        start_time = time.time()
        clicks_in_minute = 0
        while clicks_in_minute < 40 and current_amount <= target_amount:
            await click_button(bot_name, current_amount=current_amount)
            clicks_in_minute += 1
            # Adjust this if needed to click about 40 times per minute
            time.sleep(1.5)
        print("Pausing for 30 seconds...")
        time.sleep(30)
        elapsed_time = time.time() - start_time
        print(f"Minute elapsed (actual: {elapsed_time:.2f} seconds)")

    print(f"Target amount reached: {current_amount}")

if __name__ == "__main__":
    if load_dotenv():
        print("Loaded environment variables from .env file")
    else:
        print("No .env file found")
        exit(1)

    # Your API ID and Hash
    api_id = os.getenv('APP_ID')
    api_hash = os.getenv('APP_HASH')
    bot_token = os.getenv('BOT_TOKEN')
    phone_number = os.getenv('PHONE_NUMBER')

    # Target amount to reach
    target_amount = 1200  # Change this to your desired target

    # Initialize variables
    current_amount = 0

    client = TelegramClient('my_session', api_id, api_hash)
    client.start(phone=phone_number)
    with client:
        client.loop.run_until_complete(main(bot_name='Мinеr Bоt🌍', current_amount=current_amount, target_amount=target_amount))
