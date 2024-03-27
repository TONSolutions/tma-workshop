import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    InlineQueryHandler,
    ChosenInlineResultHandler,
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
                "title": "Workshop | Inline Query Updater",
                "input_message_content": {
                    "message_text": "Hi there! I'm an inline query updater!",
                },
                "reply_markup": {
                    "inline_keyboard": [
                        [{"text": "Click me", "url": "https://t.me/tonlabs_workshops"}]
                    ]
                },
            }
        ],
        cache_time=0,
    )


async def chosen_inline_result_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Chosen inline result handler

    Args:
        update: update
        context: context

    Returns:
        None
    """
    inline_message_id = update.chosen_inline_result.inline_message_id

    await asyncio.sleep(5)

    await app.bot.edit_message_text(
        inline_message_id=inline_message_id,
        text="I'm an updated message!",
        reply_markup={
            "inline_keyboard": [
                [
                    {
                        "text": "And even button updated!",
                        "url": "https://t.me/candyflipline",
                    }
                ]
            ]
        },
    )


app = ApplicationBuilder().token("{TOKEN}").build()

app.add_handler(InlineQueryHandler(inline_query_handler))
app.add_handler(ChosenInlineResultHandler(chosen_inline_result_handler))

app.run_polling()
