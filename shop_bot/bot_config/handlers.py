from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.types.successful_payment import SuccessfulPayment
import shop_bot.database.requests as rq
import shop_bot.bot_config.keyboards as kb
from shop_bot.bot_config.bot import bot

router = Router()

PAYMENT_TOKEN = "2051251535:TEST:OTk5MDA4ODgxLTU"


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(
        "✨ Hello! I'm your Magic Brews bot 🧙‍♂️.\n"
        "I have a cauldron full of magical potions!\n"
        "Choose the category of potion you need 🐍: \n",
        reply_markup=await kb.inline_categories()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Some help text")


@router.callback_query(F.data.startswith("category_"))
async def category_items(callback: CallbackQuery):
    await callback.answer("You made your choice! ✨🌟")
    await callback.message.answer(
        text="Chose the potion you need 🧪",
        reply_markup=await kb.inline_items(int(callback.data.split("_")[1]))
    )


class Handler(StatesGroup):
    item_id = State()
    item_price = State()


@router.callback_query(F.data.startswith("item_"))
async def item(callback: CallbackQuery):
    item_data = await rq.get_item(int(callback.data.split("_")[1]))

    await callback.answer("Excellent pick! ✨")
    await callback.message.answer(
        text=f"__Name__\n"
             f"{item_data.name}\n\n"
             f"__Description__\n"
             f"🪄{item_data.description}\n\n"
             f"Price: $ {item_data.price}",
        reply_markup=await kb.item_details(item_data.id)
    )


@router.callback_query(F.data.startswith("back_"))
async def back_to_categories(callback: CallbackQuery):
    await callback.answer("Return to the Magic Brews Menu... 🍵")
    await callback.message.answer(
        text="Chose the potion you need 🧪",
        reply_markup=await kb.inline_categories()
    )


@router.callback_query(F.data.startswith("to_pay"))
async def to_pay(callback: CallbackQuery):
    item_data = await rq.get_item(int(callback.data.split("_")[-1]))
    await callback.answer("Processing your payment...")

    item_price = calculate_price(item_data.price)

    prices = [
        LabeledPrice(label="item", amount=int(item_price * 100)),
    ]

    await bot.send_invoice(
        callback.message.chat.id,
        title="Buying a magic brew...",
        description=item_data.name,
        provider_token="2051251535:TEST:OTk5MDA4ODgxLTU",
        currency="USD",
        photo_url="https://img.freepik.com/premium-vector/magic-cauldron-flat-illustration_44769-59.jpg",
        photo_width=600,
        photo_height=468,
        is_flexible=False,
        prices=prices,
        payload="test-invoice-payload")


def calculate_price(price_in_usd_str: str) -> float:
    return float(price_in_usd_str)


@router.pre_checkout_query(lambda query: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
