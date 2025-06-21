import axios from 'axios';

/**
 * API base instance. Adjust the baseURL if frontend and backend are served from different origins.
 */
const api = axios.create({
  baseURL: '/api', // assumes "/api" is the root for backend endpoints (adjust if backend is elsewhere)
  withCredentials: true, // important for session/cookie authentication
});

/** Expense and ExpenseInput types for API usage. */
export interface Expense {
  id: number;
  amount: number;
  description: string;
  date: string;
  category?: string | null;
}

export type ExpenseInput = Omit<Expense, 'id'> & { id?: number };

/**
 * Fetch all user expenses (GET /api/expenses/).
 * PUBLIC_INTERFACE
 */
export async function getExpenses(): Promise<Expense[]> {
  const response = await api.get<Expense[]>('/expenses/');
  return response.data;
}

/**
 * Add a new expense (POST /api/expenses/).
 * PUBLIC_INTERFACE
 */
export async function addExpense(expense: ExpenseInput): Promise<Expense> {
  const response = await api.post<Expense>('/expenses/', expense);
  return response.data;
}

/**
 * Update an expense by ID (PUT /api/expenses/:id/).
 * PUBLIC_INTERFACE
 */
export async function updateExpense(id: number, expense: ExpenseInput): Promise<Expense> {
  const response = await api.put<Expense>(`/expenses/${id}/`, expense);
  return response.data;
}

/**
 * Delete an expense by ID (DELETE /api/expenses/:id/).
 * PUBLIC_INTERFACE
 */
export async function deleteExpense(id: number): Promise<void> {
  await api.delete(`/expenses/${id}/`);
}
