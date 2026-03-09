<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="../styles.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="/script.js"></script>
    <link rel="icon" href="/src/logo/snu_logo.png"/>
    <link rel="apple-touch-icon" href="/src/logo/snu_logo.png"/>
  </head>

  <body>
    <!-- Navbar 포함 -->
    <!--#include virtual="/navbar.asp" -->

    <br /><br /><br /><br /><br /><br /><br /><br />

    <section class="gallery-section standard-section">
        <div class="section-header">
          <h2>2020</h2>
        </div>
      </section>

    <div class="page-navigation">
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
        <h2>2020 추계학술대회</h2>
      </div>

      <div class="row">
        <div class="column">
          <img src="/src/gallery/20/13.jpg" onclick="expandImage(this);" />
        </div>
        <div class="column">
          <img src="/src/gallery/20/14.jpg" onclick="expandImage(this);" />
        </div>
        <div class="column">
          <img src="/src/gallery/20/15.jpg" onclick="expandImage(this);" />
        </div>
      </div>

      <div class="expanding-container">
        <span onclick="closeImage(this);" class="closebtn">&times;</span>
        <img class="expandedImg" />
      </div>
    </section>

    <section class="gallery-section standard-section">
      <div class="section-header">
        <h2>트라이월드홀딩스와의 업무협약</h2>
      </div>

      <img src="/src/gallery/20/12.jpg" style="width: 80vh" />
    </section>

    <section class="gallery-section standard-section">
      <div class="section-header">
        <h2>2020 학위수여식</h2>
      </div>

      <div class="row">
        <div class="column">
          <img src="/src/gallery/20/10.jpg" onclick="expandImage(this);" />
        </div>
        <div class="column">
          <img src="/src/gallery/20/11.jpg" onclick="expandImage(this);" />
        </div>
      </div>

      <div class="expanding-container">
        <span onclick="closeImage(this);" class="closebtn">&times;</span>
        <img class="expandedImg" />
      </div>
    </section>

    <section class="gallery-section standard-section">
      <div class="section-header">
        <h2>2020 워크샵</h2>
      </div>

      <div class="row">
        <div class="column">
          <img src="/src/gallery/20/4.jpg" onclick="expandImage(this);" />
        </div>
        <div class="column">
          <img src="/src/gallery/20/5.jpg" onclick="expandImage(this);" />
        </div>
        <div class="column">
          <img src="/src/gallery/20/6.jpg" onclick="expandImage(this);" />
        </div>
        <div class="column">
          <img src="/src/gallery/20/7.jpg" onclick="expandImage(this);" />
        </div>
        <div class="column">
          <img src="/src/gallery/20/8.jpg" onclick="expandImage(this);" />
        </div>
        <div class="column">
          <img src="/src/gallery/20/9.jpg" onclick="expandImage(this);" />
        </div>
      </div>

      <div class="expanding-container">
        <span onclick="closeImage(this);" class="closebtn">&times;</span>
        <img class="expandedImg" />
      </div>
    </section>

    <section class="gallery-section standard-section">
      <div class="section-header">
        <h2>INFORMS 2020 Monterey</h2>
      </div>

      <div class="row">
        <div class="column">
          <img src="/src/gallery/20/01.jpg" onclick="expandImage(this);" />
        </div>
        <div class="column">
          <img src="/src/gallery/20/02.jpg" onclick="expandImage(this);" />
        </div>
        <div class="column">
          <img src="/src/gallery/20/03.jpg" onclick="expandImage(this);" />
        </div>
      </div>

      <div class="expanding-container">
        <span onclick="closeImage(this);" class="closebtn">&times;</span>
        <img class="expandedImg" />
      </div>
    </section>
    <!-- 상단 이동 버튼 -->
    <div class="scroll-to-top" id="scrollToTop">↑</div>

    <!-- Footer 포함 -->
    <!--#include virtual="/footer.asp" -->

    <script>
        // 페이지가 로드될 때 실행
        document.addEventListener('DOMContentLoaded', function() {
            const scrollToTopBtn = document.getElementById('scrollToTop');

            // 버튼 클릭 이벤트 리스너
            scrollToTopBtn.addEventListener('click', function() {
                // 부드러운 스크롤링 효과
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        });
    </script>

</body>
</html>
