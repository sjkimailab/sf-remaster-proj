"""
스마트 목업 이미지 추출 스크립트
기획 텍스트 이미지와 실제 웹 목업 이미지를 구별하여 추출

목업 이미지 특징:
- 큰 크기 (일반적으로 1000x600 이상)
- 가로형 비율 (16:9 또는 16:10)
- 페이지 중앙/상단에 위치
- 웹 브라우저 UI 패턴 (주소창, 탭 등)
- 반복되는 레이아웃 패턴
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

try:
    import fitz  # PyMuPDF
except ImportError:
    print("필요한 라이브러리를 설치해주세요:")
    print("pip install PyMuPDF")
    sys.exit(1)

def is_web_mockup(width, height, area, y_pos, page_height, page_width):
    """
    이미지가 웹 목업인지 판별
    
    기준:
    1. 크기: 너무 작지 않음 (최소 800x400 정도)
    2. 비율: 가로형 (너비가 높이보다 크거나 비슷)
    3. 위치: 페이지 중앙/상단 (상단 60% 이내)
    4. 면적: 페이지의 상당 부분 차지
    """
    # 1. 최소 크기 체크
    if width < 600 or height < 300:
        return False
    
    # 2. 면적 체크 (최소 180,000 픽셀, 약 600x300)
    if area < 180000:
        return False
    
    # 3. 비율 체크 - 가로형 (너비 >= 높이 * 1.2)
    aspect_ratio = width / height if height > 0 else 0
    if aspect_ratio < 1.0:  # 세로형은 목업이 아님
        return False
    
    # 4. 위치 체크 - 페이지 상단 70% 이내에 위치
    page_center_y = page_height * 0.5
    if y_pos > page_center_y * 1.4:  # 페이지 하단은 제외
        return False
    
    # 5. 페이지 대비 크기 - 페이지 너비의 50% 이상 차지
    width_ratio = width / page_width if page_width > 0 else 0
    if width_ratio < 0.4:  # 페이지 너비의 40% 미만이면 너무 작음
        return False
    
    # 6. 종횡비 범위 체크 (1.0 ~ 3.5 사이, 즉 가로형이지만 너무 길지 않음)
    if aspect_ratio > 3.5:
        return False
    
    return True

def get_image_size_from_bytes(image_bytes, base_image_meta):
    """이미지 메타데이터에서 크기 추출"""
    width = base_image_meta.get("width", 0)
    height = base_image_meta.get("height", 0)
    
    if width > 0 and height > 0:
        return width, height
    
    return None, None

def extract_smart_mockups(pdf_path, output_dir):
    """
    스마트하게 웹 목업 이미지만 추출
    """
    output_path = Path(output_dir) / "other"
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        pdf_document = fitz.open(pdf_path)
        mockup_count = 0
        planning_count = 0
        skipped_count = 0
        
        print(f"Opening PDF: {pdf_path}")
        print(f"Total pages: {len(pdf_document)}")
        print("=" * 60)
        print("Analyzing images to distinguish mockups from planning graphics...")
        print("=" * 60)
        
        # 페이지별로 이미지 수집
        page_images = defaultdict(list)
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            image_list = page.get_images(full=True)
            page_rect = page.rect
            page_width = page_rect.width
            page_height = page_rect.height
            
            print(f"\nPage {page_num + 1}:")
            print(f"  Page size: {page_width:.0f}x{page_height:.0f}")
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # 이미지 크기 가져오기
                    width, height = get_image_size_from_bytes(image_bytes, base_image)
                    
                    # 메타데이터에서 크기를 가져올 수 없으면 PDF 좌표에서 추정
                    if width is None or height is None or width == 0 or height == 0:
                        img_rects = page.get_image_rects(xref)
                        if img_rects:
                            rect = img_rects[0]
                            width_pdf = rect.x1 - rect.x0
                            height_pdf = rect.y1 - rect.y0
                            
                            # PDF 좌표를 실제 픽셀 크기로 변환
                            if page_width > 0 and page_height > 0:
                                width_ratio = width_pdf / page_width
                                height_ratio = height_pdf / page_height
                                # 페이지가 960x540 (PDF 분석 결과)라고 가정
                                estimated_page_width = 960
                                estimated_page_height = 540
                                width = int(width_ratio * estimated_page_width * 1.5)
                                height = int(height_ratio * estimated_page_height * 1.5)
                            else:
                                width = int(width_pdf * 1.5)
                                height = int(height_pdf * 1.5)
                        else:
                            skipped_count += 1
                            continue
                    
                    area = width * height
                    aspect_ratio = width / height if height > 0 else 0
                    
                    # 이미지 위치 정보
                    img_rects = page.get_image_rects(xref)
                    y_pos = 0
                    x_pos = 0
                    if img_rects:
                        rect = img_rects[0]
                        y_pos = rect.y0  # 페이지 상단에서의 거리
                        x_pos = rect.x0  # 페이지 왼쪽에서의 거리
                    
                    # 목업인지 판별
                    is_mockup = is_web_mockup(width, height, area, y_pos, page_height, page_width)
                    
                    image_info = {
                        'xref': xref,
                        'index': img_index,
                        'bytes': image_bytes,
                        'ext': image_ext,
                        'width': width,
                        'height': height,
                        'area': area,
                        'aspect_ratio': aspect_ratio,
                        'y_pos': y_pos,
                        'x_pos': x_pos,
                        'is_mockup': is_mockup
                    }
                    
                    page_images[page_num].append(image_info)
                    
                    # 출력
                    category = "MOCKUP" if is_mockup else "PLANNING"
                    ratio_str = f"{aspect_ratio:.2f}"
                    print(f"  [{category}] img{img_index + 1}: {width}x{height} (area: {area:,}, ratio: {ratio_str}, y: {y_pos:.0f})")
                    
                    if is_mockup:
                        mockup_count += 1
                    else:
                        planning_count += 1
                    
                except Exception as e:
                    print(f"  [WARN] img {img_index + 1}: {e}")
                    skipped_count += 1
                    continue
        
        # 목업 이미지만 추출
        print("\n" + "=" * 60)
        print("Extracting mockup images only...")
        print("=" * 60)
        
        extracted_count = 0
        for page_num in sorted(page_images.keys()):
            mockups = [img for img in page_images[page_num] if img['is_mockup']]
            
            if mockups:
                print(f"\nPage {page_num + 1} - {len(mockups)} mockup(s):")
                
                # 면적 순으로 정렬 (큰 것부터)
                mockups.sort(key=lambda x: -x['area'])
                
                for img_info in mockups:
                    width = img_info['width']
                    height = img_info['height']
                    area = img_info['area']
                    aspect_ratio = img_info['aspect_ratio']
                    
                    # 파일명 생성
                    image_filename = f"page{page_num + 1}_img{img_info['index'] + 1}_{width}x{height}.{img_info['ext']}"
                    image_path = output_path / image_filename
                    
                    # 저장
                    with open(image_path, "wb") as image_file:
                        image_file.write(img_info['bytes'])
                    
                    extracted_count += 1
                    ratio_str = f"{aspect_ratio:.2f}"
                    print(f"  [OK] {image_filename}")
                    print(f"    Size: {width}x{height}px | Area: {area:,} | Ratio: {ratio_str}")
        
        pdf_document.close()
        
        print("\n" + "=" * 60)
        print(f"[DONE] Extraction complete!")
        print(f"[INFO] Total images analyzed: {mockup_count + planning_count}")
        print(f"[INFO] Mockups identified: {mockup_count}")
        print(f"[INFO] Planning graphics: {planning_count}")
        print(f"[INFO] Mockups extracted: {extracted_count}")
        print(f"[INFO] Images skipped: {skipped_count}")
        print(f"[INFO] Save location: {output_dir}/other")
        
    except Exception as e:
        print(f"[ERROR] Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    pdf_file = project_root / "SF리마스터 웹기획서_260115.pdf"
    output_directory = project_root / "assets" / "images"
    
    if not pdf_file.exists():
        print(f"[ERROR] PDF file not found: {pdf_file}")
        sys.exit(1)
    
    extract_smart_mockups(pdf_file, output_directory)