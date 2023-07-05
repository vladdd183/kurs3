 
<script>
  import LoginForm from './LoginForm.svelte';
  import RegisterForm from './RegisterForm.svelte';
  import TaskLists from './TaskLists.svelte';

  let isAuthenticated = !!localStorage.getItem('token');

  function handleLogin() {
    isAuthenticated = true;
  }
</script>

{#if !isAuthenticated}
  <h1>Вход</h1>
  <LoginForm on:login={handleLogin} />
  <h1>Регистрация</h1>
  <RegisterForm on:login={handleLogin} />
{:else}
  <h1>Списки задач</h1>
  <TaskLists />
{/if}
