"""
자동으로 누락된 이미지를 탐지하고 매핑하는 스크립트
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

# HTML, CSS, JS 파일에서 참조하는 이미지 경로 추출
required_images = set()

# HTML 파일 스캔
html_file = project_root / "src" / "html" / "index.html"
if html_file.exists():
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # src="..." 또는 src='...' 패턴 추출
        for match in re.finditer(r'src=["\']([^"\']+)["\']', content):
            path = match.group(1)
            if path.startswith('/assets/images/'):
                required_images.add(path[1:])  # 앞의 '/' 제거

# JavaScript 파일 스캔
js_file = project_root / "src" / "js" / "main.js"
if js_file.exists():
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # url(...) 패턴 추출
        for match in re.finditer(r'url\(([^)]+)\)', content):
            path = match.group(1).strip('\'"')
            if path.startswith('/assets/images/'):
                required_images.add(path[1:])

print(f"Found {len(required_images)} required image paths in code")
print("Checking for missing images...\n")

# 필요한 이미지 중 누락된 것 찾기
missing_images = []
for img_path in required_images:
    full_path = project_root / img_path
    if not full_path.exists():
        missing_images.append(img_path)
        print(f"[MISSING] {img_path}")

if not missing_images:
    print("All required images exist!")
else:
    print(f"\nFound {len(missing_images)} missing images. Attempting to map from extracted images...\n")
    
    # extracted 이미지 목록 가져오기
    extracted_files = list(other_dir.glob('*.png')) + list(other_dir.glob('*.jpg')) + list(other_dir.glob('*.jpeg'))
    
    # 매핑 시도
    for missing_path in missing_images:
        # 경로에서 파일명 추출
        filename = Path(missing_path).name
        target_folder = Path(missing_path).parent.name
        
        print(f"Searching for replacement for {filename} in {target_folder} folder...")
        
        # 파일명 기반으로 유사한 이미지 찾기
        found = False
        
        # 1. 파일명과 정확히 일치하는 경우 찾기 (다른 확장자 포함)
        name_without_ext = Path(filename).stem
        for ext_file in extracted_files:
            if Path(ext_file).stem.lower() == name_without_ext.lower():
                target_path = target_dirs[target_folder] / filename
                # 확장자 유지
                if ext_file.suffix.lower() != target_path.suffix.lower():
                    filename = name_without_ext + ext_file.suffix.lower()
                    target_path = target_dirs[target_folder] / filename
                
                shutil.copy2(ext_file, target_path)
                print(f"  [OK] Mapped: {ext_file.name} -> {target_folder}/{filename}")
                found = True
                break
        
        # 2. 페이지 1의 큰 이미지를 hero fallback으로 사용
        if not found and 'hero-bg-fallback' in filename.lower() and target_folder == 'hero':
            # page1의 큰 이미지 찾기 (img3, img4, img5 등)
            for page1_img in sorted(other_dir.glob('page1_img*.png')) + sorted(other_dir.glob('page1_img*.jpg')):
                # 큰 이미지일 가능성이 높은 것 (번호가 큰 것)
                if int(re.search(r'img(\d+)', page1_img.name).group(1)) >= 3:
                    target_path = target_dirs[target_folder] / filename
                    # JPG로 변환할 필요는 없고, PNG면 그대로 사용
                    if page1_img.suffix.lower() == '.png' and filename.endswith('.jpg'):
                        filename = name_without_ext + '.png'
                        target_path = target_dirs[target_folder] / filename
                    shutil.copy2(page1_img, target_path)
                    print(f"  [OK] Mapped: {page1_img.name} -> {target_folder}/{filename}")
                    found = True
                    break
        
        if not found:
            print(f"  [FAIL] Could not find replacement for {filename}")

print("\n[COMPLETE] Auto-mapping finished!")
