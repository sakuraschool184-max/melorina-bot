from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():

    buttons = [
        [
            InlineKeyboardButton(
                "🌸 چت با ملورینا",
                callback_data="chat"
            )
        ],
        [
            InlineKeyboardButton(
                "🎭 تغییر شخصیت",
                callback_data="personality"
            )
        ],
        [
            InlineKeyboardButton(
                "📖 بیوگرافی کیوت",
                callback_data="bio"
            )
        ],
        [
            InlineKeyboardButton(
                "🎮 بازی با ملورینا",
                callback_data="game"
            )
        ]
    ]

    return InlineKeyboardMarkup(buttons)



def join_channels():

    channels = [
        ("① کانال اول 🌸", "https://t.me/team_Yuri"),
        ("② کانال دوم 🌸", "https://t.me/pinkii008"),
        ("③ کانال سوم 🌸", "https://t.me/Yuriteam77"),
        ("④ کانال چهارم 🌸", "https://t.me/animeYuri7"),
        ("⑤ کانال پنجم 🌸", "https://t.me/Yuri90ok"),
    ]

    buttons = []

    for name, url in channels:
        buttons.append(
            [
                InlineKeyboardButton(
                    name,
                    url=url
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "✅ عضو شدم",
                callback_data="check_join"
            )
        ]
    )

    return InlineKeyboardMarkup(buttons)
