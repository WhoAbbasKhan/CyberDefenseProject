"use client"

import Link from "next/link"
import { ShieldCheck, Lock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { auth } from "@/lib/auth"
import { toast } from "sonner"

export default function LoginPage() {
    const router = useRouter()
    const [isLoading, setIsLoading] = useState(false)

    async function onSubmit(event: React.FormEvent) {
        event.preventDefault()
        setIsLoading(true)

        try {
            // Get values from form directly or use controlled inputs
            // For simplicity in this shadcn template, we can access by ID if not using React Hook Form
            // But better to grab from event target if possible or refs. 
            // Let's use getElementById since the Inputs have IDs
            const email = (document.getElementById("email") as HTMLInputElement).value
            const password = (document.getElementById("password") as HTMLInputElement).value

            await auth.login(email, password)
            toast.success("Login successful")
            router.push("/dashboard")
        } catch (error: any) {
            console.error(error)
            toast.error(error.message || "Failed to login")
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="container relative flex h-screen flex-col items-center justify-center md:grid lg:max-w-none lg:grid-cols-2 lg:px-0 bg-background text-foreground">
            {/* Left Side - Brand/Marketing */}
            <div className="relative hidden h-full flex-col bg-secondary p-10 text-white dark:border-r lg:flex">
                <div className="absolute inset-0 bg-zinc-900" />
                <div className="relative z-20 flex items-center text-lg font-medium gap-2">
                    <ShieldCheck className="h-6 w-6 text-primary" />
                    CyberDefense Platform
                </div>
                <div className="relative z-20 mt-auto">
                    <blockquote className="space-y-2">
                        <p className="text-lg">
                            &ldquo;Security isn't just about defense. It's about knowing what's happening before it affects your business. Unify your intelligence.&rdquo;
                        </p>
                        <footer className="text-sm">Sofia Davis, CISO</footer>
                    </blockquote>
                </div>
            </div>

            {/* Right Side - Login Form */}
            <div className="lg:p-8">
                <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
                    <div className="flex flex-col space-y-2 text-center">
                        <h1 className="text-2xl font-semibold tracking-tight">
                            Welcome back
                        </h1>
                        <p className="text-sm text-muted-foreground">
                            Enter your credentials to access the command center
                        </p>
                    </div>

                    <Card className="border-0 shadow-none">
                        <form onSubmit={onSubmit}>
                            <CardContent className="grid gap-4 p-0">
                                <div className="grid gap-2">
                                    <Input id="email" placeholder="name@example.com" type="email" autoCapitalize="none" autoComplete="email" autoCorrect="off" disabled={isLoading} required />
                                </div>
                                <div className="grid gap-2">
                                    <Input id="password" placeholder="Password" type="password" disabled={isLoading} required />
                                </div>
                            </CardContent>

                            <CardFooter className="flex flex-col gap-4 p-0 mt-4">
                                <Button className="w-full" disabled={isLoading}>
                                    {isLoading ? "Authenticating..." : "Sign In with Email"}
                                </Button>
                                <p className="px-8 text-center text-xs text-muted-foreground">
                                    <Lock className="inline h-3 w-3 mr-1" />
                                    Protected by enterprise-grade security
                                </p>
                            </CardFooter>
                        </form>
                    </Card>

                    <p className="px-8 text-center text-xs text-muted-foreground">
                        Don&apos;t have an account?{" "}
                        {/* In a real app, this would go to a signup flow */}
                        <Link href="/onboarding" className="underline underline-offset-4 hover:text-primary">
                            Start Enterprise Trial
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    )
}
