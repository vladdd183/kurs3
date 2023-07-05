<script>
   import { onMount } from 'svelte';
  import { getAllTaskLists, createList, deleteList } from './api.js';
  import Tasks from './Tasks.svelte';

  let taskLists = [];

  async function loadTaskLists() {
    try {
      taskLists = await getAllTaskLists();
    } catch (error) {
      console.error(error);
    }
  }

  onMount(loadTaskLists); 
  let newListTitle = '';

  async function handleCreateList() {
    try {
    const newTaskList = await createList(newListTitle);
    taskLists = [...taskLists, newTaskList]; // Добавить новый объект taskList в список
  } catch (error) {
    console.error(error);
  }}

  async function handleDeleteList(listId) {
    try {
      await deleteList(listId);
      taskLists = taskLists.filter(list => list.id !== listId);
    } catch (error) {
      console.error(error);
    }
  }
</script>

<!-- Добавьте форму для создания нового списка задач -->
<label>
  Новый список задач:
  <input type="text" bind:value="{newListTitle}" />
</label>
<button on:click="{handleCreateList}">Добавить список</button>

<!-- Добавьте кнопку удаления для каждого списка задач -->
{#each taskLists as taskList}
  <h2>{taskList.name} <button on:click={() => handleDeleteList(taskList.id)}>Удалить</button></h2>
  <Tasks taskListId="{taskList.id}" />
{/each}
