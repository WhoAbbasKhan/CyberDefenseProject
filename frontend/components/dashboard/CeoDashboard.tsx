"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function CeoDashboard() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">Executive Overview</h2>
                <span className="text-sm text-muted-foreground">Last updated: Just now</span>
            </div>

            {/* Risk Score */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card className="glass col-span-1">
                    <CardHeader>
                        <CardTitle className="text-lg">Cyber Risk Score</CardTitle>
                    </CardHeader>
                    <CardContent className="flex flex-col items-center justify-center p-6">
                        <div className="relative flex items-center justify-center h-40 w-40 rounded-full border-8 border-primary/20">
                            <span className="text-4xl font-bold text-primary">B+</span>
                        </div>
                        <p className="mt-4 text-center text-sm text-muted-foreground">
                            Your organization is performing better than 85% of peers.
                        </p>
                    </CardContent>
                </Card>

                <Card className="glass col-span-2">
                    <CardHeader>
                        <CardTitle className="text-lg">Financial Impact Prevention</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <div className="flex items-center justify-between border-b pb-4">
                                <div>
                                    <p className="font-medium">Potential Loss Averted</p>
                                    <p className="text-xs text-muted-foreground">Based on blocked attacks this month</p>
                                </div>
                                <div className="text-2xl font-bold text-success">$145,000</div>
                            </div>
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="font-medium">Compliance Status</p>
                                    <p className="text-xs text-muted-foreground">SOC2, ISO27001</p>
                                </div>
                                <div className="text-xl font-bold text-primary">On Track</div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
