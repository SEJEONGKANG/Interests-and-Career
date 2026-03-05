<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="../styles.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="/script.js"></script>
    <link rel="icon" href="/src/logo/snu_logo.png" />
    <link rel="apple-touch-icon" href="/src/logo/snu_logo.png" />
  </head>

  <body>
    <!-- Navbar 포함 -->
    <!--#include virtual="/navbar.asp" -->

    <br /><br /><br /><br /><br /><br /><br /><br />

    <section class="gallery-section standard-section">
      <div class="section-header">
        <h2>2026</h2>
      </div>
    </section>

    <div class="page-navigation">
      <a href="./gallery_2026.asp" class="nav-button">2026</a>
      <a href="./gallery_2025.asp" class="nav-button">2025</a>
      <a href="./gallery_2024.asp" class="nav-button">2024</a>
      <a href="./gallery_2023.asp" class="nav-button">2023</a>
      <a href="./gallery_2022.asp" class="nav-button">2022</a>
      <a href="./gallery_2021.asp" class="nav-button">2021</a>
      <a href="./gallery_2020.asp" class="nav-button">2020</a>
      <a href="./gallery_2019.asp" class="nav-button">2019</a>
      <a href="./gallery_2018.asp" class="nav-button">2018</a>
      <a href="./gallery_2017.asp" class="nav-button">2017</a>
      <a href="./gallery_2016.asp" class="nav-button">2016</a>
      <a href="./gallery_2015.asp" class="nav-button">2015</a>
      <a href="./gallery_2014.asp" class="nav-button">2014</a>
      <a href="./gallery_2013.asp" class="nav-button">2013</a>
    </div>

    <section class="gallery-section standard-section">
      <div class="section-header">
        <h2>Yang 교수님, Strazzullo 교수님 세미나</h2>
      </div>

      <div class="row">
        <div class="column">
          <img
            src="/src/gallery/26/260112_1.jpg"
            onclick="expandImage(this);"
          />
        </div>
        <div class="column">
          <img
            src="/src/gallery/26/260112_2.jpg"
            onclick="expandImage(this);"
          />
        </div>
        <div class="column">
          <img
            src="/src/gallery/26/260112_3.jpg"
            onclick="expandImage(this);"
          />
        </div>
        <div class="column">
          <img
            src="/src/gallery/26/260112_4.jpg"
            onclick="expandImage(this);"
          />
        </div>
        <div class="column">
          <img
            src="/src/gallery/26/260123_1.png"
            onclick="expandImage(this);"
          />
        </div>
      </div>

      <div class="expanding-container">
        <span onclick="closeImage(this);" class="closebtn">&times;</span>
        <img class="expandedImg" />
      </div>
    </section>

    <section class="gallery-section standard-section">
      <div class="section-header">
        <h2>김민정 박사 독일 포스트닥 환송회</h2>
      </div>

      <img src="/src/gallery/26/260123_2.jpg" style="width: 80vh" />
    </section>

    <!-- 상단 이동 버튼 -->
    <div class="scroll-to-top" id="scrollToTop">↑</div>

    <!-- Footer 포함 -->
    <!--#include virtual="/footer.asp" -->

    <script>
      // 페이지가 로드될 때 실행
      document.addEventListener("DOMContentLoaded", function () {
        const scrollToTopBtn = document.getElementById("scrollToTop");

        // 버튼 클릭 이벤트 리스너
        scrollToTopBtn.addEventListener("click", function () {
          // 부드러운 스크롤링 효과
          window.scrollTo({
            top: 0,
            behavior: "smooth",
          });
        });
      });
    </script>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        let currentYear = 2025;
        const footer = document.querySelector("footer"); // 기존 footer 요소 가져오기

        function loadGallery(year) {
          fetch(`./gallery_${year}.asp`)
            .then((response) => response.text())
            .then((html) => {
              const parser = new DOMParser();
              const doc = parser.parseFromString(html, "text/html");
              const newSections = doc.querySelectorAll(".gallery-section");

              newSections.forEach((section) => {
                document.body.insertBefore(section, footer); // footer 앞에 삽입
              });

              observeLastSection(year);
            })
            .catch((error) =>
              console.error(`${year} 갤러리를 불러오는 중 오류 발생:`, error)
            );
        }

        function observeLastSection(year) {
          const sections = document.querySelectorAll(".gallery-section");
          const newLastSection = sections[sections.length - 1];

          const observer = new IntersectionObserver(
            (entries) => {
              entries.forEach((entry) => {
                if (entry.isIntersecting) {
                  observer.unobserve(entry.target);
                  currentYear--;
                  if (currentYear >= 2013) {
                    loadGallery(currentYear);
                  }
                }
              });
            },
            { threshold: 0.5 }
          );

          observer.observe(newLastSection);
        }

        loadGallery(currentYear);
      });
    </script>
  </body>
</html>
