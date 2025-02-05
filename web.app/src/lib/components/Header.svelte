<script lang="ts">
  let currentTime = new Date();
  
  setInterval(() => {
    currentTime = new Date();
  }, 1000);
</script>

<header class="header">
  <div class="logo">2x.fan</div>
  <nav class="nav">
    <a href="/">首页</a>
    <a href="/about">关于</a>
  </nav>
</header>

<style>
  .header {
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 60px;
  }

  .logo {
    font-size: 1.5rem;
    font-weight: bold;
  }

  .time {
    font-family: monospace;
    font-size: 1.2rem;
  }

  .nav a {
    color: white;
    text-decoration: none;
    margin-left: 1rem;
  }

  .nav a:hover {
    color: #ff4444;
  }
</style> 