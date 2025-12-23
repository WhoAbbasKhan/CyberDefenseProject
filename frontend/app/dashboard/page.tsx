"use client"

import { useState } from "react"
import DashboardLayout from "@/components/layout/DashboardLayout"
import { SecurityDashboard } from "@/components/dashboard/SecurityDashboard"
import { CeoDashboard } from "@/components/dashboard/CeoDashboard"
import { EmployeeDashboard } from "@/components/dashboard/EmployeeDashboard"
import { Button } from "@/components/ui/button"
import { PasskeyRegisterButton } from "@/components/auth/PasskeyManager"

export default function DashboardPage() {
    // Mock Role Switching for Demo
    const [role, setRole] = useState<"ceo" | "it" | "employee">("it")

    return (
        <DashboardLayout>
            <div className="mb-6 flex items-center justify-between">
                <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>

                {/* Role Switcher Debugger */}
                <div className="flex gap-2 rounded-md bg-muted p-1">
                    {(["ceo", "it", "employee"] as const).map((r) => (
                        <Button
                            key={r}
                            variant={role === r ? "default" : "ghost"}
                            size="sm"
                            onClick={() => setRole(r)}
                            className="capitalize"
                        >
                            {r}
                        </Button>
                    ))}
                </div>

                <PasskeyRegisterButton />
            </div>

            {role === "it" && <SecurityDashboard />}
            {role === "ceo" && <CeoDashboard />}
            {role === "employee" && <EmployeeDashboard />}

        </DashboardLayout>
    )
}
