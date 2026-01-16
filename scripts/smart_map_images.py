"""
스마트 이미지 매핑 스크립트
추출된 이미지를 분석하여 HTML에서 필요한 이미지에 자동으로 매핑
"""

import shutil
import re
from pathlib import Path

# 프로젝트 루트 경로
project_root = Path(__file__).parent.parent
other_dir = project_root / "assets" / "images" / "other"

# 타겟 디렉토리
target_dirs = {
    'logo': project_root / "assets" / "images" / "logo",
    'hero': project_root / "assets" / "images" / "hero",
    'features': project_root / "assets" / "images" / "features",
    'news': project_root / "assets" / "images" / "news",
    'icons': project_root / "assets" / "images" / "icons",
}

# 디렉토리 생성
for dir_path in target_dirs.values():
    dir_path.mkdir(parents=True, exist_ok=True)

# 매핑 규칙 정의 (페이지 번호, 이미지 번호 패턴, 타겟 폴더, 타겟 파일명)
# 실제로 추출된 이미지를 기반으로 매핑
mapping_rules = [
    # 히어로 이미지 (페이지 3의 큰 웹 목업)
    (3, 39, 'hero', 'main-hero.jpeg'),  # page3_img39_2080x1234.jpeg - 가장 큰 웹 목업
    (3, 1, 'hero', 'hero-bg-fallback.jpeg'),  # page3_img1_1257x629.jpeg
    
    # 게임 특징 이미지 (페이지 7, 11의 큰 이미지들)
    (7, 1, 'features', 'level-design.jpeg'),  # page7_img1_1622x912.jpeg
    (11, 2, 'features', 'moving-control.jpeg'),  # page11_img2_942x602.jpeg
    (11, 3, 'features', 'shooting-system.jpeg'),  # page11_img3_946x548.jpeg
    (11, 4, 'features', 'weapon-system.jpeg'),  # page11_img4_943x462.jpeg
    
    # 뉴스 썸네일 (페이지 13, 15의 이미지들)
    (13, 7, 'news', 'news-001.jpeg'),  # page13_img7_667x345.jpeg
    (15, 1, 'news', 'news-002.jpeg'),  # page15_img1_1617x302.jpeg
    (16, 1, 'news', 'news-003.jpeg'),  # page16_img1_1617x302.jpeg
    (18, 1, 'news', 'news-004.jpeg'),  # page18_img1_1212x756.jpeg
    
    # 로고는 기존 파일 유지하거나 다른 이미지에서 추출 필요
]

print("Starting smart image mapping...")
print("=" * 60)

# 추출된 이미지 목록 가져오기
extracted_files = list(other_dir.glob('*.png')) + list(other_dir.glob('*.jpg')) + list(other_dir.glob('*.jpeg'))
print(f"Found {len(extracted_files)} extracted images in other/ folder\n")

# 이미지 크기별로 정렬 (큰 이미지 우선)
def get_image_size(filepath):
    """파일명에서 크기 정보 추출"""
    match = re.search(r'_(\d+)x(\d+)', filepath.stem)
    if match:
        w, h = int(match.group(1)), int(match.group(2))
        return w * h
    return 0

extracted_files.sort(key=get_image_size, reverse=True)

mapped_count = 0
failed_count = 0

# 매핑 규칙 적용
for page_num, img_num, target_folder, target_filename in mapping_rules:
    # 페이지와 이미지 번호로 파일 찾기
    pattern = f"page{page_num}_img{img_num}"
    
    # 정확한 매칭 먼저 시도
    found_file = None
    for file in extracted_files:
        if file.stem.startswith(pattern):
            found_file = file
            break
    
    # 정확한 매칭이 없으면 유사한 것 찾기 (페이지 번호만 일치)
    if not found_file:
        for file in extracted_files:
            if file.stem.startswith(f"page{page_num}_img"):
                found_file = file
                print(f"  [WARN] Exact match not found for {pattern}, using {file.name}")
                break
    
    if found_file:
        target_path = target_dirs[target_folder] / target_filename
        # 확장자 확인 및 조정
        source_ext = found_file.suffix.lower()
        target_ext = Path(target_filename).suffix.lower()
        
        # 확장자가 다르면 타겟 파일명 조정
        if source_ext != target_ext:
            new_target = target_path.stem + source_ext
            target_path = target_dirs[target_folder] / new_target
            print(f"  [INFO] Adjusting extension: {target_filename} -> {new_target}")
        
        try:
            shutil.copy2(found_file, target_path)
            size_info = ""
            size_match = re.search(r'_(\d+)x(\d+)', found_file.stem)
            if size_match:
                size_info = f" ({size_match.group(1)}x{size_match.group(2)}px)"
            print(f"  [OK] Mapped: {found_file.name}{size_info} -> {target_folder}/{target_path.name}")
            mapped_count += 1
        except Exception as e:
            print(f"  [FAIL] Could not copy {found_file.name}: {e}")
            failed_count += 1
    else:
        print(f"  [FAIL] Could not find image for {pattern} -> {target_folder}/{target_filename}")
        failed_count += 1

print("\n" + "=" * 60)
print(f"[COMPLETE] Mapping finished!")
print(f"  Successfully mapped: {mapped_count} images")
print(f"  Failed: {failed_count} images")