import asyncio
from playwright.async_api import async_playwright

PHONE_NUMBER = '32537795'
EMAIL        = 'gakyumya992@mirai.re'
PLATFORM     = 'Android'
MESSAGE      = 'Halo, saya ingin menanyakan tentang akun WhatsApp saya. Mohon bantuan tim support segera terima kasih.'
URL          = 'https://www.whatsapp.com/contact/noclient'

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        page = await browser.new_page(viewport={'width': 1280, 'height': 2000})

        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
        })

        print('[*] Membuka halaman...')
        await page.goto(URL, wait_until='networkidle')
        await page.wait_for_timeout(3000)

        print('[*] Mengisi nomor...')
        all_inputs = page.locator('input:not([type="radio"])')
        await all_inputs.nth(0).fill(PHONE_NUMBER)

        print('[*] Mengisi email...')
        await all_inputs.nth(1).fill(EMAIL)
        await all_inputs.nth(2).fill(EMAIL)

        print('[*] Memilih platform...')
        await page.get_by_label(PLATFORM).check()

        print('[*] Mengisi pesan...')
        await page.locator('textarea').first.fill(MESSAGE)

        await page.wait_for_timeout(1500)

        print('[*] Klik Next Step...')
        await page.get_by_role('button', name='Next Step').click()
        await page.wait_for_timeout(4000)

        await page.screenshot(path='hasil_submit.png', full_page=True)
        print('[+] Selesai! Screenshot: hasil_submit.png')

        await browser.close()

asyncio.run(run_bot())
