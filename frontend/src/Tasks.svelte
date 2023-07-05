<script>
  import { onMount } from 'svelte';
  import { getTasks, createTask, updateTask, deleteTask } from './api.js';

  export let taskListId;

  let tasks = [];
  let newTaskTitle = '';

  async function loadTasks() {
    try {
      tasks = await getTasks(taskListId);
    } catch (error) {
      console.error(error);
    }
  }

  onMount(loadTasks);

  async function handleCreateTask() {
    try {
      const newTask = await createTask(taskListId, newTaskTitle);
      tasks = [...tasks, newTask]; // Добавить новый объект task в список
    } catch (error) {
      console.error(error);
    }
  }

  async function handleToggleTask(task) {
    try {
      const updatedTask = await updateTask({ ...task, completed: !task.completed });
      tasks = tasks.map(t => (t.id === updatedTask.id ? updatedTask : t));
    } catch (error) {
      console.error(error);
    }
  }

  async function handleDeleteTask(taskId) {
    try {
      await deleteTask(taskId);
      tasks = tasks.filter(task => task.id !== taskId);
    } catch (error) {
      console.error(error);
    }
  }

  loadTasks();
</script>

<!-- Добавьте кнопку удаления для каждой задачи -->
<ul>
  {#each tasks as task}
    <li>
      <input type="checkbox" checked="{task.completed}" on:change={() => handleToggleTask(task)} />
      {task.title} <button on:click={() => handleDeleteTask(task.id)}>Удалить</button>
    </li>
  {/each}
</ul>

<label>
  Новая задача:
  <input type="text" bind:value="{newTaskTitle}" />
</label>
<button on:click="{handleCreateTask}">Добавить задачу</button>
