"use client";

import { useParams } from "next/navigation";
import { TopBar } from "@/components/layout/TopBar";
import { Sidebar } from "@/components/layout/Sidebar";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { KillChainTimeline } from "@/components/security/KillChainTimeline";
import { RiskAnalysisPanel } from "@/components/security/RiskAnalysisPanel";
import { PlaybookWidget } from "@/components/security/PlaybookWidget";
import { ThreatBadge } from "@/components/security/SecurityBadges";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Clock, MapPin, Monitor, Server, User as UserIcon } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function IncidentDetailsPage() {
    const params = useParams();
    const id = params?.id as string;

    // Mock Data for Visualization (Module D, E, A, C)
    const incidentData = {
        id: id,
        title: "Suspicious Login & Data Exfiltration Attempt",
        severity: "CRITICAL",
        status: "OPEN",
        timestamp: "Today, 10:42 AM",
        actor: {
            ip: "45.133.1.22",
            location: "Pyongyang, KP",
            user: "finance_admin@velvet.net",
            device: "Unknown Linux Device"
        },
        killChainStage: "Exploitation",
        riskScore: 92,
        threatIntel: {
            isKnown: true,
            type: "APT Group (Lazarus)",
            confidence: 98
        },
        playbook: {
            name: "High Severity Account Lock",
            actions: [
                { name: "Risk Score Calculation", status: "SUCCESS" as const, timestamp: "10:42:01" },
                { name: "Threat Intel Lookup", status: "SUCCESS" as const, timestamp: "10:42:02" },
                { name: "Block IP Address", status: "SUCCESS" as const, timestamp: "10:42:02" },
                { name: "Lock User Account", status: "SUCCESS" as const, timestamp: "10:42:03" },
                { name: "Notify SOC Team", status: "RUNNING" as const, timestamp: "10:42:05" }
            ]
        }
    };

    return (
        <div className="flex h-screen bg-background font-sans dark">
            <Sidebar className="w-64 border-r hidden md:block" />
            <div className="flex-1 flex flex-col overflow-hidden">
                <TopBar />
                <main className="flex-1 overflow-y-auto p-6 space-y-6">

                    {/* Header */}
                    <div className="flex items-center justify-between">
                        <div className="space-y-1">
                            <div className="flex items-center gap-2">
                                <Link href="/dashboard" className="text-muted-foreground hover:text-foreground">
                                    <ArrowLeft className="w-4 h-4" />
                                </Link>
                                <h2 className="text-2xl font-bold tracking-tight">{incidentData.title}</h2>
                                <Badge variant="destructive" className="ml-2">CRITICAL</Badge>
                                <Badge variant="outline" className="border-blue-500 text-blue-500">OPEN</Badge>
                            </div>
                            <div className="flex items-center gap-4 text-sm text-muted-foreground ml-6">
                                <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {incidentData.timestamp}</span>
                                <span className="flex items-center gap-1"><Server className="w-3 h-3" /> Asset: Finance DB</span>
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <Button variant="outline">Export Evidence</Button>
                            <Button variant="default" className="bg-blue-600 hover:bg-blue-700">Manage Incident</Button>
                        </div>
                    </div>

                    {/* Module D: Kill Chain Visualization */}
                    <Card className="border-blue-500/20 bg-blue-500/5">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-sm font-medium text-blue-400">ATTACK KILL CHAIN PROGRESSION</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <KillChainTimeline currentStage={incidentData.killChainStage} />
                        </CardContent>
                    </Card>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

                        {/* Left Column: Context & Intel (Module E) */}
                        <div className="space-y-6 col-span-2">
                            <Card>
                                <CardHeader>
                                    <CardTitle>Attacker Context (Threat Intel)</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-6">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="p-4 bg-muted/50 rounded-lg space-y-1">
                                            <span className="text-xs text-muted-foreground uppercase flex items-center gap-1"><MapPin className="w-3 h-3" /> Source IP</span>
                                            <div className="font-mono text-lg">{incidentData.actor.ip}</div>
                                            <div className="text-sm text-muted-foreground">{incidentData.actor.location}</div>
                                        </div>
                                        <div className="p-4 bg-muted/50 rounded-lg space-y-1">
                                            <span className="text-xs text-muted-foreground uppercase flex items-center gap-1"><UserIcon className="w-3 h-3" /> User Account</span>
                                            <div className="font-medium">{incidentData.actor.user}</div>
                                        </div>
                                    </div>

                                    <div className="p-4 border border-destructive/20 bg-destructive/5 rounded-lg space-y-3">
                                        <div className="flex items-center justify-between">
                                            <h4 className="font-semibold text-destructive flex items-center gap-2">
                                                Global Threat Intelligence Match
                                            </h4>
                                            <ThreatBadge type={incidentData.threatIntel.type} confidence={incidentData.threatIntel.confidence} />
                                        </div>
                                        <p className="text-sm text-muted-foreground">
                                            This IP address matches a known indicator of compromise linked to the <strong>Lazarus Group</strong>.
                                            Observed activity pattern matches <span className="font-mono text-xs bg-muted px-1 rounded">T1110 (Brute Force)</span> and <span className="font-mono text-xs bg-muted px-1 rounded">T1041 (Exfiltration)</span>.
                                        </p>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Right Column: Risk & Defense (Module A, C, I) */}
                        <div className="space-y-6">

                            {/* Module A & C: Risk Analysis */}
                            <RiskAnalysisPanel
                                score={incidentData.riskScore}
                                isAnomaly={true}
                                factors={[
                                    { name: "Known Malicious IP", description: "Source matched threat feed", weight: "HIGH" },
                                    { name: "Abnormal Data Volume", description: ">500MB download", weight: "MEDIUM" },
                                    { name: "Off-Hours Login", description: "Login at 3 AM local time", weight: "MEDIUM" }
                                ]}
                            />

                            {/* Module I: Playbook */}
                            <PlaybookWidget
                                playbookName={incidentData.playbook.name}
                                actions={incidentData.playbook.actions}
                            />
                        </div>
                    </div>
                </main>
            </div>
        </div>
    );
}
