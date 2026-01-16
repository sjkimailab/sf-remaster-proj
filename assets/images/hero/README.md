# 히어로 섹션 이미지

이 폴더에는 메인 히어로 섹션에서 사용하는 이미지들이 배치됩니다.

## 필요한 이미지

### PDF에서 추출할 이미지:
- `main-hero.png` - 메인 히어로 대표 이미지
- PDF의 메인 페이지 히어로 섹션에서 추출

## 사용 위치

- `src/html/index.html` - Hero Section
  ```html
  <img src="../../assets/images/hero/main-hero.png" alt="스페셜포스 리마스터">
  ```

## 이미지 추출 방법

1. PDF에서 메인 페이지(첫 페이지)의 히어로 섹션 이미지를 확인
2. 해당 이미지를 추출하여 `main-hero.png`로 저장
3. 권장 해상도: 최소 1920x1080px (웹용 최적화)
