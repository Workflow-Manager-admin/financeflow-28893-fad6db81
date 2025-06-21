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

/** Category and CategoryInput types for API usage. */
export interface Category {
  id: number;
  name: string;
}
export type CategoryInput = Omit<Category, 'id'> & { id?: number };

/** MonthlyStatistics type for dashboard visualization. */
export interface MonthlyStatistics {
  month: number;
  year: number;
  total: number;
  by_category: Record<string, number>;
}

/**
 * Fetch all user categories (GET /api/categories/).
 * PUBLIC_INTERFACE
 */
export async function getCategories(): Promise<Category[]> {
  const response = await api.get<Category[]>('/categories/');
  return response.data;
}

/**
 * Add a new category (POST /api/categories/).
 * PUBLIC_INTERFACE
 */
export async function addCategory(category: CategoryInput): Promise<Category> {
  const response = await api.post<Category>('/categories/', category);
  return response.data;
}

/**
 * Update a category by ID (PUT /api/categories/:id/).
 * PUBLIC_INTERFACE
 */
export async function updateCategory(id: number, category: CategoryInput): Promise<Category> {
  const response = await api.put<Category>(`/categories/${id}/`, category);
  return response.data;
}

/**
 * Delete a category by ID (DELETE /api/categories/:id/).
 * PUBLIC_INTERFACE
 */
export async function deleteCategory(id: number): Promise<void> {
  await api.delete(`/categories/${id}/`);
}

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

/**
 * Fetch monthly statistics (GET /api/statistics/monthly/?year=&month=)
 * PUBLIC_INTERFACE
 */
export async function getMonthlyStatistics(year: number, month: number): Promise<MonthlyStatistics> {
  const response = await api.get<MonthlyStatistics>(`/statistics/monthly/?year=${year}&month=${month}`);
  return response.data;
}
