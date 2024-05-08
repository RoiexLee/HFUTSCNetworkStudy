# HFUTSCNetworkStudy

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

[README CHINESE](./README_EN.md)
[README ENGLISH](./README_EN.md)

一个用于自动完成 HFUT 第二课堂网络学习模块的 Github 工作流，使用 GitHub Actions 和 Python，支持单选题、多选题和视频题

## 目录

- [安装](#安装)
- [使用](#使用)
- [徽章](#徽章)
- [相关工作](#相关工作)
- [维护者](#维护者)
- [证书](#证书)

## 安装

### 本地安装

你可以通过下述步骤进行本地安装

```shell
$ git clone https://github.com/RoiexLee/HFUTSCNetworkStudy.git
$ pip install -r requirements.txt
```

之后，你可以按照 [本地使用](#本地使用) 运行脚本

### GitHub Actions 安装

你同样也可以使用 Github Actions 安装本项目

查看 [GitHub Actions 使用](#github-actions-使用) 部分获得更多信息

## 使用

### 获得 key_session 和 secret

1. 安装 Fiddler 并且配置证书，这个过程可以参考 [这里](https://zhuanlan.zhihu.com/p/410150022)
2. 安装微信 PC 版并且进入 HFUT 第二课堂小程序，准备抓包
3. 登录并且进入网络学习模块，选择一篇文章点击进入，等待加载完毕退出，此时 key_session 和 secret 可以在某个记录中的 header 中查看，注意进入文章时才有 secret

   ![image](./images/key_session_and_secret.png)

### 本地使用

```shell
$ python checkin.py --key_session <key_session> --secret <secret> --page_max 1
```

### GitHub Actions 使用

1. Fork 这个仓库
2. 在仓库设置中添加 secrets，移动到 Fork 后的仓库，依次点击 `Settings > Secrets and variables > Actions > New Repository secret`
    - `KEY_SESSION`: 必须，`Secret` 填写 `key_session` 的值
    - `SECRET`: 必须，`Secret` 填写 `secret` 的值
3. Star Fork 之后的仓库以启动 GitHub Actions

## 徽章

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

## 相关工作

- [SecondClass](https://github.com/Zirconium233/SecondClass) - 一个用于自动完成 HFUT 第二课堂网络学习的 Python 脚本

## 维护者

[@RoiexLee](https://roiexlee.github.io)

## 证书

[GPL-3.0](./LICENSE) © [RoiexLee](https://roiexlee.github.io) 