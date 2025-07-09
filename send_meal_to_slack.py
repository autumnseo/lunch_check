#!/usr/bin/env python3
"""
CJ Freshmeal API를 통해 식단 정보를 가져와서 Slack으로 전송하는 스크립트
매일 오전 7시 KST에 실행되도록 GitHub Actions로 스케줄링
"""

import requests
import datetime
import json
import os
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """메인 실행 함수"""
    try:
        # 슬랙 Webhook URL (GitHub Secrets로 관리)
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        
        if not slack_webhook_url:
            logger.error("SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
            return
        
        # 오늘 날짜 (KST 기준, GitHub Actions는 UTC이므로 9시간 더함)
        today = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y%m%d')
        
        # API 호출 URL (storeIdx는 학교별로 다를 수 있음)
        store_idx = os.getenv("STORE_IDX", "6655")  # 기본값 설정
        url = f"https://front.cjfreshmeal.co.kr/meal/v1/today-all-meal?storeIdx={store_idx}&mealDt={today}&reqType=total"
        
        logger.info(f"식단 정보 조회 중: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            logger.info("API 호출 성공")
        except Exception as e:
            error_message = f"❌ 식단 불러오기 실패: {e}"
            logger.error(error_message)
            requests.post(slack_webhook_url, json={"text": error_message})
            raise
        
        # 슬랙 메시지 생성
        message_blocks = []
        
        for meal in data.get('data', []):
            meal_time = meal.get("mealTimeName", "식사")
            menus = ", ".join([item["menuName"] for item in meal.get("menus", [])])
            message_blocks.append(f"*{meal_time}*\n{menus}")
        
        if not message_blocks:
            final_message = "오늘은 등록된 식단 정보가 없습니다."
        else:
            final_message = "\n\n".join(message_blocks)
        
        # 슬랙 전송
        payload = {
            "text": f"🍱 *오늘의 식단 ({today})*\n\n{final_message}",
            "username": "🍽️ 급식 알리미",
            "icon_emoji": ":fork_and_knife:"
        }
        
        response = requests.post(slack_webhook_url, json=payload, timeout=30)
        response.raise_for_status()
        
        logger.info("Slack 메시지 전송 완료!")
        
    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {e}")
        raise

if __name__ == "__main__":
    main() 