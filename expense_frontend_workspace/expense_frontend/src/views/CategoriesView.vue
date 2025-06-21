<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  getCategories,
  addCategory,
  updateCategory,
  deleteCategory,
  type Category,
  type CategoryInput
} from '../api'

// State variables
const categories = ref<Category[]>([])
const loading = ref<boolean>(true)
const error = ref<string | null>(null)

// Modal/dialog state
const showDialog = ref<boolean>(false)
const dialogMode = ref<'add' | 'edit'>('add')
const formCategory = ref<Partial<CategoryInput>>({})
const dialogError = ref<string | null>(null)

function resetForm(): void {
  formCategory.value = {}
  dialogError.value = null
}

async function loadCategories(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    const data = await getCategories()
    categories.value = data
  } catch (err) {
    if (typeof err === 'object' && err !== null && 'response' in err) {
      // @ts-expect-error axios error with response
      error.value = err.response?.data?.detail ?? 'Failed to load categories'
    } else {
      error.value = 'Failed to load categories'
    }
  } finally {
    loading.value = false
  }
}

function openDialog(mode: 'add' | 'edit', category?: Category): void {
  dialogMode.value = mode
  resetForm()
  if (category) {
    formCategory.value = { ...category }
  }
  showDialog.value = true
}

async function handleSave(): Promise<void> {
  dialogError.value = null
  try {
    if (dialogMode.value === 'add') {
      await addCategory(formCategory.value as CategoryInput)
    } else if (formCategory.value.id !== undefined) {
      await updateCategory(formCategory.value.id, formCategory.value as CategoryInput)
    }
    await loadCategories()
    showDialog.value = false
  } catch (err) {
    if (typeof err === 'object' && err !== null && 'response' in err) {
      // @ts-expect-error axios error with response
      dialogError.value = err.response?.data?.detail ?? 'Failed to save category'
    } else {
      dialogError.value = 'Failed to save category'
    }
  }
}

async function handleDelete(category: Category): Promise<void> {
  if (!confirm('Delete this category?\n\nAll expenses assigned to this category will be affected.')) return
  try {
    await deleteCategory(category.id)
    await loadCategories()
  } catch (err) {
    if (typeof err === 'object' && err !== null && 'response' in err) {
      // @ts-expect-error axios error with response
      error.value = err.response?.data?.detail ?? 'Failed to delete category'
    } else {
      error.value = 'Failed to delete category'
    }
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<template>
  <section>
    <h2>Categories</h2>
    <div class="action-bar">
      <input
        type="search"
        placeholder="Search categories... (not implemented)"
        disabled
      />
      <button class="add-category-btn" @click="openDialog('add')">+ Add Category</button>
    </div>
    <div v-if="loading" class="categories-table-placeholder">Loading categories...</div>
    <div v-else-if="error" class="categories-table-placeholder" style="color:#c00;">
      {{ error }}
    </div>
    <div v-else>
      <table class="categories-table">
        <thead>
          <tr>
            <th style="width:16em;">Name</th>
            <th style="min-width:90px;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cat in categories" :key="cat.id">
            <td>{{ cat.name }}</td>
            <td>
              <button @click="openDialog('edit', cat)">Edit</button>
              <button @click="handleDelete(cat)">Delete</button>
            </td>
          </tr>
          <tr v-if="categories.length === 0">
            <td colspan="2" style="color: #888;">No categories found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Dialog for add/edit category -->
    <div v-if="showDialog" class="category-dialog-overlay">
      <div class="category-dialog">
        <h3>{{ dialogMode === 'add' ? 'Add Category' : 'Edit Category' }}</h3>
        <form @submit.prevent="handleSave">
          <input
            v-model="formCategory.name"
            type="text"
            placeholder="Category name"
            required
            maxlength="50"
            autocomplete="off"
          />
          <div class="dialog-actions">
            <button type="submit" class="save-btn">
              {{ dialogMode === 'add' ? 'Add' : 'Update' }}
            </button>
            <button type="button" @click="showDialog = false">Cancel</button>
          </div>
          <div v-if="dialogError" class="dialog-error">{{ dialogError }}</div>
        </form>
      </div>
    </div>
  </section>
</template>

<style scoped>
.action-bar {
  display: flex;
  gap: 0.8em;
  align-items: center;
  margin-bottom: 1.4em;
}
.add-category-btn {
  background: var(--primary, #1976d2);
  color: #fff;
  border-radius: 5px;
  border: none;
  padding: 6px 15px;
  font-weight: 500;
  cursor: pointer;
  opacity: 1;
}
.categories-table-placeholder {
  border-radius: 8px;
  border: 1px dashed #e0e0e0;
  min-height: 160px;
  padding: 2rem 1rem;
  text-align: center;
  color: #757575;
}
.categories-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.3em 0;
}
.categories-table th,
.categories-table td {
  border: 1px solid #eee;
  padding: 10px 14px;
  text-align: left;
  font-size: 1.06em;
}
.categories-table th {
  background: #f4f8fd;
  color: #222;
  font-weight: 600;
}
.categories-table td button {
  margin-right: 7px;
  background: var(--accent, #ffb300);
  color: #222;
  border: none;
  border-radius: 5px;
  padding: 3px 12px;
  cursor: pointer;
  font-size: 0.96em;
}
.category-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: #0005;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99;
}
.category-dialog {
  background: #fff;
  border-radius: 10px;
  min-width: 300px;
  max-width: 95vw;
  padding: 2rem 1.5rem 1.3rem 1.5rem;
  box-shadow: 0 4px 30px #0002;
  display: flex;
  flex-direction: column;
  gap: 1.05em;
}
.category-dialog form > input {
  width: 100%;
  display: block;
  margin-bottom: 0.9em;
  font-size: 1em;
  padding: 6px 11px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.dialog-actions {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}
.save-btn {
  background: var(--primary, #1976d2);
  color: #fff;
}
.dialog-error {
  color: #d32f2f;
  margin-top: 0.7em;
  background: #fff3f3;
  border-radius: 7px;
  padding: 0.52em 0.7em;
  font-size: 0.97em;
}
</style>
