from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://www.tokopedia.com/"
SEARCH_KEYWORD = "mouse wireless"


def setup_driver():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(), options=options)
    wait = WebDriverWait(driver, 25)
    return driver, wait


def close_popup_if_present(driver):
    popup_selectors = [
        (By.CSS_SELECTOR, "button[aria-label='Tutup']"),
        (By.CSS_SELECTOR, "button[aria-label='Close']"),
        (By.CSS_SELECTOR, "div[role='dialog'] button"),
    ]

    for by, selector in popup_selectors:
        try:
            close_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((by, selector))
            )
            close_button.click()
            return
        except TimeoutException:
            continue
        except Exception:
            continue


def print_result(step_number, description, status):
    print(f"{step_number}. {description} -> {status}")


def pause_step(message):
    input(f"\n{message}\nTekan Enter di terminal setelah selesai...")


def get_visible_element(driver, locators):
    for by, selector in locators:
        elements = driver.find_elements(by, selector)
        for element in elements:
            if element.is_displayed():
                return element
    return None


def element_exists(driver, locators):
    return get_visible_element(driver, locators) is not None


def switch_to_latest_window(driver):
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])


def run_tokopedia_scenarios():
    driver, wait = setup_driver()

    try:
        # Test 1: membuka halaman web
        driver.get(BASE_URL)
        close_popup_if_present(driver)
        wait.until(lambda d: "tokopedia" in d.title.lower())
        print_result(1, "Membuka halaman web Tokopedia", "BERHASIL")

        # Test 2: login akun sampai berhasil
        pause_step("Langkah 2: lakukan login akun Tokopedia sampai benar-benar berhasil masuk.")
        logged_in_indicators = [
            (By.XPATH, "//*[contains(text(), 'Akun')]"),
            (By.XPATH, "//*[contains(text(), 'Profil')]"),
            (By.XPATH, "//*[contains(text(), 'Pesanan')]"),
            (By.XPATH, "//*[contains(text(), 'Wishlist')]"),
            (By.CSS_SELECTOR, "img[alt*='profile']"),
            (By.CSS_SELECTOR, "img[alt*='avatar']"),
            (By.CSS_SELECTOR, "[data-testid*='headerUser']"),
        ]
        assert element_exists(driver, logged_in_indicators) or "login" not in driver.current_url.lower()
        print_result(2, "Login akun Tokopedia", "BERHASIL")

        # Test 3: ketik produk pada kolom pencarian
        pause_step(f"Langkah 3: ketik '{SEARCH_KEYWORD}' pada kolom pencarian.")
        search_box = get_visible_element(
            driver,
            [
                (By.NAME, "q"),
                (By.CSS_SELECTOR, "input[type='search']"),
                (By.CSS_SELECTOR, "input[placeholder*='Cari']"),
            ],
        )
        assert search_box is not None
        assert search_box.get_attribute("value").strip().lower() == SEARCH_KEYWORD.lower()
        print_result(3, "Mengetik produk pada kolom pencarian", "BERHASIL")

        # Test 4: tekan enter lalu masuk ke halaman produk yang dicari
        pause_step("Langkah 4: tekan Enter sampai masuk ke halaman hasil pencarian produk.")
        wait.until(lambda d: "search" in d.current_url.lower() or "q=" in d.current_url.lower())
        product_list = get_visible_element(
            driver,
            [
                (By.CSS_SELECTOR, "a[data-testid='lnkProductContainer']"),
                (By.CSS_SELECTOR, "div[data-testid='divSRPContentProducts'] a"),
                (By.CSS_SELECTOR, "a[href*='tokopedia.com/']"),
            ],
        )
        assert product_list is not None
        print_result(4, "Masuk ke halaman hasil pencarian produk", "BERHASIL")

        # Test 5: klik salah satu produk dari hasil pencarian
        pause_step("Langkah 5: klik salah satu produk dari hasil pencarian sampai halaman detail produk terbuka.")
        switch_to_latest_window(driver)
        wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "h1")) > 0)
        product_title = get_visible_element(driver, [(By.CSS_SELECTOR, "h1")])
        assert product_title is not None
        print_result(5, "Membuka halaman detail produk", "BERHASIL")

        # Test 6: melihat harga produk
        pause_step("Langkah 6: lihat informasi harga produk.")
        price_info = get_visible_element(
            driver,
            [
                (By.XPATH, "//*[contains(text(), 'Rp')]"),
                (By.CSS_SELECTOR, "[data-testid='lblPDPDetailProductPrice']"),
            ],
        )
        assert price_info is not None
        print_result(6, "Melihat harga produk", "BERHASIL")

        # Test 7: melihat gambar produk
        pause_step("Langkah 7: lihat gambar produk pada halaman detail.")
        product_image = get_visible_element(
            driver,
            [
                (By.CSS_SELECTOR, "img"),
                (By.XPATH, "//img[contains(@src, 'tokopedia')]"),
            ],
        )
        assert product_image is not None
        print_result(7, "Melihat gambar produk", "BERHASIL")

        # Test 8: klik tambah ke troli
        pause_step("Langkah 8: klik tombol Tambah ke Troli atau Keranjang pada halaman detail produk.")
        cart_indicators = [
            (By.XPATH, "//*[contains(text(), 'Keranjang')]"),
            (By.XPATH, "//*[contains(text(), 'Troli')]"),
            (By.XPATH, "//*[contains(text(), 'ditambahkan')]"),
            (By.XPATH, "//*[contains(text(), 'berhasil')]"),
        ]
        assert element_exists(driver, cart_indicators)
        print_result(8, "Klik tambah ke troli", "BERHASIL")

        # Test 9: buka halaman keranjang
        pause_step("Langkah 9: buka halaman keranjang atau troli.")
        wait.until(lambda d: "cart" in d.current_url.lower() or "keranjang" in d.page_source.lower())
        print_result(9, "Membuka halaman keranjang", "BERHASIL")

        # Test 10: memastikan barang terlihat di keranjang
        pause_step("Langkah 10: pastikan barang yang dipilih terlihat di halaman keranjang.")
        cart_item = get_visible_element(
            driver,
            [
                (By.CSS_SELECTOR, "[class*='cart-item']"),
                (By.CSS_SELECTOR, "[class*='CartItem']"),
                (By.XPATH, "//*[contains(text(), 'mouse')]"),
                (By.XPATH, "//*[contains(text(), 'wireless')]"),
            ],
        )
        assert cart_item is not None
        print_result(10, "Melihat barang pada halaman keranjang", "BERHASIL")

    except Exception as error:
        print(f"Pengujian gagal: {error}")

    finally:
        driver.quit()
        print("Browser ditutup.")


if __name__ == "__main__":
    run_tokopedia_scenarios()
