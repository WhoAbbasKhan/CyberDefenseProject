"use client"

import Script from "next/script"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { toast } from "sonner"
import { auth } from "@/lib/auth"
import { useRouter } from "next/navigation"

declare var google: any;

export function GoogleLoginButton() {
    const router = useRouter()
    const [isLoading, setIsLoading] = useState(false)

    const handleGoogleLogin = () => {
        setIsLoading(true)
        const client = google.accounts.oauth2.initCodeClient({
            client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID!,
            scope: "email profile openid",
            ux_mode: "popup",
            callback: async (response: any) => {
                if (response.code) {
                    try {
                        await auth.googleLogin(response.code)
                        toast.success("Login successful")
                        router.push("/dashboard")
                    } catch (error: any) {
                        console.error("Google verify error", error)
                        if (error.message === "MFA_REQUIRED") {
                            toast.error("Security Check Required", {
                                description: "Please use your passkey or MFA method."
                            })
                            // Logic to trigger Passkey login could go here
                        } else {
                            toast.error("Failed to verify with Google")
                        }
                    } finally {
                        setIsLoading(false)
                    }
                } else {
                    setIsLoading(false)
                }
            },
            error_callback: () => {
                setIsLoading(false)
                toast.error("Google Sign-In failed")
            }
        })
        client.requestCode()
    }

    return (
        <>
            <Script src="https://accounts.google.com/gsi/client" strategy="lazyOnload" />
            <Button
                variant="outline"
                type="button"
                disabled={isLoading}
                onClick={handleGoogleLogin}
                className="w-full"
            >
                {isLoading ? (
                    "Connecting..."
                ) : (
                    <div className="flex items-center gap-2">
                        <svg className="h-4 w-4" viewBox="0 0 24 24">
                            <path
                                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                                fill="#4285F4"
                            />
                            <path
                                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                                fill="#34A853"
                            />
                            <path
                                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                                fill="#FBBC05"
                            />
                            <path
                                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                                fill="#EA4335"
                            />
                        </svg>
                        Continue with Google
                    </div>
                )}
            </Button>
        </>
    )
}
