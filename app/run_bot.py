import asyncio

from app.telegram.bot import bot, dp


async def main():
    me = await bot.get_me()
    print(f"Bot started: @{me.username}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())