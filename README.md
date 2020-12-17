# selenoid web自动化远程执行器使用实践
demo地址：https://github.com/xglh/selenoid_demo
## 一、简介
selenoid是一款开源的web自动化远程执行器，与seleium grid功能类似，具有seleium grid不具备的实时画面和录屏的优点，具体对比如下 

| 对比项 | seleium grid| selenoid |
| ------ | ------ | ------ |
| 实时预览 | N | Y |
| 录屏 | N | Y |
| 多版本浏览器 | Y | Y |
| 资源回收 | N | Y |
| 支持分布式 | Y | N |
除了不支持分布式，其他项都优于seleium grid

## 二、环境部署
依赖模块：docker、docker-compose
### 1、配置browsers.json
```python
{
  "chrome": {
    "default": "85.0",
    "versions": {
      "85.0": {
        "image": "selenoid/vnc:chrome_85.0",
        "port": "4444",
        "path": "/"
      }
    }
  },
  "firefox": {
    "default": "79.0",
    "versions": {
      "79.0": {
        "image": "selenoid/vnc:firefox_79.0",
        "port": "4444",
        "path": "/wd/hub"
      }
    }
  },
  "opera": {
    "default": "70.0",
    "versions": {
      "70.0": {
        "image": "selenoid/vnc:opera_70.0",
        "port": "4444",
        "path": "/"
      }
    }
  }
}


```
### 2、配置docker-compose编排文件
保存为docker-compose.yml，与browsers.json放在同一目录下
```python
version: '3'
services:
  selenoid:
    image: "aerokube/selenoid"
    network_mode: bridge
    restart: always
    ports:
      - "4444:4444"
    volumes:
      - "$PWD:/etc/selenoid/" # assumed current dir contains browsers.json
      - "$PWD/video/:/opt/selenoid/video/" # 
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "$PWD/logs/:/opt/selenoid/logs/"
    # 录屏保存地址
    environment: 
      - OVERRIDE_VIDEO_OUTPUT_DIR=$PWD/video/
    # limit为允许开启实例最大值
    command: -limit 10 -service-startup-timeout 1m -retry-count 3 -enable-file-upload -log-output-dir /opt/selenoid/logs
 
  selenoid-ui:
    image: "aerokube/selenoid-ui"
    network_mode: bridge
    restart: always
    links:
      - selenoid
    ports:
      - "8080:8080"
    command: ["--selenoid-uri", "http://selenoid:4444"]

```
### 3、拉取浏览器镜像与录屏工具镜像
```python
docker pull selenoid/vnc:chrome_85.0
docker pull selenoid/vnc:firefox_79.0
docker pull selenoid/vnc:opera_70.0
docker pull selenoid/video-recorder:latest-release
```
### 4、启动docker-compose
```python
docker-compose -f docker-compose.yml
```
### 5、打开selenoid控制台
http://ip:4444

## 三、接入web自动化
```python
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
            "version": "85.0",
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

    def test_baidu_opera(self):
        capabilities = {
            # 测试用例名称
            "name": "test_baidu_opera",
            # 浏览器类型
            "browserName": "opera",
            # 版本号
            "version": "79.0",
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
```

## 四、接入多版本浏览器
### 1、docker接入
chrome支持48.0~78.0[版本](https://hub.docker.com/r/selenoid/vnc_chrome/tags?page=1&ordering=last_updated)  
firefox支持3.6~83.0[版本](https://hub.docker.com/r/selenoid/vnc_firefox/tags?page=1&ordering=last_updated)  
opera支持33.0~72.0[版本](https://hub.docker.com/r/selenoid/vnc_opera/tags?page=1&ordering=last_updated)  
找到对应版本号，pull镜像，并将版本号加入到browsers.json中
### 2、非docker接入
以IE为例
#### 1)、下载[IEDriverServer](http://www.seleniumhq.org/download/)
#### 2)、下载[selenoid_win_amd64.exe](https://github.com/aerokube/selenoid/releases/latest)
#### 3)、配置browsers.json
```python
{
  "internet explorer": {
    "default": "11",
    "versions": {
      "11": {
        "image": ["C:\\IEDriverServer.exe", "--log-level=DEBUG"]
      }
    }
  }
}
```
#### 4)、启动Selenoid
```python
./selenoid_win_amd64.exe -conf ./browsers.json -disable-docker
```
#### 5)、打开hub测试地址
http://localhost:4444/wd/hub  
备注：其他类型浏览器找到对应驱动即可，目前已接入ie，qq，360浏览器