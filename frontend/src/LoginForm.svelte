<script>
  import { createEventDispatcher } from 'svelte';
  import { login } from './api.js';

  const dispatch = createEventDispatcher();
  let username = '';
  let password = '';

  let errorMessage = '';

  async function handleSubmit() {
    try {
      const { token } = await login(username, password);
      localStorage.setItem('token', token);
      dispatch('login');
    } catch (error) {
      errorMessage = error.message || 'Ошибка при входе';
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <label>
    Имя пользователя:
    <input type="text" bind:value="{username}" />
  </label>
  <label>
    Пароль:
    <input type="password" bind:value="{password}" />
  </label>
  <button type="submit">Войти</button>
</form>


{#if errorMessage}
  <div class="error-message">{errorMessage}</div>
{/if}
