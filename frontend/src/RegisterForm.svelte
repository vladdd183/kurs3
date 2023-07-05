 
<script>
  import { register } from './api.js';

  let username = '';
  let password = '';

  let errorMessage = '';
  let successMessage = '';

  async function handleSubmit() {
    try {
      await register(username, password);
      successMessage = 'Регистрация прошла успешно';
      errorMessage = '';
    } catch (error) {
      errorMessage = error.message || 'Ошибка при регистрации';
      successMessage = '';
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
  <button type="submit">Зарегистрироваться</button>
</form>

{#if successMessage}
  <div class="success-message">{successMessage}</div>
{/if}
{#if errorMessage}
  <div class="error-message">{errorMessage}</div>
{/if}
