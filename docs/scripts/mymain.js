
function start(){
	document.getElementById("teamSelector").addEventListener("change", doStuff,)
};
function doStuff(){
	setScores();
	getScores();
};
function getScores(){

  if (app1.ffteams.length > 0){
    for (var i=0; i<app1.ffteams.length; i++){
      if (app1.ffteams[i]){
        var tim = app1.ffteams[i]
        var tim_score_card = []
        for(k=0; k < 10; k++){
          var score=0
          for (var j=0; j<app1.players.length; j++){
            var pim = app1.players[j]
            if (app1.ffteams[i].stats.roster.includes(pim.name)){
              score+=Number(pim.score[k])
            }
          }
          tim_score_card.push(score.toFixed(2))
        }
        tim.stats.record = tim_score_card
      }
    }
  }
  
};
function setScores(){
    var t_scores = []
    for (var j=0; j < app1.players.length; j++){
      var symbol = app1.players[j]
      var score_card = [];
      for (i = 0; i < 10; i++) {
        var k, d, a, cs, g, score = null;
        var day1 = (i * 2)
        var day2 = (i * 2) + 1
        k = Number(symbol.stats.kills[day1]) + Number(symbol.stats.kills[day2])
        d = Number(symbol.stats.deaths[day1]) + Number(symbol.stats.deaths[day2])
        a = Number(symbol.stats.assists[day1]) + Number(symbol.stats.assists[day2])
        cs = Number(symbol.stats.cs[day1]) + Number(symbol.stats.cs[day2])
        g = Number(symbol.stats.gold[day1]) + Number(symbol.stats.gold[day2])
        score = k - 0.75*d + 0.5*a + 0.01*cs + 0.1*g
        score_card.push(score.toFixed(2))
      }
      symbol.score = score_card
    }
}
window.addEventListener("load", start, false);