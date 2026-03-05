document.addEventListener("DOMContentLoaded", function () {
  // Hamburger menu toggle
  const hamburgerMenu = document.getElementById("hamburgerMenu");
  const navLinks = document.getElementById("navLinks");

  if (hamburgerMenu && navLinks) {
    // Click and touch event for hamburger menu
    hamburgerMenu.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      this.classList.toggle("active");
      navLinks.classList.toggle("active");
    });

    hamburgerMenu.addEventListener("touchend", function (e) {
      e.preventDefault();
      e.stopPropagation();
      this.classList.toggle("active");
      navLinks.classList.toggle("active");
    });

    // Close menu when clicking outside
    document.addEventListener("click", function (event) {
      const isClickInsideNav = navLinks.contains(event.target);
      const isClickOnHamburger = hamburgerMenu.contains(event.target);

      if (
        !isClickInsideNav &&
        !isClickOnHamburger &&
        navLinks.classList.contains("active")
      ) {
        hamburgerMenu.classList.remove("active");
        navLinks.classList.remove("active");
      }
    });

    // Handle dropdown clicks on mobile
    const dropdowns = document.querySelectorAll(".dropdown");
    dropdowns.forEach((dropdown) => {
      const link = dropdown.querySelector("a");
      const hasDropdownMenu = dropdown.querySelector(".dropdown-menu");

      link.addEventListener("click", function (e) {
        if (window.innerWidth <= 800 && hasDropdownMenu) {
          // 드롭다운 메뉴가 있는 경우에만 기본 동작 방지
          e.preventDefault();
          e.stopPropagation();

          // 현재 드롭다운이 열려있는지 확인
          const isActive = dropdown.classList.contains("active");

          // 모든 드롭다운 닫기
          dropdowns.forEach((d) => d.classList.remove("active"));

          // 현재 드롭다운이 닫혀있었으면 열기
          if (!isActive) {
            dropdown.classList.add("active");
          }
        }
        // 드롭다운 메뉴가 없으면 정상적으로 링크 이동
      });
    });

    // 드롭다운 메뉴의 하위 항목 클릭 시 전체 메뉴 닫기
    const dropdownLinks = document.querySelectorAll(".dropdown-menu a");
    dropdownLinks.forEach((link) => {
      link.addEventListener("click", function () {
        if (window.innerWidth <= 800) {
          // 모든 드롭다운 닫기
          dropdowns.forEach((d) => d.classList.remove("active"));
          // 햄버거 메뉴도 닫기
          hamburgerMenu.classList.remove("active");
          navLinks.classList.remove("active");
        }
      });
    });
  }

  // On page load, animate elements
  const revealElements = document.querySelectorAll(".reveal-on-scroll");

  if (revealElements.length > 0) {
    const revealOnScroll = () => {
      const windowHeight = window.innerHeight;
      revealElements.forEach((element) => {
        const elementTop = element.getBoundingClientRect().top;
        if (elementTop < windowHeight * 0.8) {
          element.classList.add("visible");
        }
      });
    };

    window.addEventListener("scroll", revealOnScroll);
    revealOnScroll(); // Initial check to reveal on page load
  }

  // Image Slider functionality
  let currentIndex = 0;
  const images = document.querySelectorAll(".slider-image");
  const totalImages = images.length;

  if (totalImages > 0) {
    const sliderContainer = document.querySelector(".slider-container");

    function changeImage() {
      currentIndex = (currentIndex + 1) % totalImages;
      if (sliderContainer) {
        sliderContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
      }
    }

    // Auto slider change every 3 seconds
    setInterval(changeImage, 3000);

    // Allow manual click change (clicking the slider will advance to next image)
    document
      .querySelector(".image-slider")
      ?.addEventListener("click", changeImage);
  }

  // Researchers hover effect (데스크톱에서만)
  const profileImages = document.querySelectorAll(".profile-image");
  if (profileImages.length > 0) {
    // 터치 디바이스 감지
    const isTouchDevice =
      "ontouchstart" in window || navigator.maxTouchPoints > 0;

    // 데스크톱에서만 호버 효과 적용 (모바일에서 이미지 겹침 방지)
    if (!isTouchDevice && window.innerWidth > 800) {
      profileImages.forEach((image) => {
        image.addEventListener("mouseenter", () => {
          image.closest(".card")?.classList.add("image-focus");
        });

        image.addEventListener("mouseleave", () => {
          image.closest(".card")?.classList.remove("image-focus");
        });
      });
    }
  }

  // Gallery expand function
  window.expandImage = function (img) {
    const section = img.closest("section"); // 클릭된 이미지가 속한 섹션 찾기
    const expandingContainer = section.querySelector(".expanding-container");
    const expandedImg = section.querySelector(".expandedImg");

    if (
      expandingContainer.style.display === "block" &&
      expandedImg.src === img.src
    ) {
      // 동일한 이미지를 클릭하면 닫기
      expandingContainer.style.display = "none";
    } else {
      // 새 이미지 표시
      expandedImg.src = img.src;
      expandingContainer.style.display = "block";
    }
  };

  // Close expanded image
  window.closeImage = function (btn) {
    const expandingContainer = btn.closest(".expanding-container");
    expandingContainer.style.display = "none";
  };
});
