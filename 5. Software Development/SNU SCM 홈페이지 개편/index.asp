<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="styles.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <base href="/" />
    <link rel="icon" href="/src/logo/favicon.ico"/>
    <link rel="apple-touch-icon" href="/src/logo/favicon.ico"/>
  </head>
  <body>
    <!-- Navbar 포함 -->
    <!--#include file="navbar.asp" -->

    <main>
      <!-- Section 0: Welcome -->
      <section class="welcome">
        <div class="line">
          <h1>Welcome to SNU SCM Lab</h1>
        </div>
        <div class="line">
          <h2>Seoul National University</h2>
        </div>
        <div class="line">
          <h2>Supply Chain Management Lab</h2>
        </div>
      </section>

      <!-- Section 1: Research Area -->
      <section class="research-area reveal-on-scroll">
        <div class="text-container">
          <h3>Main Research Areas</h3>
          <div class="reveal-on-scroll">
            <ul>
              <li>Production Planning and Control</li>
              <li>Supply Chain Management</li>
              <li>Production Scheduling</li>
              <li>Simulation</li>
              <li>Inventory Theory</li>
              <li>JIT Applications</li>
              <li>Analysis of Manufacturing Systems</li>
            </ul>
          </div>
        </div>

        <div class="image-slider" id="slider">
          <div class="slider-container">
            <img
              src="/src/gallery/25/250226_4.jpg"
              alt="Photo 1"
              class="slider-image"
            />
            <img
              src="/src/gallery/25/250226_2.jpg"
              alt="Photo 2"
              class="slider-image"
            />
            <img
              src="/src/gallery/25/250102.jpg"
              alt="Photo 3"
              class="slider-image"
            />
          </div>
        </div>
      </section>

      <!-- Section 2: Lab Info -->
      <section class="lab-info reveal-on-scroll">
        <div class="text-container">
          <h3>Lab Overview</h3>
          <div class="reveal-on-scroll">
            <p></p>
            <li><strong>Established Year</strong> 1992</li>
            <p></p>
            <li>
              <strong>Location</strong> Seoul, Gwanak-gu, Gwanak-ro 1,
              Department of Industrial Engineering, Seoul National University,
              Building 39, Room 312
            </li>
            <p></p>
            <li>
              <strong>Research Focus</strong> Optimization & Decision Support Systems, Simulation & Stochastic Modeling, AI in Industrial Engineering
            </li>
            <p></p>
          </div>
        </div>
      </section>

      <!-- Section 3: Gallery Preview -->
      <section class="gallery-preview reveal-on-scroll">
        <h1>Gallery Preview</h1>
        <div class="gallery-items">
          <div class="gallery-item reveal-on-scroll">
            <a href="../gallery/gallery_2025.asp">
              <img
                src="/src/gallery/25/250214_5.jpg"
                alt="Gallery Image 1"
                style="height: 15vh"
              />
            </a>
          </div>
          <div class="gallery-item reveal-on-scroll">
            <a href="../gallery/gallery_2025.asp">
              <img
                src="/src/gallery/25/250214_3.jpg"
                alt="Gallery Image 2"
                style="height: 15vh"
              />
            </a>
          </div>
          <div class="gallery-item reveal-on-scroll">
            <a href="../gallery/gallery_2025.asp">
              <img
                src="/src/gallery/25/250102_2.jpg"
                alt="Gallery Image 3"
                style="height: 15vh"
              />
            </a>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer 포함 -->
    <!--#include file="footer.asp" -->

    <script src="/script.js"></script>
  </body>
</html>
