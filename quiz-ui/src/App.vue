<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <aside class="sidebar">
      <div class="logo-container">
        <img src="@/assets/QuizLogo.png" alt="Logo" class="logo" />
      </div>
      <nav>
        <RouterLink to="/">Accueil</RouterLink>
        <RouterLink to="/admin">Administrateur</RouterLink>
      </nav>
    </aside>
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.sidebar {
  width: 20%;
  background-color: #1635b257;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-container {
  margin-bottom: 2rem;
}

.logo {
  width: 150px;
  height: auto;
}

.sidebar nav {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.sidebar a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s;
  text-align: center;
}

.sidebar a:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.main-content {
  flex: 1;
  /*display: flex;*/
  justify-content: center;
  align-items: center;
  overflow: auto;
}

@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
    flex-direction: row;
    justify-content: space-around;
  }

  .sidebar nav {
    flex-direction: row;
  }
}
</style>
