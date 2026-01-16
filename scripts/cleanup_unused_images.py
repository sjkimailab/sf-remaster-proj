"""
사용되지 않는 이미지 파일을 정리하는 스크립트
코드에서 실제로 사용되는 이미지만 확인하고 나머지는 삭제합니다.
"""

import shutil
import re
from pathlib import Path

# 프로젝트 루트 경로
project_root = Path(__file__).parent.parent
images_root = project_root / "assets" / "images"
other_dir = images_root / "other"

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

# CSS 파일 스캔
css_dir = project_root / "src" / "css"
for css_file in css_dir.glob("*.css"):
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # url(...) 패턴 추출
        for match in re.finditer(r'url\(([^)]+)\)', content):
            path = match.group(1).strip('\'"')
            if path.startswith('/assets/images/') or path.startswith('../assets/images/'):
                # 상대 경로 처리
                if path.startswith('../'):
                    path = 'assets/images/' + path[3:]
                elif path.startswith('/'):
                    path = path[1:]
                required_images.add(path)

print(f"Found {len(required_images)} required image paths in code:")
for img in sorted(required_images):
    print(f"  - {img}")

# 실제 파일 경로로 변환
required_files = set()
for img_path in required_images:
    full_path = project_root / img_path
    if full_path.exists():
        required_files.add(full_path.resolve())
    # SVG도 체크 (동일 이름의 SVG가 있으면 유지)
    svg_path = full_path.with_suffix('.svg')
    if svg_path.exists():
        required_files.add(svg_path.resolve())

print(f"\nRequired files: {len(required_files)}")

# 모든 이미지 파일 찾기 (other 제외)
all_image_files = []
for folder in ['logo', 'hero', 'features', 'news', 'icons', 'backgrounds']:
    folder_path = images_root / folder
    if folder_path.exists():
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.svg']:
            all_image_files.extend(folder_path.glob(ext))
            all_image_files.extend(folder_path.glob(ext.upper()))

# README 파일은 제외
all_image_files = [f for f in all_image_files if f.name != 'README.md']

# 사용되지 않는 파일 찾기
unused_files = []
for img_file in all_image_files:
    if img_file.resolve() not in required_files:
        unused_files.append(img_file)

print(f"\nUnused files found: {len(unused_files)}")

# other 폴더는 전체 삭제 (추출된 원본 이미지들이므로)
other_files_count = 0
if other_dir.exists():
    for file in other_dir.rglob('*'):
        if file.is_file() and file.name != 'README.md':
            other_files_count += 1

print(f"Files in 'other' folder: {other_files_count}")

# 삭제할 파일 목록 출력
print("\n=== Files to be deleted ===")
print(f"\n1. Unused files in organized folders ({len(unused_files)} files):")
for f in sorted(unused_files):
    print(f"   - {f.relative_to(project_root)}")

print(f"\n2. All files in 'other' folder ({other_files_count} files)")

# 사용자 확인 없이 자동 삭제
delete_choice = True  # 자동으로 삭제 진행

if delete_choice:
    deleted_count = 0
    
    # 사용되지 않는 파일 삭제
    for file in unused_files:
        try:
            file.unlink()
            print(f"[DELETED] {file.relative_to(project_root)}")
            deleted_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to delete {file.relative_to(project_root)}: {e}")
    
    # other 폴더 전체 삭제
    if other_dir.exists():
        try:
            for file in other_dir.rglob('*'):
                if file.is_file() and file.name != 'README.md':
                    file.unlink()
                    deleted_count += 1
            # 빈 폴더 삭제 시도 (다른 파일이 있으면 유지)
            try:
                if not any(other_dir.iterdir()):
                    other_dir.rmdir()
                    print(f"[DELETED] Empty folder: {other_dir.relative_to(project_root)}")
            except:
                pass  # 폴더가 비어있지 않으면 유지
        except Exception as e:
            print(f"[ERROR] Failed to clean 'other' folder: {e}")
    
    print(f"\n=== Cleanup complete ===")
    print(f"Total files deleted: {deleted_count}")
    print(f"Required files remaining: {len(required_files)}")
else:
    print("\nCleanup cancelled.")
