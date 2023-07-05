const API_BASE_URL = 'http://localhost:3000';

async function apiRequest(path, options = {}) {
  const authToken = localStorage.getItem('token');
  const headers = {
    ...options.headers,
    ...(authToken ? { 'Authorization': `Bearer ${authToken}` } : {}),
  };

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.message || 'Ошибка при выполнении запроса');
  }
  return data;
}
export async function register(username, password) {
  const data = await apiRequest('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });

  localStorage.setItem('token', data.token);
  return data;
}

export async function login(username, password) {
  const data = await apiRequest('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });

  localStorage.setItem('token', data.token);
  return data;
}


export async function getAllTaskLists() {
  const response = await apiRequest('/lists');
  return response.task_lists;
}

export async function getTasks(taskListId) {
  const response = await apiRequest(`/lists/${taskListId}/tasks`);
  return response.tasks;
}

export async function createTask(taskListId, title) {
  const response = await apiRequest(`/lists/${taskListId}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  });
  return response.task; // Вернуть созданный объект task
}

export async function updateTask(task) {
  return apiRequest(`/tasks/${task.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(task),
  });
}


// Добавьте функцию для создания списка задач
export async function createList(title) {
  const response = await apiRequest('/lists', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  });
  return response.task_list; // Вернуть созданный объект task_list
}

// Добавьте функцию для удаления списка задач
export async function deleteList(listId) {
  return apiRequest(`/lists/${listId}`, {
    method: 'DELETE'
  });
}

// Добавьте функцию для удаления задачи
export async function deleteTask(taskId) {
  return apiRequest(`/tasks/${taskId}`, {
    method: 'DELETE'
  });
}
