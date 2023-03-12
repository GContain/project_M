function view_map(lat, lng) {
    var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
        mapOption = {
            center: new kakao.maps.LatLng(lat, lng), // 지도의 중심좌표
            level: 6 // 지도의 확대 레벨
        };

    var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

    // 마커가 표시될 위치입니다 
    var markerPosition = new kakao.maps.LatLng(lat, lng);

    // 마커를 생성합니다
    var marker = new kakao.maps.Marker({
        position: markerPosition
    });

    // 마커가 지도 위에 표시되도록 설정합니다
    marker.setMap(map);

    // 아래 코드는 지도 위의 마커를 제거하는 코드입니다
    // marker.setMap(null);
}

function view1_map(lat, lng) {

    var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
        mapOption = {
            center: new kakao.maps.LatLng(lat, lng), // 지도의 중심좌표
            level: 3 // 지도의 확대 레벨
        };

    var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

    // 일반 지도와 스카이뷰로 지도 타입을 전환할 수 있는 지도타입 컨트롤을 생성합니다
    var mapTypeControl = new kakao.maps.MapTypeControl();

    // 지도 타입 컨트롤을 지도에 표시합니다
    map.addControl(mapTypeControl, kakao.maps.ControlPosition.TOPRIGHT);

    function getInfo() {
        // 지도의 현재 중심좌표를 얻어옵니다 
        var center = map.getCenter();

        // 지도의 현재 레벨을 얻어옵니다
        var level = map.getLevel();

        // 지도타입을 얻어옵니다
        var mapTypeId = map.getMapTypeId();

        // 지도의 현재 영역을 얻어옵니다 
        var bounds = map.getBounds();

        // 영역의 남서쪽 좌표를 얻어옵니다 
        var swLatLng = bounds.getSouthWest();

        // 영역의 북동쪽 좌표를 얻어옵니다 
        var neLatLng = bounds.getNorthEast();

        // 영역정보를 문자열로 얻어옵니다. ((남,서), (북,동)) 형식입니다
        var boundsStr = bounds.toString();


        var message = '지도 중심좌표는 위도 ' + center.getLat() + ', <br>';
        message += '경도 ' + center.getLng() + ' 이고 <br>';
        message += '지도 레벨은 ' + level + ' 입니다 <br> <br>';
        message += '지도 타입은 ' + mapTypeId + ' 이고 <br> ';
        message += '지도의 남서쪽 좌표는 ' + swLatLng.getLat() + ', ' + swLatLng.getLng() + ' 이고 <br>';
        message += '북동쪽 좌표는 ' + neLatLng.getLat() + ', ' + neLatLng.getLng() + ' 입니다';

        // 개발자도구를 통해 직접 message 내용을 확인해 보세요.
        // ex) console.log(message);
    }

}

// DB에 보유하고 있는 산의 위치를 모두 표시하는 함수
function view_all(mountain_latlng, mountain_name) {
    var mapContainer = document.getElementById('map'), // 지도를 표시할 div
        mapOption = { 
            center: new kakao.maps.LatLng(35.872940, 127.863671), // 지도의 중심좌표
            level: 13 // 지도의 확대 레벨
        };

    var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

    m_latlng = mountain_latlng;
    m_name = mountain_name;
    // console.log(m_latlng, m_name);  // 데이터 확인용

    // 특수문자, 괄호, 점 모두 제거 - 공백은 제거 안함
    let reg = /[`~!@#$%^&*()_|+\-=?;:'",<>\{\}\[\]\\\/]/gim;
    m_latlng = m_latlng.replace(reg, "").split(' ');
    console.log(m_latlng);

    m_name = m_name.replace(reg, "").split(' ');
    console.log(m_name);

    // 마커를 표시할 위치와 title 객체 배열입니다 
    var positions = [];
    for (var i = 0; i < m_name.length; i++ ) {
            temp = {
            title: m_name[i], 
            latlng: new kakao.maps.LatLng(m_latlng[i*2], m_latlng[i*2+1])
            }
            positions.push(temp)
    }

    // 마커 이미지의 이미지 주소입니다
    var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
        
    for (var i = 0; i < positions.length; i ++) {
        
        // 마커 이미지의 이미지 크기 입니다
        var imageSize = new kakao.maps.Size(24, 35); 
        
        // 마커 이미지를 생성합니다    
        var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 
        
        // 마커를 생성합니다
        var marker = new kakao.maps.Marker({
            map: map, // 마커를 표시할 지도
            position: positions[i].latlng, // 마커를 표시할 위치
            title : positions[i].title, // 마커의 타이틀, 마커에 마우스를 올리면 타이틀이 표시됩니다
            image : markerImage // 마커 이미지 
        });

        marker.setMap(map);
    }
}