# 로고 이미지

이 폴더에는 프로젝트에서 사용하는 모든 로고 파일들이 배치됩니다.

## 필요한 이미지

### PDF에서 추출할 이미지:
- `shield-logo.png` - 스페셜포스 방패 로고 (히어로 섹션용)
- `dragonfly-logo.png` - DragonFly 회사 로고 (푸터용)

## 사용 위치

### Shield Logo
- `src/html/index.html` - Hero Section
  ```html
  <img src="../../assets/images/logo/shield-logo.png" alt="스페셜포스 로고">
  ```

### DragonFly Logo
- `src/html/index.html` - Footer
  ```html
  <img src="../../assets/images/logo/dragonfly-logo.png" alt="DragonFly">
  ```

## 이미지 추출 방법

1. PDF에서 로고가 표시된 페이지 확인
2. 로고 이미지를 추출
3. PNG 형식으로 저장 (투명 배경 권장)
4. 권장 해상도:
   - Shield Logo: 최소 300x300px
   - DragonFly Logo: 최소 200x60px
