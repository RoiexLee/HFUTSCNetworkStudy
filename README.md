# GladosAutoCheckin

A GitHub workflow to check in Glados automatically uses GitHub Actions and Python.

## Table of Contents

- [Usage](#usage)
- [License](#license)

## Usage

1. Fork this repository.
2. Add the following secrets in the repository settings.
   - `COOKIES`: Required, your Glados Cookies.
     - Firstly, log in [Glados](https://glados.rocks/) and visit [Glados Checkin](https://glados.rocks/console/checkin).
     - Secondly, press `F12` to open the developer tools, clicking on the Network tab and pressing `ctrl` and `r` to refreshing the page.
     - Thirdly, find the request with the name `checkin` and copy the value of the `Cookie` header.
     - Fourthly, move to GitHub respiratory `Settings > Secrets and variables > Actions > New Repository secret`, the `Name` is `COOKIES` and the `Sercret` is the value of the `Cookie` header.
     - Note, `COOKIES` support multiple cookies, they should be split with `&`.
     
   ![image](./images/image.png)

   - `TOKEN`: Optional, your PushDeer token.
     - You can get it from [PushDeer](https://www.pushdeer.com/product.html).
3. Star the repository you Forked.

## License

[GPL-3.0](./LICENSE) © [RoiexLee](https://roiexlee.github.io) 