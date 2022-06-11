import os

import undetected_chromedriver as uc

from models.models import Proxy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Driver:
    def __init__(self, proxy: Proxy):
        self.proxy_host = "fproxy.site"#proxy.host
        self.proxy_port = 10120#1050
        self.proxy_user = "pABesC"#"D5wjXo"
        self.proxy_password = "URUN7eB9tAZ9"#"mdND08zT1b"

    def proxy_extension(self):
        manifest_json = """
                    {
                        "version": "1.0.0",
                        "manifest_version": 2,
                        "name": "Chrome Proxy",
                        "permissions": [
                            "proxy",
                            "tabs",
                            "unlimitedStorage",
                            "storage",
                            "<all_urls>",
                            "webRequest",
                            "webRequestBlocking"
                        ],
                        "background": {
                            "scripts": ["background.js"]
                        },
                        "minimum_chrome_version":"22.0.0"
                    }
                    """

        background_js = """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                      singleProxy: {
                        scheme: "http",
                        host: "%(host)s",
                        port: parseInt(%(port)d)
                      },
                      bypassList: ["localhost"]
                    }
                  };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%(user)s",
                        password: "%(pass)s"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
                """ % {
            "host": self.proxy_host,
            "port": self.proxy_port,
            "user": self.proxy_user,
            "pass": self.proxy_password,
        }

        plugin_path = os.path.join(BASE_DIR, f"temp")
        with open("temp/manifest.json",'w') as file:
            file.write(manifest_json)
        with open("temp/background.js",'w') as file:
            file.write(background_js)

        return plugin_path

    def driver_init(self):
        proxy_extension_path = self.proxy_extension()
        driver_options = uc.ChromeOptions()

        driver_options.add_argument("--start-maximized")
        driver_options.add_argument('--no-default-browser-check')
        driver_options.add_argument('--no-first-run')
        driver_options.add_argument('--disable-infobars')
        driver_options.add_argument(f"--load-extension={proxy_extension_path}")

        driver = uc.Chrome(
            options=driver_options,
            executable_path=os.path.join(BASE_DIR, "webdriver\\chromedriver.exe"),

        )

        return driver
