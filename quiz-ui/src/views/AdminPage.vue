<template>
  <div class="admin-container">
    <h1>Tableau de bord</h1>
    <div v-if="!token">
      <input v-model="password" type="password" placeholder="Enter password" />
      <button @click="login">Connexion</button>
    </div>
    <div v-else>
      <nav>
        <button @click="setAdminMode('list')">Liste des questions</button>
        <button @click="setAdminMode('new')">Ajouter une question</button>
        <button @click="deleteAllQuestions()" class="red-button">Supprimer toutes les questions</button>
        <button @click="deleteAllParticipations()" class="red-button">Supprimer toutes les participations</button>
        <button @click="rebuildDb()">Reconstruire la base de données</button>
      </nav>
      <div v-if="!isThere10Questions" class="centered-red-text">Le quiz doit contenir 10 questions.</div>
      <component :is="currentComponent" :questions="localQuestions" @edit-question="setAdminModeToEdit" @question-saved="handleQuestionSaved" @question-deleted="getAllQuestions"></component>
      <QuestionEdition
        v-if="adminMode === 'edit'"
        :question="currentQuestion"
        @question-saved="handleQuestionSaved"
        @close-question-edition="setAdminMode('list')"
      />

  
      
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import QuestionsList from '@/views/QuestionList.vue';
import QuestionEdition from '@/views/QuestionEdition.vue';
import QuizApiBackService from '@/services/QuizApiBackService'; 

const token = ref(localStorage.getItem('authToken'));
const password = ref('');
const adminMode = ref('list');
const currentQuestion = ref(null);
const all_questions = ref([]); 
const error = ref(null); 
var isThere10Questions = ref(true);

window.addEventListener('beforeunload', logOut);

var localQuestions = ref([]);

const login = async () => {
  try {
    const response = await QuizApiBackService.postLogin(password.value);
    if (response.status === 200) {
      token.value = response.data.token;
      localStorage.setItem('authToken', token.value);
    } else {
      alert('Incorrect password');
    }
  } catch (error) {
    console.error(error);
    alert('An error occurred during login');
  }
};


const setAdminMode = (mode) => {
  adminMode.value = mode;
};

const setAdminModeToEdit = (question) => {
  currentQuestion.value = question;
  adminMode.value = 'edit';
};

const currentComponent = computed(() => {
  if (adminMode.value === 'edit') return QuestionEdition;
  if (adminMode.value === 'new') return QuestionEdition;
  return QuestionsList;
});

const handleQuestionSaved = (updatedQuestion) => {
  const index = localQuestions.value.findIndex(q => q.id === updatedQuestion.id);
  if (index !== -1) {
    localQuestions.value[index] = updatedQuestion;
  } else {
    localQuestions.value.push(updatedQuestion);
  }
  adminMode.value = 'list';
};



onMounted(async () => {
  try {
    const response = await QuizApiBackService.getAllQuestions();

    if (response && response.status === 200) {
      all_questions.value = response.data;
      var all_questions_formated = [];
      var answers = [];
      for(let question of all_questions.value) {

        for(let possibleAnswers of question.possibleAnswers){
          answers.push(possibleAnswers.text);
        }
        all_questions_formated.push(
          {
            id : question.id,
            text : question.text,
            image : question.image,
            answers : answers
          }

        );
        answers=[];

      }

      localQuestions.value = all_questions_formated;

      if(localQuestions.value.length != 10){
        isThere10Questions.value = false;
      }
      else{
        isThere10Questions.value=true;
      }

      
    } else {
      throw new Error('Failed to fetch all-questions');
    }
  } catch (err) {
    error.value = 'Failed to fetch all-questions';
    console.error(err); 
  }
});


async function deleteAllQuestions() {
  try {
    const response = await QuizApiBackService.deleteAllQuestions();
    if (response.status === 204) {
      console.log('Toutes les questions ont été supprimées avec succès');
      await getAllQuestions();
    } else {
      console.error('Une erreur s\'est produite lors de la suppression des questions');
    }
  } catch (error) {
    console.error(error);
  }
}

async function getAllQuestions() {
  try {
    localQuestions.value = [];
    const response = await QuizApiBackService.getAllQuestions();
    if (response.status === 200) {
      all_questions.value = response.data;
      // Mettre à jour localQuestions avec les nouvelles données
      localQuestions.value = formatQuestions(all_questions.value);
      if(localQuestions.value.length != 10){
        isThere10Questions.value = false;
      }
      else{
        isThere10Questions.value=true;
      }
    } else {
      throw new Error('Failed to fetch all-questions');
    }
  } catch (err) {
    error.value = 'Failed to fetch all-questions';
    console.error(err);
  }
}

function formatQuestions(questions) {
  const formattedQuestions = [];
  for (let question of questions) {
    const answers = question.possibleAnswers.map(answer => answer.text);
    formattedQuestions.push({
      id: question.id,
      text: question.text,
      image: question.image,
      answers: answers
    });
  }
  return formattedQuestions;
}

async function deleteAllParticipations() {
  try {
    const response = await QuizApiBackService.deleteAllParticipations();
    if (response.status === 204) {
      console.log('Toutes les participations ont été supprimées avec succès');
      alert('Toutes les participations ont été supprimées avec succès');
    } else {
      console.error('Une erreur s\'est produite lors de la suppression des participations');
    }
  } catch (error) {
    console.error(error);
  }
}

async function rebuildDb(){
  try{
    const response = await QuizApiBackService.rebuildDb();
    if(response.status === 200) {
      console.log('Base de données reconstruite avec succès');
      getAllQuestions();
    } else {
      console.error('Une erreur s\'est produite lors de la reconstruction de la base de données');
    }
  } catch (error) {
    console.error(error);
  }
}



function logOut() {
  localStorage.removeItem('authToken');
  token.value = null;
};

</script>

<style scoped>
.admin-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background-color: #f0f4f8;
  min-height: 100vh;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
}

input {
  padding: 0.5rem;
  font-size: 1rem;
  margin-bottom: 1rem;
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

.red-button {
  background-color: #e74c3c;
}

.red-button:hover {
  background-color: #c0392b;
}


nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.centered-red-text {
  text-align: center;
  color: red;
}

</style>
