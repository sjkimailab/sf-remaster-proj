# 아이콘 이미지

이 폴더에는 프로젝트에서 사용하는 아이콘 파일들이 배치됩니다.

## 필요한 이미지

### PDF에서 추출할 이미지:
- `steam-icon.png` - Steam 플랫폼 아이콘
- `epic-icon.png` - Epic Games 플랫폼 아이콘

## 사용 위치

- `src/html/index.html` - Game Start Modal
  ```html
  <img src="../../assets/images/icons/steam-icon.png" alt="Steam">
  <img src="../../assets/images/icons/epic-icon.png" alt="Epic Games">
  ```

## 이미지 추출 방법

1. PDF에서 게임 시작 팝업 관련 페이지 확인
2. Steam, Epic Games 아이콘 추출
3. PNG 형식으로 저장 (투명 배경 권장)
4. 권장 해상도: 최소 64x64px 또는 128x128px

## 대안

PDF에 아이콘이 없는 경우:
- Steam 로고: [Steam Press Kit](https://partner.steamgames.com/doc/store/assets)
- Epic Games 로고: [Epic Games Brand Guidelines](https://www.epicgames.com/site/en-US/brand)
