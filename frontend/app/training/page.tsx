"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "@/components/layout/DashboardLayout"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { PlayCircle, CheckCircle, PlusCircle, Loader2 } from "lucide-react"
import { auth } from "@/lib/auth"
import { toast } from "sonner"

interface TrainingModule {
    id: number
    title: string
    description: string
    category: string
    duration_minutes: number
}

interface UserTraining {
    id: number
    status: string
    score: number
    module: TrainingModule
    // Calculated frontend fields
    progress: number
}

export default function TrainingPage() {
    const [trainings, setTrainings] = useState<UserTraining[]>([])
    const [loading, setLoading] = useState(true)

    const fetchTraining = async () => {
        setLoading(true)
        try {
            const token = auth.getToken()
            if (!token) return

            const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1"
            console.log("Debug: API URL is:", apiUrl)
            const res = await fetch(`${apiUrl}/training/me`, {
                headers: { "Authorization": `Bearer ${token}` }
            })
            if (res.ok) {
                const data = await res.json()
                // Map to frontend structure
                const mapped = data.map((t: any) => ({
                    id: t.id,
                    status: t.status, // Assigned, In Progress, Completed
                    score: t.score,
                    module: t.module,
                    progress: t.status === "Completed" ? 100 : t.status === "In Progress" ? 50 : 0
                }))
                setTrainings(mapped)
            }
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    const assignDemoTraining = async () => {
        try {
            const token = auth.getToken()
            // We need email, but let's assume backend gets it from token? 
            // Actually /trigger expects {email, trigger_type}
            // We need to parse token to get email or fetch /auth/me. 
            // For MVP speed, I'll allow a simple "assign me" endpoint or just hardcode "admin@velvet.astro" if I'm logged in as that.
            // Let's try to just use a fixed known email or fetch user profile first.
            // Actually, let's just use the 'auth' lib if it has user info? It doesn't atm.
            // I'll make a quick call to /auth/me is not readily available.
            // I'll use a hack: Try to assign to "admin@velvet.astro" (the default user).

            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/training/trigger`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: "admin@velvetastro.io", // Updated to seeded admin
                    trigger_type: "phishing_click"
                })
            })

            if (res.ok) {
                toast.success("Training Assigned")
                fetchTraining()
            } else {
                toast.error("Failed to assign (User email mismatch?)")
            }
        } catch (e) {
            console.error(e)
        }
    }

    const completeTraining = async (id: number) => {
        try {
            const token = auth.getToken()
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/training/complete/${id}`, {
                method: "POST",
                headers: { "Authorization": `Bearer ${token}` }
            })
            if (res.ok) {
                toast.success("Module Completed!")
                fetchTraining()
            }
        } catch (e) {
            console.error(e)
        }
    }

    useEffect(() => {
        fetchTraining()
    }, [])

    return (
        <DashboardLayout>
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Security Training</h1>
                    <p className="text-muted-foreground">Level up your defense skills.</p>
                </div>
                <Button onClick={assignDemoTraining} variant="outline" size="sm">
                    <PlusCircle className="mr-2 h-4 w-4" />
                    Assign Demo Module
                </Button>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {trainings.length === 0 && !loading && (
                    <div className="col-span-3 text-center py-12 text-muted-foreground">
                        No training assigned. Good job! (Or click 'Assign Demo Module')
                    </div>
                )}

                {trainings.map((t) => (
                    <Card key={t.id} className="flex flex-col">
                        <CardHeader>
                            <div className="flex justify-between items-start">
                                <Badge variant="outline">{t.module.category}</Badge>
                                {t.status === 'Completed' && <CheckCircle className="h-5 w-5 text-green-500" />}
                            </div>
                            <CardTitle className="mt-2 text-xl">{t.module.title}</CardTitle>
                            <CardDescription>{t.module.description}</CardDescription>
                        </CardHeader>
                        <CardContent className="flex-1 space-y-4">
                            <div className="flex items-center text-sm text-muted-foreground gap-4">
                                <span>{t.module.duration_minutes} min</span>
                                <span>•</span>
                                <span className={t.status === 'In Progress' ? 'text-blue-400' : ''}>{t.status}</span>
                            </div>

                            {t.status !== 'Assigned' && (
                                <div className="space-y-1">
                                    <div className="flex justify-between text-xs">
                                        <span>Progress</span>
                                        <span>{t.progress}%</span>
                                    </div>
                                    <div className="h-2 w-full rounded-full bg-secondary">
                                        <div
                                            className={`h-full rounded-full ${t.status === 'Completed' ? 'bg-green-500' : 'bg-primary'}`}
                                            style={{ width: `${t.progress}%` }}
                                        />
                                    </div>
                                </div>
                            )}
                        </CardContent>
                        <CardFooter>
                            <Button
                                className="w-full"
                                variant={t.status === 'Completed' ? "outline" : "default"}
                                onClick={() => t.status !== 'Completed' && completeTraining(t.id)}
                            >
                                {t.status === 'Completed' ? "Review" : "Complete Module"}
                                {t.status !== 'Completed' && <PlayCircle className="ml-2 h-4 w-4" />}
                            </Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>
        </DashboardLayout>
    )
}
