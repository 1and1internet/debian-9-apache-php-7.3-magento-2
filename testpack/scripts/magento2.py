#!/usr/bin/env python3

import unittest
from testpack_helper_library.unittests.dockertests import Test1and1Common
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
import time


class Test1and1Magnento2Image(Test1and1Common):

    @classmethod
    def setUpClass(cls):
        Test1and1Common.setUpClass(environment={"SKIPINSTALL": "true"})

    # <tests to run>

    def test_docker_logs(self):
        expected_log_lines = [
            "Process 'apache-2.4' changed state to 'STARTING'",
            "Unpacking latest magento2 into /var/www/html"
        ]
        container_logs = self.logs()
        for expected_log_line in expected_log_lines:
            self.assertTrue(
                container_logs.find(expected_log_line) > -1,
                msg="Docker log line missing: %s from (%s)" % (expected_log_line, container_logs)
            )

    def test_php73_cli(self):
        self.assertPackageIsInstalled("php7.3-cli")

    def test_default_app(self):
        # Wait for magento to be unpacked before testing
        time.sleep(5)
        driver = self.getChromeDriver()
        url = "%s/setup/#/landing-install" % Test1and1Common.endpoint
        driver.get(url)
        print("TITLE1", driver.title)
        try:
            WebDriverWait(driver, 60).until(expected_conditions.title_contains('Magento'))
        except TimeoutException:
            pass
        print("TITLE2", driver.title)
        self.assertTrue(driver.title.find('Magento') > -1, msg="App not available")

    # </tests to run>

if __name__ == '__main__':
    unittest.main(verbosity=1)
