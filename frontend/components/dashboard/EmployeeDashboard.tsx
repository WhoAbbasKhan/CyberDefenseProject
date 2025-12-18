"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { CheckCircle2, PlayCircle } from "lucide-react"

export function EmployeeDashboard() {
    return (
        <div className="space-y-6">
            <h2 className="text-xl font-semibold">My Security Center</h2>

            <div className="grid gap-6 md:grid-cols-2">

                {/* Training Status */}
                <Card>
                    <CardHeader>
                        <CardTitle>Training Progress</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <span>Q4 Security Awareness</span>
                                <span className="font-medium">75%</span>
                            </div>
                            <div className="h-2 w-full rounded-full bg-secondary">
                                <div className="h-full w-3/4 rounded-full bg-primary" />
                            </div>
                        </div>

                        <div className="rounded-lg border p-4 bg-muted/20">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <div className="rounded-full bg-primary/10 p-2">
                                        <PlayCircle className="h-5 w-5 text-primary" />
                                    </div>
                                    <div>
                                        <h4 className="font-medium">Phishing 101</h4>
                                        <p className="text-xs text-muted-foreground">Due in 3 days</p>
                                    </div>
                                </div>
                                <Button size="sm">Resume</Button>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Recent Activity */}
                <Card>
                    <CardHeader>
                        <CardTitle>Recent Activity</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {[
                                "Logged in from Windows (New York)",
                                "Completed 'Password Security' module",
                                "Changed password"
                            ].map((activity, i) => (
                                <div key={i} className="flex items-center gap-3 text-sm">
                                    <CheckCircle2 className="h-4 w-4 text-green-500" />
                                    <span>{activity}</span>
                                    <span className="ml-auto text-xs text-muted-foreground">2d ago</span>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
