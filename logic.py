import random, asyncio, aiohttp
from openai import AsyncOpenAI
from config import OPENAI_API_KEY, CRYPTO_BOT_TOKEN

# Инициализируем асинхронный клиент OpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class AIService:
    @staticmethod
    async def consult(prompt):
        """Интеграция с ChatGPT для консультаций и квестов"""
        try:
            response = await client.chat.completions.create(
                model="gpt-4o", # Можно заменить на gpt-3.5-turbo для экономии
                messages=[
                    {"role": "system", "content": "Ты — ИИ-модуль управления Empire OS. Твоя цель — помогать пользователям и модерировать биржу. Отвечай кратко, властно и по делу."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Ошибка нейрочипа: {str(e)}"

    @staticmethod
    async def verify_p2p_lot(title):
        """ИИ-модерация лота через ChatGPT"""
        prompt = f"Проверь название товара: '{title}'. Если это спам, наркотики или мошенничество, ответь 'BLOCK'. Если всё ок, ответь 'OK'."
        res = await AIService.consult(prompt)
        return "OK" in res.upper()

class PaymentService:
    # (Оставляем без изменений, так как это CryptoBot)
    @staticmethod
    async def create_invoice(amount):
        url = "https://pay.crypt.bot/api/createInvoice"
        headers = {'Crypto-Pay-API-Token': CRYPTO_BOT_TOKEN}
        payload = {'asset': 'USDT', 'amount': str(amount)}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                data = await resp.json()
                return data['result']['pay_url'], data['result']['invoice_id']

class Games:
    @staticmethod
    def slots():
        syms = ["💎", "🎰", "💰", "🍒"]
        res = [random.choice(syms) for _ in range(3)]
        is_win = res[0] == res[1] == res[2]
        return res, is_win