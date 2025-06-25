<template>
  <div class="score-page">
    <img src="@/assets/trophee.png" alt="Score Image" class="score-image" />
    <h1>Votre Score : {{ currentScore }}</h1>
    <h2>Votre Rang : {{ rank }}</h2>
    <h2>Meilleurs Scores :</h2>
    <table class="score-table">
      <thead>
        <tr>
          <th>Rang</th>
          <th>Nom du Joueur</th>
          <th>Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(participation, index) in bestScores" :key="index">
          <td>#{{ index + 1 }}</td>
          <td>{{ participation.playerName }}</td>
          <td>{{ participation.score }}</td>
        </tr>
      </tbody>
    </table>
    <button @click="goToHomePage">Retour à la Page d'Accueil</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';
import QuizApiBackService from '@/services/QuizApiBackService';


const router = useRouter();
const currentScore = ref(0);
const rank = ref(0);
var bestScores = ref([]);
const error = ref('');

onMounted(() => {
  currentScore.value = participationStorageService.getParticipationScore();
  rank.value = participationStorageService.getRank(currentScore.value);
  bestScores.value = participationStorageService.getBestScores();
  fetchAllParticipations();
});



async function fetchAllParticipations() {
  try {
    const response = await QuizApiBackService.getAllParticipations();
    if (response && response.status === 200) {
      bestScores.value=response.data.allParticipations.slice(0,5);
    } else {
      throw new Error('Failed to fetch all-participations');
    }
  } catch (err) {
    error.value = 'Failed to fetch all-participations';
    console.error(err);
    return [];
  }
}

function goToHomePage() {
  router.push('/');
}
</script>

<style scoped>
.score-page {
  text-align: center; /* Center content horizontally */
  padding: 2rem; /* Add some padding */
}

.score-image {
  max-width: 200px;
  height: auto;
  margin-bottom: 2rem;
}

h1, h2 {
  margin-bottom: 1rem; /* Add some space after headings */
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

button {
  margin-top: 2rem; /* Add space above the button */
  padding: 0.75rem 1.5rem; /* Add padding to the button */
  font-size: 1rem; /* Increase font size */
  color: #fff;
  background-color: #1635b257;
  border: none;
  border-radius: 5px;
  cursor: pointer; /* Change cursor to pointer */
  transition: background-color 0.3s, transform 0.3s;
}

button:hover {
  background-color: #0e1d58ce;
  transform: scale(1.05);
}
</style>
