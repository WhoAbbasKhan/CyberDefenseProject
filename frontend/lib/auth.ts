const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

export const auth = {
    async login(email: string, password: string) {
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: formData,
        });

        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.detail || "Login failed");
        }

        const data = await res.json();
        localStorage.setItem("token", data.access_token);
        return data;
    },

    logout() {
        localStorage.removeItem("token");
        window.location.href = "/login";
    },

    getToken() {
        if (typeof window === "undefined") return null;
        return localStorage.getItem("token");
    },

    isAuthenticated() {
        if (typeof window === "undefined") return false;
        return !!localStorage.getItem("token");
    }
};
