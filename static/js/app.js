const cards = document.querySelectorAll(".tweet-card");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2 }
  );

  cards.forEach((card) => observer.observe(card));
} else {
  cards.forEach((card) => card.classList.add("in-view"));
}

const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(";").shift();
  }
  return "";
};

const csrfToken = getCookie("csrftoken");

document.querySelectorAll(".js-like-form").forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const response = await fetch(form.action, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
      credentials: "same-origin",
      body: new FormData(form),
    });

    if (!response.ok) {
      form.submit();
      return;
    }

    const data = await response.json();
    const button = form.querySelector(".like-btn");
    const count = form.querySelector(".like-count");
    if (count) {
      count.textContent = data.like_count;
    }
    if (button) {
      button.innerHTML = `${data.liked ? "❤️ أعجبتني" : "🤍 لايك"} <span class="count like-count">${data.like_count}</span>`;
    }
  });
});

