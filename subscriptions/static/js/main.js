$(document).ready(function () {
  var modal = $("#taskModal");
  var btn = $("#openModal");
  var span = $("#closeModal");
  var form = $("#taskForm");
  var url = form.data("url");
  var csrfToken = $('meta[name="csrf-token"]').attr("content");

  btn.click(function () {
    modal.show();
  });

  span.click(function () {
    modal.hide();
  });

  $(window).click(function (event) {
    if (event.target == modal[0]) {
      modal.hide();
    }
  });

  form.submit(function (event) {
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: url,
      data: $(this).serialize(),
      success: function (response) {
        if (response.task && response.task.task) {
          const taskHtml = `<li class="task_form" data-id="${response.task.id}">
                              ${response.task.task}
                              <div class="mt-3">
                                <button hx-post="/update/${
                                  response.task.id
                                }/" hx-confirm="Do you want to complete the task?" hx-target="#taskList" hx-headers='{"X-CSRFToken": "${csrfToken}"}' class="btn btn-success me-2">Completed</button>
                                <button hx-post="/delete/${
                                  response.task.id
                                }/" hx-target="#taskList" hx-headers='{"X-CSRFToken": "${csrfToken}"}' hx-swap="outerHtml" hx-confirm="Do you want to delete the task?" class="btn btn-danger">Delete</button>
                              </div>
                              <span class="category-label category-{{ task.category }} p-3 mb-2 bg-dark text-white">
                              ${ response.task.category}
                              </span>
                              <h2 class="status">Status : <span class="${
                                response.task.status ? "done" : "progress"
                              }">
                                ${
                                  response.task.status
                                    ? "Completed"
                                    : "In progress.."
                                }
                              </span></h2>
                            </li>`;
          $("#taskList").append(taskHtml);
          modal.hide();
          htmx.process(document.body);
        } else {
          alert("Не удалось получить данные задачи.");
        }
      },
    });
  });

  document.body.addEventListener("htmx:afterRequest", function () {
    htmx.process(document.body);
  });

  $(document).on("click", ".btn-success", function (event) {
    event.preventDefault();
    let button = $(this);
    let url = button.attr("hx-post");

    $.ajax({
      type: "POST",
      url: url,
      headers: {
        "X-CSRFToken": csrfToken,
      },
      success: function (response) {
        let [tasksHtml, rubiesHtml] = response.split("||");
        $("#taskList").html(tasksHtml);
        $("#rubies-count").replaceWith(rubiesHtml);
        htmx.process(document.body);
      },
    });
  });
});


document.addEventListener('DOMContentLoaded', () => {
    const categoryButton = document.getElementById('category-button');
    const categoryList = document.getElementById('category-list');
    const categories = document.querySelectorAll('.category');
    const taskSections = document.querySelectorAll('.tasks');

    // Toggle visibility of category list on button click
    categoryButton.addEventListener('click', () => {
        categoryList.classList.toggle('hidden');
    });

    // Handle category selection
    categories.forEach(category => {
        category.addEventListener('click', () => {
            const selectedCategory = category.getAttribute('data-category');

            taskSections.forEach(section => {
                section.classList.add('hidden');
            });

            document.querySelector(`.tasks[data-category="${selectedCategory}"]`).classList.remove('hidden');

            // Hide category list after selection
            categoryList.classList.add('hidden');
        });
    });
});

