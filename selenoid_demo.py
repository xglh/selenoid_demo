#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/17 20:10
# @Author : liuhui
# @desc :
import time
from selenium import webdriver


class TestClass:

    def test_baidu_chrome(self):
        capabilities = {
            # 测试用例名称
            "name": "test_baidu_chrome",
            # 浏览器类型
            "browserName": "chrome",
            # 版本号
            "version": "",
            # 开启远程VNC实时画面
            "enableVNC": True,
            # 开启视频录制
            "enableVideo": True,
            # 保存视频名称
            "videoName": "test_baidu_chrome.mp4"
        }
        driver = webdriver.Remote(
            command_executor="http://10.118.80.65:4444/wd/hub",
            desired_capabilities=capabilities)

        driver.get('https://www.baidu.com')
        driver.find_element_by_id('kw').send_keys('selenoid')
        time.sleep(2)
        driver.quit()

    def test_baidu_firefox(self):
        capabilities = {
            # 测试用例名称
            "name": "test_baidu_firefox",
            # 浏览器类型
            "browserName": "firefox",
            # 版本号
            "version": "79.0",
            # 开启远程VNC实时画面
            "enableVNC": True,
            # 开启视频录制
            "enableVideo": True,
            # 保存视频名称
            "videoName": "test_baidu_firefox.mp4"
        }
        driver = webdriver.Remote(
            command_executor="http://10.118.80.65:4444/wd/hub",
            desired_capabilities=capabilities)

        driver.get('https://www.baidu.com')
        driver.find_element_by_id('kw').send_keys('selenoid')
        time.sleep(2)
        driver.quit()

    def test_baidu_opera(self):
        capabilities = {
            # 测试用例名称
            "name": "test_baidu_opera",
            # 浏览器类型
            "browserName": "opera",
            # 版本号
            "version": "70.0",
            # 开启远程VNC实时画面
            "enableVNC": True,
            # 开启视频录制
            "enableVideo": True,
            # 保存视频名称
            "videoName": "test_baidu_opera.mp4",
            # opera浏览器需要额外参数
            "operaOptions": {"binary": "/usr/bin/opera"}
        }
        driver = webdriver.Remote(
            command_executor="http://10.118.80.65:4444/wd/hub",
            desired_capabilities=capabilities)

        driver.get('https://www.baidu.com')
        driver.find_element_by_id('kw').send_keys('selenoid')
        time.sleep(2)
        driver.quit()
