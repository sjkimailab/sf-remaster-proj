# 이미지 리소스 안내

이 폴더는 SF 리마스터 웹사이트에 사용되는 이미지 리소스를 저장하는 곳입니다.

## 📁 폴더 구조

```
assets/
├── images/
│   ├── hero/              # 히어로 섹션 이미지
│   │   └── main-hero.png
│   ├── logo/              # 로고 파일
│   │   ├── shield-logo.png
│   │   └── dragonfly-logo.png
│   ├── features/          # 게임 특징 이미지
│   │   ├── level-design.jpg
│   │   ├── moving-control.jpg
│   │   ├── shooting-system.jpg
│   │   └── weapon-system.jpg
│   ├── news/              # 새소식 썸네일
│   │   └── news-*.jpg
│   └── icons/             # 아이콘
│       ├── steam-icon.png
│       └── epic-icon.png
└── videos/                # 비디오 파일
    └── hero-bg.mp4
```

## 📋 필요한 이미지 목록

PDF에서 추출한 이미지를 위 폴더 구조에 맞춰 저장하세요.

### ✅ 필수 이미지
- [ ] `hero/main-hero.png` - 메인 히어로 이미지
- [ ] `logo/shield-logo.png` - 방패 로고 (히어로 섹션)
- [ ] `logo/dragonfly-logo.png` - DragonFly 로고 (푸터)

### 🎮 게임 특징 이미지 (4개)
- [ ] `features/level-design.jpg` - 레벨 디자인
- [ ] `features/moving-control.jpg` - 무빙 컨트롤
- [ ] `features/shooting-system.jpg` - 사격 시스템
- [ ] `features/weapon-system.jpg` - 무기 시스템

### 📰 새소식 썸네일
- [ ] `news/news-001.jpg` - 새소식 카드 썸네일 (최소 4개)

### 🎯 아이콘
- [ ] `icons/steam-icon.png` - Steam 플랫폼 아이콘
- [ ] `icons/epic-icon.png` - Epic Games 플랫폼 아이콘

### 🎬 영상 (선택사항)
- [ ] `videos/hero-bg.mp4` - 히어로 배경 영상

## 📖 상세 가이드

각 폴더별 상세 추출 가이드는 다음 문서를 참고하세요:

- 📁 `hero/README.md` - 히어로 이미지 추출 가이드
- 📁 `logo/README.md` - 로고 이미지 추출 가이드
- 📁 `features/README.md` - 게임 특징 이미지 추출 가이드
- 📁 `news/README.md` - 새소식 썸네일 추출 가이드
- 📁 `icons/README.md` - 아이콘 추출 가이드
- 📁 `../videos/README.md` - 영상 추출 가이드

**전체 가이드**: `docs/이미지추출가이드_상세.md`

## 🛠 이미지 추출 방법

### 방법 1: Python 스크립트 (자동화)
```bash
# 필요한 라이브러리 설치
pip install PyMuPDF

# 스크립트 실행
python scripts/extract_pdf_images.py
```

### 방법 2: Adobe Acrobat
1. Adobe Acrobat에서 PDF 열기
2. 도구 > 페이지 구성 선택
3. 이미지 선택 > 우클릭 > 이미지로 저장

### 방법 3: 스크린샷
1. PDF 뷰어에서 필요한 페이지 열기
2. Windows: `Win + Shift + S` (스니핑 도구)
3. 필요한 부분만 자르기
4. 적절한 폴더에 저장

## ⚠️ 주의사항

### 파일명
- HTML에 지정된 파일명과 정확히 일치해야 합니다
- 대소문자 구분 (Linux/Mac)
- 확장자 확인 (.png, .jpg, .mp4)

### 파일 형식
- 로고/아이콘: PNG (투명 배경 권장)
- 일반 이미지: JPG
- 영상: MP4 (H.264 코덱)

### 파일 경로
HTML에서는 상대 경로를 사용합니다:
```html
src="../../assets/images/hero/main-hero.png"
```

## 🔧 이미지 최적화 (권장)

웹 성능 향상을 위해 이미지 최적화를 권장합니다:

- [TinyPNG](https://tinypng.com/) - PNG/JPG 압축
- [Squoosh](https://squoosh.app/) - 온라인 이미지 최적화

**목표**: 파일 크기 최소화 + 품질 유지

---

**마지막 업데이트**: 2026-03-26
