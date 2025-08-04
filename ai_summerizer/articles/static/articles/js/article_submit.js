function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function submitArticle() {
  const articleText = document.getElementById("articleInput").value;
  const resultDiv = document.getElementById("result");

  fetch("/summarize/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie('csrftoken'),
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: "article_text=" + encodeURIComponent(articleText)
  })
  .then(res => res.json())
  .then(data => {
    if (data.error) {
      resultDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
    } else {
      resultDiv.innerHTML = `
        <h3>Summary:</h3>
        <p>${data.summary}</p>
        <h3>Tags:</h3>
        <p>${data.tags}</p>
      `;
    }
  });
}
