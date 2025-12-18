import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BrainCircuit, TrendingUp } from "lucide-react";

interface Prediction {
    type: string;
    probability: number;
    target: string;
    timeHorizon: string;
}

export function AttackForecastWidget() {
    // Mock Data (Module F)
    const predictions: Prediction[] = [
        { type: "Credential Stuffing", probability: 85, target: "Admin Portal", timeHorizon: "24h" },
        { type: "Targeted Phishing", probability: 60, target: "Finance Dept", timeHorizon: "48h" }
    ];

    return (
        <Card className="bg-gradient-to-br from-indigo-500/10 to-purple-500/10 border-indigo-500/20">
            <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium flex items-center gap-2 text-indigo-400">
                    <BrainCircuit className="w-4 h-4" />
                    AI ATTACK PREDICTION
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                {predictions.map((p, i) => (
                    <div key={i} className="flex items-center justify-between">
                        <div className="space-y-1">
                            <div className="text-sm font-semibold">{p.type}</div>
                            <div className="text-xs text-muted-foreground">Target: {p.target}</div>
                        </div>
                        <div className="text-right">
                            <div className="text-sm font-bold text-indigo-400">{p.probability}%</div>
                            <div className="text-xs text-muted-foreground flex items-center gap-1 justify-end">
                                <TrendingUp className="w-3 h-3" /> {p.timeHorizon}
                            </div>
                        </div>
                    </div>
                ))}

                <div className="pt-2 border-t border-indigo-500/20">
                    <p className="text-xs text-muted-foreground">
                        Based on heuristic analysis of recent failed logins and external threat feeds.
                    </p>
                </div>
            </CardContent>
        </Card>
    );
}
