"""
Invest KOREA Summit 2026 모바일 설문조사 QR 코드 생성 스크립트
행사 현장 배포용 고화질 PNG 이미지 생성 (Pillow 및 qrcode 라이브러리 활용)
"""

import argparse
import os
import socket
from pathlib import Path
import qrcode
from PIL import Image, ImageDraw, ImageFont


def get_local_ip():
    """행사장 Wi-Fi/LAN 환경에서 스마트폰이 접속할 수 있는 로컬 IPv4 주소 자동 탐지"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 실제 외부와 통신하지 않고 라우팅 테이블 상의 로컬 IP 획득
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def generate_qr_image(url: str, output_path: str, title: str = "2026 Invest KOREA Summit"):
    """
    고화질 QR 코드 생성 및 상단 타이틀 배너를 포함한 현장 안내용 PNG 이미지 제작
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=12,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # 기본 QR 이미지 생성 (RGB)
    qr_img = qr.make_image(fill_color="#0F2C59", back_color="#FFFFFF").convert("RGB")
    qr_w, qr_h = qr_img.size

    # 캔버스 확장 (상단 타이틀 + 하단 URL 안내)
    banner_top = 80
    banner_bottom = 60
    total_w = qr_w + 40
    total_h = qr_h + banner_top + banner_bottom

    canvas = Image.new("RGB", (total_w, total_h), "#FFFFFF")
    draw = ImageDraw.Draw(canvas)

    # 상단 네이비 배경 바
    draw.rectangle([0, 0, total_w, banner_top], fill="#0F2C59")

    # 폰트 설정 (기본 또는 시스템 폰트)
    try:
        title_font = ImageFont.truetype("malgun.ttf", 22)
        sub_font = ImageFont.truetype("malgun.ttf", 14)
        url_font = ImageFont.truetype("arial.ttf", 13)
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        url_font = ImageFont.load_default()

    # 상단 텍스트 드로잉
    draw.text((total_w // 2, 28), title, fill="#FFFFFF", font=title_font, anchor="mm")
    draw.text((total_w // 2, 56), "참가자 만족도 설문조사 / Participant Survey", fill="#93C5FD", font=sub_font, anchor="mm")

    # QR 이미지 배치
    canvas.paste(qr_img, ((total_w - qr_w) // 2, banner_top + 10))

    # 하단 URL 안내 텍스트 드로잉
    draw.text((total_w // 2, total_h - 35), "스마트폰 카메라로 QR 코드를 스캔하세요", fill="#1E293B", font=sub_font, anchor="mm")
    draw.text((total_w // 2, total_h - 15), url, fill="#64748B", font=url_font, anchor="mm")

    # 테두리 라인
    draw.rectangle([0, 0, total_w - 1, total_h - 1], outline="#E2E8F0", width=2)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    canvas.save(output_path, "PNG", quality=95)
    print(f"[OK] QR Code successfully generated:")
    print(f"     Target URL  : {url}")
    print(f"     Saved Path  : {output_path}")
    print(f"     Dimensions  : {total_w}x{total_h} px")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IKS 2026 설문조사 모바일 접속용 QR 코드 생성기")
    parser.add_argument("--url", type=str, default=None, help="설문조사 웹 서비스 URL (미지정 시 로컬 IP 기반 자동 생성)")
    parser.add_argument("--port", type=int, default=8000, help="웹 서버 포트 번호 (기본값: 8000)")
    parser.add_argument("--output", type=str, default="iks2026_survey_qr.png", help="저장할 PNG 파일 경로")

    args = parser.parse_args()

    if args.url:
        target_url = args.url
    else:
        local_ip = get_local_ip()
        target_url = f"http://{local_ip}:{args.port}/"

    generate_qr_image(target_url, args.output)

    # 정적 파일 디렉토리에도 사본 보관
    static_qr_path = Path("static/images/survey_qr.png")
    generate_qr_image(target_url, str(static_qr_path))

