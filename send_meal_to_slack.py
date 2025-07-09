#!/usr/bin/env python3
"""
CJ Freshmeal API를 통해 식단 정보를 가져와서 Slack으로 전송하는 스크립트 (Bot Token 방식)
매일 오전 7시 KST에 실행되도록 GitHub Actions로 스케줄링
"""

import requests
import datetime
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
        # Slack Bot Token 및 채널명 환경 변수
        slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
        slack_channel = "#점메방"
        
        if not slack_bot_token:
            logger.error("SLACK_BOT_TOKEN 환경 변수가 설정되지 않았습니다.")
            return
        
        # 오늘 날짜 (KST 기준, GitHub Actions는 UTC이므로 9시간 더함)
        today = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y%m%d')
        
        # store_idx를 6655로 하드코딩
        store_idx = "6655"
        url = f"https://front.cjfreshmeal.co.kr/meal/v1/today-all-meal?storeIdx={store_idx}&mealDt={today}&reqType=total"
        
        logger.info(f"식단 정보 조회 중: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            logger.info("API 호출 성공")
            logger.info(f"API 응답 데이터: {data}")  # 디버깅용 로그
        except Exception as e:
            error_message = f"❌ 식단 불러오기 실패: {e}"
            logger.error(error_message)
            send_slack_message(slack_bot_token, slack_channel, error_message)
            raise
        
        # 슬랙 메시지 생성
        message_blocks = []
        
        # 데이터 구조 확인 및 안전한 처리
        meal_data = data.get('data', {})
        logger.info(f"식단 데이터 타입: {type(meal_data)}")
        
        if isinstance(meal_data, dict):
            # 식사 시간별로 메뉴 처리
            meal_time_names = {
                '1': '🌅 아침',
                '2': '☀️ 점심', 
                '3': '🌙 저녁'
            }
            
            for meal_code, meal_list in meal_data.items():
                meal_time_name = meal_time_names.get(meal_code, f"식사 {meal_code}")
                
                if isinstance(meal_list, list) and meal_list:
                    menu_items = []
                    for meal in meal_list:
                        if isinstance(meal, dict):
                            main_dish = meal.get('name', '')
                            side_dishes = meal.get('side', '')
                            corner = meal.get('corner', '')
                            
                            menu_text = main_dish
                            if side_dishes:
                                menu_text += f" + {side_dishes}"
                            if corner:
                                menu_text += f" ({corner})"
                            
                            menu_items.append(menu_text)
                    
                    if menu_items:
                        message_blocks.append(f"*{meal_time_name}*\n• " + "\n• ".join(menu_items))
                else:
                    message_blocks.append(f"*{meal_time_name}*\n• 메뉴 정보 없음")
        else:
            logger.warning(f"식단 데이터가 딕셔너리가 아님: {type(meal_data)}")
            message_blocks.append(f"*식단 정보*\n{str(meal_data)}")
        
        if not message_blocks:
            final_message = "오늘은 등록된 식단 정보가 없습니다."
        else:
            final_message = "\n\n".join(message_blocks)
        
        # 슬랙 전송
        text = f"🍱 *오늘의 식단 ({today})*\n\n{final_message}"
        send_slack_message(slack_bot_token, slack_channel, text)
        logger.info("Slack 메시지 전송 완료!")
        
    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {e}")
        raise

def send_slack_message(token, channel, text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": text,
        "username": "🍽️ 급식 알리미",
        "icon_emoji": ":fork_and_knife:"
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    if not response.ok or not response.json().get("ok", False):
        logging.error(f"Slack 메시지 전송 실패: {response.text}")
    return response

if __name__ == "__main__":
    main() 