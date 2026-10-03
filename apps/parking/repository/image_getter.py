from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from datetime import datetime
import time
import sys
import os
import cv2


DEFAULT_TEST_URL = "https://www.worldcam.pl/liveview/36999"
DEFAULT_OUT_DIR  = "."

def _generate_filename(out_dir=DEFAULT_OUT_DIR):
    """Return a path like ./worldcam_2026-10-03_14-52-07_482.png"""
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")[:-3]
    return os.path.join(out_dir, f"worldcam_{ts}.png")


def enter_player_context(driver, timeout=20):
    driver.switch_to.default_content()
    if driver.find_elements(By.TAG_NAME, "video"):
        return True

    print("-> Looking for iframe with the player ...")
    end = time.time() + timeout
    while time.time() < end:
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for i, fr in enumerate(iframes):
            try:
                driver.switch_to.frame(fr)
                if driver.find_elements(By.TAG_NAME, "video"):
                    print(f"   video found in iframe #{i}")
                    return True
            except WebDriverException:
                pass
            driver.switch_to.default_content()
        time.sleep(1)

    print("   no iframe with <video> found")
    return False


def wait_for_stream(driver, timeout=60):
    print(f"-> Waiting for stream (max {timeout}s) ...")
    end = time.time() + timeout
    while time.time() < end:
        try:
            s = driver.execute_script("""
                const v = document.querySelector('video');
                if (!v) return {found:false};
                return {found:true, readyState:v.readyState, paused:v.paused,
                        currentTime:v.currentTime, w:v.videoWidth, h:v.videoHeight};
            """)
            if s and s.get("found") and s["w"] > 0:
                print(f"   video readyState={s['readyState']} paused={s['paused']} "
                      f"t={s['currentTime']:.2f}s size={s['w']}x{s['h']}")
                if s["readyState"] >= 2 and not s["paused"] and s["currentTime"] > 0.5:
                    print("   stream is playing")
                    return True
        except Exception as e:
            print("   (info)", e)
        time.sleep(2)
    print("   stream did not start in time")
    return False


def grab_video_frame(driver, path):
    """
    Save one <video> frame as PNG.
    1) tries element.screenshot()  <- works even for cross-origin
    2) fallback: canvas -> base64  <- works only for same-origin
    """
    video = driver.find_element(By.TAG_NAME, "video")

    try:
        if os.path.exists(path):
            os.remove(path)
        video.screenshot(path)
        size = os.path.getsize(path)
        if size > 1000:
            print(f"   [element.screenshot] saved: {path} ({size // 1024} KB)")
            return True
        print(f"   [element.screenshot] file only {size} B - trying canvas")
    except Exception as e:
        print("   [element.screenshot] error:", e)

    try:
        import base64
        data_url = driver.execute_script("""
            const v = document.querySelector('video');
            if (!v || !v.videoWidth) return null;
            const c = document.createElement('canvas');
            c.width = v.videoWidth; c.height = v.videoHeight;
            c.getContext('2d').drawImage(v, 0, 0, c.width, c.height);
            try { return c.toDataURL('image/png'); }
            catch (e) { return null; }
        """)
        if data_url and data_url.startswith("data:image/png;base64,"):
            raw = base64.b64decode(data_url.split(",", 1)[1])
            with open(path, "wb") as f:
                f.write(raw)
            print(f"   [canvas] saved: {path} ({len(raw) // 1024} KB)")
            return True
        print("   [canvas] tainted / no data - skipping")
    except Exception as e:
        print("   [canvas] error:", e)

    return False

def get_image(url,
              output_path=None,
              out_dir=DEFAULT_OUT_DIR,
              timeout=60,
              headless=True,
              window_size=(1920, 1080),
              driver=None,
              quit_driver=True):
    """
    Open a WorldCam live view page and save one frame from the stream.

    Args:
        url:          page URL (required) - e.g. "https://www.worldcam.pl/liveview/36999"
        output_path:  full path for the PNG. If None, a timestamped name is
                      generated automatically in 'out_dir'.
        out_dir:      directory for auto-generated filenames (default: ".")
        timeout:      max seconds to wait for the stream (default: 60)
        headless:     run Chrome in headless mode (default: True)
        window_size:  (width, height) of the browser window
        driver:       optional already-created Selenium WebDriver.
                      If provided, the function will NOT create a new one.
        quit_driver:  if True, close the browser after the call.
                      Ignored when 'driver' was passed in.

    Returns:
        str   absolute path to the saved PNG, or
        None  on failure.
    """
    if not url:
        raise ValueError("url is required")

    if output_path is None:
        output_path = _generate_filename(out_dir)

    own_driver = driver is None

    if own_driver:
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--mute-audio")
        options.add_argument("--disable-notifications")
        options.add_argument("--autoplay-policy=no-user-gesture-required")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=options)
        driver.execute_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
        driver.set_window_size(*window_size)

    try:
        print(f"-> Opening: {url}")
        driver.get(url)
        time.sleep(3)

        try:
            b = WebDriverWait(driver, 4).until(
                lambda d: d.find_element(
                    By.XPATH,
                    "//button[contains(., 'Akceptuj') or contains(., 'Zgadzam') "
                    "or contains(., 'Rozumiem') or contains(., 'Accept') "
                    "or contains(., 'Agree')]"))
            driver.execute_script("arguments[0].click();", b)
            print("   cookies OK")
            time.sleep(1)
        except Exception:
            pass

        if not enter_player_context(driver, timeout=20):
            print("   no iframe with the player found")
            driver.save_screenshot("worldcam_error.png")
            return None

        try:
            play = driver.find_element(By.CSS_SELECTOR, "div.play-wrapper")
            if play.is_displayed():
                driver.execute_script("arguments[0].click();", play)
                print("   play clicked")
        except Exception:
            pass

        if not wait_for_stream(driver, timeout=timeout):
            print("   stream did not start - trying to grab a frame anyway")

        time.sleep(0.5)
        ok = grab_video_frame(driver, output_path)

        if ok:
            image = cv2.imread(output_path)
            os.remove(output_path)

            if image is None:
                print("   failed to read the saved frame")
                return None
            return image

        print("   failed to save the video frame")
        return None

    except Exception as e:
        print("   error:", repr(e))
        try:
            driver.save_screenshot("worldcam_error.png")
            print("   worldcam_error.png")
        except Exception:
            pass
        return None

    finally:
        if own_driver and quit_driver:
            driver.quit()
            print("-> Done.")


if __name__ == "__main__":
    result = get_image(DEFAULT_TEST_URL)
    if result is not None:
        print(f"OK -> shape {result.shape}")
        sys.exit(0)
    print("FAILED")
    sys.exit(1)