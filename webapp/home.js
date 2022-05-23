function getSolution() {
  word = document.getElementById("key_input").value;
  document.getElementById("key_input").disable = true;
  document.getElementById("key_submit").disable = true;
  let headers = new Headers();
  // headers.append("Content-Type", "application/json");
  headers.append("Accept", "application/json");
  headers.append("Origin", "http://127.0.0.1:5000");

  console.log(word);
  fetch(`http://127.0.0.1:5000/solution?key=${word}`, {
    method: "GET",
    headers: headers,
  })
    .then((response) => {
      return response.json();
    })
    .then((res) => {
      console.log(res);
      play(res);
      document.getElementById("key_input").disable = false;
      document.getElementById("key_submit").disable = false;
    })
    .catch((err) => {
      console.log(err);
      document.getElementById("key_input").disable = false;
      document.getElementById("key_submit").disable = false;
    });
}

function play(solution) {
  if (!solution) {
    alert("Not in dictionary");
    return;
  }
  for (i = 1; i <= 30; i++) {
    el = document.getElementById(String(i));
    el.style = "";
    el.textContent = "";
    el.classList.remove("animate__flipInX");
  }
  count = 1;
  solution.forEach((s) => {
    for (i = 0; i < 5; i++) {
      el = document.getElementById(String(count));
      el.textContent = s[0].charAt(i);
      count++;
      tileColor = getTileColor(i, s[1]);
      el.classList.add("animate__flipInX");
      el.style = `background-color:${tileColor};border-color:${tileColor}`;
    }
    // document.getElementById(String(count));
    // count++;
  });
  // if (solution[solution.length - 1][1].reduce((a, b) => a + b) === 10) {
  //   alert("Win!");
  // } else {
  //   alert("Game Over!");
  // }

  function getTileColor(index, sol) {
    if (sol[index] == 1) {
      return "rgb(181, 159, 59)";
    } else if (sol[index] == 2) {
      return "rgb(83, 141, 78)";
    } else {
      return "rgb(58, 58, 60)";
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  createSquares();
  //   getNewWord();

  // let guessedWords = [[]];
  // let availableSpace = 1;

  // let word;
  // let guessedWordCount = 0;

  // const keys = document.querySelectorAll(".keyboard-row button");

  // //   function getNewWord() {
  // //     fetch(`https://wordsapiv1.p.rapidapi.com/words/?random=true&lettersMin=5&lettersMax=5`, {
  // //       method: "GET",
  // //       headers: {
  // //         "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
  // //         "x-rapidapi-key": "<YOUR_KEY_GOES_HERE>",
  // //       },
  // //     })
  // //       .then((response) => {
  // //         return response.json();
  // //       })
  // //       .then((res) => {
  // //         word = res.word;
  // //       })
  // //       .catch((err) => {
  // //         console.error(err);
  // //       });
  // //   }

  // function getCurrentWordArr() {
  //   const numberOfGuessedWords = guessedWords.length;
  //   return guessedWords[numberOfGuessedWords - 1];
  // }

  // function updateGuessedWords(letter) {
  //   const currentWordArr = getCurrentWordArr();

  //   if (currentWordArr && currentWordArr.length < 5) {
  //     currentWordArr.push(letter);

  //     const availableSpaceEl = document.getElementById(String(availableSpace));

  //     availableSpace = availableSpace + 1;
  //     availableSpaceEl.textContent = letter;
  //   }
  // }

  // function getTileColor(letter, index) {
  //   const isCorrectLetter = word.includes(letter);

  //   if (!isCorrectLetter) {
  //     return "rgb(58, 58, 60)";
  //   }

  //   const letterInThatPosition = word.charAt(index);
  //   const isCorrectPosition = letter === letterInThatPosition;

  //   if (isCorrectPosition) {
  //     return "rgb(83, 141, 78)";
  //   }

  //   return "rgb(181, 159, 59)";
  // }

  // function handleSubmitWord() {
  //   const currentWordArr = getCurrentWordArr();
  //   if (currentWordArr.length !== 5) {
  //     window.alert("Word must be 5 letters");
  //   }

  //   const currentWord = currentWordArr.join("");

  //   fetch(`https://wordsapiv1.p.rapidapi.com/words/${currentWord}`, {
  //     method: "GET",
  //     headers: {
  //       "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
  //       "x-rapidapi-key": "61c5e3986dmsh20c1bee95c2230dp18d1efjsn4668bbcfc1b3",
  //     },
  //   })
  //     .then((res) => {
  //       if (!res.ok) {
  //         throw Error();
  //       }

  //       const firstLetterId = guessedWordCount * 5 + 1;
  //       const interval = 200;
  //       currentWordArr.forEach((letter, index) => {
  //         setTimeout(() => {
  //           const tileColor = getTileColor(letter, index);

  //           const letterId = firstLetterId + index;
  //           const letterEl = document.getElementById(letterId);
  //           letterEl.classList.add("animate__flipInX");
  //           letterEl.style = `background-color:${tileColor};border-color:${tileColor}`;
  //         }, interval * index);
  //       });

  //       guessedWordCount += 1;

  //       if (currentWord === word) {
  //         window.alert("Congratulations!");
  //       }

  //       if (guessedWords.length === 6) {
  //         window.alert(`Sorry, you have no more guesses! The word is ${word}.`);
  //       }

  //       guessedWords.push([]);
  //     })
  //     .catch(() => {
  //       window.alert("Word is not recognised!");
  //     });
  // }

  function createSquares() {
    const gameBoard = document.getElementById("board");

    for (let index = 0; index < 30; index++) {
      let square = document.createElement("div");
      square.classList.add("square");
      square.classList.add("animate__animated");
      square.setAttribute("id", index + 1);
      gameBoard.appendChild(square);
    }
  }

  // function handleDeleteLetter() {
  //   const currentWordArr = getCurrentWordArr();
  //   const removedLetter = currentWordArr.pop();

  //   guessedWords[guessedWords.length - 1] = currentWordArr;

  //   const lastLetterEl = document.getElementById(String(availableSpace - 1));

  //   lastLetterEl.textContent = "";
  //   availableSpace = availableSpace - 1;
  // }

  // for (let i = 0; i < keys.length; i++) {
  //   keys[i].onclick = ({ target }) => {
  //     const letter = target.getAttribute("data-key");

  //     if (letter === "enter") {
  //       handleSubmitWord();
  //       return;
  //     }

  //     if (letter === "del") {
  //       handleDeleteLetter();
  //       return;
  //     }

  //     updateGuessedWords(letter);
  //   };
  // }
});
