from telethon import TelegramClient

# Nhập API ID và API Hash của bạn
api_id = 26573563
api_hash = 'eceb503191c94fa067efd91f6fff4add'
phone_number = '+84989503646'

# Khởi tạo client và session
client = TelegramClient('user.session', api_id, api_hash)

async def main():
    await client.start(phone_number)
    print("Đăng nhập thành công, session đã được lưu.")
    await client.disconnect()

client.loop.run_until_complete(main())
