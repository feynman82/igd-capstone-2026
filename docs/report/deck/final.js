// The whole final deck for 3 November: five segments in the presentation order of docs/TEAM.md,
// and the close. Each segment is its owner's file in segments/; change a slide there, not here.
const { newDeck } = require("./common");

const deck = newDeck({ title: "PARROT: final presentation, 3 November 2026", author: "IGD ILP Group 1" });
for (const segment of ["christian", "zee", "desmond", "yew-mun", "siew", "close"]) {
  require("./segments/" + segment)(deck);
}
deck.finish(process.argv[2]);
