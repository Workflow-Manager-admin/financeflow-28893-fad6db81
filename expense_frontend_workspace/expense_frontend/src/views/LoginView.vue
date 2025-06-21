<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Simple auth state: Could be replaced by Pinia/global store
const isLoggedIn = ref(false)
const authError = ref('')
const isLoading = ref(false)

const isRegister = ref(false)
const form = ref({
  username: '',
  password: '',
  confirmPassword: '',
})

function clearForm() {
  form.value = {
    username: '',
    password: '',
    confirmPassword: ''
  }
  authError.value = ''
}

async function handleLogin() {
  authError.value = ''
  isLoading.value = true
  try {
    const response = await fetch('/api/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: "include", // ensures cookie session for Django
      body: JSON.stringify({
        username: form.value.username,
        password: form.value.password
      })
    })
    const data = await response.json()
    if (response.ok) {
      isLoggedIn.value = true
      authError.value = ''
      clearForm()
      router.push({ name: 'dashboard' })
    } else {
      authError.value = data?.detail || data?.error || 'Invalid credentials'
    }
  } catch {
    authError.value = 'Network error'
  } finally {
    isLoading.value = false
  }
}

async function handleRegister() {
  authError.value = ''
  isLoading.value = true
  // Basic client-side check
  if (form.value.password !== form.value.confirmPassword) {
    authError.value = "Passwords do not match"
    isLoading.value = false
    return
  }
  try {
    const response = await fetch('/api/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: "include",
      body: JSON.stringify({
        username: form.value.username,
        password: form.value.password
      })
    })
    const data = await response.json()
    if (response.ok) {
      isLoggedIn.value = true
      authError.value = ''
      clearForm()
      router.push({ name: 'dashboard' })
    } else {
      authError.value = data?.detail || data?.username?.[0] || data?.error || 'Registration failed'
    }
  } catch {
    authError.value = 'Network error'
  } finally {
    isLoading.value = false
  }
}

async function handleLogout() {
  authError.value = ''
  isLoading.value = true
  try {
    const response = await fetch('/api/logout/', {
      method: 'POST',
      credentials: 'include'
    })
    if (response.ok) {
      isLoggedIn.value = false
      clearForm()
      router.push({ name: 'login' })
    } else {
      authError.value = 'Logout failed'
    }
  } catch {
    authError.value = 'Network error'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <section class="auth-section">
    <h2 v-if="!isRegister">Sign in</h2>
    <h2 v-else>Register</h2>
    <div v-if="!isLoggedIn">
      <form
        class="auth-form"
        @submit.prevent="isRegister ? handleRegister() : handleLogin()"
        autocomplete="off"
      >
        <div class="form-group">
          <input
            v-model="form.username"
            type="text"
            placeholder="Username"
            required
            autocomplete="username"
            class="input"
          />
        </div>
        <div class="form-group">
          <input
            v-model="form.password"
            type="password"
            placeholder="Password"
            required
            autocomplete="current-password"
            class="input"
          />
        </div>
        <div class="form-group" v-if="isRegister">
          <input
            v-model="form.confirmPassword"
            type="password"
            placeholder="Confirm Password"
            required
            autocomplete="new-password"
            class="input"
          />
        </div>
        <div class="actions">
          <button
            class="btn primary"
            type="submit"
            :disabled="isLoading"
          >
            {{ isRegister ? 'Register' : 'Login' }}
          </button>
        </div>
        <div class="form-footer">
          <span v-if="!isRegister">Don’t have an account?
            <a href="#" @click.prevent="isRegister = true; clearForm()">Register</a>
          </span>
          <span v-else>Already have an account?
            <a href="#" @click.prevent="isRegister = false; clearForm()">Login</a>
          </span>
        </div>
        <div v-if="authError" class="error-msg">{{ authError }}</div>
      </form>
    </div>
    <div v-else>
      <div class="logged-in-panel">
        <p>Logged in as <b>{{ form.username }}</b></p>
        <button @click="handleLogout" class="btn secondary" :disabled="isLoading">
          Log out
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.auth-section {
  max-width: 370px;
  margin: 3.6rem auto 0;
  background: #fff;
  padding: 2.2rem 1rem 2rem 1rem;
  border-radius: 14px;
  box-shadow: 0 2px 14px #0002;
  text-align: center;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  margin-top: 1.3rem;
}

.input {
  width: 90%;
  padding: 0.7em 1em;
  border-radius: 7px;
  border: 1px solid #bbb;
  font-size: 1em;
  outline: none;
  transition: border 0.14s;
}
.input:focus {
  border-color: var(--primary, #1976d2);
}

.form-group {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.actions {
  margin-top: 0.5em;
}

.btn {
  padding: 0.55em 1.7em;
  border: none;
  border-radius: 7px;
  font-size: 1.06em;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.16s, color 0.16s;
}
.btn.primary {
  background: var(--primary, #1976d2);
  color: #fff;
}
.btn.secondary {
  background: var(--accent, #ffb300);
  color: #222;
}

.form-footer {
  margin-top: 1em;
  font-size: 0.95em;
  color: #777;
}
.form-footer a {
  color: var(--primary, #1976d2);
  cursor: pointer;
  text-decoration: underline;
}

.error-msg {
  margin-top: 1.2em;
  color: #d32f2f;
  background: #fff3f3;
  border-radius: 7px;
  padding: 0.6em 1.1em;
  font-size: 0.98em;
}

.logged-in-panel {
  margin-top: 2.7em;
}
</style>
