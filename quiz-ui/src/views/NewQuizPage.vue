<template>
  <div class="outer-container">
    <div class="container mt-5">
      <img src="@/assets/quizMas.png" alt="Quiz Image" class="quiz-image" />
      <h1 class="mb-4">Nouvelle Partie de Quiz</h1>
      <form @submit.prevent="launchNewQuiz">
        <div class="mb-3">
          <label for="username" class="form-label">Saisissez votre nom :</label>
          <input type="text" id="username" v-model="username" class="form-control" placeholder="Votre nom" required />
        </div>
        <button type="submit" class="btn btn-outline-success">Commencer</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from "@/services/ParticipationStorageService";

const username = ref('');
const router = useRouter();

function launchNewQuiz() {
  if (username.value.trim()) {
    // Enregistrer le nom du joueur
    participationStorageService.savePlayerName(username.value);
    console.log("Launch new quiz with", username.value);
    // Naviguer vers la page des questions avec le nom du joueur en tant que paramètre
    router.push({ path: '/questions', query: { playerName: username.value } });
  } else {
    alert("Veuillez saisir votre nom pour commencer.");
  }
}
</script>


<style scoped>
.outer-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem 0;
  background-color: #f0f4f8;
}

.container {
  max-width: 700px;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 7px rgba(0, 0, 0, 0.1);
  text-align: center;
  margin: 2rem 0;
}

.quiz-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 1.5rem;
  max-height: 200px; 
}

h1 {
  font-size: 2rem;
  color: #333;
}

.form-label {
  font-size: 1.25rem;
  color: #555;
}

.form-control {
  padding: 0.75rem;
  font-size: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  margin-top: 1rem;
}

.btn-outline-success {
  color: #1635b257;
  border-color: #1635b257;
}

.btn-outline-success:hover {
  background-color: #1635b257;
}

@media (max-width: 768px) {
  .container {
    margin-top: 2rem;
    padding: 1.5rem;
  }

  h1 {
    font-size: 1.75rem;
  }

  .form-label {
    font-size: 1rem;
  }

  .form-control {
    font-size: 0.875rem;
  }

  .btn {
    font-size: 0.875rem;
  }
}
</style>
