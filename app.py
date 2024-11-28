import os
from telethon.sync import TelegramClient, events
import re
import urllib.parse

# Lấy thông tin từ biến môi trường
api_id = int(os.getenv("API_ID"))  # API_ID từ biến môi trường
api_hash = os.getenv("API_HASH")  # API_HASH từ biến môi trường
source_group = os.getenv("SOURCE_GROUP")  # Nhóm nguồn
destination_group = os.getenv("DESTINATION_GROUP")  # Nhóm đích
affiliate_id = os.getenv("AFFILIATE_ID", "17385530062")  # Affiliate ID từ biến môi trường

# Kết nối với tài khoản Telegram
client = TelegramClient('user', api_id, api_hash)

def add_https_to_links(text):
    """Thêm https:// trước các liên kết bắt đầu bằng s.shopee.vn"""
    # Thêm https:// trước các liên kết ngắn Shopee chưa có https://
    return re.sub(r'\bs\.shopee\.vn', r'https://s.shopee.vn', text)

def convert_to_full_shopee_link(text, affiliate_id):
    """Chuyển đổi link ngắn Shopee thành link đầy đủ với affiliate ID"""
    # Tìm các link Shopee ngắn trong tin nhắn
    matches = re.findall(r'https://s.shopee.vn/(\S+)', text)
    for match in matches:
        # Chuyển đổi link ngắn thành link đầy đủ với affiliate ID
        # Mã hóa toàn bộ URL origin_link, bao gồm https://
        origin_link = urllib.parse.quote_plus(f'https://s.shopee.vn/{match}')
        full_link = f"https://shope.ee/an_redir?origin_link={origin_link}&affiliate_id={affiliate_id}&sub_id=1review"
        # Thay thế các link ngắn Shopee bằng link đầy đủ
        text = text.replace(f"https://s.shopee.vn/{match}", full_link)
    return text

@client.on(events.NewMessage(chats=source_group))  # Lắng nghe tin nhắn từ nhóm nguồn
async def forward_message(event):
    try:
        # Lấy nội dung tin nhắn
        message = event.message

        # Sửa nội dung tin nhắn: thêm https:// trước liên kết và chuyển đổi thành link đầy đủ
        if message.text:
            modified_text = add_https_to_links(message.text)  # Thêm https:// vào link
            modified_text = convert_to_full_shopee_link(modified_text, affiliate_id)  # Chuyển đổi link thành đầy đủ
        else:
            modified_text = message.text

        # Gửi tin nhắn đã chỉnh sửa đến nhóm đích
        await client.send_message(destination_group, modified_text)
        print(f"Đã chuyển tiếp tin nhắn: {modified_text}")
    except Exception as e:
        print(f"Lỗi khi chuyển tiếp tin nhắn: {e}")

# Bắt đầu lắng nghe
print("Đang lắng nghe tin nhắn...")
client.start()
client.run_until_disconnected()
