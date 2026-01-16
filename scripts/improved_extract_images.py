"""
개선된 이미지 추출 스크립트
PDF에서 웹사이트에 실제로 필요한 이미지만 정확하게 추출

개선 사항:
1. 페이지별 우선순위 기반 추출
2. 이미지 위치 분석 (페이지 상단/중앙 = 주요 이미지)
3. 비율 분석 (웹 목업은 보통 가로형)
4. 중복 이미지 제거
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

def get_image_size_from_bytes(image_bytes, base_image_meta):
    """이미지 메타데이터에서 크기 추출 (Pillow 없이)"""
    # 먼저 메타데이터에서 크기 확인
    width = base_image_meta.get("width", 0)
    height = base_image_meta.get("height", 0)
    
    # 메타데이터에 없으면 None 반환 (PDF 좌표에서 추정하도록)
    if width > 0 and height > 0:
        return width, height
    
    return None, None

def extract_priority_images(pdf_path, output_dir, min_area=50000):
    """
    우선순위 기반 이미지 추출
    
    Args:
        pdf_path: PDF 파일 경로
        output_dir: 이미지를 저장할 디렉토리
        min_area: 최소 이미지 면적 (width * height)
    """
    output_path = Path(output_dir) / "other"
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 페이지별 우선순위 (낮은 숫자 = 높은 우선순위)
    page_priority = {
        1: 1,   # 첫 페이지 - 로고, 히어로
        2: 2,   # 게임 특징
        3: 1,   # 히어로 섹션
        4: 2,
        5: 3,
        6: 3,
        7: 2,   # 게임 특징
        8: 3,
        9: 3,
        10: 3,
        11: 2,  # 게임 특징
        12: 3,
        13: 2,  # 뉴스
        14: 2,
        15: 2,
        16: 2,
        17: 3,
        18: 2,
    }
    
    # 이미지 저장 (중복 체크용)
    seen_images = {}  # (width, height, page_y) -> filename
    
    try:
        pdf_document = fitz.open(pdf_path)
        image_count = 0
        skipped_count = 0
        
        print(f"Opening PDF: {pdf_path}")
        print(f"Total pages: {len(pdf_document)}")
        print(f"Minimum area: {min_area} pixels")
        print("=" * 60)
        
        # 페이지별로 이미지 수집 및 정렬
        page_images = defaultdict(list)
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            image_list = page.get_images(full=True)
            
            priority = page_priority.get(page_num + 1, 10)  # 기본값 10
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # 실제 이미지 크기 가져오기
                    width, height = get_image_size_from_bytes(image_bytes, base_image)
                    
                    # 메타데이터에서 크기를 가져올 수 없으면 PDF 좌표에서 추정
                    if width is None or height is None or width == 0 or height == 0:
                        img_rects = page.get_image_rects(xref)
                        if img_rects:
                            rect = img_rects[0]
                            width_pdf = rect.x1 - rect.x0
                            height_pdf = rect.y1 - rect.y0
                            
                            # 페이지 크기와 비교하여 실제 픽셀 크기 추정
                            page_rect = page.rect
                            # PDF는 보통 72 DPI이지만, 실제 해상도는 더 높을 수 있음
                            # 이미지가 페이지에서 차지하는 비율을 계산
                            if page_rect.width > 0 and page_rect.height > 0:
                                width_ratio = width_pdf / page_rect.width
                                height_ratio = height_pdf / page_rect.height
                                # 페이지가 960x540 (PDF 분석 결과)라고 가정하고 실제 픽셀 계산
                                estimated_page_width = 960
                                estimated_page_height = 540
                                width = int(width_ratio * estimated_page_width * 1.5)  # 1.5배로 실제 해상도 추정
                                height = int(height_ratio * estimated_page_height * 1.5)
                            else:
                                # DPI 변환 (PDF는 보통 72 DPI, 실제는 더 높을 수 있음)
                                width = int(width_pdf * 1.5)
                                height = int(height_pdf * 1.5)
                    
                    # 면적 필터링
                    area = width * height
                    if area < min_area:
                        skipped_count += 1
                        continue
                    
                    # 이미지 위치 정보
                    img_rects = page.get_image_rects(xref)
                    page_y = 0
                    if img_rects:
                        rect = img_rects[0]
                        page_y = rect.y0  # 페이지 상단에서의 거리
                    
                    # 이미지 정보 저장
                    page_images[page_num].append({
                        'xref': xref,
                        'index': img_index,
                        'bytes': image_bytes,
                        'ext': image_ext,
                        'width': width,
                        'height': height,
                        'area': area,
                        'y_pos': page_y,
                        'priority': priority,
                        'ratio': width / height if height > 0 else 0
                    })
                    
                except Exception as e:
                    print(f"  [WARN] Page {page_num + 1} img {img_index + 1}: {e}")
                    continue
        
        # 페이지별로 정렬하고 추출
        # 우선순위가 높고, 면적이 크고, 상단에 위치한 이미지 우선
        for page_num in sorted(page_images.keys()):
            images = page_images[page_num]
            
            # 정렬: 우선순위 -> 면적 -> 위치(상단 우선)
            images.sort(key=lambda x: (-x['priority'], -x['area'], x['y_pos']))
            
            print(f"\nPage {page_num + 1} (priority: {images[0]['priority'] if images else 'N/A'}):")
            
            for img_info in images:
                width = img_info['width']
                height = img_info['height']
                area = img_info['area']
                ratio = img_info['ratio']
                
                # 중복 체크 (비슷한 크기의 이미지 제외)
                key = (width, height, int(img_info['y_pos'] / 100) * 100)  # 100px 단위로 그룹화
                if key in seen_images:
                    skipped_count += 1
                    print(f"  [SKIP] img{img_info['index'] + 1}: Duplicate or similar to {seen_images[key]}")
                    continue
                
                # 파일명 생성
                image_filename = f"page{page_num + 1}_img{img_info['index'] + 1}_{width}x{height}.{img_info['ext']}"
                image_path = output_path / image_filename
                
                # 저장
                with open(image_path, "wb") as image_file:
                    image_file.write(img_info['bytes'])
                
                seen_images[key] = image_filename
                image_count += 1
                
                # 이미지 정보 출력
                ratio_str = f"{ratio:.2f}" if ratio > 0 else "N/A"
                print(f"  [OK] {image_filename}")
                print(f"    Size: {width}x{height}px (area: {area:,}) | Ratio: {ratio_str} | Y: {img_info['y_pos']:.0f}")
        
        pdf_document.close()
        
        print("\n" + "=" * 60)
        print(f"[DONE] Extraction complete!")
        print(f"[INFO] Total {image_count} images extracted.")
        print(f"[INFO] {skipped_count} images filtered out (too small or duplicate).")
        print(f"[INFO] Save location: {output_dir}/other")
        
        # 크기별 통계
        if image_count > 0:
            print("\n[SUMMARY] Images by size category:")
            image_files = list(output_path.glob("*.png")) + list(output_path.glob("*.jpg")) + list(output_path.glob("*.jpeg"))
            
            large = []  # 1000x600+
            medium = []  # 500x300+
            small = []  # 나머지
            
            for img_file in image_files:
                name = img_file.stem
                if "_" in name and "x" in name:
                    try:
                        size_part = name.split("_")[-1]
                        if "x" in size_part:
                            w, h = map(int, size_part.split("x"))
                            if w >= 1000 and h >= 600:
                                large.append((name, w, h))
                            elif w >= 500 and h >= 300:
                                medium.append((name, w, h))
                            else:
                                small.append((name, w, h))
                    except:
                        pass
            
            print(f"  Large (1000x600+): {len(large)} files")
            for name, w, h in large[:5]:
                print(f"     - {name}")
            
            print(f"  Medium (500x300+): {len(medium)} files")
            for name, w, h in medium[:5]:
                print(f"     - {name}")
            
            if small:
                print(f"  Small (<500x300): {len(small)} files")
        
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
    
    # 최소 면적 50,000 픽셀 (예: 250x200) - 작은 아이콘 제외
    extract_priority_images(pdf_file, output_directory, min_area=50000)