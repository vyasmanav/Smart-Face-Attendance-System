class Head extends HTMLElement {
    connectedCallback(){
        this.innerHTML = `
        <link rel="stylesheet" href="assets/css/animate.css">
        <link rel="stylesheet" href="assets/css/bootstrap.min.css">
        <link rel="stylesheet" href="assets/css/font-awesome.min.css">
        <link rel="stylesheet" href="assets/css/slick.css">
        <link rel="stylesheet" href="assets/css/meanmenu.css">
        <link rel="stylesheet" href="assets/css/magnific-popup.css">
        <link rel="stylesheet" href="assets/css/style.css">
        `
    }
}

class Header extends HTMLElement {
    connectedCallback() {
      this.innerHTML = `
      <!-- Header Section -->
      <header class="header-section">
          <!-- Topbar Area -->
          <div class="topbar-area">
              <div class="container">
                  <div class="row">
                      <div class="col-lg-6">
                          <div class="topbar-contact">
                              <a href="#"><span><i class="fa fa-phone"></i></span> +(402) 762 441 83</a>
                              <a href="#" class="margin-left email-address"><span><i class="fa fa-envelope"></i></span>
                                  support@example.com</a>
                          </div>
                      </div>
                      <div class="col-lg-6">
                          <div class="topbar-button">
                              <a href="login.html"><span><i class="fa fa-sign-in"></i></span> Login</a>
                              <a href="register.html" class="margin-left"><span><i class="fa fa-user"></i></span>
                                  Register</a>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
  
          <!-- Menu Area -->
          <div class="menu-area">
              <div class="container">
                  <div class="row align-items-center">
                      <div class="col-lg-2">
                          <div class="logo-area">
                              <div class="symbol">
                                  <a href="#">
                                      <img src="assets/images/newlogo.jpg" alt="logo">
                                  </a>
                                  <h5>    
                                      <!-- 462 -->
                                      </h5>
                              </div>
                          </div>
                      </div>
                      <div class="col-lg-9">
                          <nav id="mobile-menu">
                              <ul class="main-menu">
                            
                                  <li><a href="student-contect.html">contact</a></li>
                                  <li class="menu-btn"><a href="student-about.html">About Us</a></li>
                              </ul>
                          </nav>
                      </div>
                  </div>
              </div>
              <div class="mobile-menu"></div>
          </div>
      </header>
  

        `
    }
  }
  //Footer
  class Footer extends HTMLElement {
    connectedCallback() {
      this.innerHTML = 
        `
      <!-- Footer Section -->
      <footer class="footer-section padding-top-115">
          <div class="container">
              <!-- Widget Area -->
              <div class="widget-area padding-bottom-60">
                  <div class="row">
                      <div class="col-lg-3 col-md-6">
                          <div class="footer-widget about-widget">
                              <div class="widget-title">
                                  <h5>about us</h5>
                              </div>
                              <p>The Smart Face Attendance System is an advanced solution that simplifies attendance tracking using facial recognition. It improves efficiency, accuracy, and security while offering a smooth and user-friendly experience.</p>
                          </div>
                      </div>
                
                      <div class="col-lg-3 col-md-6">
                          <div class="footer-widget address-widget">
                              <div class="widget-title">
                                  <h5>address</h5>
                              </div>
                              <ul>
                                  <li><span class="i fa fa-envelope"></span><span
                                          class="text-lowercase margin-left-10">ljcca@gmail.com</span></li>
                                  <li><span class="i fa fa-phone"></span><span class="margin-left-10">+91 1234567890 
                                          </span></li>
                                  <li><span class="i fa fa-building"></span><span class="margin-left-10">Vastrapur,
                                          IIM</span>
                                  </li>
                              </ul>
                          </div>
                      </div>
                  </div>
              </div>
              <!-- Copyright Area -->
              <div class="copyright-area padding-20">
                  <div class="row">
                      <div class="col-md-6">
                          <div class="copyright-left">
                              <span>Copyright <a href="#">SFAS</a> 2025 All Right Reserved.</span>
                          </div>
                      </div>
                      <div class="col-md-6">
                          <div class="copyright-links">
                              <ul>
                                  <li><a href="#">about</a></li>
                                  <li><a href="#">contact</a></li>
                              </ul>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </footer>
  
        `
      
    }
  }

class JS extends HTMLElement {
    connectedCallback(){
        this.innerHTML = `
        <script src="assets/js/vendor/jquery-2.2.4.min.js"></script>
        <script src="assets/js/vendor/bootstrap.min.js"></script>
        <script src="assets/js/vendor/slick.min.js"></script>
        <script src="assets/js/vendor/counterup.min.js"></script>
        <script src="assets/js/vendor/waypoints.min.js"></script>
        <script src="assets/js/vendor/easing.min.js"></script>
        <script src="assets/js/vendor/meanmenu.min.js"></script>
        <script src="assets/js/vendor/jquery.magnific-popup.js"></script>
        <script src="assets/js/vendor/wow.min.js"></script>
        <script src="assets/js/main.js"></script>
        `
    }
}
  
  customElements.define('main-header', Header);
  customElements.define('main-css',Head)
  customElements.define('main-js',JS)
  customElements.define('main-footer', Footer);