from google import genai
import os
import sys
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드 (있으면 자동 반영)
load_dotenv()


def main() -> None:
    """GEMINI_API_KEY를 확인하고, 간단한 요청을 보낸 뒤 결과를 출력합니다."""

    # 환경변수에서 API 키 읽기
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            "오류: GEMINI_API_KEY 환경변수가 설정되어 있지 않습니다.\n"
            "- .env 파일에 GEMINI_API_KEY=your_key 를 추가하거나\n"
            "- 터미널에서 export GEMINI_API_KEY=\"your_key\" 로 설정한 뒤 다시 실행하세요."
        )
        sys.exit(1)

    try:
        # 안전하게 api_key를 전달해서 클라이언트 초기화
        client = genai.Client(api_key=api_key)

        # 간단한 프롬프트(한국어)로 응답 요청
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="인공지능이 어떻게 작동하는지 한두 문장으로 설명해 줘."
        )

        # 응답 텍스트 출력
        print(response.text)
    except Exception as e:
        # 인증/네트워크 등 일반적인 오류 처리
        print(f"초기 요청 중 오류가 발생했습니다: {e}")
        sys.exit(1)

    # 사용자와 대화하는 반복문
    print("\n=== Gemini AI 대화 시작 ===")
    print("질문을 입력하세요. 종료하려면 'exit'를 입력하세요.\n")
    
    while True:
        # 사용자 입력 받기
        user_input = input("질문: ").strip()
        
        # 'exit' 입력 시 종료
        if user_input.lower() == 'exit':
            print("프로그램을 종료합니다.")
            break
        
        # 빈 입력은 무시
        if not user_input:
            print("질문을 입력해주세요.\n")
            continue
        
        try:
            # 사용자 질문을 Gemini에 전송
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input
            )
            
            # 답변 출력
            print(f"\n답변: {response.text}\n")
            
        except Exception as e:
            # 개별 요청 오류 처리 (프로그램은 계속 실행)
            print(f"오류가 발생했습니다: {e}\n")


if __name__ == "__main__":
    main()