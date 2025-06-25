export default {
  clear() {
    window.localStorage.removeItem("playerName");
    window.localStorage.removeItem("participationScore");
    window.localStorage.removeItem("totalQuestions");
    window.localStorage.removeItem("totalGlobalTime");
    window.localStorage.removeItem("participations");
  },
  savePlayerName(playerName) {
    window.localStorage.setItem("playerName", playerName);
  },
  getPlayerName() {
    return window.localStorage.getItem("playerName");
  },
  getParticipationScore() {
    return parseInt(window.localStorage.getItem("participationScore"), 10);
  },
  saveTotalQuestions(total) {
    window.localStorage.setItem("totalQuestions", total);
  },
  getTotalQuestions() {
    return parseInt(window.localStorage.getItem("totalQuestions"), 10);
  },
  saveTotalGlobalTime(totalGlobalTime) {
    window.localStorage.setItem("totalGlobalTime", totalGlobalTime);
  },
  getTotalGlobalTime() {
    return parseInt(window.localStorage.getItem("totalGlobalTime"), 10);
  },
  getParticipationScores() {
    return JSON.parse(window.localStorage.getItem("participations")) || [];
  },
  getBestScores() {
    const participations = this.getParticipationScores();
    return participations.sort((a, b) => {
      if (b.score === a.score) {
        return a.totalGlobalTime - b.totalGlobalTime;
      }
      return b.score - a.score;
    }).slice(0, 5);
  },
  getRank(currentScore) {
    const participations = this.getParticipationScores();
    const sortedParticipations = participations.sort((a, b) => {
      if (b.score === a.score) {
        return a.totalGlobalTime - b.totalGlobalTime;
      }
      return b.score - a.score;
    });
    return sortedParticipations.findIndex(participation => participation.score === currentScore) + 1;
  },
  saveParticipation(score) {
    const playerName = this.getPlayerName();
    const participations = JSON.parse(window.localStorage.getItem("participations")) || [];
    const totalGlobalTime = this.getTotalGlobalTime();
    participations.push({ playerName, score, totalGlobalTime });
    window.localStorage.setItem("participations", JSON.stringify(participations));
    window.localStorage.setItem("participationScore", score);
    this.saveTotalGlobalTime(0);
  },
};
