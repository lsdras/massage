var HOME_PATH = window.HOME_PATH || '.';

var POSITIONS = data;

var map = new naver.maps.Map('map', {
    center: new naver.maps.LatLng(35.2289348, 126.8476802),
    zoom: 14
});

var bounds = map.getBounds(),
    southWest = bounds.getSW(),
    northEast = bounds.getNE(),
    lngSpan = northEast.lng() - southWest.lng(),
    latSpan = northEast.lat() - southWest.lat();

var markers = [],
    infowindows = [];

for (var i = 0; i < POSITIONS.length; i++) {


    var position = new naver.maps.LatLng(POSITIONS[i].y, POSITIONS[i].x);
    var marker = new naver.maps.Marker({
        map: map,
        position: position,
        title: POSITIONS[i].name,
        icon: {
            url: "https://github.com/navermaps/maps.js.en/blob/master/docs/img/example/pin_map.png",
            size: new naver.maps.Size(24, 37),
            scaledSize: new naver.maps.Size(25, 34),
            anchor: new naver.maps.Point(12, 37),
            origin: new naver.maps.Point(POSITIONS[i].y, POSITIONS[i].x)
        },
        zIndex: 100
    });
    var infoWindow = new naver.maps.InfoWindow({
        content: '<div style="width:200px;text-align:left;padding:10px;">'
            + '업체명: <b>' + POSITIONS[i].name + '</b><br>'
            + '전화: <b>' + POSITIONS[i].phone + '</b><br>'
            + '안마사협회 관련: <a href="' + POSITIONS[i].hlink + '"><b>' + POSITIONS[i].checked + '</b></a><br>'
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

    var mapBounds = map.getBounds();
    var marker, position;

    for (var i = 0; i < markers.length; i++) {

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
        var marker = markers[seq],
            infoWindow = infowindows[seq];

        if (infoWindow.getMap()) {
            infoWindow.close();
        } else {
            infoWindow.open(map, marker);
        }
    }
}

for (var i = 0, ii = markers.length; i < ii; i++) {
    naver.maps.Event.addListener(markers[i], 'click', getClickHandler(i));
}
