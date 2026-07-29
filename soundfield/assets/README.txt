SoundField 소개 페이지 — 에셋 넣는 곳
=====================================

아래 "파일명" 그대로 이 폴더(assets/)에 넣으면 표시됩니다.
- 미리보기: index.html 을 브라우저로 열기 (assets/ 가 옆에 있어야 이미지 보임)
- 배포용 단일 파일: 상위 폴더에서  python build_standalone.py  실행
    → index_standalone.html 하나로 이미지가 전부 박혀서(그림/움짤 포함) 어디서 열어도 보임

움짤(움직이는 이미지)은 .gif 로 넣으면 <img> 에서 자동 재생됩니다.
(어느 화면 슬롯이든 .gif 를 같은 파일명으로 넣으면 그 자리에서 움직임)

권장 캡처 (PNG 또는 움짤 GIF, 가로형):
  hero.png            메인 창 전체 (좌 트리 + 중앙 결과 + 하단 파형)   [16:10]
  shot_indexing.png   인덱싱 진행 / 라이브러리 현황 진행 화면            [16:9]
  shot_search.png     검색어 + 다중 필터 + 결과 테이블                  [16:10]
  shot_browser.png    좌측 라이브러리 트리 + 탭                         [4:3]
  shot_player.png     파형 + 재생 컨트롤                               [16:9]
  shot_segment.png    세그먼트 자동 분할 표시                          [16:9]
  shot_history.png    재생 히스토리 드로어                             [16:9]
  shot_export.png     구간 선택 + 내보내기                             [16:9]
  shot_status.png     라이브러리 현황 다이얼로그 (재시도/제거)          [16:10]
  shot_extra.png      (선택) 원하는 추가 화면                          [16:10]

테마 3종 (페이지 표시 순서: Neutral=기본, Neon, Light):
  theme_neutral.png   Neutral(그레이) 테마 전체 화면 — 기본 테마        [16:10]
  theme_neon.png      Neon(다크 네이비) 테마 전체 화면                  [16:10]
  theme_light.png     Light(베이지) 테마 전체 화면                      [16:10]

팁
- 캡처 비율은 위 [ ] 권장값에 가깝게 하면 잘림이 적습니다(object-fit: cover, 상단 정렬).
- 파일명이 정확해야 자동으로 붙습니다. 대소문자 구분됨.
- 구동 영상(mp4) 섹션은 제거됨 — 움짤 GIF 를 화면 슬롯에 넣는 방식으로 대체.
