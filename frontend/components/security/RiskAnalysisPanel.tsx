import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { RiskBadge } from "./SecurityBadges";

interface RiskFactor {
    name: string;
    description: string;
    weight: "HIGH" | "MEDIUM" | "LOW";
}

interface RiskAnalysisProps {
    score: number;
    factors: RiskFactor[];
    isAnomaly: boolean;
}

export function RiskAnalysisPanel({ score, factors, isAnomaly }: RiskAnalysisProps) {
    return (
        <Card className={isAnomaly ? "border-red-500/50 bg-red-500/5" : ""}>
            <CardHeader>
                <div className="flex items-center justify-between">
                    <div>
                        <CardTitle>Risk Analysis</CardTitle>
                        <CardDescription>Real-time Session Evaluation</CardDescription>
                    </div>
                    <RiskBadge score={score} />
                </div>
            </CardHeader>
            <CardContent className="space-y-4">
                {isAnomaly && (
                    <div className="p-3 bg-red-500/10 border border-red-500/20 rounded text-sm text-red-400 font-medium">
                        ⚠️ Behavioral Anomaly Detected (Deviation from Baseline)
                    </div>
                )}

                <div className="space-y-2">
                    <h4 className="text-sm font-medium text-muted-foreground">Contributing Factors</h4>
                    {factors.length === 0 ? (
                        <p className="text-sm text-muted-foreground/50">No negative factors detected.</p>
                    ) : (
                        factors.map((f, i) => (
                            <div key={i} className="flex items-center justify-between text-sm p-2 bg-muted/50 rounded">
                                <span>{f.name}</span>
                                <span className={
                                    f.weight === "HIGH" ? "text-red-500" :
                                        f.weight === "MEDIUM" ? "text-yellow-500" : "text-blue-500"
                                }>{f.weight}</span>
                            </div>
                        ))
                    )}
                </div>
            </CardContent>
        </Card>
    );
}
