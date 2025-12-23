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

    async googleLogin(token: string) {
        const res = await fetch(`${API_URL}/auth/google/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ token }),
        });

        if (!res.ok) {
            const error = await res.json();
            if (error.detail === "MFA_REQUIRED") {
                throw new Error("MFA_REQUIRED");
            }
            throw new Error(error.detail || "Google login failed");
        }

        const data = await res.json();
        localStorage.setItem("token", data.access_token);
        return data;
    },

    // Passkey Registration
    async registerPasskeyOptions(username: string) {
        // Need token? Yes usually.
        const token = this.getToken();
        const headers: any = { "Content-Type": "application/json" };
        if (token) headers["Authorization"] = `Bearer ${token}`;

        const res = await fetch(`${API_URL}/auth/passkey/register/options`, {
            method: "POST",
            headers,
            body: JSON.stringify({ username, display_name: username })
        });
        if (!res.ok) throw new Error("Failed to get reg options");
        return res.json();
    },

    async verifyPasskeyRegistration(response: any) {
        const token = this.getToken();
        const headers: any = { "Content-Type": "application/json" };
        if (token) headers["Authorization"] = `Bearer ${token}`;

        const res = await fetch(`${API_URL}/auth/passkey/register/verify`, {
            method: "POST",
            headers,
            body: JSON.stringify(response)
        });
        if (!res.ok) throw new Error("Failed to verify registration");
        return res.json();
    },

    // Passkey Login
    async loginPasskeyOptions(username?: string) {
        const res = await fetch(`${API_URL}/auth/passkey/login/options`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username })
        });
        if (!res.ok) throw new Error("Failed to get login options");
        return res.json();
    },

    async verifyPasskeyLogin(response: any) {
        const res = await fetch(`${API_URL}/auth/passkey/login/verify`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(response)
        });

        if (!res.ok) throw new Error("Failed to verify login");

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
