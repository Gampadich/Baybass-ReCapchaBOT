import asyncio
import random
from playwright.async_api import async_playwright
from speechToText import transcribe_audio

async def human_delay(min_sec=1, max_sec=3):
    await asyncio.sleep(random.uniform(min_sec, max_sec))

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            viewport=None
        )

        page = await context.new_page()

        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        await page.goto("https://www.google.com/recaptcha/api2/demo")

        await human_delay(2, 4)

        await page.wait_for_selector('iframe[title="reCAPTCHA"]')
        anchor_frame = None
        for frame in page.frames:
            if 'api2/anchor' in frame.url:
                anchor_frame = frame
                break

        if anchor_frame:
            await human_delay(1, 2)
            await anchor_frame.click('#recaptcha-anchor')

        await human_delay(2, 3)

        challenge_layout = page.frame_locator('iframe[title*="challenge"]')
        audioButton = challenge_layout.locator('#recaptcha-audio-button')

        if await audioButton.is_visible():
            await human_delay(1, 2)
            await audioButton.click()

        await human_delay(2, 3)

        download_link_locator = challenge_layout.locator('.rc-audiochallenge-tdownload-link')

        try:
            await download_link_locator.wait_for(state="attached", timeout=5000)
            audio_url = await download_link_locator.get_attribute('href')

            if audio_url:
                response = await page.request.get(audio_url)
                audio_bytes = await response.body()
                audio_filename = "captcha_audio.mp3"
                with open(audio_filename, "wb") as f:
                    f.write(audio_bytes)
            else:
                print("Атрибут href порожній.")
        except Exception as e:
            print(f"Помилка: Елемент завантаження не з'явився за 5 секунд. Деталі: {e}")

        text = transcribe_audio()
        print(f'Captcha text: {text}')

        await human_delay(3, 5)

        input_locator = challenge_layout.locator('#audio-response')

        try:
            await input_locator.wait_for(state="attached", timeout=5000)
            await input_locator.fill(text)
        except Exception as e:
            print(f'Cant find input: {e}')

        await human_delay(3, 5)

        verify_button = challenge_layout.locator('#recaptcha-verify-button')

        try:
            await verify_button.wait_for(state="attached", timeout=5000)
            await verify_button.click()
        except Exception as e:
            print(f'Cant find verify button: {e}')

        await human_delay(3, 5)

        submit_button = page.locator('#recaptcha-demo-submit')
        await submit_button.click()

        await human_delay(3, 5)

        success_text = page.locator('.recaptcha-success')

        if await success_text.is_visible():
            print('Success!')

        await page.wait_for_timeout(5000)
        await browser.close()


asyncio.run(main())