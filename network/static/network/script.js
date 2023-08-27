document.addEventListener('DOMContentLoaded', () => {

    const editingTextareas = document.querySelectorAll('.edit-post-form');
    editingTextareas.forEach(form => {
      form.style.display = 'none';
    });

});

function editPost(formId, content) {
    const form = document.getElementById(`edit-${formId}`);
    form.style.display = 'block';
    const textContent = document.getElementById(`contentedit-${formId}`);
    textContent.innerHTML = content
    // Hide the content paragraph
    document.getElementById(`content-${formId}`).style.display = 'none';
    document.getElementById(`editbutton-${formId}`).style.display = 'none';
    document.getElementById(`div-edit-${formId}`).classList.add("mb-5");
  }

function unLike(id){
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  fetch(`/unlike_post/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({
        liked: true,
        post: id
    })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById(`likes-${id}`).innerHTML = `&#128154 ${data['likes']}`;
    const button = document.getElementById(`unlike-button-${id}`);
    button.id = `like-button-${id}`;
    button.onclick = ()=> like(id);
    button.innerHTML = 'Like';
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function like(id){
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  fetch(`/like_post/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({
        liked: true,
        post: id
    })
  })
  .then(response => response.json())
  .then(data => {
    const button = document.getElementById(`like-button-${id}`);
    button.id = `unlike-button-${id}`;
    button.onclick = ()=> unLike(id);
    button.innerHTML = 'Unlike';
    document.getElementById(`likes-${id}`).innerHTML = `&#128154 ${data["likes"]}`;
  })
  .catch(error => {
    console.error('Error:', error);
  });
}