# python generate_qrcode.py

import qrcode


bot_username = "Advert202407_bot"
bot_link = f"https://t.me/{bot_username}"

# Генерация QR-кода
qr = qrcode.make(bot_link)

# Сохранение QR-кода в файл
qr.save("bot_qr_code.png")

print("QR код успешно создан и сохранен как 'bot_qr_code.png'")
