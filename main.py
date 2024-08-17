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
                            if button.text == '⛏ Clic':
                                start = time.time()
                                max_amount = 1200
                                while current_amount <= max_amount:
                                    try:
                                        await button.click()
                                        print(
                                            f"Clicked button! Current amount: {current_amount}")
                                        
                                    except Exception as e:
                                        print(f"Error clicking button: {e}")
                                    time.sleep(1.5)
                                    message = await client.get_messages(dialog, ids=message.id)
                                    text = str(message.text).split('\n')[0]
                                    text = text.split(' ')[-1]
                                    current_amount = int(text.split('/')[0])
                                    max_amount = int(text.split('/')[1])
                                if current_amount >= 1200:
                                    print(f'Target amount reached: {current_amount}/{max_amount}\n')
                                    print(f'Completed in {time.strftime("%H:%M:%S", time.gmtime(time.time() - start))}')
                                    exit(0)
                                    return True

                            else:
                                print("Button text not found")


async def main(bot_name: str, current_amount=0, target_amount=1200):
    out = await click_button(bot_name, current_amount=current_amount)
    print(f"Target amount reached")
    exit(0 if out else 1)

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
