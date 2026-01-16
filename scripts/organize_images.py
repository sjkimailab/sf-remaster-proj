"""
추출된 이미지를 적절한 폴더로 정리하는 스크립트
"""
import shutil
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

# 이미지 매핑: (소스 파일명, 타겟 폴더, 타겟 파일명)
# 참고: 확장자는 실제 소스 파일 확장자를 유지합니다
image_mappings = [
    # 로고 (페이지 1의 첫 번째 이미지들을 사용)
    ('page1_img1.png', 'logo', 'shield-logo.png'),
    ('page1_img2.png', 'logo', 'dragonfly-logo.png'),
    
    # 히어로 (페이지 1의 큰 이미지 사용)
    ('page1_img3.png', 'hero', 'main-hero.png'),
    
    # 게임 특징 이미지 - 기존 파일이 이미 있으므로 매핑 제거
    # ('page2_img1.jpeg', 'features', 'level-design.jpg'),  # 기존 파일 사용
    # ('page2_img2.png', 'features', 'moving-control.png'),  # 기존 파일 사용
    # ('page2_img3.png', 'features', 'shooting-system.png'),  # 기존 파일 사용
    # ('page2_img4.png', 'features', 'weapon-system.png'),  # 기존 파일 사용
    
    # 새소식 썸네일 (page13 사용, page3_img1이 없으므로)
    ('page13_img1.png', 'news', 'news-001.png'),
    ('page3_img2.png', 'news', 'news-002.png'),
    ('page3_img3.png', 'news', 'news-003.png'),
    ('page3_img4.png', 'news', 'news-004.png'),
]

# 이미지 복사
copied_count = 0
for source_file, target_folder, target_file in image_mappings:
    source_path = other_dir / source_file
    target_path = target_dirs[target_folder] / target_file
    
    if source_path.exists():
        # 실제 소스 파일의 확장자를 확인하여 타겟 파일명에 반영
        source_ext = source_path.suffix.lower()
        target_ext = Path(target_file).suffix.lower()
        
        # 확장자가 다른 경우 실제 소스 파일 확장자 사용
        if source_ext != target_ext:
            target_file = target_file.rsplit('.', 1)[0] + source_ext
            target_path = target_dirs[target_folder] / target_file
        
        shutil.copy2(source_path, target_path)
        print(f"[OK] Copied: {source_file} -> {target_folder}/{target_path.name}")
        copied_count += 1
    else:
        print(f"[FAIL] Not found: {source_file}")

print(f"\n[COMPLETE] {copied_count} images organized")
