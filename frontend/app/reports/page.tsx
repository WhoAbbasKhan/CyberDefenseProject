"use client"

import DashboardLayout from "@/components/layout/DashboardLayout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { FileText, Download, Share2, Loader2, Plus } from "lucide-react"
import { useEffect, useState } from "react"
import { toast } from "sonner"
import { auth } from "@/lib/auth"

interface Report {
    id: number
    name: string
    date: string
    type: string
    size: string
}

export default function ReportsPage() {
    const [reports, setReports] = useState<Report[]>([])
    const [loading, setLoading] = useState(true)

    const fetchReports = async () => {
        try {
            const token = auth.getToken()
            if (!token) return

            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/reporting/`, {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            })
            if (!res.ok) throw new Error("Failed to fetch reports")
            const data = await res.json()
            setReports(data)
        } catch (error) {
            console.error("Error fetching reports:", error)
            toast.error("Failed to fetch reports.")
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchReports()
    }, [])

    const handleCreateReport = async () => {
        const newReportName = `Custom Report - ${new Date().toLocaleTimeString()}`
        try {
            const res = await fetch("http://localhost:8000/api/v1/reporting/custom", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer mock_token"
                },
                body: JSON.stringify({ name: newReportName, type: "Custom" })
            })
            if (!res.ok) throw new Error("Failed to create report")
            const savedReport = await res.json()
            setReports([savedReport, ...reports])
            toast.success("Report created successfully!")
        } catch (error) {
            console.error("Error creating report:", error)
            toast.error("Failed to create report.")
        }
    }

    return (
        <DashboardLayout>
            <div className="mb-8">
                <h1 className="text-3xl font-bold tracking-tight">Reports & Compliance</h1>
                <p className="text-muted-foreground">Download and manage your security documentation.</p>
            </div>

            <div className="grid gap-6 lg:grid-cols-2">
                <Card className="glass">
                    <CardHeader>
                        <CardTitle>Generated Reports</CardTitle>
                        <CardDescription>Automatically generated periodic reports.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        {loading ? (
                            <div className="flex justify-center p-8">
                                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {reports.length === 0 ? (
                                    <p className="text-center text-muted-foreground py-4">No reports found.</p>
                                ) : (
                                    reports.map((report) => (
                                        <div key={report.id} className="flex items-center justify-between rounded-lg border p-4 hover:bg-muted/50 transition-colors">
                                            <div className="flex items-center gap-4">
                                                <div className="rounded-lg bg-primary/10 p-2">
                                                    <FileText className="h-6 w-6 text-primary" />
                                                </div>
                                                <div>
                                                    <h4 className="font-medium">{report.name}</h4>
                                                    <p className="text-xs text-muted-foreground">{report.date} • {report.type}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <Button size="sm" variant="ghost">
                                                    <Share2 className="h-4 w-4" />
                                                </Button>
                                                <Button size="sm" variant="outline">
                                                    <Download className="mr-2 h-4 w-4" />
                                                    PDF
                                                </Button>
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        )}
                    </CardContent>
                </Card>

                <Card className="border-dashed border-2">
                    <CardHeader>
                        <CardTitle>Generate Custom Report</CardTitle>
                        <CardDescription>Select parameters to export specific data.</CardDescription>
                    </CardHeader>
                    <CardContent className="flex flex-col items-center justify-center space-y-4 py-8 text-center">
                        <div className="rounded-full bg-muted p-4">
                            <FileText className="h-8 w-8 text-muted-foreground" />
                        </div>
                        <p className="text-sm text-muted-foreground max-w-xs">
                            Create a custom report based on specific date ranges, attack types, or user groups.
                        </p>
                        <Button onClick={handleCreateReport}>
                            <Plus className="mr-2 h-4 w-4" />
                            Create New Report
                        </Button>
                    </CardContent>
                </Card>
            </div>
        </DashboardLayout>
    )
}
