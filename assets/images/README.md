# 이미지 리소스 안내

이 폴더는 SF 리마스터 웹사이트에 사용되는 이미지 리소스를 저장하는 곳입니다.

## 폴더 구조

```
assets/images/
├── hero/              # 히어로 섹션 이미지
│   ├── hero-bg-fallback.jpg  # 배경 대체 이미지
│   └── main-hero.png         # 메인 히어로 이미지
├── logo/              # 로고 파일
│   ├── shield-logo.png       # 방패 로고
│   └── dragonfly-logo.png    # DragonFly 로고
├── news/              # 새소식 썸네일
│   └── placeholder.jpg
├── features/          # 게임 특징 이미지
│   ├── level-design.jpg
│   ├── moving-control.jpg
│   ├── shooting-system.jpg
│   └── weapon-system.jpg
├── icons/             # 아이콘 (별도 폴더 사용)
│   ├── steam-icon.png
│   └── epic-icon.png
└── videos/            # 비디오 파일 (선택사항)
    └── hero-bg.mp4
```

## 이미지 준비 필요

PDF에서 추출한 이미지를 위 폴더 구조에 맞춰 저장하세요.

### 필수 이미지
- [ ] `logo/shield-logo.png` - 방패 로고
- [ ] `logo/dragonfly-logo.png` - DragonFly 로고
- [ ] `hero/main-hero.png` - 메인 히어로 이미지
- [ ] `hero/hero-bg-fallback.jpg` - 배경 대체 이미지 (비디오 없을 경우)

### 선택 이미지
- [ ] `features/` 폴더의 게임 특징 이미지들
- [ ] `news/placeholder.jpg` - 새소식 썸네일
- [ ] `videos/hero-bg.mp4` - 히어로 배경 영상

## 임시 플레이스홀더

이미지가 준비되지 않은 경우, 브라우저에서 이미지가 보이지 않습니다. 
개발 중에는 임시로 플레이스홀더 이미지를 사용하거나, CSS로 배경색을 적용할 수 있습니다.
