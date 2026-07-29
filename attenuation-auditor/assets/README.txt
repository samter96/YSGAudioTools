Attenuation Auditor 소개 페이지 — 에셋 넣는 곳
==============================================

아래 "파일명" 그대로 이 폴더(assets/)에 넣으면 표시됩니다.
- 미리보기: index.html 을 브라우저로 열기 (assets/ 가 옆에 있어야 이미지 보임)
- 배포용 단일 파일: 상위 폴더에서  python build_standalone.py  실행
    → index_standalone.html 하나로 이미지가 전부 박혀서 어디서 열어도 보임

움짤(움직이는 이미지)은 .gif 로 넣으면 <img> 에서 자동 재생됩니다.
(어느 화면 슬롯이든 .gif 를 같은 파일명으로 넣으면 그 자리에서 움직임)

필요한 캡처
-----------
  hero.png                    메인 창 전체 (좌 스코프 트리 + 우 위반 목록)   [16:10]
  shot_scope.png              좌측 스캔 범위 트리 + 오브젝트 타입 패널       [4:3]
  shot_result.png             스캔 후 위반 목록 테이블                       [16:9]
  shot_exception.png          예외 처리 탭                                   [16:9]

이미 들어있는 것
----------------
  wwise_property_editor.png   Wwise Property Editor 의 Listener Relative     [3:4]
                              Routing / Attenuation 섹션
                              → 저장소(Wwise-Attenuation-Auditor/screenshots)
                                에 있던 것을 그대로 가져옴. 교체해도 됩니다.

팁
---
- 캡처 비율은 위 [ ] 권장값에 가깝게 하면 잘림이 적습니다.
  (object-fit: contain 이라 잘리지는 않고 여백이 생깁니다)
- 파일명이 정확해야 자동으로 붙습니다. 대소문자 구분됨.
- 파일이 없으면 그 자리에 파일명이 적힌 회색 플레이스홀더가 보입니다.
  즉 지금 상태로도 페이지는 정상적으로 열립니다.
- 위반 목록 캡처는 실제 위반 행이 몇 개 보이는 상태가 설명에 좋습니다.
  다만 사내 에셋 이름·경로가 이미지에 들어가니 공유 범위를 고려하세요.
