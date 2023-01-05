
📌 Place-Repository
=============

## ❗️Description
 **Place Repository**는 음식점 평가 웹페이지로 사용자가 자신이 가본 음식점을 평가하고 그 기록을 저장할 수 있는 웹 페이지입니다.<br>
 우리는 가봤던 음식점 중 괜찮았던 곳을 다른 사람에게 추천하거나 재방문 하는 경우가 많습니다. 그때, 음식점의 이 름이 뭐였는지 까먹거나, 비슷한 메뉴가 많은 경우 어떤 음식이 맛있었는지 헷갈리는 경우가 있습니다. Place Repository는 음식점에 대해 평가하고 그에 대한 코멘트를 기록함으로써 이러한 문제를 해결할 수 있습니다.<br>
 기존의 음식점을 평가하는 기능들은 대부분 평가가 5단계로만 가능해 상세한 평가가 어려운 단점이 있습니다. 이것을 개선하여 Place Repository에서는 0레벨부터 10레벨까지 11레벨로 장소에 대한 평가가 가능하고 그 장소에 대한 코멘트를 작성할 수 있습니다. 또한 기존에는 내가 평가한 장소에 대한 정보를 한 번에 모아 보기 힘든 점을 개선하여 내가 저장한 장소와 그 평가들을 한 번에 볼 수 있습니다.<br>
구현하려고 한 주요 기능은 `(1) 로그인 및 가입 기능`, `(2) 음식점 링크를 입력하여 평가하고 코멘트를 달아 저장하는 기능`, `(3) 사용자가 저장한 음식점을 모아 보는 기능`, `(4) 사용자가 선택한 음식점 타입에 따라 평점 순으로 음식점을 추천하는 기능`, `(5) 추천 받은 음식점 즐겨찾기에 등록하는 기능`입니다.

## ❗️ERD
<img src="https://github.com/chaeyoungeee/Place-Repository/blob/main/img/erd(1).png" width="90%">
<img src="https://github.com/chaeyoungeee/Place-Repository/blob/main/img/erd(2).png" width="90%">

## ❗️Main Functions
> 첫번째 기능은 **회원 가입 기능**입니다. <br>
> 사용자는 회원 가입을 하기 위해 아이디와 비밀번호를 입력해야 합니다. 입력한 정보는 user 테이블에 저장됩니다. 회원 가입 이후 로그인을 하여 나머지 기능들을 이용할 수 있습니다.
###### [1] Sign up 페이지
<img src="https://github.com/chaeyoungeee/Place-Repository/blob/main/img/sign_up.png" width="70%">

###### [2] Login 페이지
<img src="https://github.com/chaeyoungeee/Place-Repository/blob/main/img/login.png" width="70%"><br><br>

> 두번째 기능은 **음식점 링크를 입력하여 평가하고 코멘트를 달아 저장소에 저장하는 기능**입니다. <br>
> 사용자는 Save Place 페이지에서 URL에 네이버에 검색한 음식점 링크를 입력하고, 0레벨부터 10레벨 중 평점을 선택하고, 코멘트를 입력하여 음식점을 저장할 수 있습니다. 사용자가 입력한 링크에서 크롤링 해온 음식점명, 평점, 위치, 타입 데이터는 place 테이블에 저장됩니다. 만약 place 테이블에 중복되는 데이터가 있다면 저장되지 않습니다. 또한 사용자의 평점 과 아이디, 음식점명, 코멘트는 place_comment 테이블에 저장됩니다. 만약 사용자가 자신이 이미 저장한 음식점을 다시 저장하면 평점과 코멘트가 업데이트 됩니다.
###### [3] Save Place 페이지
<img src="https://github.com/chaeyoungeee/Place-Repository/blob/main/img/save_place.png" width="70%"><br><br>

> 세번째 기능은 **사용자 자신이 저장한 음식점을 모아보는 기능**입니다. <br>
> 사용자가 Save Place 페이지에서 Go storage 버튼을 누르면, place_comment 테이블에 저장된 아이디가 현재 사용자의 아이디와 일치하는 데이터를 선택해 음식 점명, 음식점 타입, 사용자 평점, 코멘트를 제공해줍니다.
###### [4] Place Storage 페이지
<img src="https://github.com/chaeyoungeee/Place-Repository/blob/main/img/place_storage.png" width="70%"><br><br>

> 네번째 기능은 **사용자가 음식점 타입을 선택하면 음식점을 추천해주는 기능**입니다. <br>
> 사용자가 Save Place 페이지에서 Recommend 버튼을 누르면 place 테이블에 저장된 데이터 중 음식점 타입들을 선택해 와 사용자에게 제공해줍니다. 사용자는 전체보기나 이 타입들 중 하나를 선택해 음식점 타입에 따라 추천 받을 수 있습니다. 사용자가 음식점 타입을 선택하면 place 테이블에서 사용자가 선택한 음식점 타입과 같은 음식점 타입을 가지는 데이터를 선택해 와 사용자에 게 평점이 높은 순으로 제공해줍니다.
###### [5] Select Type 페이지
<img src="https://github.com/chaeyoungeee/Place-Repository/blob/main/img/select_type.png" width="70%"><br><br>

> 다섯번째 기능은 **추천 받은 음식점을 즐겨찾기에 등록하는 기능**입니다. <br>
> 사용자는 추천 받은 음식점 밑의 Favorites 버튼을 눌러 음식점을 즐겨찾기에 등록할 수 있습니다. 사용자가 Favorites 버튼을 누르면 favorites 테이블에 사용자 의 아이디와 그 음식점명이 저장됩니다. 즐겨찾기로 등록된 음식점은 Save Place 페이지의 Favorites 버튼을 누르면 모아볼 수 있습니다. 사용자가 Save Place 페이지의 Favorites 버튼을 누르면 favorites 테이블에서 현재 로그인한 사 용자의 아이디와 일치하는 아이디의 음식점명을 선택해옵니다. 그 후 place 테이블에서 앞에서 선택해 온 음식점명과 일치하는 음식점명을 가진 데이터의 음식점명, 음식점 타입, 평점, 위치를 선택해 와 사용자에게 제공해줍니다.
###### [6] Favorite 페이지
<img src="https://github.com/chaeyoungeee/Place-Repository/blob/main/img/favorite.png" width="70%">
