// Yew Mun's segment of the final deck on its own: retrieval and the evaluation results.
// The whole deck is final.js; the slides themselves are in segments/yew-mun.js.
const { newDeck } = require("./common");

const deck = newDeck({ title: "PARROT final deck: retrieval and evaluation", author: "Yew Mun" });
require("./segments/yew-mun")(deck);
deck.finish(process.argv[2]);
