"use client"

import { useEffect, useState } from "react"
import DashboardLayout from "@/components/layout/DashboardLayout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Plus, Trash2, Save, Loader2 } from "lucide-react"
import { auth } from "@/lib/auth"
import { toast } from "sonner" // Assuming sonner or similar exists, or alert

interface DefenseRule {
    id: number
    name: string
    if_type: string
    if_severity: string
    then_action: string
    is_active: boolean
}

export default function DefensePage() {
    const [rules, setRules] = useState<DefenseRule[]>([])
    const [loading, setLoading] = useState(true)
    const [newRule, setNewRule] = useState({
        name: "",
        if_type: "SQL Injection",
        if_severity: "High",
        then_action: "Block IP"
    })

    const fetchRules = async () => {
        setLoading(true)
        try {
            const token = auth.getToken()
            if (!token) return

            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/defense/rules`, {
                headers: { "Authorization": `Bearer ${token}` }
            })
            if (res.ok) {
                const data = await res.json()
                setRules(data)
            }
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    const createRule = async () => {
        if (!newRule.name) return
        try {
            const token = auth.getToken()
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/defense/rules`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(newRule)
            })
            if (res.ok) {
                // toast.success("Rule created")
                setNewRule({ ...newRule, name: "" })
                fetchRules()
            }
        } catch (e) {
            console.error(e)
        }
    }

    const deleteRule = async (id: number) => {
        try {
            const token = auth.getToken()
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/defense/rules/${id}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            })
            if (res.ok) {
                fetchRules()
            }
        } catch (e) {
            console.error(e)
        }
    }

    useEffect(() => {
        fetchRules()
    }, [])

    return (
        <DashboardLayout>
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Defense Rules</h1>
                    <p className="text-muted-foreground">Automate your response to detected threats.</p>
                </div>
                <Button onClick={fetchRules} variant="ghost">
                    <Loader2 className={`mr-2 h-4 w-4 ${loading ? "animate-spin" : ""}`} />
                    Refresh
                </Button>
            </div>

            <div className="grid gap-6 lg:grid-cols-3">
                {/* Rule List */}
                <div className="col-span-2 space-y-4">
                    {rules.length === 0 && !loading && (
                        <div className="text-center py-12 text-muted-foreground bg-muted/10 rounded-lg border border-dashed">
                            No rules configured. Add one below.
                        </div>
                    )}
                    {rules.map((rule) => (
                        <Card key={rule.id} className="glass hover:bg-muted/5 transition-colors group relative">
                            <Button
                                variant="ghost"
                                size="icon"
                                className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 text-destructive hover:bg-destructive/10"
                                onClick={() => deleteRule(rule.id)}
                            >
                                <Trash2 className="h-4 w-4" />
                            </Button>
                            <CardHeader className="flex flex-row items-center justify-between pb-2">
                                <div className="space-y-1">
                                    <CardTitle className="text-base">{rule.name}</CardTitle>
                                    <div className="flex gap-2">
                                        <Badge variant="outline">{rule.if_type}</Badge>
                                        <Badge variant="destructive" className="text-[10px]">{rule.if_severity}</Badge>
                                    </div>
                                </div>
                                <div className="flex items-center gap-2 pr-8">
                                    <Badge variant={rule.is_active ? "success" : "secondary"}>
                                        {rule.is_active ? "Active" : "Disabled"}
                                    </Badge>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <div className="flex items-center gap-2 text-sm text-muted-foreground bg-secondary/50 p-2 rounded-md font-mono">
                                    <span className="text-primary">IF</span> {rule.if_type} == {rule.if_severity} <span className="text-primary">THEN</span> {rule.then_action}
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>

                {/* Quick Builder */}
                <Card className="col-span-1 border-primary/20 bg-primary/5 h-fit">
                    <CardHeader>
                        <CardTitle>Logic Builder</CardTitle>
                        <CardDescription>Drafting new rule...</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Rule Name</label>
                            <Input
                                placeholder="e.g. Block Phishing IPs"
                                value={newRule.name}
                                onChange={(e) => setNewRule({ ...newRule, name: e.target.value })}
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium">If Attack Type is:</label>
                            <select
                                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                                value={newRule.if_type}
                                onChange={(e) => setNewRule({ ...newRule, if_type: e.target.value })}
                            >
                                <option>Phishing</option>
                                <option>SQL Injection</option>
                                <option>Brute Force</option>
                                <option>XSS</option>
                            </select>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium">And Severity is:</label>
                            <select
                                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                                value={newRule.if_severity}
                                onChange={(e) => setNewRule({ ...newRule, if_severity: e.target.value })}
                            >
                                <option>Critical</option>
                                <option>High</option>
                                <option>Medium</option>
                                <option>Low</option>
                            </select>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium">Then Action:</label>
                            <select
                                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                                value={newRule.then_action}
                                onChange={(e) => setNewRule({ ...newRule, then_action: e.target.value })}
                            >
                                <option>Block IP Address</option>
                                <option>Lock User Account</option>
                                <option>Quarantine Email</option>
                                <option>Alert Admin</option>
                            </select>
                        </div>

                        <Button className="w-full mt-4" onClick={createRule} disabled={!newRule.name}>
                            <Save className="mr-2 h-4 w-4" />
                            Save Rule
                        </Button>
                    </CardContent>
                </Card>
            </div>
        </DashboardLayout>
    )
}
