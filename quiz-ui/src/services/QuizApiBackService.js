import axios from "axios";


const instance = axios.create({
  baseURL: `${import.meta.env.VITE_BACK_URL}`,
  json: true
});



export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getAllQuestions() {
    return this.call("get", "all-questions/");
  },
  postParticipation(playerName, answers) {
    const body = {
      playerName: playerName,
      answers: answers
    };
    return this.call("post", "participations", body);
  },
  getAllParticipations() {
    return this.call("get", "participations/all");
  },
  deleteAllQuestions() {
    const token = localStorage.getItem('authToken');
    return this.call("delete", "questions/all", null, token);
  },
  deleteAllParticipations() {
    const token = localStorage.getItem('authToken');
    return this.call("delete", "participations/all", null, token);
  },
  deleteQuestion(id) {
    const token = localStorage.getItem('authToken');
    return this.call("delete", `questions/${id}`, null, token);
  },
  rebuildDb() {
    const token = localStorage.getItem('authToken');
    return this.call("post", `rebuild-db`, null, token);
  },
  postLogin(password) {
    const body = { "password": password };
    return this.call("post", "login", body);
  },
  postQuestion(question) {
    const token = localStorage.getItem('authToken');
    return this.call("post", "questions", question, token);
  },
  getQuestion(position) {
    return position;
  }
};







