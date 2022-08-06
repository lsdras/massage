
const HOME_PATH = window.HOME_PATH || '.';

const POSITIONS = data;

const map = new naver.maps.Map('map', {
    center: new naver.maps.LatLng(35.2289348, 126.8476802),
    zoom: 14
});


let markers = [],
    infowindows = [];

for (var i = 0; i < POSITIONS.length; i++) {

    let position = new naver.maps.LatLng(POSITIONS[i].y, POSITIONS[i].x);

    let img_url = undefined;
    if (POSITIONS[i].checked.startsWith("O")) {
        img_url = "./images/ico_pin_blue.png"
    } else if (POSITIONS[i].checked.startsWith("X")) {
        img_url = "./images/ico_pin_red.png"
    } else {
        img_url = "./images/ico_pin_brown.png"
    }

    let marker = new naver.maps.Marker({
        map: map,
        position: position,
        title: POSITIONS[i].name,
        icon: {
            url: img_url,
            size: new naver.maps.Size(25, 34),
            scaledSize: new naver.maps.Size(25, 34),
        },
        zIndex: 100
    });

    let infoWindow = new naver.maps.InfoWindow({
        content: '<div style="width:200px;text-align:left;padding:10px;">'
            + '업체명: <b>' + POSITIONS[i].name + '</b><br>'
            + '전화: <b>' + POSITIONS[i].phone + '</b><br>'
            + '안마사협회 관련: <a href="' + POSITIONS[i].link + '"><b>' + POSITIONS[i].checked + '</b></a><br>'
            + '주소: ' + POSITIONS[i].unique_addr + '<br>'
            + '</div>'
    });

    markers.push(marker);
    infowindows.push(infoWindow);
};

naver.maps.Event.addListener(map, 'idle', function () {
    updateMarkers(map, markers);
});

function updateMarkers(map, markers) {

    let mapBounds = map.getBounds();
    let marker, position;

    for (let i = 0; i < markers.length; i++) {

        marker = markers[i]
        position = marker.getPosition();

        if (mapBounds.hasLatLng(position)) {
            showMarker(map, marker);
        } else {
            hideMarker(map, marker);
        }
    }
}

function showMarker(map, marker) {

    if (marker.setMap()) return;
    marker.setMap(map);
}

function hideMarker(map, marker) {

    if (!marker.setMap()) return;
    marker.setMap(null);
}

// 해당 마커의 인덱스를 seq라는 클로저 변수로 저장하는 이벤트 핸들러를 반환합니다.
function getClickHandler(seq) {
    return function (e) {
        let marker = markers[seq],
            infoWindow = infowindows[seq];

        if (infoWindow.getMap()) {
            infoWindow.close();
        } else {
            infoWindow.open(map, marker);
        }
    }
}

for (let i = 0, ii = markers.length; i < ii; i++) {
    naver.maps.Event.addListener(markers[i], 'click', getClickHandler(i));
}


function onSuccessGeolocation(position) {
    let location = new naver.maps.LatLng(position.coords.latitude,
        position.coords.longitude);
    let infowindow = new naver.maps.InfoWindow();
    map.setCenter(location);
    map.setZoom(14);

    infowindow.setContent('<div style="padding:20px;">' + '<b>현위치</b><br>(GeoLocation API에 따른 값으로, 오차가 발생할 수 있습니다.)' + '</div>');

    infowindow.open(map, location);
    //console.log('Coordinates: ' + location.toString());
}

function onErrorGeolocation() {
    let center = map.getCenter();
    let infowindow = new naver.maps.InfoWindow();
    infowindow.setContent('<div style="padding:20px;">' +
        '<h5 style="margin-bottom:5px;color:#f00;">Geolocation failed!</h5>' + "latitude: " + center.lat() + "<br />longitude: " + center.lng() + '</div>');

    infowindow.open(map, center);
}

window.addEventListener('load', function () {
    if (navigator.geolocation) {
        /**
         * navigator.geolocation 은 Chrome 50 버젼 이후로 HTTP 환경에서 사용이 Deprecate 되어 HTTPS 환경에서만 사용 가능 합니다.
         * http://localhost 에서는 사용이 가능하며, 테스트 목적으로, Chrome 의 바로가기를 만들어서 아래와 같이 설정하면 접속은 가능합니다.
         * chrome.exe --unsafely-treat-insecure-origin-as-secure="http://example.com"
         */
        navigator.geolocation.getCurrentPosition(onSuccessGeolocation, onErrorGeolocation);
    } else {
        let infowindow = new naver.maps.InfoWindow();
        let center = map.getCenter();
        infowindow.setContent('<div style="padding:20px;"><h5 style="margin-bottom:5px;color:#f00;">위치정보 사용 불가능.</h5></div>');
        infowindow.open(map, center);
    }
});

