// ----------------- DATA FLOW: LOGIN MODULE -----------------
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        };

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Success: Redirect from auth module to data management dashboard
                window.location.href = '/dashboard';
            }
        } catch (err) {
            document.getElementById('errorMsg').innerText = "Invalid login credentials.";
        }
    });
}

// ----------------- DATA FLOW: TASK ASSIGNMENT -----------------
const taskForm = document.getElementById('taskForm');
if (taskForm) {
    // Dropdown population: Pull employee entries down from database instantly on load
    document.addEventListener("DOMContentLoaded", async () => {
        const res = await fetch('/api/employees');
        const employees = await res.json();
        const dropdown = document.getElementById('empDropdown');
        
        employees.forEach(emp => {
            let opt = new Option(emp.full_name, emp.id);
            dropdown.add(opt);
        });
    });

    // Handle Task Form Submission
    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const taskPayload = {
            title: document.getElementById('taskTitle').value,
            assigned_to: document.getElementById('empDropdown').value,
            status: document.getElementById('taskStatus').value
        };

        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskPayload)
        });

        const statusResult = await response.json();
        if (statusResult.success) {
            alert("💥 Pipeline Complete! UI -> Python Middleware -> MySQL successfully saved your task.");
            taskForm.reset();
        }
    });
}
