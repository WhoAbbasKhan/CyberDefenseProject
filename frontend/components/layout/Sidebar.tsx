"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
    LayoutDashboard,
    ShieldAlert,
    Map,
    FileText,
    Settings,
    GraduationCap,
    ShieldCheck,
    Globe,
    LogOut
} from "lucide-react"

import { cn } from "@/lib/utils"
import { auth } from "@/lib/auth"

interface SidebarNavProps extends React.HTMLAttributes<HTMLElement> {
    userRole?: "admin" | "it" | "employee" | "ceo"
}

export function Sidebar({ className, userRole = "it", ...props }: SidebarNavProps) {
    return (
        <nav
            className={cn(
                "relative hidden h-screen w-64 flex-col border-r bg-card pt-6 md:flex",
                className
            )}
            {...props}
        >
            {/* Brand */}
            <div className="mb-8 px-6 flex items-center gap-2">
                <ShieldCheck className="h-8 w-8 text-primary" />
                <span className="text-lg font-bold tracking-tight">CyberDefense</span>
            </div>

            {/* Navigation Info */}
            <div className="px-4 mb-2">
                <h4 className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    Menu
                </h4>
            </div>

            <div className="flex-1 space-y-1 px-3">
                <NavItem href="/dashboard" icon={LayoutDashboard}>Overview</NavItem>

                {/* IT / Admin Routes */}
                <NavItem href="/attacks" icon={ShieldAlert}>Live Attacks</NavItem>
                <NavItem href="/map" icon={Globe}>Threat Map</NavItem>
                <NavItem href="/defense" icon={Map}>Defense Rules</NavItem>

                {/* Shared Routes */}
                <NavItem href="/reports" icon={FileText}>Reports</NavItem>
                <NavItem href="/training" icon={GraduationCap}>Training</NavItem>
            </div>

            {/* Bottom Actions */}
            <div className="mt-auto p-4 border-t border-border/50 space-y-1">
                <NavItem href="/settings" icon={Settings}>Settings</NavItem>
                <button
                    onClick={() => {
                        auth.logout()
                    }}
                    className="group flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-destructive/10 hover:text-destructive transition-colors"
                >
                    <LogOut className="h-4 w-4" />
                    <span>Log Out</span>
                </button>
            </div>
        </nav>
    )
}

function NavItem({ href, icon: Icon, children }: { href: string; icon: any; children: React.ReactNode }) {
    // Basic active state check (mocked for now since using Next.js app router which needs hook)
    // In real app use usePathname()
    const isActive = false

    return (
        <Link
            href={href}
            className={cn(
                "group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground transition-colors",
                isActive ? "bg-accent text-accent-foreground" : "text-muted-foreground"
            )}
        >
            <Icon className="h-4 w-4" />
            <span>{children}</span>
        </Link>
    )
}
