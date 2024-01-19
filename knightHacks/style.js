import dotEnv from "dotenv";
ai = require("apiai")(process.env.APIAI_TOKEN);
import OpenAI from "openai";

const openai = new OpenAI();

async function main() {
  const completion = await openai.chat.completions.create({
    //messages: [{"role": "system", "content": "You are a helpful assistant."},
      //  {"role": "user", "content": "Who won the world series in 2020?"},
        //{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        //{"role": "user", "content": "Where was it played?"}],
    model: "gpt-3.5-turbo",
  });

  console.log(completion.choices[0]);
}
main();

let slideIndex = 1; // start on first slide
showSlide(slideIndex);

function moveSlide(n) {
  showSlide((slideIndex += n));
}

function showSlide(n) {
  let i;
  let slides = document.getElementsByClassName("slide");
  if (n > slides.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slides.length;
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].classList.remove("active");
  }
  slides[slideIndex - 1].classList.add("active");
}

document.addEventListener("DOMContentLoaded", function () {
  let prevButton = document.querySelector(".prev");
  let nextButton = document.querySelector(".next");

  prevButton.addEventListener("click", function () {
    moveSlide(-1);
  });

  nextButton.addEventListener("click", function () {
    moveSlide(1);
  });
});

let slideInterval = setInterval(function () {
  moveSlide(1);
}, 5000);
