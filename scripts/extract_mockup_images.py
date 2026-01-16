"""
PDF에서 웹 브라우저 목업 이미지만 정확히 추출하는 스크립트
이미지 크기와 위치를 분석하여 유의미한 목업 이미지만 추출
"""

import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("필요한 라이브러리를 설치해주세요:")
    print("pip install PyMuPDF")
    sys.exit(1)

def extract_mockup_images(pdf_path, output_dir, min_width=300, min_height=200):
    """
    PDF에서 웹 브라우저 목업 이미지만 추출합니다.
    
    Args:
        pdf_path: PDF 파일 경로
        output_dir: 이미지를 저장할 디렉토리
        min_width: 최소 이미지 너비 (픽셀) - 작은 아이콘 필터링
        min_height: 최소 이미지 높이 (픽셀) - 작은 아이콘 필터링
    """
    # 출력 디렉토리 생성
    output_path = Path(output_dir) / "other"
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        pdf_document = fitz.open(pdf_path)
        image_count = 0
        skipped_count = 0
        
        print(f"Opening PDF: {pdf_path}")
        print(f"Total pages: {len(pdf_document)}")
        print(f"Filter condition: minimum size {min_width}x{min_height}px")
        print("=" * 60)
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            image_list = page.get_images(full=True)
            
            print(f"\nAnalyzing page {page_num + 1}...")
            
            page_image_count = 0
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # 이미지 크기 및 위치 정보 확인
                    img_rects = page.get_image_rects(xref)
                    
                    # 이미지 크기 추정 (PDF 좌표에서 픽셀 크기 계산)
                    width = height = 0
                    if img_rects:
                        rect = img_rects[0]
                        # PDF 좌표를 픽셀 크기로 변환 (일반적으로 72 DPI 기준)
                        # 실제 해상도를 추정하기 위해 rect 크기 사용
                        width_pdf = rect.x1 - rect.x0
                        height_pdf = rect.y1 - rect.y0
                        
                        # 페이지 크기로 정규화하여 실제 크기 추정
                        page_rect = page.rect
                        # 이미지가 페이지의 어느 비율을 차지하는지 계산
                        width_ratio = width_pdf / (page_rect.width or 1)
                        height_ratio = height_pdf / (page_rect.height or 1)
                        
                        # 추정 크기 (PDF 해상도 96 DPI 가정)
                        width = int(width_pdf * (96 / 72))
                        height = int(height_pdf * (96 / 72))
                    
                    # 이미지 메타데이터에서 실제 크기 확인 시도
                    if "width" in base_image and "height" in base_image:
                        width = base_image.get("width", width)
                        height = base_image.get("height", height)
                    
                    # 크기 필터링 (크기 정보가 있는 경우만)
                    if width > 0 and height > 0:
                        if width < min_width or height < min_height:
                            skipped_count += 1
                            continue
                        
                        # 저장
                        image_filename = f"page{page_num + 1}_img{img_index + 1}_{width}x{height}.{image_ext}"
                        image_path = output_path / image_filename
                        
                        with open(image_path, "wb") as image_file:
                            image_file.write(image_bytes)
                        
                        # 위치 정보 출력
                        location_info = ""
                        if img_rects:
                            rect = img_rects[0]
                            location_info = f"Location: ({rect.x0:.0f}, {rect.y0:.0f}) ~ ({rect.x1:.0f}, {rect.y1:.0f})"
                        
                        print(f"  [OK] Extracted: {image_filename}")
                        print(f"    Size: {width}x{height}px | {location_info}")
                        
                        image_count += 1
                        page_image_count += 1
                    else:
                        # 크기 정보가 없어도 저장 (하지만 파일명에 크기 정보 없음)
                        image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
                        image_path = output_path / image_filename
                        
                        with open(image_path, "wb") as image_file:
                            image_file.write(image_bytes)
                        
                        print(f"  [OK] Extracted: {image_filename} (no size info)")
                        image_count += 1
                        page_image_count += 1
                    
                except Exception as e:
                    print(f"  [FAIL] Image extraction failed: {e}")
                    continue
            
            if page_image_count > 0:
                print(f"  -> Page {page_num + 1}: {page_image_count} images extracted")
        
        pdf_document.close()
        
        print("\n" + "=" * 60)
        print(f"[DONE] Complete!")
        print(f"[INFO] Total {image_count} mockup images extracted.")
        print(f"[INFO] {skipped_count} small images filtered out.")
        print(f"[INFO] Save location: {output_dir}/other")
        
        # 추출된 이미지 요약
        if image_count > 0:
            print("\n[SUMMARY] Extracted images by size:")
            image_files = list(output_path.glob("*.png")) + list(output_path.glob("*.jpg")) + list(output_path.glob("*.jpeg"))
            large_images = []
            medium_images = []
            
            for img_file in image_files:
                # 파일명에서 크기 정보 추출
                name = img_file.stem
                if "_" in name and "x" in name:
                    try:
                        size_part = name.split("_")[-1]  # 마지막 부분 (예: "800x600")
                        if "x" in size_part:
                            w, h = map(int, size_part.split("x"))
                            if w >= 800 or h >= 600:
                                large_images.append((img_file.name, w, h))
                            elif w >= 400 or h >= 300:
                                medium_images.append((img_file.name, w, h))
                    except:
                        pass
            
            if large_images:
                print(f"  Large images (800x600+): {len(large_images)} files")
                for name, w, h in large_images[:10]:  # 최대 10개 표시
                    print(f"     - {name}")
            
            if medium_images:
                print(f"  Medium images (400x300+): {len(medium_images)} files")
                for name, w, h in medium_images[:10]:  # 최대 10개 표시
                    print(f"     - {name}")
        
    except Exception as e:
        print(f"[ERROR] Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 현재 프로젝트 경로
    project_root = Path(__file__).parent.parent
    pdf_file = project_root / "SF리마스터 웹기획서_260115.pdf"
    output_directory = project_root / "assets" / "images"
    
    if not pdf_file.exists():
        print(f"[ERROR] PDF file not found: {pdf_file}")
        sys.exit(1)
    
    # 웹 브라우저 목업은 일반적으로 크기가 큼
    # 최소 300x200 이상인 이미지만 추출 (작은 아이콘 제외)
    extract_mockup_images(pdf_file, output_directory, min_width=300, min_height=200)
