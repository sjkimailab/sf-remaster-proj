// SF 리마스터 메인 JavaScript

document.addEventListener('DOMContentLoaded', function() {
  
  // ============================================
  // Mobile Menu Toggle
  // ============================================
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const navMenu = document.querySelector('.nav-menu');
  
  if (mobileMenuToggle && navMenu) {
    mobileMenuToggle.addEventListener('click', function() {
      navMenu.classList.toggle('active');
      this.classList.toggle('active');
    });
    
    // 외부 클릭 시 메뉴 닫기
    document.addEventListener('click', function(e) {
      if (!navMenu.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
        navMenu.classList.remove('active');
        mobileMenuToggle.classList.remove('active');
      }
    });
  }
  
  // ============================================
  // Game Start Modal
  // ============================================
  const gameStartBtn = document.getElementById('gameStartBtn');
  const gameStartModal = document.getElementById('gameStartModal');
  const modalClose = document.querySelector('.modal-close');
  const modalBackdrop = document.querySelector('.modal-backdrop');
  
  // 모달 열기
  if (gameStartBtn && gameStartModal) {
    gameStartBtn.addEventListener('click', function() {
      gameStartModal.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  }
  
  // 모달 닫기
  function closeModal() {
    if (gameStartModal) {
      gameStartModal.classList.remove('active');
      document.body.style.overflow = '';
    }
  }
  
  if (modalClose) {
    modalClose.addEventListener('click', closeModal);
  }
  
  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', closeModal);
  }
  
  // ESC 키로 모달 닫기
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && gameStartModal && gameStartModal.classList.contains('active')) {
      closeModal();
    }
  });
  
  // ============================================
  // Smooth Scroll
  // ============================================
  const links = document.querySelectorAll('a[href^="#"]');
  
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#' || href === '') return;
      
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
  
  // ============================================
  // Header Scroll Effect
  // ============================================
  const header = document.querySelector('.header');
  let lastScroll = 0;
  
  window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset;
    
    if (header) {
      if (currentScroll > 100) {
        header.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
        header.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
      } else {
        header.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        header.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)';
      }
    }
    
    lastScroll = currentScroll;
  });
  
  // ============================================
  // News Card Click Handler
  // ============================================
  const newsCards = document.querySelectorAll('.news-card');
  
  newsCards.forEach(card => {
    card.addEventListener('click', function() {
      // 실제 구현 시 게시글 상세 페이지로 이동
      const newsTitle = this.querySelector('.news-title')?.textContent;
      console.log('News clicked:', newsTitle);
      // window.location.href = `/news/detail/[id]`;
    });
  });
  
  // ============================================
  // Feature Card Hover Animation
  // ============================================
  const featureCards = document.querySelectorAll('.feature-card');
  
  featureCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-10px)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });
  
  // ============================================
  // Video Background Fallback
  // ============================================
  const heroVideo = document.getElementById('heroVideo');
  
  if (heroVideo) {
    heroVideo.addEventListener('error', function() {
      // 영상 로드 실패 시 배경 이미지로 대체
      const heroSection = document.querySelector('.hero-section');
      if (heroSection) {
          heroSection.style.backgroundImage = 'url(/assets/images/hero/hero-bg-fallback.jpg)';
        heroSection.style.backgroundSize = 'cover';
        heroSection.style.backgroundPosition = 'center';
        this.style.display = 'none';
      }
    });
  }
  
  // ============================================
  // Lazy Loading Images (기본 구현)
  // ============================================
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
            observer.unobserve(img);
          }
        }
      });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
      imageObserver.observe(img);
    });
  }
  
  // ============================================
  // Image Error Handling (이미지 로드 실패 처리)
  // ============================================
  function handleImageError(img) {
    // 이미지 로드 실패 시 placeholder 처리
    img.classList.add('img-error');
    
    // alt 텍스트를 이용한 placeholder 생성
    const altText = img.alt || '이미지';
    const placeholder = document.createElement('div');
    placeholder.className = 'img-placeholder';
    placeholder.textContent = altText;
    
    // 부모 요소에 placeholder 추가
    if (img.parentElement) {
      img.style.display = 'none';
      img.parentElement.appendChild(placeholder);
    }
  }
  
  // 모든 이미지에 오류 핸들러 추가
  document.querySelectorAll('img').forEach(img => {
    // 이미 로드된 이미지 중 실패한 것 처리
    if (!img.complete || img.naturalHeight === 0) {
      handleImageError(img);
    }
    
    // 이미지 로드 실패 이벤트 리스너
    img.addEventListener('error', function() {
      handleImageError(this);
    });
  });
  
  console.log('SF 리마스터 웹사이트 로드 완료');
});
