<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getExpenses, addExpense, updateExpense, deleteExpense } from '../api'
import type { Expense, ExpenseInput } from '../api'

// State variables
const expenses = ref<Expense[]>([])
const loading = ref<boolean>(true)
const error = ref<string | null>(null)

// For new/edit dialog (simple modal state for demonstration)
const showDialog = ref<boolean>(false)
const dialogMode = ref<'add' | 'edit'>('add')
const formExpense = ref<Partial<ExpenseInput>>({})
const dialogError = ref<string | null>(null)

function resetForm(): void {
  formExpense.value = {}
  dialogError.value = null
}

async function loadExpenses(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    const data = await getExpenses()
    expenses.value = data
  } catch (err) {
    if (typeof err === 'object' && err !== null && 'response' in err) {
      // @ts-expect-error The error is an axios error type with a response property
      error.value = err.response?.data?.detail ?? 'Failed to load expenses'
    } else {
      error.value = 'Failed to load expenses'
    }
  } finally {
    loading.value = false
  }
}

// Open modal for add/edit
function openDialog(mode: 'add' | 'edit', expense?: Expense): void {
  dialogMode.value = mode
  resetForm()
  if (expense) {
    formExpense.value = { ...expense }
  }
  showDialog.value = true
}

// CRUD ops
async function handleSave(): Promise<void> {
  dialogError.value = null
  try {
    if (dialogMode.value === 'add') {
      await addExpense(formExpense.value as ExpenseInput)
    } else if (formExpense.value.id !== undefined) {
      await updateExpense(formExpense.value.id, formExpense.value as ExpenseInput)
    }
    await loadExpenses()
    showDialog.value = false
  } catch (err) {
    if (typeof err === 'object' && err !== null && 'response' in err) {
      // @ts-expect-error The error is an axios error type with a response property
      dialogError.value = err.response?.data?.detail ?? 'Failed to save expense'
    } else {
      dialogError.value = 'Failed to save expense'
    }
  }
}

async function handleDelete(expense: Expense): Promise<void> {
  if (!confirm('Delete this expense?')) return
  try {
    await deleteExpense(expense.id)
    await loadExpenses()
  } catch (err) {
    if (typeof err === 'object' && err !== null && 'response' in err) {
      // @ts-expect-error The error is an axios error type with a response property
      error.value = err.response?.data?.detail ?? 'Failed to delete expense'
    } else {
      error.value = 'Failed to delete expense'
    }
  }
}

onMounted(() => {
  loadExpenses()
})

</script>

<template>
  <section>
    <h2>Expenses</h2>
    <div class="action-bar">
      <input
        type="search"
        placeholder="Search expenses... (not implemented)"
        disabled
      />
      <button class="filter-btn" disabled>Filter</button>
      <button class="add-expense-btn" @click="openDialog('add')">+ Add Expense</button>
    </div>
    <div v-if="loading" class="expenses-table-placeholder">Loading expenses...</div>
    <div v-else-if="error" class="expenses-table-placeholder" style="color:#c00;">
      {{ error }}
    </div>
    <div v-else>
      <table class="expenses-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Amount</th>
            <th>Description</th>
            <th>Category</th>
            <th style="min-width:90px;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="e in expenses" :key="e.id">
            <td>{{ e.date }}</td>
            <td>{{ e.amount }}</td>
            <td>{{ e.description }}</td>
            <td>{{ e.category ?? '—' }}</td>
            <td>
              <button @click="openDialog('edit', e)">Edit</button>
              <button @click="handleDelete(e)">Delete</button>
            </td>
          </tr>
          <tr v-if="expenses.length === 0">
            <td colspan="5" style="color: #888;">No expenses found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Dialog for add/edit expense -->
    <div v-if="showDialog" class="expense-dialog-overlay">
      <div class="expense-dialog">
        <h3>{{ dialogMode === 'add' ? 'Add Expense' : 'Edit Expense' }}</h3>
        <form @submit.prevent="handleSave">
          <input
            v-model="formExpense.date"
            type="date"
            required
            placeholder="Date"
          />
          <input
            v-model.number="formExpense.amount"
            type="number"
            step="0.01"
            min="0"
            required
            placeholder="Amount"
          />
          <input
            v-model="formExpense.description"
            type="text"
            placeholder="Description"
            required
          />
          <input
            v-model="formExpense.category"
            type="text"
            placeholder="Category (optional)"
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
.filter-btn,
.add-expense-btn {
  background: var(--primary, #1976d2);
  color: #fff;
  border-radius: 5px;
  border: none;
  padding: 6px 14px;
  font-weight: 500;
  cursor: pointer;
  opacity: 1;
}
.expenses-table-placeholder {
  border-radius: 8px;
  border: 1px dashed #ddd;
  min-height: 220px;
  padding: 2.3rem 1rem;
  text-align: center;
  color: #757575;
}
.expenses-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.3em 0;
}
.expenses-table th,
.expenses-table td {
  border: 1px solid #eee;
  padding: 8px 10px;
  text-align: left;
}
.expenses-table th {
  background: #f4f8fd;
  color: #222;
  font-weight: 600;
}
.expenses-table td button {
  margin-right: 8px;
  background: var(--accent, #ffb300);
  color: #222;
  border: none;
  border-radius: 5px;
  padding: 3px 13px;
  cursor: pointer;
  font-size: 0.98em;
}
.expense-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: #0007;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99;
}
.expense-dialog {
  background: #fff;
  border-radius: 10px;
  min-width: 320px;
  max-width: 95vw;
  padding: 2rem 1.7rem 1.3rem 1.7rem;
  box-shadow: 0 4px 30px #0002;
  display: flex;
  flex-direction: column;
  gap: 1.05em;
}
.expense-dialog form > input {
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
