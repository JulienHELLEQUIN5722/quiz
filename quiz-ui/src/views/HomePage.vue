<template>
  <div class="home-container">
    <header>
      <h1>Quiz Geographie !</h1>
      <img src="@/assets/quizMas.png" alt="Quiz Image" class="quiz-image" />
      <p class="description">
        Bienvenue sur notre jeu de quiz de géographie ! Testez vos connaissances sur les capitales du monde. <br>
        Attention, il y a un chrono ! Bonne chance !
      </p>
      <router-link to="/new-quiz" class="start-quiz-button">Commencer le Quiz</router-link>
    </header>
    
    <section class="leaderboard">
      <h2>Classement</h2>
      <div class="leaderboard-content">
        <div v-if="sortedScores.length > 0">
          <table class="score-table">
            <thead>
              <tr>
                <th>Rang</th>
                <th>Nom du Joueur</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(scoreEntry, index) in sortedScores.slice(0,10)" :key="index">
                <td>#{{ index + 1 }}</td>
                <td>{{ scoreEntry.playerName }}</td>
                <td>{{ scoreEntry.score }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else>
          <p>Pas de score enregistré. Commence et prends la première place !</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import participationStorageService from '@/services/ParticipationStorageService';
import QuizApiBackService from '@/services/QuizApiBackService';

const registeredScores = ref([]);
const error = ref('');
const sortedScores = ref([]);

onMounted(() => {
  registeredScores.value = participationStorageService.getParticipationScores();
  fetchAllParticipations();
});


async function fetchAllParticipations() {
  try {
    const response = await QuizApiBackService.getAllParticipations();
    if (response && response.status === 200) {
      sortedScores.value = response.data.allParticipations;
    } else {
      throw new Error('Failed to fetch all-participations');
    }
  } catch (err) {
    error.value = 'Failed to fetch all-participations';
    console.error(err);
  }
}
</script>

<style scoped>
/* Votre style ici */
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background-color: #f0f4f8;
  min-height: 100vh;
  color: #333;
  overflow: auto;
}

header {
  text-align: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #1635b257;
}

.quiz-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 1.5rem;
  max-height: 300px; 
}

.description {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  color: #555;
}

.start-quiz-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  font-size: 1.25rem;
  color: #fff;
  background-color: #1635b257; 
  border: none;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s, transform 0.3s;
  cursor: pointer;
}

.start-quiz-button:hover {
  background-color: #0e1d58ce;
  transform: scale(1.05);
}

.leaderboard {
  width: 100%;
  max-width: 700px;
  background-color: rgba(255, 255, 255, 0.8); /* Transparent background */
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  text-align: center;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 600px; /* Set a fixed max height */
}

.leaderboard-content {
  overflow-y: auto;
  max-height: 100%; 
  width: 100%;
}

.leaderboard h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #333;
}

.score-entry {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #e0e0e0;
  transition: background-color 0.3s;
}

.score-entry:last-child {
  border-bottom: none;
}

.score-entry:hover {
  background-color: #f9f9f9;
}

.rank {
  font-weight: bold;
  color: #1635b257;
}

.player-name {
  flex: 1;
  text-align: left;
  margin-left: 1rem;
}

.score {
  font-weight: bold;
  color: #333;
}

.score-table {
  width: 100%;
  max-width: 600px;
  margin: 1rem auto;
  border-collapse: collapse;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.score-table th, .score-table td {
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
}

.score-table th {
  background-color: #1635b257;
  color: white;
}

.score-table tbody tr:nth-child(odd) {
  background-color: #f9f9f9;
}

.score-table tbody tr:hover {
  background-color: #f1f1f1;
}

@media (max-width: 768px) {
  .home-container {
    padding: 1rem;
  }

  .leaderboard {
    padding: 1rem;
    max-height: 50vh; /* Adjust height for small screens */
  }

  .start-quiz-button {
    font-size: 1rem;
    padding: 0.5rem 1rem;
  }

  .description {
    font-size: 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .leaderboard h2 {
    font-size: 1.5rem;
  }

  .score-entry {
    font-size: 0.875rem;
  }
}
</style>
