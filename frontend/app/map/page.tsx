"use client"

import { useEffect, useRef, useState } from "react"
import DashboardLayout from "@/components/layout/DashboardLayout"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ShieldAlert, Globe } from "lucide-react"

// Simple interface for an attack
interface AttackPoint {
    id: number
    x: number
    y: number
    type: string
    origin: string
    destination: string
    timestamp: number
}

export default function ThreatMapPage() {
    const canvasRef = useRef<HTMLCanvasElement>(null)
    const [stats, setStats] = useState({ active: 0, blocked: 0 })
    const [recentAttacks, setRecentAttacks] = useState<AttackPoint[]>([])

    // Animation Loop
    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return

        const ctx = canvas.getContext("2d")
        if (!ctx) return

        let animationFrameId: number
        let attacks: AttackPoint[] = []

        // Resize canvas
        const resize = () => {
            const parent = canvas.parentElement
            if (parent) {
                canvas.width = parent.clientWidth
                canvas.height = parent.clientHeight
            }
        }
        window.addEventListener("resize", resize)
        resize()

        // Generate random attacks periodically
        const interval = setInterval(() => {
            if (Math.random() > 0.3) return // 30% chance per tick

            const startX = Math.random() * canvas.width
            const startY = Math.random() * canvas.height
            const endX = Math.random() * canvas.width
            const endY = Math.random() * canvas.height

            attacks.push({
                id: Date.now(),
                x: startX,
                y: startY,
                type: Math.random() > 0.5 ? "DDoS" : "SQL Injection",
                origin: "Unknown",
                destination: "Velvet Corp",
                timestamp: 0
            })

            // Keep array clean
            if (attacks.length > 20) attacks.shift()

            // Update stats
            setStats(prev => ({
                active: prev.active + 1,
                blocked: prev.blocked + (Math.random() > 0.8 ? 1 : 0) // Randomly block
            }))

            // Update list for UI
            setRecentAttacks(current => [...current, attacks[attacks.length - 1]].slice(-5))

        }, 800)

        // Render Frame
        const render = () => {
            ctx.fillStyle = "rgba(0,0,0,0.1)" // Trail effect
            ctx.fillRect(0, 0, canvas.width, canvas.height)

            // Draw generic "World Map" dots (Simulated for premium look without heavy geojson)
            // Just a grid representing the cyber-space
            ctx.fillStyle = "rgba(50, 200, 255, 0.05)"
            for (let i = 0; i < canvas.width; i += 40) {
                for (let j = 0; j < canvas.height; j += 40) {
                    ctx.beginPath()
                    ctx.arc(i, j, 1, 0, Math.PI * 2)
                    ctx.fill()
                }
            }

            // Draw Attacks
            attacks.forEach((attack, index) => {
                attack.timestamp++

                // Draw Expanding Circle (Hit)
                ctx.beginPath()
                ctx.strokeStyle = `rgba(255, 50, 50, ${1 - attack.timestamp / 100})`
                ctx.lineWidth = 2
                ctx.arc(attack.x, attack.y, attack.timestamp * 1.5, 0, Math.PI * 2)
                ctx.stroke()

                // Draw Line (optional, simplified as "hits" for now)
            })

            // Remove old
            attacks = attacks.filter(a => a.timestamp < 100)

            animationFrameId = requestAnimationFrame(render)
        }
        render()

        return () => {
            window.removeEventListener("resize", resize)
            cancelAnimationFrame(animationFrameId)
            clearInterval(interval)
        }
    }, [])

    return (
        <DashboardLayout>
            <div className="flex flex-col h-[calc(100vh-100px)] space-y-4">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Global Threat Map</h1>
                        <p className="text-muted-foreground">Real-time visualization of cyber-kinetic activity.</p>
                    </div>
                    <div className="flex gap-4">
                        <Card className="p-3 flex items-center gap-3 bg-destructive/10 border-destructive/20">
                            <ShieldAlert className="h-5 w-5 text-destructive" />
                            <div>
                                <div className="text-2xl font-bold leading-none">{stats.active}</div>
                                <div className="text-xs text-muted-foreground">Intercepted</div>
                            </div>
                        </Card>
                        <Card className="p-3 flex items-center gap-3 bg-secondary/50">
                            <Globe className="h-5 w-5 text-primary" />
                            <div>
                                <div className="text-2xl font-bold leading-none text-primary">Live</div>
                                <div className="text-xs text-muted-foreground">Status</div>
                            </div>
                        </Card>
                    </div>
                </div>

                <Card className="flex-1 relative overflow-hidden border-primary/20 bg-background/50 backdrop-blur-sm">
                    {/* Map Canvas */}
                    <canvas
                        ref={canvasRef}
                        className="absolute inset-0 w-full h-full block"
                    />

                    {/* Overlay UI */}
                    <div className="absolute top-4 right-4 w-64 space-y-2">
                        <CardTitle className="text-xs uppercase tracking-wider text-muted-foreground mb-2">Recent Vectors</CardTitle>
                        {recentAttacks.map(attack => (
                            <div key={attack.id} className="bg-black/80 backdrop-blur-md rounded border border-white/10 p-2 text-xs flex justify-between animate-in slide-in-from-right fade-in duration-300">
                                <span className="text-destructive font-bold">{attack.type}</span>
                                <span className="text-muted-foreground">{attack.origin}</span>
                            </div>
                        ))}
                    </div>
                </Card>
            </div>
        </DashboardLayout>
    )
}
