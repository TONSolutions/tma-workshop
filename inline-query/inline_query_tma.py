from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    InlineQueryHandler,
)


async def inline_query_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Inline query handler

    Args:
        update: update
        context: context

    Returns:
        None
    """
    await update.inline_query.answer(
        [
            {
                "type": "article",
                "id": "some_id",
                "title": "Workshop | Inline Query TMA",
                "input_message_content": {
                    "message_text": "Hi there! I'm an inline query!",
                },
                "reply_markup": {
                    "inline_keyboard": [
                        [{"text": "Click me", "url": "https://t.me/ton_solutions_en"}]
                    ]
                },
            }
        ],
        button={
            # Be careful! This is not the same as the button parameter in the InlineQueryResult class
            # It will not send user details in #tgWebAppData
            "text": "Click me",
            "web_app": {"url": "https://web-app.com/"},
        },
        cache_time=0,
    )


app = ApplicationBuilder().token("{TOKEN}").build()

app.add_handler(InlineQueryHandler(inline_query_handler))

app.run_polling()
