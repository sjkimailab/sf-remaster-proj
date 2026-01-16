# 영상 파일

이 폴더에는 프로젝트에서 사용하는 영상 파일들이 배치됩니다.

## 필요한 영상

### PDF에서 추출할 영상:
- `hero-bg.mp4` - 히어로 섹션 배경 영상 (무한 재생)

## 사용 위치

- `src/html/index.html` - Hero Section
  ```html
  <video autoplay muted loop playsinline>
    <source src="../../assets/videos/hero-bg.mp4" type="video/mp4">
  </video>
  ```

## 영상 추출 방법

1. PDF에서 히어로 섹션 관련 영상 확인
2. 영상 파일이 포함된 경우 추출
3. MP4 형식으로 저장 (H.264 코덱 권장)
4. 권장 사양:
   - 해상도: 1920x1080px
   - 프레임레이트: 30fps
   - 파일 크기: 최적화 (웹용, 가능하면 5MB 이하)

## 대안

PDF에 영상이 없는 경우:
- 대표 이미지로 대체 가능
- 또는 샘플 배경 영상 사용

## 참고

HTML에서는 영상이 없을 경우 배경 이미지로 대체되도록 설정되어 있습니다.
