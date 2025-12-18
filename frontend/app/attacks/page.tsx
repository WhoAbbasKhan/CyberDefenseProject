"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "@/components/layout/DashboardLayout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, MapPin, ShieldAlert, RefreshCw } from "lucide-react"
import { auth } from "@/lib/auth"

interface AttackEvent {
    id: number
    attack_type: string
    target_url: string
    source_ip: string
    severity: string
    timestamp: string
    country?: string
}

export default function AttacksPage() {
    const [attacks, setAttacks] = useState<AttackEvent[]>([])
    const [loading, setLoading] = useState(true)

    const fetchAttacks = async () => {
        setLoading(true)
        try {
            const token = auth.getToken()
            if (!token) return

            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/monitor/events?limit=50`, {
                headers: { "Authorization": `Bearer ${token}` }
            })
            if (res.ok) {
                const data = await res.json()
                setAttacks(data)
            }
        } catch (e) {
            console.error("Failed to fetch attacks", e)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchAttacks()
        // Poll every 10s
        const interval = setInterval(fetchAttacks, 10000)
        return () => clearInterval(interval)
    }, [])

    return (
        <DashboardLayout>
            <div className="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between mb-6">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Live Attacks</h1>
                    <p className="text-muted-foreground">Real-time monitoring of security events.</p>
                </div>

                <div className="flex items-center gap-2">
                    <div className="relative">
                        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                        <Input placeholder="Filter by IP..." className="pl-9 w-[250px]" />
                    </div>
                    <Button variant="outline" onClick={fetchAttacks} disabled={loading}>
                        <RefreshCw className={`mr-2 h-4 w-4 ${loading ? "animate-spin" : ""}`} />
                        Refresh
                    </Button>
                </div>
            </div>

            <Card className="glass">
                <CardHeader>
                    <CardTitle>Event Log</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {/* Table Header */}
                        <div className="grid grid-cols-6 gap-4 border-b pb-2 text-sm font-medium text-muted-foreground">
                            <div className="col-span-2">Type / Target</div>
                            <div className="col-span-1">Source</div>
                            <div className="col-span-1">Severity</div>
                            <div className="col-span-1">Status</div>
                            <div className="col-span-1 text-right">Time</div>
                        </div>

                        {/* Rows */}
                        {attacks.length === 0 && !loading && (
                            <div className="text-center py-8 text-muted-foreground">No recorded attacks found.</div>
                        )}

                        {attacks.map((attack) => (
                            <div key={attack.id} className="grid grid-cols-6 gap-4 items-center text-sm py-2 hover:bg-muted/30 rounded-md px-1 transition-colors bg-secondary/10 border border-transparent hover:border-muted">
                                <div className="col-span-2">
                                    <div className="flex items-center gap-2 font-medium">
                                        <ShieldAlert className="h-4 w-4 text-muted-foreground" />
                                        {attack.attack_type || "Web Request"}
                                    </div>
                                    <div className="text-xs text-muted-foreground pl-6 truncate">{attack.target_url}</div>
                                </div>
                                <div className="col-span-1">
                                    <div>{attack.source_ip}</div>
                                    <div className="flex items-center gap-1 text-xs text-muted-foreground">
                                        <MapPin className="h-3 w-3" /> {attack.country || "Unknown"}
                                    </div>
                                </div>
                                <div className="col-span-1">
                                    <Badge variant={attack.severity as any} className="capitalize">
                                        {attack.severity}
                                    </Badge>
                                </div>
                                <div className="col-span-1">
                                    <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset ${attack.severity === 'critical' ? 'bg-red-500/10 text-red-500 ring-red-500/20' :
                                        'bg-blue-500/10 text-blue-400 ring-blue-500/20'
                                        }`}>
                                        {attack.attack_type ? "Detected" : "Logged"}
                                    </span>
                                </div>
                                <div className="col-span-1 text-right text-muted-foreground text-xs">
                                    {new Date(attack.timestamp + "Z").toLocaleTimeString()}
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </DashboardLayout>
    )
}
