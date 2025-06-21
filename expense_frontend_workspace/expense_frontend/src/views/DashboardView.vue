<script setup lang="ts">
// Placeholders for chart, table and dialog in dashboard.
</script>

<template>
  <section>
    <h2>Monthly Dashboard</h2>
    <div class="dashboard-content">
      <div class="chart-card">
        <div class="chart-placeholder">[Chart Visualization Placeholder]</div>
      </div>
      <div class="table-card">
        <div class="table-header">
          <span>Recent Expenses</span>
          <button disabled class="add-expense-btn">+ Add Expense</button>
        </div>
        <div class="expense-table-placeholder">
          [Expense Table Placeholder]
        </div>
      </div>
    </div>
    <div class="dialog-placeholder">
      [Expense Entry/Edit Dialog Placeholder]
    </div>
  </section>
</template>

<style scoped>
.dashboard-content {
  display: flex;
  flex-wrap: wrap;
  gap: 2.2rem;
}
.chart-card, .table-card {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 20px #0001;
  padding: 1.5rem 1.5rem 2rem 1.8rem;
  min-width: 290px;
}
.chart-card {
  flex: 2 0 340px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 270px;
  margin-bottom: 1.5rem;
}
.table-card {
  flex: 3 0 420px;
  display: flex;
  flex-direction: column;
  min-height: 300px;
}
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.25rem;
  margin-bottom: 1.1rem;
}
.add-expense-btn {
  background: var(--accent, #ffb300);
  border: none;
  color: #222;
  border-radius: 5px;
  padding: 6px 17px;
  font-size: 1em;
  font-weight: 500;
  cursor: pointer;
  opacity: 0.55;
}
.expense-table-placeholder {
  border-radius: 8px;
  border: 1px dashed #ddd;
  padding: 2.6rem 1rem;
  text-align: center;
  color: #757575;
}
.dialog-placeholder {
  margin-top: 2.3rem;
  padding: 1rem;
  background: #f8f8fb;
  border-radius: 9px;
  text-align: center;
  color: #928200;
  font-size: 1.08em;
}
</style>
