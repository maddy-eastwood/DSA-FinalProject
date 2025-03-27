<script>
    import '../app.css';
    let { children } = $props();
</script>


<header class="title-outer-container">
    <div class="title-inner-container">
      <h1 class="webpage-title">What I Eat in a Day</h1>
    </div>
  </header>
{@render children()}

<style>
    .webpage-title {
      font-size: 28px;
      font-weight: 500;
      color: #079CFF;
    }
    
    .title-outer-container {
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #80D2FF;
      padding: 10px 24px;
      border-radius: 50px;
    }
    
    .title-inner-container {
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #92D5FA;
      width: 300px;
      height: 100px;
      border-radius: 50px;
    }
    </style>