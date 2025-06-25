<template>
  <div class="quiz-container">
    <QuestionDisplay 
      v-if="currentQuestion" 
      :question="currentQuestion" 
      @answer-selected="answerClickedHandler"
      :onTimeUp="handleTimeUp"
      :startGlobalTimer="startGlobalTimer"
    />
    <div v-else class="loading">Loading Questions...</div>
  </div>
</template>

<script setup>
import { ref, onMounted} from 'vue';
import { useRouter, useRoute } from 'vue-router';
import QuestionDisplay from '@/views/QuestionDisplay.vue';
import participationStorageService from '@/services/ParticipationStorageService';
import QuizApiBackService from '@/services/QuizApiBackService';

const currentQuestion = ref(null);
const totalNumberOfQuestions = ref(0);
const currentQuestionPosition = ref(0);
const score = ref(0);
const totalGlobalTime = ref(0);
const questions = ref([]);
const userAnswers = ref([]); 
const error = ref('');
let startTime = null;
let globalInterval = null;

const router = useRouter();
const route = useRoute();
const playerName = route.query.playerName ? route.query.playerName : 'Bruno';


async function fetchQuestions() {
  try {
    const response = await QuizApiBackService.getAllQuestions();
    if (response && response.status === 200) {
      const all_questions_formated = response.data.map(question => ({
        id: question.id,
        text: question.text,
        image: question.image,
        answers: question.possibleAnswers.map(pa => pa.text)
      }));
      return all_questions_formated;
    } else {
      throw new Error('Failed to fetch all-questions');
    }
  } catch (err) {
    error.value = 'Failed to fetch all-questions';
    console.error(err);
    return [];
  }
}

async function loadQuestionByPosition(position) {
  if (position < questions.value.length) {
    currentQuestion.value = questions.value[position];
  } else {
    await endQuiz();
  }
}

function answerClickedHandler(answerPosition) {
  userAnswers.value.push({
    questionId: currentQuestion.value.id,
    answerPosition: answerPosition,
    questionPosition: currentQuestionPosition.value + 1 
  });
  moveToNextQuestion();
}

function handleTimeUp() {
  userAnswers.value.push({
    questionId: currentQuestion.value.id,
    answer: null 
  });
  moveToNextQuestion();
}

function moveToNextQuestion() {
  if (currentQuestionPosition.value < totalNumberOfQuestions.value - 1) {
    currentQuestionPosition.value++;
    loadQuestionByPosition(currentQuestionPosition.value);
  } else {
    endQuiz();
  }
}

async function endQuiz() {
  totalGlobalTime.value = Math.floor((new Date() - startTime) / 1000);
  clearInterval(globalInterval);
  
  const formattedAnswers = userAnswers.value.map(ua => ua.answerPosition);


  // Envoyer les réponses au back pour obtenir le score
  try {
    const response = await QuizApiBackService.postParticipation(playerName, formattedAnswers);
    if (response && response.status === 200) {
      score.value = response.data.score;
      participationStorageService.saveParticipation(score.value);
      participationStorageService.saveTotalQuestions(totalNumberOfQuestions.value);
      participationStorageService.saveTotalGlobalTime(totalGlobalTime.value); 
      router.push('/score'); 
    } else {
      throw new Error('Failed to submit answers');
    }
  } catch (err) {
    console.error('Failed to submit answers', err);
  }
}

function startGlobalTimer() {
  startTime = new Date();
  totalGlobalTime.value = 0; 
  globalInterval = setInterval(() => {
    totalGlobalTime.value = Math.floor((new Date() - startTime) / 1000);
  }, 1000);
}

onMounted(async () => {
  startGlobalTimer();
  questions.value = await fetchQuestions();
  totalNumberOfQuestions.value = questions.value.length;
  loadQuestionByPosition(currentQuestionPosition.value);
});
</script>

<style scoped>
.quiz-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  overflow: hidden;
  background-color: #f9f9f9;
}

.loading {
  font-style: italic;
  color: gray;
}
</style>
