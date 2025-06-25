<template>
  <div class="questions-list">
    <h2>Liste des questions</h2>
    <div v-if="questions.length" class="questions-container">
      <div v-for="(question, index) in questions" :key="question.id" class="question-card">
        <div class="question-header">
          <span class="question-number">Question {{ index + 1 }}</span>
          <div class="question-actions">
            <button @click="modifDetail">Détail</button>
            <button @click="deleteQuestion(question.id)">Supprimer</button>
          </div>
        </div>
        <div class="question-text">{{ question.text }}</div>
        <div v-for="(answer, index) in question.answers" :key="index" v-if="wantDetail">
          <span >{{ answer }}</span>
        </div>

      </div>
    </div>
    <div v-else>
      <p>Aucune question.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import QuizApiBackService from '@/services/QuizApiBackService'; 
const error = ref(null);
const props = defineProps({
  questions: Array
});
var wantDetail=ref(false);

function modifDetail(){
  wantDetail.value=!wantDetail.value;
}

const emit = defineEmits(['edit-question', 'update:questions', 'question-deleted', 'view-question']);



async function deleteQuestion(id) {
  try {
    const response = await QuizApiBackService.deleteQuestion(id);
    if (response.status === 204) {
      console.log('Question supprimé avec succès');
      emit('question-deleted');
    } else {
      console.error('Une erreur s\'est produite lors de la suppression de la question');
    }
  } catch (error) {
    console.error(error);
  }
}


</script>

<style scoped>
.questions-list {
  width: 100%;
  padding: 2rem;
  background-color: #f0f4f8;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  text-align: center;
}

.questions-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.question-card {
  background-color: #fff;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  width: 100%;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.question-number {
  font-weight: bold;
  color: #1635b257;
  font-size: 1rem;
}

.question-actions {
  display: flex;
  gap: 0.5rem;
}

button {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  cursor: pointer;
  border: none;
  border-radius: 5px;
  background-color: #1635b257;
  color: white;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #36a972;
}

button:nth-child(2) {
  background-color: #e74c3c;
}

button:nth-child(2):hover {
  background-color: #c0392b;
}

.question-text {
  font-size: 1rem;
  color: #333;
}
</style>
