# vai sincrono mesmo, projeto simplisinho
from playwright.sync_api import sync_playwright
import pandas as pd
import os

# função base


def quote_scraper(base_url: str = "https://quotes.toscrape.com/"):
    with sync_playwright() as p:
        # iniciar browser
        browser = p.chromium.launch(headless=False)
        # iniciar a pagina
        page = browser.new_page()
        # evitar travamento
        page.set_default_timeout(10000)

        # acessar a url foda lá de teste
        print(f"Acessing: {base_url}")
        page.goto(base_url)

        lista = []

        while True:
            # esperar quotes carregarem (já q vão ser extraidas)
            print("Waitings for quotes...")
            page.wait_for_selector(".quote")

            # extrair as parada agora (quotes)
            print("Scraping quotes...")
            quotes = page.locator(".quote")

            quotes_count = quotes.count()
            for i in range(quotes_count):
                # seleciona o quote da posição i #nth serve pra selecionar o elemtno da posição i
                quote = quotes.nth(i)
                # pegar o texto do elemento text
                texto = quote.locator(".text").inner_text()
                autor = quote.locator(".author").inner_text()

                lista.append({"text": texto, "author": autor})

            # tentar ver se tem mais paginas
            next_bot = page.locator("a:has-text('Next')")

            # se o botãp n existir a pagina acabou, n sobrou nada 😢
            if next_bot.count() == 0:
                print("No more pages found.")
                break

            # se existir, clica e espera carregar
            print("Next page...")
            next_bot.first.click()
            page.wait_for_selector(".quote")

        # fechar o navegador
        browser.close()

    # fazer o dataframe foda lá
    df = pd.DataFrame(lista)

    os.makedirs("data", exist_ok=True)

    # passar o dataframe pra arquivo csv
    output_path = os.path.join("data", "quotes.csv")
    df.to_csv(output_path, index=False)
    print("Scraping completed! Quotes saved in quotes.csv")


quote_scraper()
