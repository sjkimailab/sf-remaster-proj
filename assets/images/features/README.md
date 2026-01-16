# 게임 특징 이미지

이 폴더에는 게임 특징 섹션에서 사용하는 이미지들이 배치됩니다.

## 필요한 이미지

### PDF에서 추출할 이미지 (4개):
- `level-design.jpg` - 레벨 디자인 특징 이미지
- `moving-control.jpg` - 무빙 컨트롤 특징 이미지
- `shooting-system.jpg` - 사격 시스템 특징 이미지
- `weapon-system.jpg` - 무기 시스템 특징 이미지

## 사용 위치

- `src/html/index.html` - Game Features Section
  ```html
  <img src="../../assets/images/features/level-design.jpg" alt="레벨 디자인">
  <img src="../../assets/images/features/moving-control.jpg" alt="무빙 컨트롤">
  <img src="../../assets/images/features/shooting-system.jpg" alt="사격 시스템">
  <img src="../../assets/images/features/weapon-system.jpg" alt="무기 시스템">
  ```

## 이미지 추출 방법

1. PDF에서 "게임 특징" 섹션 페이지 확인
2. 각 특징별 이미지를 추출
3. JPG 형식으로 저장
4. 권장 해상도: 최소 800x600px (16:9 또는 4:3 비율)
