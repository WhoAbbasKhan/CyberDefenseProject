"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { ShieldCheck, CheckCircle2, ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export default function OnboardingPage() {
    const router = useRouter()
    const [step, setStep] = useState(1)
    const [isLoading, setIsLoading] = useState(false)

    // Step 1: Org Name
    // Step 2: Role
    // Step 3: Success

    const handleNext = () => {
        if (step < 3) {
            setStep(step + 1)
        } else {
            // Finish
            setIsLoading(true)
            setTimeout(() => router.push("/dashboard"), 1000)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-background p-4">
            <Card className="w-full max-w-lg shadow-2xl border-muted">
                <CardHeader className="text-center">
                    <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                        <ShieldCheck className="h-6 w-6 text-primary" />
                    </div>
                    <CardTitle className="text-xl">Setup Organization</CardTitle>
                    <CardDescription>
                        Step {step} of 3
                    </CardDescription>
                    <div className="mt-2 h-1 w-full bg-secondary rounded-full overflow-hidden">
                        <div
                            className="h-full bg-primary transition-all duration-500 ease-out"
                            style={{ width: `${(step / 3) * 100}%` }}
                        />
                    </div>
                </CardHeader>

                <CardContent className="py-6">
                    {step === 1 && (
                        <div className="space-y-4 animate-in fade-in slide-in-from-right-8 duration-300">
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Organization Name</label>
                                <Input placeholder="e.g. Acme Corp" autoFocus />
                                <p className="text-xs text-muted-foreground">This will be your workspace identifier.</p>
                            </div>
                        </div>
                    )}

                    {step === 2 && (
                        <div className="space-y-4 animate-in fade-in slide-in-from-right-8 duration-300">
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Select Your Role</label>
                                <div className="grid grid-cols-1 gap-2">
                                    {["CISO / Security Admin", "IT Manager", "CEO / Executive"].map((role) => (
                                        <div key={role} className="flex items-center space-x-2 rounded-md border p-4 hover:bg-accent cursor-pointer transition-colors">
                                            <div className="h-4 w-4 rounded-full border border-primary" />
                                            <span className="text-sm">{role}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {step === 3 && (
                        <div className="flex flex-col items-center justify-center space-y-4 text-center animate-in fade-in zoom-in duration-300">
                            <CheckCircle2 className="h-16 w-16 text-success" />
                            <h3 className="text-lg font-semibold">Trial Activated!</h3>
                            <p className="text-muted-foreground text-sm max-w-xs">
                                Your enterprise environment is ready. You have 14 days of full access.
                            </p>
                            <Badge variant="secondary" className="mt-2">Pro Plan (Trial)</Badge>
                        </div>
                    )}
                </CardContent>

                <CardFooter className="flex justify-between">
                    <Button variant="ghost" disabled={step === 1 || step === 3} onClick={() => setStep(step - 1)}>
                        Back
                    </Button>
                    <Button onClick={handleNext} disabled={isLoading}>
                        {step === 3 ? (isLoading ? "Redirecting..." : "Enter Dashboard") : (
                            <>
                                Next <ArrowRight className="ml-2 h-4 w-4" />
                            </>
                        )}
                    </Button>
                </CardFooter>
            </Card>
        </div>
    )
}
