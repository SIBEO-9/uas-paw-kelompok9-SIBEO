// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:6543/api"

// Helper function untuk handle API calls
async function apiCall(endpoint, options) {
  const token = localStorage.getItem("token")

  const headers = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options?.headers,
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.message || `API Error: ${response.statusText}`)
  }

  return response.json()
}

// Auth Service
export const authService = {
  async register(name, email, password, role) {
    return apiCall("/register", {
      method: "POST",
      body: JSON.stringify({ name, email, password, role }),
    })
  },

  async login(email, password) {
    return apiCall("/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    })
  },

  async logout() {
    return apiCall("/logout", { method: "POST" })
  },
}

// Course Service
export const courseService = {
  async getAllCourses() {
    return apiCall("/courses", { method: "GET" })
  },

  async getCourseById(id) {
    return apiCall(`/courses/${id}`, { method: "GET" })
  },

  async createCourse(data) {
    return apiCall("/courses", {
      method: "POST",
      body: JSON.stringify(data),
    })
  },

  async updateCourse(id, data) {
    return apiCall(`/courses/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  },

  async deleteCourse(id) {
    return apiCall(`/courses/${id}`, { method: "DELETE" })
  },

  async getModules(courseId) {
    return apiCall(`/courses/${courseId}/modules`, { method: "GET" })
  },

  async getStudents(courseId) {
    return apiCall(`/courses/${courseId}/students`, { method: "GET" })
  },
}

// Enrollment Service
export const enrollmentService = {
  async enroll(courseId) {
    return apiCall("/enrollments", {
      method: "POST",
      body: JSON.stringify({ course_id: courseId }),
    })
  },

  async getMyCourses() {
    return apiCall("/enrollments/me", { method: "GET" })
  },

  async unenroll(enrollmentId) {
    return apiCall(`/enrollments/${enrollmentId}`, { method: "DELETE" })
  },
}

// Module Service
export const moduleService = {
  async createModule(courseId, data) {
    return apiCall(`/courses/${courseId}/modules`, {
      method: "POST",
      body: JSON.stringify(data),
    })
  },

  async updateModule(moduleId, data) {
    return apiCall(`/modules/${moduleId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  },

  async deleteModule(moduleId) {
    return apiCall(`/modules/${moduleId}`, { method: "DELETE" })
  },
}

// Dashboard Service
export const dashboardService = {
  async getInstructorDashboard() {
    return apiCall("/instructor/dashboard", { method: "GET" })
  },

  async getStudentProgress() {
    return apiCall("/student/progress", { method: "GET" })
  },
}
