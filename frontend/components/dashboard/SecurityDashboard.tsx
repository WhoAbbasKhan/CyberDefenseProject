"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, Shield, Globe, Activity, Zap, Loader2 } from "lucide-react"
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { AttackForecastWidget } from "@/components/security/AttackForecastWidget"
import { useEffect, useState } from "react"
import { toast } from "sonner"
import { auth } from "@/lib/auth"

export function SecurityDashboard() {
    const [loading, setLoading] = useState(true)
    const [metrics, setMetrics] = useState<any>(null)

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const token = auth.getToken()
                if (!token) {
                    // Redirect to login if no token
                    window.location.href = "/login"
                    return
                }

                const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/incidents/stats`, {
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                })
                if (!res.ok) throw new Error("Failed to fetch stats")
                const data = await res.json()
                setMetrics(data)
            } catch (error) {
                console.error("Error fetching dashboard stats:", error)
                // toast.error("Failed to load dashboard metrics") 
                // Don't show toast on load to avoid spam if backend is down during dev
            } finally {
                setLoading(false)
            }
        }
        fetchStats()
    }, [])

    if (loading) {
        return (
            <div className="flex h-[400px] items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        )
    }

    // Fallback if fetch failed
    if (!metrics) {
        return <div className="p-4 text-center text-muted-foreground">Dashboard data unavailable. Is backend running?</div>
    }

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Top Metrics */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card className="glass border-l-4 border-l-primary">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Active Threats
                        </CardTitle>
                        <Activity className="h-4 w-4 text-primary" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{metrics.active_threats}</div>
                        <p className="text-xs text-muted-foreground">
                            +2 from last hour
                        </p>
                    </CardContent>
                </Card>

                <Card className="glass border-l-4 border-l-destructive">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Critical Incidents
                        </CardTitle>
                        <AlertCircle className="h-4 w-4 text-destructive" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-destructive">{metrics.critical_incidents}</div>
                        <p className="text-xs text-muted-foreground">
                            Requires attention
                        </p>
                    </CardContent>
                </Card>

                <div className="col-span-1 md:col-span-2 lg:col-span-1 row-span-2">
                    <AttackForecastWidget />
                </div>

                <Card className="glass border-l-4 border-l-success">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Systems Protected
                        </CardTitle>
                        <Shield className="h-4 w-4 text-success" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{metrics.systems_protected}%</div>
                        <p className="text-xs text-muted-foreground">
                            All systems operational
                        </p>
                    </CardContent>
                </Card>

                <Card className="glass border-l-4 border-l-warning">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Global Traffic
                        </CardTitle>
                        <Globe className="h-4 w-4 text-warning" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{metrics.global_traffic}</div>
                        <p className="text-xs text-muted-foreground">
                            Requests / min
                        </p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">

                {/* Main Chart */}
                <Card className="col-span-4 glass">
                    <CardHeader>
                        <CardTitle>Attack Volume (24h)</CardTitle>
                    </CardHeader>
                    <CardContent className="pl-2">
                        <div className="h-[300px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={metrics.chart_data}>
                                    <defs>
                                        <linearGradient id="colorAttacks" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.8} />
                                            <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted/20" vertical={false} />
                                    <XAxis dataKey="name" className="text-xs text-muted-foreground" tickLine={false} axisLine={false} />
                                    <YAxis className="text-xs text-muted-foreground" tickLine={false} axisLine={false} />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', color: 'hsl(var(--foreground))' }}
                                        itemStyle={{ color: 'hsl(var(--foreground))' }}
                                    />
                                    <Area type="monotone" dataKey="attacks" stroke="hsl(var(--primary))" fillOpacity={1} fill="url(#colorAttacks)" />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                </Card>

                {/* Live Feed */}
                <Card className="col-span-3 glass flex flex-col">
                    <CardHeader>
                        <CardTitle>Live Attack Feed</CardTitle>
                        <CardDescription>Real-time threat detection stream</CardDescription>
                    </CardHeader>
                    <CardContent className="flex-1 overflow-hidden">
                        <div className="space-y-4 pr-2 max-h-[300px] overflow-y-auto">
                            {metrics.recent_attacks.map((attack: any) => (
                                <div key={attack.id} className="flex items-center justify-between rounded-lg border p-3 hover:bg-muted/50 transition-colors">
                                    <div className="flex items-center gap-4">
                                        <div className={`rounded-full p-2 bg-${attack.severity === 'critical' ? 'destructive' : attack.severity === 'high' ? 'orange-500' : 'blue-500'}/10`}>
                                            <Zap className={`h-4 w-4 ${attack.severity === 'critical' ? 'text-destructive' : attack.severity === 'high' ? 'text-orange-500' : 'text-blue-500'}`} />
                                        </div>
                                        <div className="space-y-1">
                                            <p className="text-sm font-medium leading-none">{attack.type}</p>
                                            <p className="text-xs text-muted-foreground">{attack.target}</p>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <Badge variant={attack.severity as any} className="uppercase text-[10px]">{attack.severity}</Badge>
                                        <p className="text-[10px] text-muted-foreground mt-1">{attack.time}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
