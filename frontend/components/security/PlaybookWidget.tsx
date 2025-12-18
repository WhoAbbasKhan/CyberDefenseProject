"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Shield, Play } from "lucide-react";
import { useState } from "react";

interface PlaybookAction {
    name: string;
    status: "PENDING" | "RUNNING" | "SUCCESS" | "FAILED";
    timestamp: string;
}

interface PlaybookWidgetProps {
    playbookName: string;
    actions: PlaybookAction[];
}

export function PlaybookWidget({ playbookName, actions }: PlaybookWidgetProps) {
    const [isPaused, setIsPaused] = useState(false);

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <Shield className="w-4 h-4 text-purple-500" />
                    Automated Defense: {playbookName}
                </CardTitle>
                <Button
                    variant={isPaused ? "outline" : "ghost"}
                    size="sm"
                    onClick={() => setIsPaused(!isPaused)}
                    className={isPaused ? "text-yellow-500 border-yellow-500/50" : "text-muted-foreground hover:text-foreground"}
                >
                    {isPaused ? "RESUME" : "PAUSE"}
                </Button>
            </CardHeader>
            <CardContent>
                <div className="space-y-3">
                    {actions.map((action, i) => (
                        <div key={i} className="flex items-center gap-3 text-sm">
                            <div className={`w-2 h-2 rounded-full ${action.status === "SUCCESS" ? "bg-green-500" :
                                    action.status === "RUNNING" ? "bg-blue-500 animate-pulse" :
                                        action.status === "FAILED" ? "bg-red-500" : "bg-muted"
                                }`} />
                            <div className="flex-1 flex justify-between">
                                <span className={action.status === "PENDING" ? "text-muted-foreground" : ""}>{action.name}</span>
                                <span className="text-xs text-muted-foreground">{action.timestamp}</span>
                            </div>
                        </div>
                    ))}
                    <Button variant="secondary" size="sm" className="w-full mt-2 gap-2 text-xs">
                        <Play className="w-3 h-3" />
                        Run Manual Action
                    </Button>
                </div>
            </CardContent>
        </Card>
    )
}
