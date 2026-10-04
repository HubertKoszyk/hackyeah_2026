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
    """
    Generate a timestamp-based filename for a captured WorldCam frame.

    The filename contains the current date and time with millisecond
    precision and is created inside the specified output directory.

    Args:
        out_dir (str): Directory where the generated file path should point.

    Returns: str: Path to the generated PNG file.
    """

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")[:-3]
    return os.path.join(out_dir, f"worldcam_{ts}.png")


def enter_player_context(driver, timeout=20):
    """
    Find and enter the browser context containing the video player.
    The function first checks the current document for a <video> element.
    If none is found, it searches through available iframes until a video
    element is found or the timeout expires.

    Args:
        driver (webdriver.Chrome): Selenium WebDriver instance.
        timeout (int): Maximum number of seconds to search for the video.

    Returns: bool: True if a context containing a <video> element was found, otherwise False.
    """

    driver.switch_to.default_content()
    if driver.find_elements(By.TAG_NAME, "video"):
        return True

    #print("-> Looking for iframe with the player ...")
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
    """
    Wait until the video stream starts playing.
    The function periodically checks the <video> element's ready state,
    playback state, current playback time, and video dimensions.
    The stream is considered ready when it has valid dimensions, is not
    paused, and has played for more than 0.5 seconds.

    Args:
        driver (webdriver.Chrome): Selenium WebDriver instance.
        timeout (int): Maximum number of seconds to wait for the stream.

    Returns: bool: True if the stream started playing within the timeout, otherwise False.
    """

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
    Capture the current frame of the video and save it as a PNG image.
    The function first attempts to use Selenium's element screenshot functionality.
    If that fails, it attempts to draw the video onto a canvas and extract the image as a base64-encoded PNG.
    The canvas method may fail when the video is served from another origin and the canvas
    becomes security-tainted.

    Args:
        driver (webdriver.Chrome): Selenium WebDriver instance.
        path (str): Destination path for the PNG image.

    Returns: bool: True if a frame was successfully saved, otherwise False.
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
    Capture a single frame from a WorldCam live video stream.
    The function opens the specified WorldCam page using
    Selenium, handles the cookie dialog when present, locates the video player, waits for the
    stream to start, and captures the current video frame.
    The captured PNG is loaded into a NumPy array using OpenCV and the temporary PNG
    file is then removed. If an existing Selenium WebDriver is provided, it is reused
    instead of creating a new browser instance.

    Args:
        url (str): URL of the WorldCam live view page.
        output_path (str | None): Path where the temporary PNG frame should be saved. If None, a timestamped path is generated.
        out_dir (str): Directory used when generating an automatic output path.
        timeout (int): Maximum number of seconds to wait for the stream.
        headless (bool): Whether to run Chrome in headless mode when creating a new WebDriver.
        window_size (tuple[int, int]): Browser window width and height.
        driver (webdriver.Chrome | None): Optional existing Selenium WebDriver. If provided, a new driver is not created.
        quit_driver (bool): Whether to close the browser after the operation when the driver was created by this function.

        Returns: numpy.ndarray | None: Captured video frame as an OpenCV image array, or None if the frame
        could not be captured.

        Raises: ValueError: If the URL is empty or None.
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