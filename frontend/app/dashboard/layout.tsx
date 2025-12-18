"use client"

import { AuthGuard } from "@/components/auth/AuthGuard"
import { Sidebar } from "@/components/layout/Sidebar"

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    // We already have a Sidebar/Layout in the individual page.tsx mostly? 
    // Let's check if the existing page.tsx includes the sidebar. 
    // If we add it here, we should remove it from page.tsx to avoid duplication.
    // For now, let's just wrap strictly with AuthGuard to stay safe and not break layout.

    return (
        <AuthGuard>
            {children}
        </AuthGuard>
    )
}
