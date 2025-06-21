<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getMonthlyStatistics, getExpenses, type Expense, type MonthlyStatistics } from '../api'

// State for statistics
const loadingStats = ref(true)
const statsError = ref<string | null>(null)
const statistics = ref<MonthlyStatistics | null>(null)
const now = new Date()
const curYear = now.getFullYear()
const curMonth = now.getMonth() + 1  // JS: 0-11, backend: 1-12

// State for recent expenses
const loadingExpenses = ref(true)
const expensesError = ref<string | null>(null)
const recentExpenses = ref<Expense[]>([])

// Chart processing
function prepareChartData(stats: MonthlyStatistics | null) {
  if (!stats || !stats.by_category) return []
  const categories = Object.entries(stats.by_category)
  const total = stats.total || 1
  // Compute angles for each category for the pie chart
  let acc = 0
  return categories.map(([cat, value]) => {
    const percent = value / total
    const angle = percent * 360
    const arc = {
      start: acc,
      end: acc + angle,
      label: cat,
      value: value
    }
    acc += angle
    return arc
  })
}

// Color palette for 6 categories (repeat if more)
const pieColors = [
  "#1976d2", "#ffb300", "#4caf50", "#e53935", "#fbc02d", "#8e24aa"
]

function describeArc(cx:number, cy:number, r:number, startAngle:number, endAngle:number) {
  // https://stackoverflow.com/a/18473154
  const toRadians = (deg:number) => (deg-90) * Math.PI / 180.0
  const x1 = cx + r * Math.cos(toRadians(startAngle))
  const y1 = cy + r * Math.sin(toRadians(startAngle))
  const x2 = cx + r * Math.cos(toRadians(endAngle))
  const y2 = cy + r * Math.sin(toRadians(endAngle))
  const largeArcFlag = endAngle - startAngle > 180 ? 1 : 0
  return [
    `M ${cx} ${cy}`,
    `L ${x1} ${y1}`,
    `A ${r} ${r} 0 ${largeArcFlag} 1 ${x2} ${y2}`,
    "Z"
  ].join(" ")
}

// LOAD stats and expenses
async function loadStatistics() {
  loadingStats.value = true
  statsError.value = null
  try {
    statistics.value = await getMonthlyStatistics(curYear, curMonth)
  } catch (e) {
    // Type guard for Axios error
    if (typeof e === 'object' && e !== null && 'response' in e) {
      const err = e as { response?: { data?: { detail?: string } } }
      statsError.value = err.response?.data?.detail || "Failed to load statistics"
    } else {
      statsError.value = "Failed to load statistics"
    }
    statistics.value = null
  } finally {
    loadingStats.value = false
  }
}
async function loadRecentExpenses() {
  loadingExpenses.value = true
  expensesError.value = null
  try {
    const allExpenses = await getExpenses()
    recentExpenses.value = allExpenses
      .sort((a, b) => b.date.localeCompare(a.date))
      .slice(0, 5)
  } catch (e) {
    // Type guard for Axios error
    if (typeof e === 'object' && e !== null && 'response' in e) {
      const err = e as { response?: { data?: { detail?: string } } }
      expensesError.value = err.response?.data?.detail || "Failed to load expenses"
    } else {
      expensesError.value = "Failed to load expenses"
    }
    recentExpenses.value = []
  } finally {
    loadingExpenses.value = false
  }
}
onMounted(() => {
  loadStatistics()
  loadRecentExpenses()
})
</script>

<template>
  <section>
    <h2>Monthly Dashboard</h2>
    <div class="dashboard-content">
      <div class="chart-card">
        <div v-if="loadingStats" class="chart-placeholder">Loading chart...</div>
        <div v-else-if="statsError" class="chart-placeholder" style="color:#e53935;">{{ statsError }}</div>
        <div v-else-if="!statistics || statistics.total === 0" class="chart-placeholder">No data for this month.</div>
        <div v-else class="pie-chart-wrap">
          <!-- SVG Pie Chart for expenses by category -->
          <svg viewBox="0 0 170 170" width="170" height="170" style="display:block; margin:auto;">
            <g v-for="arc in prepareChartData(statistics)" :key="arc.label">
              <path
                :d="describeArc(85, 85, 70, arc.start, arc.end)"
                :fill="pieColors[(prepareChartData(statistics).findIndex(a => a.label === arc.label))%pieColors.length]"
                :stroke="'#fff'"
                stroke-width="2"
              />
            </g>
          </svg>
          <div class="pie-legend">
            <div v-for="arc in prepareChartData(statistics)" :key="arc.label" class="pie-legend-item">
              <span
                class="pie-legend-color"
                :style="{ background: pieColors[(prepareChartData(statistics).findIndex(a => a.label === arc.label))%pieColors.length] }"
              ></span>
              <span class="pie-legend-label">{{ arc.label }}:</span>
              <b>{{ arc.value.toFixed(2) }}</b>
            </div>
          </div>
          <div class="stats-total">Total: <b>{{ statistics.total.toFixed(2) }}</b></div>
        </div>
      </div>
      <div class="table-card">
        <div class="table-header">
          <span>Recent Expenses</span>
          <button class="add-expense-btn" disabled>+ Add Expense</button>
        </div>
        <div v-if="loadingExpenses" class="expense-table-placeholder">Loading expenses...</div>
        <div v-else-if="expensesError" class="expense-table-placeholder" style="color:#e53935;">{{ expensesError }}</div>
        <div v-else>
          <table class="expense-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Amount</th>
                <th>Description</th>
                <th>Category</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="e in recentExpenses" :key="e.id">
                <td>{{ e.date }}</td>
                <td>{{ e.amount.toFixed(2) }}</td>
                <td>{{ e.description }}</td>
                <td>{{ e.category ?? '—' }}</td>
              </tr>
              <tr v-if="recentExpenses.length === 0">
                <td colspan="4" style="color: #888;">No expenses found this month.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
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
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 270px;
  margin-bottom: 1.5rem;
}
.pie-chart-wrap {
  text-align: center;
  width: 100%;
}
.pie-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1.1em;
  margin-top: 1.3em;
  justify-content: center;
}
.pie-legend-item {
  display: flex;
  align-items: center;
  gap: 0.45em;
  font-size: 1.02em;
}
.pie-legend-color {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  display: inline-block;
  margin-right: 0.5em;
  border: 1.3px solid #fff;
  box-shadow: 0 1px 4px #0001;
}
.pie-legend-label {
  margin-right: 0.2em;
}
.stats-total {
  margin-top: 1.2em;
  font-size: 1.05em;
  font-weight: bold;
  color: #1976d2;
  text-align: center;
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
.expense-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.3em 0;
}
.expense-table th,
.expense-table td {
  border: 1px solid #eee;
  padding: 9px 13px;
  text-align: left;
  font-size: 1.06em;
}
.expense-table th {
  background: #f4f8fd;
  color: #222;
  font-weight: 600;
}
</style>
