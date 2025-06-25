<template>
  <div class="question-edition">
    <h2>Edit Question</h2>
    <form @submit.prevent="saveQuestion">
      <label>
        Titre :
        <input v-model="localQuestion.title" type="text" required />
      </label>
      <label>
        Question :
        <input v-model="localQuestion.text" type="text" required />
      </label>
      <label>
        Image:
        <input v-model="localQuestion.image" type="text" required />
        <small>  Exemple : /Images/France.jpg</small>
      </label>
      <!-- <label>
        Image:
        <ImageUpload @file-change="imageFileChangedHandler" :initialFileDataUrl="localQuestion.image" />
      </label> -->
      <div v-for="(answer, index) in localQuestion.possibleAnswers" :key="index">
        <label>
          &nbsp;Réponse possible {{ index + 1 }}:
          <input v-model="localQuestion.possibleAnswers[index].text" type="text" required />
        </label>
        <label>
          &nbsp;Réponse correcte :
          <input v-model="correctAnswerIndex" type="radio" :value="index" />
        </label>
      </div>

      <button type="submit">Ajouter</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import ImageUpload from '@/views/ImageUpload.vue';
import QuizApiBackService from '@/services/QuizApiBackService'; 

const error = ref(null);
const correctAnswerIndex = ref(null);



const props = defineProps({
  question: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['question-saved', 'close-question-edition']);

const localQuestion = ref({
  title: props.question.title || '',
  text: props.question.text || '',
  image: props.question.image || '/Images/France.jpg',
  position: props.question.position || 1,
  possibleAnswers: props.question.possibleAnswers ? props.question.possibleAnswers.map(answer => ({ ...answer })) : [
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false }
  ]
});


watch(props, (newProps) => {
  localQuestion.value = {
    title: newProps.question.title || '',
    text: newProps.question.text || '',
    image: newProps.question.image || 'falseb64imagecontent',
    position: newProps.question.position || 1,
    possibleAnswers: newProps.question.possibleAnswers ? newProps.question.possibleAnswers.map(answer => ({ ...answer })) : [
      { text: '', isCorrect: false },
      { text: '', isCorrect: false },
      { text: '', isCorrect: false },
      { text: '', isCorrect: false }
    ]
  };
});



async function saveQuestion() {
  try {
    const response = await QuizApiBackService.postQuestion(localQuestion.value);
    if (response.status === 200) {
      console.log('Question ajouté avec succès');
      emit('close-question-edition');
    } else {
      console.error("Une erreur s\'est produite lors de l\'ajout de la question");
    }
  } catch(error) {
    console.error(error);
  }
}

const imageFileChangedHandler = (b64String) => {
  localQuestion.value.image = b64String;
};

const setCorrectAnswer = (index) => {
  correctAnswerIndex.value = index;
  localQuestion.value.possibleAnswers.forEach((answer, i) => {
    answer.isCorrect = i === index;
  });
};

watch(() => correctAnswerIndex.value, (newIndex) => {
  setCorrectAnswer(newIndex);
});

watch(() => localQuestion.value.possibleAnswers, () => {
  correctAnswerIndex.value = localQuestion.value.possibleAnswers.findIndex(answer => answer.isCorrect);
}, { deep: true });
</script>




<style scoped>
.question-edition {
  width: 100%;
  max-width: 600px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 1rem;
}

input {
  padding: 0.5rem;
  font-size: 1rem;
  margin-top: 0.5rem;
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


</style>
