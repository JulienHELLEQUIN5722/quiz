<template>
  <div class="question-container">
    <div class="question-header">
      <div class="timer">{{ timer }}</div>
      <h2>{{ question.text }}</h2>
    </div>
    <img v-if="question.image" :src="question.image" class="question-image" />
    <div class="answers">
      <button 
        v-for="(answer, index) in question.answers" 
        :key="index" 
        :class="answerClasses[index]" 
        @click="answerClickedHandler(index + 1)" 
      >
        <span :class="shapeClasses[index]"></span>
        {{ answer }}
      </button>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';

const props = defineProps({
  question: Object,
  onTimeUp: Function,
  onAnswerSelected: Function,
  startGlobalTimer: Function
});

const timer = ref(5);
let interval = null;

const emit = defineEmits(['answer-selected']);

const answerClasses = ['red', 'blue', 'yellow', 'green'];
const shapeClasses = ['triangle', 'diamond', 'circle', 'square'];

onMounted(() => {
  startTimer();
  props.startGlobalTimer(); // Commencer le global timer
});

onBeforeUnmount(() => {
  clearInterval(interval);
});

watch(() => props.question, () => {
  resetTimer();
  startTimer();
});

function startTimer() {
  clearInterval(interval);
  timer.value = 15;
  interval = setInterval(() => {
    if (timer.value > 0) {
      timer.value -= 1;
    } else {
      clearInterval(interval);
      props.onTimeUp();
    }
  }, 1000);
}

function resetTimer() {
  timer.value = 5;
}

function answerClickedHandler(answerPosition) {
  clearInterval(interval);
  props.onAnswerSelected(answerPosition);
}
</script>



<style scoped>
.question-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  height: 90%;
  width: 90%;
  background-color: #f9f9f9;
  padding: 2%;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.question-header .timer {
  background-color: #6a1b9a;
  color: white;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.question-header h2 {
  margin: 0;
  flex: 1;
  text-align: center;
}

.question-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 1rem;
  max-height: 40%;
}
.answers {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  width: 100%;
}

.answers button {
  flex: 1 1 45%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1635b257;
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  position: relative;
  min-width: 45%;
  height: 100px;
}

.answers button:hover {
  transform: scale(1.05);
}

.answers .triangle {
  width: 0;
  height: 0;
  border-left: 12px solid transparent;
  border-right: 12px solid transparent;
  border-bottom: 20px solid white;
  margin-right: 8px;
}

.answers .diamond {
  width: 20px;
  height: 20px;
  background-color: white;
  transform: rotate(45deg);
  margin-right: 8px;
}

.answers .circle {
  width: 20px;
  height: 20px;
  background-color: white;
  border-radius: 50%;
  margin-right: 8px;
}

.answers .square {
  width: 20px;
  height: 20px;
  background-color: white;
  margin-right: 8px;
}

.answers .red {
  background-color: #e53935;
}

.answers .blue {
  background-color: #1e88e5;
}

.answers .yellow {
  background-color: #fdd835;
}

.answers .green {
  background-color: #43a047;
}
</style>
