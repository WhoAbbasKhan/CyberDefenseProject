"use client"

import { Button } from "@/components/ui/button"
import { useState } from "react"
import { toast } from "sonner"
import { auth } from "@/lib/auth"
import { startRegistration, startAuthentication } from "@simplewebauthn/browser"
import { Fingerprint } from "lucide-react"
import { useRouter } from "next/navigation"

export function PasskeyLoginButton() {
    const router = useRouter()
    const [isLoading, setIsLoading] = useState(false)

    const handleLogin = async () => {
        setIsLoading(true)
        try {
            // 1. Get options
            const options = await auth.loginPasskeyOptions()

            // 2. Browser interaction
            const authResp = await startAuthentication(options)

            // 3. Verify
            await auth.verifyPasskeyLogin(authResp)
            toast.success("Logged in with Passkey")
            router.push("/dashboard")
        } catch (error: any) {
            console.error(error)
            toast.error("Passkey login failed", { description: error.message })
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <Button variant="secondary" onClick={handleLogin} disabled={isLoading} className="w-full">
            <Fingerprint className="mr-2 h-4 w-4" />
            {isLoading ? "Verifying..." : "Sign in with Passkey"}
        </Button>
    )
}

export function PasskeyRegisterButton() {
    const [isLoading, setIsLoading] = useState(false)

    const handleRegister = async () => {
        setIsLoading(true)
        try {
            // User must be logged in implicitly via token in auth.ts
            // 1. Get options
            // Pass username from current user context if available, or just rely on backend user from token
            const options = await auth.registerPasskeyOptions("current_user")

            // 2. Browser interaction
            const regResp = await startRegistration(options)

            // 3. Verify
            await auth.verifyPasskeyRegistration(regResp)
            toast.success("Passkey registered successfully!")
        } catch (error: any) {
            console.error(error)
            toast.error("Failed to register passkey", { description: error.message })
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="p-4 border rounded-lg bg-card text-card-foreground">
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="font-semibold">Passkeys</h3>
                    <p className="text-sm text-muted-foreground">Use FaceID, TouchID, or Windows Hello</p>
                </div>
                <Button onClick={handleRegister} disabled={isLoading}>
                    {isLoading ? "Registering..." : "Enable Passkey"}
                </Button>
            </div>
        </div>
    )
}
