<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>연락처 | 연구실</title>
    <link rel="stylesheet" href="../styles.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script
      type="text/javascript"
      src="https://oapi.map.naver.com/openapi/v3/maps.js?ncpClientId=ba8320xkuv"
    ></script>
    <link rel="icon" href="/src/logo/snu_logo.png"/>
    <link rel="apple-touch-icon" href="/src/logo/snu_logo.png"/>
  </head>
  <body>
    <!-- Navbar 포함 -->
    <!--#include virtual="/navbar.asp" -->

    <br /><br /><br /><br /><br /><br /><br /><br />

    <div id="map" style="width: 100%; height: 400px"></div>

    <script>
      var mapOptions = {
        center: new naver.maps.LatLng(37.4547424, 126.9514475),
        zoom: 18,
      };

      var map = new naver.maps.Map("map", mapOptions);

      // Add marker
      var marker = new naver.maps.Marker({
        position: new naver.maps.LatLng(37.4547424, 126.9514475),
        map: map,
        title: "서울대학교 공과대학 산업공학과",
      });

      // Add info window
      var contentString = [
        '<div class="iw_inner" style="padding: 10px;">',
        "   <h3>SNU SCM LAB</h3>",
        "   <p>서울대학교 39동 312호</p>",
        "</div>",
      ].join("");

      var infowindow = new naver.maps.InfoWindow({
        content: contentString,
      });

      // Add click event to marker
      naver.maps.Event.addListener(marker, "click", function (e) {
        if (infowindow.getMap()) {
          infowindow.close();
        } else {
          infowindow.open(map, marker);
        }
      });
    </script>

    <main class="contact-container">
      <h1>Contact</h1>
      <address class="contact-info">
        <p>
          <strong>주소:</strong> 서울특별시 관악구 관악로 1 서울대학교 공과대학
          산업공학과 39동 312호
        </p>
        <p><strong>전화:</strong> 02-880-7152</p>
      </address>
    </main>

    <!-- Footer 포함 -->
    <!--#include virtual="/footer.asp" -->
    
    <script src="/script.js"></script>
  </body>
</html>
