import argparse
import json
import logging
import time

import requests
import urllib3

urllib3.disable_warnings()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Answer:

    def __init__(self, secret, key_session):
        self.url = "https://dekt.hfut.edu.cn"
        self.endpoint_page = "/scReports/api/wx/netlearning/page/{page}/{size}"
        self.endpoint_questions = "/scReports/api/wx/netlearning/questions/{article_id}"
        self.endpoint_answer = "/scReports/api/wx/netlearning/answer/{question_id}"

        self.session = requests.session()
        self.session.headers = {
            "Host": "dekt.hfut.edu.cn",
            "Connection": "keep-alive",
            "secret": secret,
            "key_session": key_session,
            "xweb_xhr": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wx1e3feaf804330562/99/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

    @staticmethod
    def get_permutations(nums):
        """
        Get all permutations of a list of numbers
        :param nums:
        :return:
        """
        result = []

        def backtrack(start, path):
            result.append(path[:])

            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()

        backtrack(0, [])
        return result

    def get_articles(self, page=1, size=10, colum_type="99"):
        endpoint_page = self.endpoint_page.format(page=page, size=size)
        # columType is for different categories, for example, 0 for learning new thoughts, 99 for latest
        data = {
            "category": "",
            "columnType": colum_type
        }
        try:
            res = self.session.post(url=self.url + endpoint_page, data=json.dumps(data))
            if res.status_code == 200:
                res_json = res.json()
                if res_json["code"] == "1005":
                    logger.info(res_json["errMsg"])
                    return None
                if res_json["code"] == "200":
                    return res_json["data"]["list"]
            res.raise_for_status()
        except requests.RequestException as e:
            logger.error(e)
            return None

    def study(self, article_id):
        """
        Study an article
        :param article_id:
        :return: 0 if failed, 1 if already reached today, 2 if already answered, 3 if no questions, 4 if successes
        """
        logger.info(f"Study article id: {article_id}")
        endpoint_questions = self.endpoint_questions.format(article_id=article_id)
        try:
            res_questions = self.session.get(url=self.url + endpoint_questions)
            if res_questions.status_code != 200:
                res_questions.raise_for_status()
        except requests.RequestException as e:
            logger.error(e)
            return 0

        res_questions_json = res_questions.json()
        if res_questions_json["data"]["todayReach"]:
            logger.info("Already reached today, skip")
            return 1
        if res_questions_json["data"]["accquieCredit"]:
            logger.info("Already answered, skip")
            return 2
        questions = res_questions_json["data"]["questions"]
        if len(questions) == 0:
            logger.info("No questions in this article")
            return 3
        for question in questions:
            endpoint_answer = self.endpoint_answer.format(question_id=question["id"])
            # que_type is 0 for single choice, 1 for multiple choice
            que_type = question["queType"]
            choices = [option["id"] for option in question["optionList"]]

            if que_type == 0:
                for choice in choices:
                    try:
                        res_answer = self.session.post(url=self.url + endpoint_answer, data=json.dumps([choice]))
                        if res_answer.status_code == 200:
                            desc = res_answer.json()["data"]["desc"]
                            if "恭喜" in desc:
                                logger.info("Answer successfully")
                                return 4
                            if "错误" in desc:
                                logger.info("Answer failed, continue")
                                continue
                        else:
                            res_answer.raise_for_status()
                    except requests.RequestException as e:
                        logger.error(e)
                        return 0
            elif que_type == 1:
                permutations = self.get_permutations(choices)
                # skip empty list
                for permutation in permutations[1:]:
                    try:
                        res_answer = self.session.post(url=self.url + endpoint_answer, data=json.dumps(permutation))
                        if res_answer.status_code == 200:
                            desc = res_answer.json()["data"]["desc"]
                            if "恭喜" in desc:
                                logger.info("Answer successfully")
                                return 4
                            if "错误" in desc:
                                logger.info("Answer failed, continue")
                                continue
                        else:
                            res_answer.raise_for_status()
                    except requests.RequestException as e:
                        logger.error(e)
                        return 0

    def run(self, page_max=1):
        for page in range(1, page_max + 1):
            logger.info(f"Search in page {page}")
            articles = self.get_articles(page)
            if articles is None:
                continue
            for article in articles:
                if article["correct"] == "已完成":
                    logger.info(f"Study article id: {article['id']}")
                    logger.info("Already answered, skip")
                    continue
                ret = self.study(article["id"])
                if ret == 1:
                    return
            logger.info(f"Search in page {page} finished")


parser = argparse.ArgumentParser()
parser.add_argument("--key_session", type=str, required=True, help="Key session")
parser.add_argument("--secret", type=str, required=True, help="Secret")
parser.add_argument("--page_max", type=int, default=1, help="Max page to search")
args = parser.parse_args()

if __name__ == "__main__":
    ans = Answer(secret=args.secret, key_session=args.key_session)
    ans.run(page_max=args.page_max)
