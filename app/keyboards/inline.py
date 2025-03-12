from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)


# Клавиатура для выбора пола
kb_gender = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='👨🏻‍️ Я парень', callback_data='male')],
        [InlineKeyboardButton(text='👩🏻‍️ Я девушка', callback_data='female')]
    ]
)


# Клавиатура для выбора рода занятий
kb_profession = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🎓 Я студент', callback_data='student')],
        [InlineKeyboardButton(text='💼 Я предприниматель', callback_data='businessman')],
        [InlineKeyboardButton(text='🏢 Работаю в найме', callback_data='employee')],
        [InlineKeyboardButton(text='🖥️ Фрилансер', callback_data='freelancer')]
    ]
)


# Клавиатура для выбора возрастной группы
kb_age = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🧑‍🎓👩‍🎓 18 – 24', callback_data='age_18_24')],
        [InlineKeyboardButton(text='🧔👩‍🦰 25 – 27', callback_data='age_25_27')],
        [InlineKeyboardButton(text='👨‍🦰👩‍🦳 28 – 40', callback_data='age_28_40')],
        [InlineKeyboardButton(text='🧓👵 41 – 55', callback_data='age_41_55')],
        [InlineKeyboardButton(text='🎩👒 55+', callback_data='age_55_plus')],
    ]
)

# Клавиатура для выбора места жительства
kb_residence = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🏡 В Москве', callback_data='city')],
        [InlineKeyboardButton(text='🏰 В Московской области', callback_data='region')],
        [InlineKeyboardButton(text='🏰 Я турист', callback_data='tourist')],
    ]
)


# Клавиатура для выбора компании
kb_company = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🙍‍♂️ Один/одна', callback_data='alone')],
        [InlineKeyboardButton(text='💑 С девушкой/парнем', callback_data='couple')],
        [InlineKeyboardButton(text='👨‍👩‍👧‍👦 С женой/мужем', callback_data='married')],
        [InlineKeyboardButton(text='👨‍👩‍👦‍👦 С родными/детьми', callback_data='family')],
        [InlineKeyboardButton(text='🫂 С друзьями', callback_data='friends')],
        [InlineKeyboardButton(text='👔 С коллегами по работе', callback_data='colleagues')],
    ]
)


# Клавиатура для выбора причин
kb_reason = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🍽 Качество кухни', callback_data='quality')],
        [InlineKeyboardButton(text='🎶 Атмосфера', callback_data='atmosphere')],
        [InlineKeyboardButton(text='💰 Цены', callback_data='prices')],
        [InlineKeyboardButton(text='📍 Удобное расположение', callback_data='location')],
        [InlineKeyboardButton(text='📸 "Инстаграмность" интерьера', callback_data='instagrammable')],
        [InlineKeyboardButton(text='⚡ Скорость обслуживания', callback_data='service_speed')],
        [InlineKeyboardButton(text='🗣 Рекомендации друзей', callback_data='friends_recommend')],
        [InlineKeyboardButton(text='🎁 Специальные акции', callback_data='special_offers')],
    ]
)


# Клавиатура для выбора источника
kb_advertising_sources = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='📷 Instagram/Reels', callback_data='instagram')],
        [InlineKeyboardButton(text='🌍 VK', callback_data='vk')],
        [InlineKeyboardButton(text='🗣 Рекомендации друзей', callback_data='friends_recommend')],
        [InlineKeyboardButton(text='🔎 Поиск в Google, Яндекс картах', callback_data='search')],
        [InlineKeyboardButton(text='🚶‍♂️ Проходил(а) мимо', callback_data='walk_by')],
    ]
)


# Клавиатура для выбора частоты посещения
kb_visit_frequency = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✨ Впервые', callback_data='first_time')],
        [InlineKeyboardButton(text='🔥 Чаще раза в неделю', callback_data='more_than_weekly')],
        [InlineKeyboardButton(text='📅 1-3 раза в месяц', callback_data='monthly')],
        [InlineKeyboardButton(text='🗓 Раз в 2-3 месяца', callback_data='every_few_months')],
        [InlineKeyboardButton(text='⏳ Реже', callback_data='rarely')],
    ]
)


# Клавиатура для выбора повода
kb_purpose = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🍳 Повседневный завтрак/обед/ужин',
                          callback_data='everyday_meal')],
    [InlineKeyboardButton(text='💑 Свидание', callback_data='date')],
    [InlineKeyboardButton(text='💼 Деловая встреча', callback_data='business_meeting')],
    [InlineKeyboardButton(text='🎉 Семейный праздник', callback_data='family_celebration')]
])


# Клавиатура для выбора предпочтений
kb_food_preferences = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🥩 Мясные блюда', callback_data='meat_dishes')],
        [InlineKeyboardButton(text='🐟 Рыба и морепродукты', callback_data='fish_seafood')],
        [InlineKeyboardButton(text='🥦 Вегетарианские/веганские позиции', callback_data='vegan_options')],
        [InlineKeyboardButton(text='🍰 Десерты', callback_data='desserts')],
        [InlineKeyboardButton(text='🍹 Алкогольные коктейли', callback_data='alcohol_cocktails')],
        [InlineKeyboardButton(text='☕ Кофе/чай', callback_data='coffee_tea')],
    ]
)

# Клавиатура для пропуска
kb_skip = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⏭️ Пропустить', callback_data='skip')]
    ]
)


# Клавиатура для выбора атмосферы
kb_atmosphere = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🛋️ Уютная и расслабляющая', callback_data='cozy_relaxing')],
        [InlineKeyboardButton(text='✨ Современная и стильная', callback_data='modern_stylish')],
        [InlineKeyboardButton(text='🎉 Шумная и оживленная', callback_data='loud_lively')],
        [InlineKeyboardButton(text='🙂 Обычная', callback_data='ordinary')]
    ]
)


# Клавиатура для оценки обслуживания
kb_service_rating = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⏳ Скорость', callback_data='speed')],
        [InlineKeyboardButton(text='😊 Вежливость персонала', callback_data='politeness')],
        [InlineKeyboardButton(text='🔍 Внимание к деталям', callback_data='attention_to_details')],
        [InlineKeyboardButton(text='👍 Все нравится', callback_data='everything_good')]
    ]
)


# Клавиатура для улучшений
kb_improvements = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='📜 Обновление меню', callback_data='update_menu')],
        [InlineKeyboardButton(text='🛋 Обновление интерьера', callback_data='update_interior')],
        [InlineKeyboardButton(text='💰 Снижение цен', callback_data='lower_prices')],
        [InlineKeyboardButton(text='🎵 Улучшение музыки', callback_data='better_music')]
    ]
)


# Клавиатура для помех посещения
kb_obstacles = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='💰 Высокие цены', callback_data='high_prices')],
        [InlineKeyboardButton(text='📍 Неудобное расположение', callback_data='inconvenient_location')],
        [InlineKeyboardButton(text='📜 Ограниченное меню', callback_data='limited_menu')],
        [InlineKeyboardButton(text='👎 Низкое качество обслуживания', callback_data='poor_service')],
        [InlineKeyboardButton(text='😊 Ничего не мешает', callback_data='no_obstacles')],
    ]
)


# Клавиатура для типов других ресторанов
kb_restaurants = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🏬 Сетевые рестораны', callback_data='chain_restaurants')],
    [InlineKeyboardButton(text='🍽️ Рестораны с высокой кухней', callback_data='fine_dining')],
    [InlineKeyboardButton(text='☕ Кафе и кофейни', callback_data='cafes')],
    [InlineKeyboardButton(text='🍸 Бары', callback_data='bars')],
])


# Клавиатура для выбора способа получения новостей
kb_news = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📱 Соц. сети, Instagram, Reels', callback_data='news_social')],
    [InlineKeyboardButton(text='🤖 Telegram-бот', callback_data='news_telegram')],
    [InlineKeyboardButton(text='🌐 Сайт и мобильное приложение', callback_data='news_site_app')],
])


# Клавиатура для шкалы рекомендаций
kb_recommendation = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='1️⃣', callback_data='recommend_1'),
        InlineKeyboardButton(text='2️⃣', callback_data='recommend_2'),
        InlineKeyboardButton(text='3️⃣', callback_data='recommend_3'),
        InlineKeyboardButton(text='4️⃣', callback_data='recommend_4'),
        InlineKeyboardButton(text='5️⃣', callback_data='recommend_5'),
    ],
    [
        InlineKeyboardButton(text='6️⃣', callback_data='recommend_6'),
        InlineKeyboardButton(text='7️⃣', callback_data='recommend_7'),
        InlineKeyboardButton(text='8️⃣', callback_data='recommend_8'),
        InlineKeyboardButton(text='9️⃣', callback_data='recommend_9'),
        InlineKeyboardButton(text='🔟', callback_data='recommend_10'),
    ],
])
