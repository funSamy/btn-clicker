from telethon import TelegramClient, Button
import time
from dotenv import load_dotenv
import os
import re
import random

# Constants for button texts
MINING_BUTTON_TEXT = '⛏ Mining'
CLICK_BUTTON_TEXT = '⛏ Clic'


async def clear_chat_history(dialog):
    """Clears the chat history of the given dialog."""
    messages = client.iter_messages(dialog)
    if messages:
        async for message in messages:
            await client.delete_messages(dialog, message)
        return True
    return False


def random_sleep(start=3, end=5):
    """Pauses execution for a random duration between start and end seconds."""
    duration = random.randint(start, end)
    print(f'Sleeping for {duration} seconds...')
    time.sleep(duration)
    print('Waking up...')


def find_button(response, button_text):
    """Searches for a button with the given text in the response."""
    if response.buttons:
        for row in response.buttons:
            for button in row:
                if button.text == button_text:
                    return button
    return None


async def start_conversation(dialog):
    """Starts a conversation with the bot and navigates to the click button."""
    print('\nStarting conversation...')
    try:
        timeout = 300  # Timeout 5 minutes in seconds
        async with client.conversation(dialog, timeout=timeout) as conv:
            await conv.send_message('/start')
            response = await conv.get_response()

            mining_button = find_button(response, MINING_BUTTON_TEXT)
            if mining_button:
                random_sleep()
                await mining_button.click()
                response = await conv.get_response()

                click_button = find_button(response, CLICK_BUTTON_TEXT)
                if click_button:
                    random_sleep()
                    await click_button.click()
                    response = await conv.get_response()
                    random_sleep()
                    return response
                else:
                    print(f"'{CLICK_BUTTON_TEXT}' button not found")
            else:
                print(f"'{MINING_BUTTON_TEXT}' button not found")
            return None

    except TimeoutError:
        print("Could not get the Bot response")
        return None


def extract_amounts(text: str):
    """Extracts the current and maximum amounts from the given text."""
    pattern = r"(\d+)/(\d+)"
    current_amount, max_amount = None, None

    # Find the first match
    match = re.search(pattern, text)
    if match:
        current_amount = int(match.group(1))
        max_amount = int(match.group(2))
    return current_amount, max_amount


async def click_mining_button(bot_name, target_amount=1200):
    """Repeatedly clicks the '⛏ Clic' button until the target amount is reached."""
    async for dialog in client.iter_dialogs():
        if dialog.name == bot_name:
            print(f"Found bot: {dialog.name}")
            print("Chat history cleared." if await clear_chat_history(dialog) else "Chat history is already empty.")

            response = await start_conversation(dialog)
            if response is None:
                print("Could not start conversation with the bot")
                return

            # current_amount, max_amount = extract_amounts(str(response.message))
            current_amount = 0
            max_amount = target_amount
            random_sleep()
            print("Conversation started with the bot")

            # Check if the target is already reached
            if current_amount >= target_amount:
                print(f'Target amount already reached: {current_amount}/{max_amount}')
                return

            async for message in client.iter_messages(dialog):
                if message.buttons:
                    button = find_button(message, CLICK_BUTTON_TEXT)
                    if button:
                        while current_amount < max_amount:
                            try:
                                await button.click()
                                print(
                                    f"Clicked button! Current amount: {current_amount}")

                                # Update current_amount and max_amount from message text
                                message = await client.get_messages(dialog, ids=message.id)
                                current_amount, max_amount = extract_amounts(
                                    str(message.text))

                            except Exception as e:
                                print(f"Error clicking button: {e}")
                            time.sleep(0.5)

                        if current_amount >= max_amount:  # Use >= to handle potential overshooting
                            print(
                                f'Target amount reached: {current_amount}/{max_amount}\n')
                            return

                    else:
                        print(f"'{CLICK_BUTTON_TEXT}' button not found")
                    return  # Exit the loop after processing the first message with buttons


async def main(bot_name: str, target_amount=1200):
    """Main function to start the mining process."""
    start_time = time.time()
    await click_mining_button(bot_name, target_amount=target_amount)
    print(f"Target amount reached")
    print(
        f'Completed in {time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))}')

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
        client.loop.run_until_complete(main(
            bot_name='Мinеr Bоt🌍', target_amount=target_amount))
