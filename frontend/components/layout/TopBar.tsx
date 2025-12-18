import Link from "next/link"
import { Bell, Search, User, ShieldCheck } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"

export function TopBar() {
    return (
        <header className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b bg-background/95 px-6 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="flex items-center gap-2 font-bold md:hidden">
                <ShieldCheck className="h-6 w-6 text-primary" />
                <span>CyberDefense</span>
            </div>

            {/* Organization Switcher (Mock) */}
            <div className="hidden md:flex items-center gap-2">
                <div className="flex h-8 items-center gap-2 rounded-md border bg-muted/50 px-3 text-sm">
                    <span className="font-medium">Acme Corp</span>
                    <span className="text-muted-foreground">|</span>
                    <span className="text-xs text-muted-foreground">Free Trial</span>
                </div>
                <Badge variant="warning" className="text-[10px] h-5">13 Days Left</Badge>
            </div>

            <div className="ml-auto flex items-center gap-4">
                {/* Global Search */}
                <div className="relative hidden sm:block">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                        type="search"
                        placeholder="Search IP, domain or user..."
                        className="w-64 pl-9 h-9 bg-secondary/50 border-transparent focus:bg-background transition-colors"
                    />
                </div>

                {/* Actions */}
                <Button variant="ghost" size="icon" className="relative text-muted-foreground hover:text-foreground">
                    <Bell className="h-5 w-5" />
                    <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-destructive" />
                </Button>

                <Button variant="ghost" size="icon" className="rounded-full">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/20">
                        <User className="h-4 w-4 text-primary" />
                    </div>
                </Button>
            </div>
        </header>
    )
}
