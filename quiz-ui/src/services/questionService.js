const API_URL = 'http://localhost:5000/api';

export default {
  async fetchQuestions() {
    const response = await fetch(`${API_URL}/questions`);
    return response.json();
  },
  async saveQuestion(question) {
    const response = await fetch(`${API_URL}/questions/${question.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(question)
    });
    return response.json();
  },
  async deleteQuestion(id) {
    await fetch(`${API_URL}/questions/${id}`, {
      method: 'DELETE'
    });
  }
};
