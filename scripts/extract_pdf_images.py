"""
PDF에서 이미지 추출 스크립트
사용법: python scripts/extract_pdf_images.py
"""

import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("필요한 라이브러리를 설치해주세요:")
    print("pip install PyMuPDF")
    print("또는 이미지 추출 도구를 사용하세요.")
    sys.exit(1)

def extract_images_from_pdf(pdf_path, output_dir):
    """
    PDF에서 이미지를 추출합니다.
    
    Args:
        pdf_path: PDF 파일 경로
        output_dir: 이미지를 저장할 디렉토리
    """
    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 서브 디렉토리 생성
    subdirs = ['hero', 'logo', 'backgrounds', 'icons', 'other']
    for subdir in subdirs:
        (output_path / subdir).mkdir(exist_ok=True)
    
    try:
        # PyMuPDF를 사용하여 이미지 추출
        pdf_document = fitz.open(pdf_path)
        image_count = 0
        
        print(f"PDF 열기: {pdf_path}")
        print(f"총 페이지 수: {len(pdf_document)}")
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            image_list = page.get_images(full=True)
            
            print(f"\n페이지 {page_num + 1} 처리 중...")
            print(f"  - 발견된 이미지: {len(image_list)}개")
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # 이미지 저장
                    image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
                    image_path = output_path / "other" / image_filename
                    
                    with open(image_path, "wb") as image_file:
                        image_file.write(image_bytes)
                    
                    image_count += 1
                    print(f"  - 저장: {image_filename}")
                    
                except Exception as e:
                    print(f"  - 이미지 추출 실패: {e}")
                    continue
        
        pdf_document.close()
        print(f"\n✅ 완료: 총 {image_count}개의 이미지를 추출했습니다.")
        print(f"📁 저장 위치: {output_dir}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("\n대안 방법:")
        print("1. Adobe Acrobat 등의 PDF 편집 프로그램 사용")
        print("2. 온라인 PDF 이미지 추출 도구 사용")
        print("3. PDF 뷰어에서 스크린샷으로 이미지 캡처")

if __name__ == "__main__":
    # 현재 프로젝트 경로
    project_root = Path(__file__).parent.parent
    pdf_file = project_root / "SF리마스터 웹기획서_260115.pdf"
    output_directory = project_root / "assets" / "images"
    
    if not pdf_file.exists():
        print(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_file}")
        sys.exit(1)
    
    extract_images_from_pdf(pdf_file, output_directory)
