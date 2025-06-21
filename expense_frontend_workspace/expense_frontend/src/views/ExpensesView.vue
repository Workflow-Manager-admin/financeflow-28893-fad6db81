<script setup lang="ts">
// Placeholder for expenses table, filter/search, and dialog
</script>

<template>
  <section>
    <h2>Expenses</h2>
    <div class="action-bar">
      <input type="search" placeholder="Search expenses..." disabled />
      <button disabled class="filter-btn">Filter</button>
      <button disabled class="add-expense-btn">+ Add Expense</button>
    </div>
    <div class="expenses-table-placeholder">
      [Expense Table Placeholder]
    </div>
    <div class="dialog-placeholder">
      [Expense Entry/Edit Dialog Placeholder]
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
.filter-btn, .add-expense-btn {
  background: var(--primary, #1976d2);
  color: #fff;
  border-radius: 5px;
  border: none;
  padding: 6px 14px;
  font-weight: 500;
  cursor: pointer;
  opacity: 0.50;
}
.expenses-table-placeholder {
  border-radius: 8px;
  border: 1px dashed #ddd;
  min-height: 220px;
  padding: 2.3rem 1rem;
  text-align: center;
  color: #757575;
}
.dialog-placeholder {
  margin-top: 2.3rem;
  padding: 1rem;
  background: #f8f8fb;
  border-radius: 9px;
  text-align: center;
  color: #1976d2;
  font-size: 1.08em;
}
</style>
